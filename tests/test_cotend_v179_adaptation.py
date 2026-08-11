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


class CoTendV179AdaptationTests(unittest.TestCase):
    def test_v179_identity_is_promoted_to_exact_r16_locks(self) -> None:
        role_map = json.loads(read("upstream/CODEX-SKILL-ROLE-MAP.json"))
        self.assertEqual(
            role_map["candidate_release"],
            "exact-source:c14d4133bf0438d435048858554c88c89a7870a3",
        )
        self.assertEqual(role_map["skill_count"], 10)
        self.assertNotIn("candidate_overlay", role_map)

        framework_lock = json.loads(read("upstream/framework.lock.json"))
        artifact_lock = json.loads(read("delivery/codex-artifact.lock.json"))
        self.assertEqual(
            framework_lock["release_id"],
            "exact-source:c14d4133bf0438d435048858554c88c89a7870a3",
        )
        self.assertEqual(
            framework_lock["framework_protocol"], "cotend-collaboration-v1.79"
        )
        self.assertEqual(artifact_lock["target"]["artifact_id"], "cotend-codex-r000016")
        self.assertEqual(artifact_lock["skill_count"], 10)
        self.assertEqual(
            artifact_lock["predecessor_targets"][0]["artifact_id"],
            "cotend-codex-r000015",
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
        self.assertEqual(validated["status"], "validated")
        self.assertEqual(validated["record_count"], 9)
        self.assertFalse(validated["writes_performed"])
        self.assertEqual(validated["network_calls"], 0)

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
        self.assertEqual(selected["records"][0]["id"], "codegraph")
        self.assertFalse(selected["adoption_authorized"])
        self.assertFalse(selected["writes_performed"])
        self.assertEqual(selected["network_calls"], 0)

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

    def test_impact_resolver_selects_only_v179_action_and_preserves_future_triggers(self) -> None:
        script = str(PROJECT_INIT / "scripts" / "resolve_framework_update.py")
        result = run_json(
            script,
            "resolve",
            "--from-version",
            "v1.76",
            "--to-version",
            "v1.79",
            "--inventory-status",
            "absent",
            "--state-reliability",
            "reliable",
            "--guard-status",
            "clear",
        )
        self.assertEqual(
            [item["action"] for item in result["actions"]],
            ["delegate_tooling_inventory_once_if_absent"],
        )
        self.assertEqual(
            result["future_trigger_entries"],
            [
                "v177-tooling-capability-registry",
                "v178-outcome-driven-solution-adequacy",
            ],
        )
        self.assertEqual(result["effective_scope"], "named_carrier")
        self.assertFalse(result["advance_allowed"])
        self.assertFalse(result["writes_performed"])
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["model_calls"], 0)

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
            "v1.79",
            "--to-version",
            "v1.79",
            "--inventory-status",
            "absent",
            "--state-reliability",
            "reliable",
            "--guard-status",
            "clear",
        )
        self.assertFalse(fresh["fast_path_no_migration"])
        self.assertTrue(fresh["inventory_bootstrap_required"])
        self.assertEqual(
            [item["action"] for item in fresh["actions"]],
            ["delegate_tooling_inventory_once_if_absent"],
        )

        fast = run_json(
            script,
            "resolve",
            "--from-version",
            "v1.79",
            "--to-version",
            "v1.79",
            "--inventory-status",
            "initialized",
            "--state-reliability",
            "reliable",
            "--guard-status",
            "clear",
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
            "v1.79",
            "--inventory-status",
            "absent",
            "--state-reliability",
            "unreliable",
            "--guard-status",
            "unknown",
        )
        self.assertEqual(legacy["effective_scope"], "legacy_bounded_audit")
        self.assertTrue(legacy["guard_stop"])
        self.assertFalse(legacy["advance_allowed"])

    def test_solution_adequacy_has_exact_triggers_near_misses_and_route_classes(self) -> None:
        closure = read(
            "skills/cotend-collaboration/references/semantic-implementation-closure.md"
        )
        acceptance = read(
            "skills/cotend-collaboration/references/acceptance-test-harness.md"
        )
        plan = read("skills/cotend-collaboration/references/plan-tree.md")
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
            self.assertIn(marker, closure)
        self.assertIn("known implementation defect", closure)
        self.assertIn("reversible choice", closure)
        self.assertIn("Outcome-Corresponding Discrimination", acceptance)
        self.assertIn("Before stacking another patch", plan)
        self.assertIn("Full and Adaptive use the same trigger", closure)

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
        self.assertIn("must not create a second truth tree", tooling)
        self.assertIn("never a new authority", workflow)

    def test_all_active_compatibility_markers_are_v179(self) -> None:
        historical = ROOT / "skills" / "cotend-collaboration" / "references" / "failure-patterns"
        stale: list[str] = []
        for path in (ROOT / "skills").rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                continue
            if historical in path.parents:
                continue
            if "v1.76" in path.read_text(encoding="utf-8", errors="ignore"):
                stale.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(stale, [])
        self.assertIn(
            "Protocol version: `cotend-collaboration-v1.79`",
            read("skills/cotend-collaboration/SKILL.md"),
        )


if __name__ == "__main__":
    unittest.main()
