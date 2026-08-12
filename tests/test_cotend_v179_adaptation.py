from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLING = ROOT / "skills" / "cotend-tooling"
PROJECT_INIT = ROOT / "skills" / "cotend-project-init"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def run_json(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CoTendV201AdaptationTests(unittest.TestCase):
    def test_v201_identity_is_promoted_to_exact_r17_locks(self) -> None:
        role_map = json.loads(read("upstream/CODEX-SKILL-ROLE-MAP.json"))
        self.assertEqual(
            role_map["candidate_release"],
            "exact-source:fe21e970bc2bdc69de5e2ce1710aef2dd156a54d",
        )
        self.assertEqual(role_map["skill_count"], 10)
        self.assertNotIn("candidate_overlay", role_map)

        framework_lock = json.loads(read("upstream/framework.lock.json"))
        artifact_lock = json.loads(read("delivery/codex-artifact.lock.json"))
        self.assertEqual(
            framework_lock["release_id"],
            "exact-source:fe21e970bc2bdc69de5e2ce1710aef2dd156a54d",
        )
        self.assertEqual(
            framework_lock["framework_protocol"], "cotend-collaboration-v2.01"
        )
        self.assertEqual(artifact_lock["target"]["artifact_id"], "cotend-codex-r000017")
        self.assertEqual(artifact_lock["skill_count"], 10)
        self.assertEqual(
            artifact_lock["predecessor_targets"][0]["artifact_id"],
            "cotend-codex-r000016",
        )

    def test_tooling_catalog_validates_and_selection_never_authorizes_adoption(self) -> None:
        script = str(TOOLING / "scripts" / "capability_catalog.py")
        catalog = str(TOOLING / "references" / "capability-catalog.json")
        validated = run_json(
            script,
            "--catalog",
            catalog,
            "validate",
            "--authority-root",
            str(ROOT),
        )
        self.assertEqual(validated["status"], "valid")
        self.assertEqual(validated["record_count"], 9)
        self.assertEqual(validated["update_locator_count"], 9)

        selected = run_json(
            script,
            "--catalog",
            catalog,
            "find",
            "--authority-root",
            str(ROOT),
            "--task",
            "navigate a Python repository",
            "--capability",
            "repository-index",
            "--stack",
            "python",
            "--platform",
            "windows",
            "--limit",
            "3",
        )
        self.assertEqual(selected["selected_count"], 1)
        self.assertEqual(selected["candidates"][0]["id"], "codegraph")
        self.assertEqual(
            selected["candidates"][0]["adoption_disposition"], "adopt_partial"
        )
        self.assertNotIn("adoption_authorized", selected)

    def test_inventory_is_bounded_read_only_and_initializes_empty_or_nonempty_state(self) -> None:
        watched = [
            ROOT / "STATUS.md",
            ROOT / "PROJECT-PLAN-TREE.md",
            ROOT / "REVIEW-LOG.md",
        ]
        before = {path: (digest(path), path.stat().st_mtime_ns) for path in watched}
        result = run_json(
            str(TOOLING / "scripts" / "project_inventory.py"),
            "--project-root",
            str(ROOT),
            "--mode",
            "bootstrap_full",
        )
        after = {path: (digest(path), path.stat().st_mtime_ns) for path in watched}
        self.assertEqual(before, after)
        self.assertEqual(
            result["contract"], "cotend.project-capability-inventory-scan.v1"
        )
        self.assertTrue(result["inventory_initialized"])
        self.assertEqual(result["reliability"], "reliable")
        self.assertFalse(result["writes_performed"])
        self.assertEqual(result["network_calls"], 0)
        paths = set(result["reconcile_paths"])
        self.assertIn("STATUS.md", paths)
        self.assertNotIn(".private-provenance", "\n".join(paths))

    def test_impact_resolver_selects_v201_actions_and_preserves_future_triggers(self) -> None:
        script = str(PROJECT_INIT / "scripts" / "resolve_framework_update.py")
        result = run_json(
            script,
            "resolve",
            "--from-version",
            "v1.79",
            "--to-version",
            "v2.01",
            "--inventory-status",
            "absent",
            "--state-reliability",
            "reliable",
            "--guard-status",
            "clear",
        )
        selected_actions = [
            action
            for item in result["merged_actions"]
            for action in item["project_actions"]
        ] + [item["project_action"] for item in result["ordered_actions"]]
        self.assertEqual(
            selected_actions,
            [
                "reconstruct_current_mvp_once",
                "delegate_tooling_inventory_once_if_absent",
                "apply_coherence_sized_execution_on_active_route",
                "apply_outcome_triggered_governance_on_active_route",
                "maintain_project_agents_router_block",
            ],
        )
        self.assertIn(
            "v183-adaptive-development-experience",
            [item["change_id"] for item in result["deferred_triggers"]],
        )
        self.assertEqual(result["required_scope"], "full_current_mvp")
        self.assertFalse(result["advance_allowed"])
        self.assertTrue(result["compatibility_receipt"]["existing_carrier_only"])

    def test_inventory_reconciles_from_checkpoint_and_fails_safe_on_tamper(self) -> None:
        script = str(TOOLING / "scripts" / "project_inventory.py")
        bootstrap = run_json(
            script,
            "--project-root",
            str(ROOT),
            "--mode",
            "bootstrap_full",
        )
        with tempfile.TemporaryDirectory(prefix="cotend-inventory-checkpoint-") as temp:
            checkpoint = Path(temp) / "checkpoint.json"
            checkpoint.write_text(
                json.dumps(bootstrap["new_checkpoint"], sort_keys=True),
                encoding="utf-8",
            )
            incremental = run_json(
                script,
                "--project-root",
                str(ROOT),
                "--mode",
                "incremental_reconcile",
                "--checkpoint",
                str(checkpoint),
            )
            self.assertEqual(incremental["mode"], "incremental_reconcile")
            self.assertEqual(incremental["fallback_reason"], "none")
            self.assertEqual(incremental["delta_count"], 0)
            self.assertEqual(
                incremental["strategy"], "git_anchor_and_evidence_digest_delta"
            )

            tampered = dict(bootstrap["new_checkpoint"])
            tampered["integrity_digest"] = "0" * 64
            checkpoint.write_text(
                json.dumps(tampered, sort_keys=True), encoding="utf-8"
            )
            fallback = run_json(
                script,
                "--project-root",
                str(ROOT),
                "--mode",
                "incremental_reconcile",
                "--checkpoint",
                str(checkpoint),
            )
        self.assertEqual(fallback["mode"], "forced_full")
        self.assertEqual(fallback["fallback_reason"], "checkpoint_invalid")
        self.assertEqual(fallback["reliability"], "incomplete")
        self.assertFalse(fallback["writes_performed"])
        self.assertEqual(fallback["network_calls"], 0)

    def test_impact_resolver_has_fast_path_and_fail_closed_legacy_path(self) -> None:
        script = str(PROJECT_INIT / "scripts" / "resolve_framework_update.py")
        fresh = run_json(
            script,
            "resolve",
            "--from-version",
            "v2.01",
            "--to-version",
            "v2.01",
            "--completed-once",
            "v172-project-understanding-reconstruction",
            "--inventory-status",
            "absent",
            "--state-reliability",
            "reliable",
            "--guard-status",
            "clear",
            "--framework-state-contract",
            "cotend.framework-update-state.v2",
            "--last-material-project-migration",
            "v2.01",
        )
        self.assertFalse(fresh["fast_path_no_migration"])
        self.assertTrue(fresh["inventory_bootstrap_required"])
        self.assertEqual(
            [
                action
                for item in fresh["merged_actions"]
                for action in item["project_actions"]
            ],
            ["delegate_tooling_inventory_once_if_absent"],
        )

        fast = run_json(
            script,
            "resolve",
            "--from-version",
            "v2.01",
            "--to-version",
            "v2.01",
            "--completed-once",
            "v172-project-understanding-reconstruction",
            "--inventory-status",
            "initialized",
            "--state-reliability",
            "reliable",
            "--guard-status",
            "clear",
            "--framework-state-contract",
            "cotend.framework-update-state.v2",
            "--last-material-project-migration",
            "v2.01",
        )
        self.assertTrue(fast["fast_path_no_migration"])
        self.assertTrue(fast["advance_allowed"])
        self.assertEqual(fast["project_reads"], [])

        legacy = run_json(
            script,
            "resolve",
            "--from-version",
            "unknown",
            "--to-version",
            "v2.01",
            "--inventory-status",
            "absent",
            "--state-reliability",
            "unreliable",
            "--guard-status",
            "unknown",
        )
        self.assertEqual(legacy["required_scope"], "legacy_bounded_audit")
        self.assertTrue(legacy["guard_stop"])
        self.assertFalse(legacy["advance_allowed"])

    def test_solution_adequacy_has_exact_triggers_near_misses_and_route_classes(self) -> None:
        closure = read(
            "skills/cotend-collaboration/references/semantic-implementation-closure.md"
        )
        solution = read(
            "skills/cotend-collaboration/references/solution-adequacy.md"
        )
        acceptance = read(
            "skills/cotend-collaboration/references/acceptance-test-harness.md"
        )
        for marker in (
            "material_fit_uncertainty",
            "significant_cost_or_lock_in",
            "key_assumption_contradicted",
            "patch_complexity_accumulating",
            "substantive_user_candidate",
            "implementation_defect",
            "parameter_or_local_design_issue",
            "route_assumption_failure",
            "protected_outcome_or_constraint_change",
        ):
            self.assertIn(marker, solution)
        self.assertIn("known implementation defects", solution)
        self.assertIn("directly evidenced reversible", solution)
        self.assertIn("Outcome-Corresponding Evidence", acceptance)
        self.assertIn("patch stacking", closure)
        self.assertIn("Full and Adaptive must produce the same trigger", solution)

    def test_candidate_keeps_c01_c19_and_adds_no_parallel_authority(self) -> None:
        capability_map = json.loads(read("upstream/CAPABILITY-IMPLEMENTATION-MAP.json"))
        self.assertEqual(capability_map["capability_count"], 19)
        self.assertEqual(
            [item["capability_id"] for item in capability_map["capabilities"]],
            [f"C{index:02d}" for index in range(1, 20)],
        )
        self.assertNotIn("candidate_overlay", capability_map)
        by_id = {
            item["capability_id"]: set(item["owners"])
            for item in capability_map["capabilities"]
        }
        self.assertIn("skills/cotend-tooling/SKILL.md", by_id["C14"])
        self.assertIn(
            "skills/cotend-tooling/scripts/project_inventory.py", by_id["C19"]
        )
        tooling = read("skills/cotend-tooling/SKILL.md")
        workflow = read("skills/cotend-tooling/references/workflow.md")
        self.assertIn(
            "never\ndecide product meaning, adoption authority or completion", tooling
        )
        self.assertIn("not adoption or execution authority", workflow)

    def test_all_active_compatibility_markers_are_v201(self) -> None:
        self.assertIn(
            "Protocol version: `cotend-collaboration-v2.01`",
            read("skills/cotend-collaboration/SKILL.md"),
        )
        self.assertIn(
            "Compatibility baseline: `cotend-collaboration-v2.01`",
            read("skills/cotend-model-upgrade/SKILL.md"),
        )


if __name__ == "__main__":
    unittest.main()
