from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_closeout_pass as closeout  # noqa: E402


class NativeCloseoutPassTests(unittest.TestCase):
    def test_repository_contract_and_twenty_three_scenarios(self) -> None:
        result = closeout.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 23)
        self.assertEqual(result["runtime_mentions"], 0)
        self.assertEqual(result["runtime_files"], 0)
        self.assertEqual(result["td07_compatibility_terms"], 0)
        self.assertEqual(result["skill_files"], 61)
        self.assertEqual(result["target_artifact"], "cotend-codex-r000015")

    def test_full_and_adaptive_use_the_same_result_contract(self) -> None:
        full = closeout.evaluate_closeout(profile="full")
        adaptive = closeout.evaluate_closeout(profile="adaptive")
        for field in closeout.CloseoutResult.__dataclass_fields__:
            if field != "profile":
                self.assertEqual(getattr(full, field), getattr(adaptive, field))

    def test_preflight_stops_before_any_write(self) -> None:
        stale = closeout.evaluate_closeout(verification_current=False)
        pending = closeout.evaluate_closeout(pending_human_decision=True)
        critical = closeout.evaluate_closeout(critical_boundary=True)
        for result in (stale, pending, critical):
            self.assertEqual(result.status, "blocked")
            self.assertFalse(result.preflight_completed)
            self.assertFalse(result.writes_performed)
            self.assertEqual(result.phase_reached, "preflight")

    def test_unrelated_sensitive_and_staged_paths_are_preserved(self) -> None:
        unrelated = closeout.evaluate_closeout(unrelated_or_unknown_path=True)
        sensitive = closeout.evaluate_closeout(sensitive_or_private_path=True)
        staged = closeout.evaluate_closeout(staged_paths_clean=False)
        for result in (unrelated, sensitive, staged):
            self.assertEqual(result.status, "blocked")
            self.assertFalse(result.writes_performed)
            self.assertTrue(result.unrelated_files_preserved)
            self.assertFalse(result.sensitive_paths_staged)

    def test_non_git_closeout_can_complete_without_a_commit(self) -> None:
        result = closeout.evaluate_closeout(
            commit_intent="not_applicable", git_repository=False
        )
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.commit_result, "not_applicable")
        self.assertEqual(result.commit_identity, "none")
        self.assertTrue(result.postcommit_verified)

        blocked = closeout.evaluate_closeout(
            commit_intent="reuse_current", git_repository=False
        )
        self.assertEqual(blocked.status, "blocked")
        self.assertEqual(blocked.blocking_reason, "git_repository_missing")

        missing_handoff = closeout.evaluate_closeout(handoff_required=True)
        self.assertEqual(missing_handoff.status, "blocked")
        self.assertEqual(
            missing_handoff.blocking_reason,
            "required_handoff_record_missing",
        )
        handoff = closeout.evaluate_closeout(
            handoff_required=True,
            authorized_paths=(
                "src/example.py",
                "tests/test_example.py",
                "STATUS.md",
                "REVIEW-LOG.md",
                "HANDOFF.md",
            ),
            required_records=("STATUS.md", "REVIEW-LOG.md", "HANDOFF.md"),
        )
        self.assertEqual(handoff.status, "completed")
        self.assertEqual(handoff.handoff_result, "updated")

    def test_record_write_failure_restores_only_owned_current_bytes(self) -> None:
        restored = closeout.evaluate_closeout(
            record_write_state="fail_owned_current"
        )
        drifted = closeout.evaluate_closeout(
            record_write_state="fail_concurrent_drift"
        )
        self.assertEqual(restored.status, "failed")
        self.assertEqual(
            restored.rollback_action, "restored_owned_precommit_writes"
        )
        self.assertEqual(drifted.status, "blocked")
        self.assertEqual(drifted.rollback_action, "preserved_concurrent_drift")
        self.assertTrue(drifted.unrelated_files_preserved)

    def test_commit_failure_rolls_back_records_without_rewriting_history(self) -> None:
        result = closeout.evaluate_closeout(commit_state="fail")
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.commit_result, "failed")
        self.assertEqual(result.phase_reached, "records_written")
        self.assertEqual(result.synchronized_records, ())
        self.assertEqual(result.handoff_result, "not_required")
        self.assertEqual(
            result.rollback_action, "restored_owned_precommit_writes"
        )
        self.assertFalse(result.history_rewrite_performed)

    def test_postcommit_failure_preserves_commit_and_evidence(self) -> None:
        result = closeout.evaluate_closeout(postcommit_state="fail")
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.commit_result, "created")
        self.assertNotEqual(result.commit_identity, "none")
        self.assertEqual(
            result.rollback_action, "postcommit_evidence_preserved"
        )
        self.assertFalse(result.history_rewrite_performed)

    def test_resume_uses_actual_phase_and_avoids_duplicate_writes(self) -> None:
        records = closeout.evaluate_closeout(resume_phase="records_written")
        commit = closeout.evaluate_closeout(resume_phase="commit_created")
        postcommit = closeout.evaluate_closeout(
            resume_phase="postcommit_verified"
        )
        self.assertFalse(records.record_writes_performed)
        self.assertFalse(commit.record_writes_performed)
        self.assertEqual(commit.commit_result, "existing_current")
        self.assertEqual(postcommit.status, "completed")
        self.assertTrue(postcommit.postcommit_verified)

        for phase in ("commit_created", "postcommit_verified", "completed_current"):
            drifted = closeout.evaluate_closeout(
                resume_phase=phase,  # type: ignore[arg-type]
                current_commit_matches=False,
            )
            self.assertEqual(drifted.status, "blocked")
            self.assertEqual(
                drifted.blocking_reason,
                "current_commit_does_not_match_checkpoint",
            )

        revalidation_failed = closeout.evaluate_closeout(
            resume_phase="completed_current", postcommit_state="fail"
        )
        self.assertEqual(revalidation_failed.status, "failed")
        self.assertFalse(revalidation_failed.idempotent_noop)
        self.assertFalse(revalidation_failed.writes_performed)

    def test_drift_and_ambiguous_side_effects_do_not_blindly_retry(self) -> None:
        drifted = closeout.evaluate_closeout(resume_phase="drifted")
        ambiguous = closeout.evaluate_closeout(
            resume_phase="ambiguous_side_effect"
        )
        self.assertEqual(
            drifted.resume_action, "restart_from_earliest_reliable_boundary"
        )
        self.assertEqual(ambiguous.status, "blocked")
        self.assertFalse(ambiguous.writes_performed)

    def test_completed_current_is_idempotent(self) -> None:
        result = closeout.evaluate_closeout(resume_phase="completed_current")
        self.assertEqual(result.status, "completed")
        self.assertTrue(result.idempotent_noop)
        self.assertFalse(result.writes_performed)

    def test_closeout_never_claims_later_authority(self) -> None:
        result = closeout.evaluate_closeout()
        self.assertFalse(result.verification_replaced)
        self.assertFalse(result.formal_review_replaced)
        self.assertFalse(result.done_claimed)
        self.assertFalse(result.user_acceptance_claimed)
        self.assertFalse(result.route_changed)
        self.assertFalse(result.push_release_publish_authorized)
        self.assertFalse(result.external_framework_owner)
        self.assertFalse(result.history_rewrite_performed)

    def test_invalid_contract_fields_are_rejected(self) -> None:
        with self.assertRaises(closeout.NativeCloseoutPassError):
            closeout.evaluate_closeout(closeout_id="")
        with self.assertRaises(closeout.NativeCloseoutPassError):
            closeout.evaluate_closeout(authorized_paths=())
        with self.assertRaises(closeout.NativeCloseoutPassError):
            closeout.evaluate_closeout(required_records=())
        with self.assertRaises(closeout.NativeCloseoutPassError):
            closeout.evaluate_closeout(commit_intent="unknown")  # type: ignore[arg-type]
        with self.assertRaises(closeout.NativeCloseoutPassError):
            closeout.evaluate_closeout(resume_phase="unknown")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
