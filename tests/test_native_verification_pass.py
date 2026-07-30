from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_verification_pass as verification  # noqa: E402


class NativeVerificationPassTests(unittest.TestCase):
    def test_repository_contract_and_twenty_three_scenarios(self) -> None:
        result = verification.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 23)
        self.assertEqual(result["runtime_mentions"], 0)
        self.assertEqual(result["runtime_files"], 0)
        self.assertEqual(result["td05_commands"], 0)
        self.assertEqual(result["remaining_commands"], 0)
        self.assertEqual(result["skill_files"], 61)
        self.assertEqual(result["target_artifact"], "cotend-codex-r000015")

    def test_full_and_adaptive_use_the_same_result_contract(self) -> None:
        full = verification.evaluate_verification(profile="full")
        adaptive = verification.evaluate_verification(profile="adaptive")
        for field in verification.VerificationResult.__dataclass_fields__:
            if field not in {"profile", "execution_shape"}:
                self.assertEqual(getattr(full, field), getattr(adaptive, field))
        self.assertNotEqual(full.execution_shape, adaptive.execution_shape)

    def test_stale_or_missing_handoff_blocks_before_inspection(self) -> None:
        missing = verification.evaluate_verification(checker_handoff="not_ready")
        stale = verification.evaluate_verification(
            implementation_identity_current=False
        )
        self.assertEqual(missing.status, "blocked")
        self.assertFalse(missing.inspection_started)
        self.assertEqual(stale.blocking_reason, "stale_implementation_identity")
        self.assertFalse(stale.writes_performed)

    def test_checker_rejects_scope_drift_and_report_only_evidence(self) -> None:
        scope = verification.evaluate_verification(scope_clean=False)
        report_only = verification.evaluate_verification(
            direct_evidence_available=False
        )
        self.assertEqual(scope.status, "failed")
        self.assertEqual(scope.unresolved_findings, 1)
        self.assertEqual(report_only.status, "blocked")
        self.assertEqual(report_only.finding_action, "reject_implementer_report_only")

    def test_fix_rebinds_identity_and_requires_successful_retest(self) -> None:
        fixed = verification.evaluate_verification(finding_state="fixable")
        failed = verification.evaluate_verification(
            finding_state="fixable", retest_passes=False
        )
        self.assertEqual(fixed.status, "passed_after_fix")
        self.assertNotEqual(
            fixed.checked_implementation_identity,
            fixed.input_implementation_identity,
        )
        self.assertEqual(fixed.formal_review_handoff, "required")
        self.assertEqual(failed.status, "failed")
        self.assertEqual(failed.formal_review_handoff, "not_ready")

    def test_required_check_cannot_be_skipped_or_weakened(self) -> None:
        missing = verification.evaluate_verification(check_state="missing")
        unavailable = verification.evaluate_verification(
            check_state="tool_unavailable"
        )
        self.assertEqual(missing.blocking_reason, "required_check_missing")
        self.assertEqual(
            unavailable.blocking_reason, "required_check_tool_unavailable"
        )
        self.assertFalse(missing.required_checks_executed)

    def test_critical_and_out_of_scope_fixes_fail_closed(self) -> None:
        critical = verification.evaluate_verification(finding_state="critical")
        outside = verification.evaluate_verification(
            finding_state="fixable", fix_within_scope=False
        )
        self.assertEqual(critical.status, "blocked")
        self.assertFalse(critical.writes_performed)
        self.assertEqual(outside.status, "failed")
        self.assertFalse(outside.writes_performed)

    def test_resume_rechecks_drift_and_never_retries_ambiguous_effects(self) -> None:
        interrupted = verification.evaluate_verification(
            resume_state="interrupted_current"
        )
        drifted = verification.evaluate_verification(resume_state="drifted")
        ambiguous = verification.evaluate_verification(
            resume_state="ambiguous_side_effect"
        )
        self.assertEqual(
            interrupted.resume_action, "continue_from_verified_checker_checkpoint"
        )
        self.assertEqual(
            drifted.resume_action, "rederive_scope_and_rerun_required_checks"
        )
        self.assertEqual(ambiguous.status, "blocked")
        self.assertFalse(ambiguous.writes_performed)

    def test_current_pass_is_idempotent(self) -> None:
        result = verification.evaluate_verification(resume_state="passed_current")
        self.assertEqual(result.status, "passed")
        self.assertTrue(result.idempotent_noop)
        self.assertFalse(result.writes_performed)
        self.assertTrue(result.independent_scope_derived)
        self.assertEqual(result.formal_review_handoff, "required")

    def test_cached_pass_is_invalidated_when_current_premises_drift(self) -> None:
        scope_drift = verification.evaluate_verification(
            resume_state="passed_current", scope_clean=False
        )
        missing_check = verification.evaluate_verification(
            resume_state="passed_current", check_state="missing"
        )
        self.assertEqual(scope_drift.status, "failed")
        self.assertFalse(scope_drift.idempotent_noop)
        self.assertEqual(
            scope_drift.resume_action, "rederive_scope_and_rerun_required_checks"
        )
        self.assertEqual(missing_check.status, "blocked")
        self.assertEqual(missing_check.blocking_reason, "required_check_missing")

    def test_checker_never_claims_later_authority(self) -> None:
        result = verification.evaluate_verification(ai_uat_required=True)
        self.assertEqual(result.ai_uat_handoff, "required")
        self.assertFalse(result.formal_review_claimed)
        self.assertFalse(result.ai_uat_claimed)
        self.assertFalse(result.user_acceptance_claimed)
        self.assertFalse(result.route_changed)
        self.assertFalse(result.release_authorized)
        self.assertFalse(result.external_framework_owner)
        self.assertTrue(result.unrelated_files_preserved)

    def test_invalid_contract_fields_are_rejected(self) -> None:
        with self.assertRaises(verification.NativeVerificationPassError):
            verification.evaluate_verification(active_leaf="")
        with self.assertRaises(verification.NativeVerificationPassError):
            verification.evaluate_verification(changed_paths=())
        with self.assertRaises(verification.NativeVerificationPassError):
            verification.evaluate_verification(required_checks=())
        with self.assertRaises(verification.NativeVerificationPassError):
            verification.evaluate_verification(check_state="unknown")  # type: ignore[arg-type]
        with self.assertRaises(verification.NativeVerificationPassError):
            verification.evaluate_verification(resume_state="unknown")  # type: ignore[arg-type]

    def test_td05_and_all_remaining_compatibility_commands_are_removed(self) -> None:
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "skills").rglob("*"))
            if path.is_file()
        ).lower()
        self.assertNotIn(verification.REMOVED_TD05_COMMAND, text)
        for command in verification.REQUIRED_REMAINING_COMMANDS:
            self.assertIn(command, text)


if __name__ == "__main__":
    unittest.main()
