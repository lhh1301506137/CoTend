from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_negative_recovery_ownership as recovery  # noqa: E402


class NativeNegativeRecoveryOwnershipTests(unittest.TestCase):
    def test_repository_contract_and_four_evidence_groups(self) -> None:
        result = recovery.verify_repository()
        self.assertEqual(
            result["status"], "native_negative_recovery_ownership_verified"
        )
        self.assertEqual(result["evidence_group_count"], 4)
        self.assertEqual(result["incident_scenario_count"], 13)
        self.assertEqual(result["native_capabilities_composed"], 8)
        self.assertEqual(result["dual_capability_baseline"], 19)
        self.assertEqual(result["mapped_skill_roles"], 8)
        self.assertFalse(result["real_project_claimed"])
        self.assertFalse(result["real_user_acceptance_claimed"])
        self.assertFalse(result["skill_behavior_changed"])
        self.assertEqual(result["target_artifact"], "cotend-codex-r000011")

    def test_foreign_conflicts_fail_closed_without_delegating_owner(self) -> None:
        for semantic_level in ("L0_L2", "L3_L4"):
            result = recovery.run_foreign_framework_conflict(
                "full", semantic_level
            )
            self.assertEqual(result.status, "blocked_safe")
            self.assertEqual(result.closeout_status, "not_started")
            self.assertTrue(result.unaffected_route_preserved)
            self.assertFalse(result.external_framework_owner)
            self.assertFalse(result.parallel_truth_created)
            self.assertFalse(result.real_user_acceptance_claimed)

    def test_unknown_and_duplicate_state_do_not_silently_reset(self) -> None:
        for state_incident in ("unknown_external", "duplicate_native_record"):
            result = recovery.run_unknown_or_drifted_state(
                "full", state_incident
            )
            self.assertEqual(result.status, "blocked_safe")
            self.assertEqual(result.closeout_status, "not_started")
            self.assertFalse(result.silent_state_reset)
            self.assertTrue(result.checkpoint_preserved)

    def test_failed_check_recovers_with_new_evidence_before_closeout(self) -> None:
        result = recovery.run_failed_check_recovery("full")
        self.assertEqual(result.status, "recovered")
        self.assertEqual(result.closeout_status, "completed")
        self.assertNotEqual(
            result.implementation_identity,
            result.recovered_implementation_identity,
        )
        self.assertNotEqual(
            result.failed_verification_identity,
            result.recovered_verification_identity,
        )
        self.assertFalse(result.stale_evidence_reused)
        self.assertFalse(result.closeout_before_recovery)
        stages = [record.stage for record in result.stage_records]
        self.assertLess(
            stages.index("verification_recovered"),
            stages.index("formal_self_review_fixture"),
        )
        self.assertLess(
            stages.index("formal_self_review_fixture"),
            stages.index("closeout_after_recovery"),
        )

    def test_recovery_failure_preserves_checkpoint_and_drift(self) -> None:
        result = recovery.run_failed_check_recovery(
            "full", recovery_failure=True
        )
        self.assertEqual(result.status, "recovery_failed_safe")
        self.assertEqual(result.closeout_status, "blocked")
        self.assertEqual(
            result.blocking_reason,
            "concurrent_record_drift_during_rollback",
        )
        self.assertTrue(result.checkpoint_preserved)
        self.assertFalse(result.release_authorized)

    def test_full_and_adaptive_negative_outcomes_are_equivalent(self) -> None:
        pairs = [
            (
                recovery.run_foreign_framework_conflict("full", "L0_L2"),
                recovery.run_foreign_framework_conflict("adaptive", "L0_L2"),
            ),
            (
                recovery.run_unknown_or_drifted_state(
                    "full", "duplicate_native_record"
                ),
                recovery.run_unknown_or_drifted_state(
                    "adaptive", "duplicate_native_record"
                ),
            ),
            (
                recovery.run_failed_check_recovery("full"),
                recovery.run_failed_check_recovery("adaptive"),
            ),
        ]
        for full, adaptive in pairs:
            self.assertEqual(
                recovery.equivalence_projection(full),
                recovery.equivalence_projection(adaptive),
            )
            self.assertEqual(full.execution_mode, "delegated_pair")
            self.assertEqual(adaptive.execution_mode, "inline")

    def test_stage_outputs_feed_the_next_stage(self) -> None:
        results = [
            recovery.run_foreign_framework_conflict("full", "L0_L2"),
            recovery.run_foreign_framework_conflict("adaptive", "L3_L4"),
            recovery.run_unknown_or_drifted_state("full", "unknown_external"),
            recovery.run_unknown_or_drifted_state(
                "adaptive", "duplicate_native_record"
            ),
            recovery.run_failed_check_recovery("full"),
            recovery.run_failed_check_recovery(
                "adaptive", recovery_failure=True
            ),
        ]
        for result in results:
            for previous, current in zip(
                result.stage_records, result.stage_records[1:]
            ):
                self.assertEqual(
                    current.input_identity,
                    previous.output_identity,
                )

    def test_protected_file_fixture_preserves_non_owned_bytes(self) -> None:
        result = recovery.run_protected_file_fixture()
        self.assertEqual(result.status, "protected")
        self.assertEqual(result.protected_file_count, 4)
        self.assertEqual(result.owned_record_count, 1)
        self.assertEqual(
            result.owned_rollback, "restored_owned_precommit_writes"
        )
        self.assertEqual(
            result.concurrent_drift_disposition, "preserved_concurrent_drift"
        )
        self.assertTrue(result.project_truth_preserved)
        self.assertTrue(result.user_files_preserved)
        self.assertTrue(result.unrelated_files_preserved)
        self.assertTrue(result.staged_external_preserved)
        self.assertFalse(result.real_project_claimed)

    def test_protected_file_tampering_is_detected(self) -> None:
        with self.assertRaises(recovery.NativeNegativeRecoveryError):
            recovery.run_protected_file_fixture(tamper_protected=True)

    def test_damaged_handoff_is_rejected(self) -> None:
        self.assertTrue(recovery.reject_damaged_handoff())

    def test_external_owner_mutation_cannot_pass(self) -> None:
        original = recovery.native_authority.evaluate_external_artifact
        bad = replace(
            original("absent"),
            external_is_authority=True,
        )
        with mock.patch.object(
            recovery.native_authority,
            "evaluate_external_artifact",
            return_value=bad,
        ):
            with self.assertRaises(recovery.NativeNegativeRecoveryError):
                recovery.run_failed_check_recovery("full")

    def test_stale_recovered_verification_identity_cannot_pass(self) -> None:
        original = recovery.native_verification.evaluate_verification

        def stale_result(**kwargs: object) -> object:
            result = original(**kwargs)
            if kwargs.get("check_state", "pass") == "pass":
                return replace(
                    result,
                    input_implementation_identity="sha256:stale",
                )
            return result

        with mock.patch.object(
            recovery.native_verification,
            "evaluate_verification",
            side_effect=stale_result,
        ):
            with self.assertRaises(recovery.NativeNegativeRecoveryError):
                recovery.run_failed_check_recovery("full")


if __name__ == "__main__":
    unittest.main()
