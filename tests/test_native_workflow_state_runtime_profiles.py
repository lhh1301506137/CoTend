from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_workflow_state_runtime_profiles as native_state  # noqa: E402


class NativeWorkflowStateRuntimeProfilesTests(unittest.TestCase):
    def test_repository_contract_and_all_scenarios(self) -> None:
        result = native_state.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 16)
        self.assertFalse(result["external_framework_owner"])
        self.assertFalse(result["external_config_modified"])
        self.assertFalse(result["legacy_source_modified"])
        self.assertTrue(result["unrelated_truth_preserved"])
        self.assertEqual(
            result["remaining_compatibility_commands"], ["trellis-finish"]
        )

    def test_session_override_does_not_rewrite_project_choice(self) -> None:
        result = native_state.evaluate_workflow(
            "current",
            native_profiles=("full",),
            session_profile="adaptive",
        )
        self.assertEqual(result.effective_profile, "adaptive")
        self.assertEqual(result.execution_mode, "inline")
        self.assertEqual(result.persisted_profile, "full")
        self.assertFalse(result.write_native_record)

    def test_switching_back_to_full_restores_delegated_pair(self) -> None:
        result = native_state.evaluate_workflow(
            "current",
            native_profiles=("adaptive",),
            session_profile="full",
            persist_session=True,
        )
        self.assertEqual(result.persisted_profile, "full")
        self.assertEqual(result.persisted_execution_mode, "delegated_pair")
        self.assertTrue(result.write_native_record)

    def test_dormant_record_requires_explicit_resume(self) -> None:
        blocked = native_state.evaluate_workflow(
            "dormant",
            native_profiles=("adaptive",),
        )
        self.assertFalse(blocked.can_continue)
        self.assertTrue(blocked.user_decision_required)
        resumed = native_state.evaluate_workflow(
            "dormant",
            native_profiles=("adaptive",),
            explicit_resume=True,
        )
        self.assertTrue(resumed.can_continue)
        self.assertEqual(resumed.state, "current")
        self.assertEqual(resumed.effective_profile, "adaptive")

    def test_duplicate_native_record_fails_closed(self) -> None:
        result = native_state.evaluate_workflow(
            "current",
            native_profiles=("full", "adaptive"),
        )
        self.assertEqual(result.state, "conflict")
        self.assertFalse(result.can_continue)
        self.assertFalse(result.write_native_record)

    def test_route_affecting_external_conflict_never_becomes_owner(self) -> None:
        result = native_state.evaluate_workflow(
            "current",
            native_profiles=("full",),
            external_state="conflict",
            external_affects_route=True,
        )
        self.assertEqual(result.state, "conflict")
        self.assertFalse(result.can_continue)
        self.assertFalse(result.external_framework_owner)
        self.assertFalse(result.external_config_modified)

    def test_legacy_migration_preserves_source_and_unrelated_truth(self) -> None:
        result = native_state.evaluate_workflow(
            "absent",
            legacy_profiles=("adaptive",),
        )
        self.assertEqual(result.persisted_profile, "adaptive")
        self.assertEqual(result.migration_result, "migrated_existing_selection")
        self.assertFalse(result.legacy_source_modified)
        self.assertTrue(result.unrelated_truth_preserved)
        self.assertFalse(result.parallel_state_tree_created)

    def test_invalid_calls_are_rejected(self) -> None:
        with self.assertRaises(native_state.NativeWorkflowStateError):
            native_state.evaluate_workflow(
                "current",
                native_profiles=("full",),
                persist_session=True,
            )
        with self.assertRaises(native_state.NativeWorkflowStateError):
            native_state.evaluate_workflow(
                "current",
                native_profiles=("full",),
                explicit_resume=True,
            )

    def test_foreign_state_owner_patterns_are_forbidden(self) -> None:
        samples = (
            ".trellis/config.yaml",
            "trellis.mode: active",
            "codex.dispatch_mode: inline",
            "Trellis Activation Decision",
            "active Trellis",
        )
        for sample in samples:
            self.assertTrue(
                any(
                    pattern.search(sample)
                    for pattern in native_state.FORBIDDEN_STATE_PATTERNS.values()
                ),
                sample,
            )


if __name__ == "__main__":
    unittest.main()
