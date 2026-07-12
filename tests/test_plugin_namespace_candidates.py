from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import evaluate_plugin_namespace_candidates as namespace  # noqa: E402


class PluginNamespaceCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        namespace.base.PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        self.evaluation_root = Path(
            tempfile.mkdtemp(
                prefix="L32-unit-", dir=namespace.base.PRIVATE_ROOT
            )
        )

    def tearDown(self) -> None:
        if self.evaluation_root.exists():
            namespace.base.remove_fixture_tree(self.evaluation_root)

    def test_short_name_map_preserves_companion_names(self) -> None:
        expected = {
            "cotend-collaboration": "collaboration",
            "cotend-diagnose-only": "diagnose-only",
            "cotend-init": "init",
            "cotend-model-upgrade": "model-upgrade",
            "cotend-project-init": "project-init",
        }
        self.assertEqual(namespace.SHORT_NAME_MAP, expected)
        self.assertEqual(
            set(namespace.COMPANION_SKILLS),
            {"grill-me", "karpathy-guidelines"},
        )
        for source, target in expected.items():
            self.assertEqual(
                namespace.target_skill_name(source, short_names=True), target
            )
            self.assertEqual(
                namespace.source_skill_name(target, short_names=True), source
            )

    def test_source_identifier_inventory_is_exact(self) -> None:
        inventory = namespace.identifier_inventory(
            namespace.base.SOURCE_SKILLS_ROOT, namespace.USER_OWNED_SKILLS
        )
        self.assertEqual(inventory["occurrences"], 77)
        self.assertEqual(inventory["files"], 15)
        self.assertEqual(
            inventory["by_identifier"],
            {
                "cotend-collaboration": 36,
                "cotend-diagnose-only": 9,
                "cotend-init": 7,
                "cotend-model-upgrade": 8,
                "cotend-project-init": 17,
            },
        )
        self.assertEqual(
            inventory["by_category"],
            {
                "agent_self_prompt": 5,
                "explicit_invocation": 5,
                "fallback_path": 2,
                "frontmatter_name": 5,
                "plain_reference": 31,
                "protocol_or_version": 7,
                "reference_path": 22,
            },
        )

    def test_identifier_categories_distinguish_reference_shapes(self) -> None:
        cases = (
            (
                "cotend-init/SKILL.md",
                "name: cotend-init",
                "cotend-init",
                "frontmatter_name",
            ),
            (
                "cotend-init/agents/openai.yaml",
                'default_prompt: "Use $cotend-init to resume."',
                "cotend-init",
                "agent_self_prompt",
            ),
            (
                "cotend-collaboration/SKILL.md",
                "Use $cotend-diagnose-only for read-only diagnosis.",
                "cotend-diagnose-only",
                "explicit_invocation",
            ),
            (
                "cotend-init/SKILL.md",
                ".codex/skills/cotend-project-init/SKILL.md",
                "cotend-project-init",
                "fallback_path",
            ),
            (
                "cotend-collaboration/SKILL.md",
                "Protocol: cotend-collaboration-v1.52",
                "cotend-collaboration",
                "protocol_or_version",
            ),
            (
                "cotend-project-init/SKILL.md",
                "Read cotend-collaboration/references/runtime-profiles.md.",
                "cotend-collaboration",
                "reference_path",
            ),
        )
        for path, line, identifier, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    namespace.classify_identifier_occurrence(
                        path, line, identifier
                    ),
                    expected,
                )

    def test_static_candidates_quantify_transform_and_residual_debt(self) -> None:
        results = {}
        transforms = {}
        for candidate in namespace.CANDIDATES:
            candidate_root = self.evaluation_root / candidate.root_name
            candidate_root.mkdir(parents=True)
            materialized = namespace.materialize_candidate_payload(
                candidate_root, candidate
            )
            transforms[candidate.candidate_id] = materialized["transforms"]
            results[candidate.candidate_id] = namespace.verify_candidate_static(
                candidate_root,
                candidate,
                env=None,
                run_official=False,
            )

        preserve = results["N1-preserve"]
        self.assertEqual(preserve["skills"], 7)
        self.assertEqual(preserve["skill_files"], 30)
        self.assertEqual(preserve["package_files"], 36)
        self.assertEqual(transforms["N1-preserve"], [])
        self.assertTrue(preserve["source_comparison"]["byte_identical"])
        self.assertEqual(preserve["source_comparison"]["moved_path_count"], 0)
        self.assertEqual(
            preserve["source_comparison"]["byte_changed_file_count"], 0
        )
        self.assertEqual(
            preserve["residual_source_identifier_inventory"]["occurrences"],
            77,
        )
        self.assertEqual(preserve["residual_migration_review_required"], 0)
        self.assertEqual(preserve["plugin_sensitive_reference_count"], 12)

        short = results["N2-short"]
        self.assertEqual(short["skills"], 7)
        self.assertEqual(short["skill_files"], 30)
        self.assertEqual(short["package_files"], 36)
        self.assertEqual(len(transforms["N2-short"]), 10)
        self.assertEqual(short["source_comparison"]["moved_path_count"], 28)
        self.assertEqual(
            short["source_comparison"]["byte_changed_file_count"], 10
        )
        self.assertFalse(short["source_comparison"]["byte_identical"])
        self.assertEqual(
            short["residual_source_identifier_inventory"]["occurrences"],
            67,
        )
        self.assertEqual(short["residual_migration_review_required"], 60)
        self.assertEqual(short["plugin_sensitive_reference_count"], 7)
        self.assertEqual(len(short["target_entrypoints"]), 5)
        self.assertEqual(
            {item["canonical_name"] for item in short["target_entrypoints"]},
            {
                "cotend:collaboration",
                "cotend:diagnose-only",
                "cotend:init",
                "cotend:model-upgrade",
                "cotend:project-init",
            },
        )
        candidate_root = self.evaluation_root / "N2-short"
        for transform in transforms["N2-short"]:
            source = namespace.base.SOURCE_SKILLS_ROOT / transform["source"]
            target = (
                candidate_root
                / "source-marketplace"
                / "plugins"
                / namespace.PLUGIN_ID
                / "skills"
                / transform["target"]
            )
            source_bytes = source.read_bytes()
            source_name = transform["source"].split("/", 1)[0]
            target_name = transform["target"].split("/", 1)[0]
            if transform["change"] == "frontmatter_name":
                expected = source_bytes.replace(
                    f"name: {source_name}".encode(),
                    f"name: {target_name}".encode(),
                    1,
                )
            else:
                expected = source_bytes.replace(
                    f"Use ${source_name}".encode(),
                    f"Use ${namespace.PLUGIN_ID}:{target_name}".encode(),
                    1,
                )
            target_bytes = target.read_bytes()
            self.assertEqual(target_bytes, expected)
            self.assertNotIn(b"\r\n", target_bytes)

    def test_candidate_state_and_write_roots_are_independent(self) -> None:
        results = {}
        for candidate in namespace.CANDIDATES:
            candidate_root = self.evaluation_root / candidate.root_name
            candidate_root.mkdir(parents=True)
            env = namespace.base.build_isolated_env(candidate_root)
            results[candidate.candidate_id] = {
                "isolation": namespace.candidate_isolation_record(
                    candidate_root, candidate, env
                )
            }
        summary = namespace.verify_candidate_isolation(
            self.evaluation_root, results
        )
        self.assertEqual(summary["physical_candidate_count"], 2)
        self.assertEqual(summary["write_root_keys_per_candidate"], 15)
        self.assertTrue(summary["candidate_roots_disjoint"])
        self.assertEqual(summary["cross_candidate_path_overlaps"], 0)

        overlapping = copy.deepcopy(results)
        overlapping["N2-short"]["isolation"]["state_path_relatives"][
            "codex_home"
        ] = "../N1-preserve/codex-home"
        with self.assertRaises(namespace.base.PluginFixtureError):
            namespace.verify_candidate_isolation(
                self.evaluation_root, overlapping
            )

    def test_remove_payloads_require_exact_candidate_identity(self) -> None:
        candidate = namespace.CANDIDATES[0]
        namespace.validate_plugin_remove(
            {
                "pluginId": candidate.selector,
                "name": namespace.PLUGIN_ID,
                "marketplaceName": candidate.marketplace,
            },
            candidate,
        )
        namespace.validate_marketplace_remove(
            {
                "marketplaceName": candidate.marketplace,
                "installedRoot": None,
            },
            candidate,
        )
        with self.assertRaises(namespace.NamespaceEvaluationError):
            namespace.validate_plugin_remove(
                {
                    "pluginId": "wrong@marketplace",
                    "name": namespace.PLUGIN_ID,
                    "marketplaceName": candidate.marketplace,
                },
                candidate,
            )

    def test_protected_boundary_excludes_only_codex_container_metadata(self) -> None:
        before = {
            "user_codex_root": {
                "exists": True,
                "kind": "directory",
                "size": 1,
                "mtime_ns": 1,
            },
            "user_codex_config": {
                "exists": True,
                "kind": "file",
                "size": 10,
                "mtime_ns": 2,
            },
            "user_agents_root": {
                "exists": True,
                "kind": "directory",
                "size": 0,
                "mtime_ns": 3,
            },
        }
        after = copy.deepcopy(before)
        after["user_codex_root"]["mtime_ns"] = 99
        with mock.patch.object(
            namespace.base, "protected_user_snapshot", return_value=after
        ):
            summary = namespace.protected_boundary_summary(before)
        self.assertEqual(
            summary["observed_volatile_container_changes"],
            ["user_codex_root"],
        )
        self.assertTrue(
            summary[
                "config_auth_plugin_skill_and_agents_metadata_unchanged"
            ]
        )

        changed_config = copy.deepcopy(after)
        changed_config["user_codex_config"]["mtime_ns"] = 100
        with mock.patch.object(
            namespace.base,
            "protected_user_snapshot",
            return_value=changed_config,
        ):
            with self.assertRaises(namespace.NamespaceEvaluationError):
                namespace.protected_boundary_summary(before)

    def test_display_led_overlay_reuses_n1_bytes_and_marks_limits(self) -> None:
        source_interfaces = namespace.load_source_interfaces()
        interfaces = [
            {
                "canonical_name": f"cotend:{source_name}",
                "display_name": interface["display_name"],
                "short_description": interface["short_description"],
                "self_invocation_token": f"${source_name}",
            }
            for source_name, interface in source_interfaces.items()
        ]
        n1_result = {
            "lifecycle": {
                "installed": {
                    "interfaces": interfaces,
                    "plugin_names": [
                        f"cotend:{name}"
                        for name in namespace.base.EXPECTED_SKILLS
                    ],
                }
            }
        }
        overlay = namespace.display_led_overlay(n1_result)
        self.assertEqual(overlay["physical_package"], "N1-preserve")
        self.assertEqual(overlay["additional_package_bytes"], 0)
        self.assertEqual(overlay["friendly_display_name_count"], 5)
        self.assertTrue(overlay["display_names_unique"])
        self.assertTrue(overlay["canonical_double_prefix_remains"])
        self.assertEqual(
            overlay["claim_to_evidence"][
                "desktop_search_render_and_natural_language"
            ],
            "not_run",
        )


if __name__ == "__main__":
    unittest.main()
