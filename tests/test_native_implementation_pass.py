from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_implementation_pass as implementation  # noqa: E402


class NativeImplementationPassTests(unittest.TestCase):
    def test_repository_contract_and_fifteen_scenarios(self) -> None:
        result = implementation.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 15)
        self.assertEqual(result["runtime_mentions"], 7)
        self.assertEqual(result["runtime_files"], 6)
        self.assertEqual(result["td04_commands"], 0)
        self.assertEqual(result["remaining_commands"], 0)
        self.assertEqual(result["skill_files"], 40)
        self.assertEqual(result["target_artifact"], "cotend-codex-r000010")

    def test_full_and_adaptive_use_the_same_result_contract(self) -> None:
        full = implementation.evaluate_implementation(profile="full")
        adaptive = implementation.evaluate_implementation(profile="adaptive")
        self.assertEqual(full.status, adaptive.status)
        self.assertEqual(full.test_action, adaptive.test_action)
        self.assertEqual(full.checker_handoff, adaptive.checker_handoff)
        self.assertEqual(full.evidence_fields, adaptive.evidence_fields)
        self.assertNotEqual(full.execution_shape, adaptive.execution_shape)

    def test_missing_authority_and_pending_decision_write_nothing(self) -> None:
        unauthorized = implementation.evaluate_implementation(authorized=False)
        pending = implementation.evaluate_implementation(
            pending_human_decision=True
        )
        self.assertEqual(unauthorized.status, "blocked")
        self.assertEqual(pending.status, "blocked")
        self.assertFalse(unauthorized.writes_performed)
        self.assertFalse(pending.writes_performed)

    def test_dependency_waits_without_implementation(self) -> None:
        result = implementation.evaluate_implementation(
            dependencies_ready=False
        )
        self.assertEqual(result.status, "dependency_waiting")
        self.assertFalse(result.implementation_started)
        self.assertFalse(result.writes_performed)

    def test_scope_and_ownership_violations_fail_closed(self) -> None:
        overlap = implementation.evaluate_implementation(ownership_clear=False)
        expansion = implementation.evaluate_implementation(
            scope_within_leaf=False
        )
        self.assertEqual(overlap.blocking_reason, "write_ownership_overlap")
        self.assertIn("scope_expansion", expansion.blocking_reason)
        self.assertFalse(overlap.writes_performed)
        self.assertFalse(expansion.writes_performed)

    def test_fixable_and_unfixable_test_failures_are_distinct(self) -> None:
        fixed = implementation.evaluate_implementation(
            test_state="fail_fixable"
        )
        blocked = implementation.evaluate_implementation(
            test_state="fail_unfixable"
        )
        self.assertEqual(fixed.status, "integration_waiting")
        self.assertEqual(fixed.test_action, "fix_in_scope_retest_and_record")
        self.assertEqual(blocked.status, "blocked")
        self.assertEqual(blocked.checker_handoff, "not_ready")

    def test_interruption_resume_revalidates_or_stops(self) -> None:
        safe = implementation.evaluate_implementation(
            resume_state="safe_checkpoint"
        )
        drifted = implementation.evaluate_implementation(resume_state="drifted")
        ambiguous = implementation.evaluate_implementation(
            resume_state="ambiguous_side_effect"
        )
        self.assertEqual(safe.resume_action, "continue_from_verified_checkpoint")
        self.assertEqual(drifted.resume_action, "revalidate_then_implement")
        self.assertEqual(ambiguous.status, "blocked")
        self.assertFalse(ambiguous.writes_performed)

    def test_closed_current_packet_is_idempotent(self) -> None:
        result = implementation.evaluate_implementation(
            resume_state="closed_current"
        )
        self.assertEqual(result.status, "closed")
        self.assertTrue(result.idempotent_noop)
        self.assertFalse(result.writes_performed)
        self.assertEqual(result.checker_handoff, "required")

    def test_implementer_never_claims_checker_or_acceptance_authority(self) -> None:
        result = implementation.evaluate_implementation()
        self.assertFalse(result.formal_checker_claimed)
        self.assertFalse(result.formal_review_claimed)
        self.assertFalse(result.user_acceptance_claimed)
        self.assertFalse(result.release_authorized)
        self.assertFalse(result.route_changed)
        self.assertTrue(result.unrelated_files_preserved)

    def test_invalid_packet_fields_are_rejected(self) -> None:
        with self.assertRaises(implementation.NativeImplementationPassError):
            implementation.evaluate_implementation(active_leaf="")
        with self.assertRaises(implementation.NativeImplementationPassError):
            implementation.evaluate_implementation(allowed_paths=())
        with self.assertRaises(implementation.NativeImplementationPassError):
            implementation.evaluate_implementation(acceptance=())
        with self.assertRaises(implementation.NativeImplementationPassError):
            implementation.evaluate_implementation(test_state="unknown")  # type: ignore[arg-type]
        with self.assertRaises(implementation.NativeImplementationPassError):
            implementation.evaluate_implementation(resume_state="unknown")  # type: ignore[arg-type]

    def test_td04_and_all_remaining_compatibility_commands_are_removed(self) -> None:
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "skills").rglob("*"))
            if path.is_file()
        ).lower()
        self.assertNotIn(implementation.REMOVED_TD04_COMMAND, text)
        for command in implementation.REQUIRED_REMAINING_COMMANDS:
            self.assertIn(command, text)


if __name__ == "__main__":
    unittest.main()
