from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_cumulative_main_journey as journey  # noqa: E402


class NativeCumulativeMainJourneyTests(unittest.TestCase):
    def test_repository_contract_and_three_evidence_groups(self) -> None:
        result = journey.verify_repository()
        self.assertEqual(
            result["status"], "native_cumulative_main_journey_verified"
        )
        self.assertEqual(result["evidence_group_count"], 3)
        self.assertEqual(result["journey_scenario_count"], 3)
        self.assertEqual(result["native_capabilities_composed"], 8)
        self.assertFalse(result["real_user_acceptance_claimed"])
        self.assertFalse(result["skill_behavior_changed"])
        self.assertEqual(result["target_artifact"], "cotend-codex-r000014")

    def test_full_and_adaptive_have_equivalent_semantic_outcomes(self) -> None:
        full = journey.run_main_journey("full")
        adaptive = journey.run_main_journey("adaptive")
        self.assertEqual(
            journey.equivalence_projection(full),
            journey.equivalence_projection(adaptive),
        )
        self.assertEqual(full.execution_mode, "delegated_pair")
        self.assertEqual(adaptive.execution_mode, "inline")
        self.assertNotEqual(full.handoff_digest, adaptive.handoff_digest)

    def test_stage_outputs_are_the_next_stage_inputs(self) -> None:
        result = journey.run_main_journey("full")
        evaluators = {record.evaluator for record in result.stage_records}
        self.assertEqual(evaluators, set(journey.EXPECTED_STAGE_EVALUATORS))
        self.assertTrue(set(journey.EXPECTED_NATIVE_EVALUATORS) <= evaluators)
        for previous, current in zip(result.stage_records, result.stage_records[1:]):
            self.assertEqual(current.input_identity, previous.output_identity)

    def test_stage_order_preserves_control_and_acceptance_boundaries(self) -> None:
        result = journey.run_main_journey("full")
        self.assertEqual(
            [record.stage for record in result.stage_records],
            [
                "project_truth_authority",
                "workflow_state_runtime_profile",
                "project_init",
                "init_handback_resume_event",
                "requirements_clarification",
                "plan_route",
                "predevelopment_readiness",
                "implementation_pass",
                "verification_pass",
                "formal_self_review_fixture",
                "closeout_pass",
                "goal_completion_gate",
                "synthetic_acceptance_gate",
                "handoff_serialization",
                "new_session_recovery",
            ],
        )

    def test_bare_continue_and_implicit_ai_cannot_accept(self) -> None:
        for event in ("continue", "implicit_ai_accept"):
            result = journey.evaluate_acceptance(
                "awaiting_explicit_acceptance", event  # type: ignore[arg-type]
            )
            self.assertEqual(result.status, "awaiting_explicit_acceptance")
            self.assertFalse(result.state_changed)
            self.assertTrue(result.explicit_event_required)
            self.assertFalse(result.real_user_acceptance_claimed)

        accepted = journey.evaluate_acceptance(
            "awaiting_explicit_acceptance", "synthetic_accept"
        )
        self.assertEqual(accepted.status, "accepted_synthetic")
        self.assertTrue(accepted.state_changed)
        self.assertFalse(accepted.real_user_acceptance_claimed)

    def test_unlabelled_synthetic_acceptance_is_rejected(self) -> None:
        with self.assertRaises(journey.NativeCumulativeJourneyError):
            journey.evaluate_acceptance(
                "awaiting_explicit_acceptance",
                "synthetic_accept",
                synthetic_fixture=False,
            )

    def test_handoff_round_trip_uses_serialized_state_and_rejects_tampering(
        self,
    ) -> None:
        result = journey.run_main_journey("full")
        recovered = journey.recover_handoff(
            result.handoff_document, session_id="independent-session"
        )
        self.assertEqual(recovered.goal_id, result.goal_id)
        self.assertEqual(recovered.decisions, result.decisions)
        self.assertEqual(recovered.route_revision, result.route_revision)
        self.assertEqual(recovered.acceptance_status, "accepted_synthetic")
        self.assertEqual(recovered.next_mode, "new_goal_needed")
        self.assertFalse(recovered.automatic_product_work_started)

        tampered = json.loads(result.handoff_document)
        tampered["payload"]["goal_id"] = "different-goal"
        with self.assertRaises(journey.NativeCumulativeJourneyError):
            journey.recover_handoff(
                json.dumps(tampered), session_id="independent-session"
            )

        missing = json.loads(result.handoff_document)
        del missing["payload"]["decisions"]
        with self.assertRaises(journey.NativeCumulativeJourneyError):
            journey.recover_handoff(
                json.dumps(missing), session_id="independent-session"
            )

    def test_interrupted_route_rebase_invalidates_old_evidence(self) -> None:
        result = journey.run_main_journey(
            "full",
            journey_id="route-rebase-test",
            route_rebase_interruption=True,
        )
        self.assertEqual(result.route_revision, 2)
        self.assertEqual(result.invalidated_identity_count, 2)
        self.assertEqual(
            result.reliable_resume_boundary,
            "earliest_jointly_trustworthy_boundary",
        )
        stages = [record.stage for record in result.stage_records]
        self.assertIn("route_rebase_interrupted", stages)
        self.assertIn("route_rebase_resumed", stages)

    def test_a_blocked_evaluator_prevents_a_false_cumulative_pass(self) -> None:
        blocked = journey.native_implementation.evaluate_implementation(
            authorized=False
        )
        with mock.patch.object(
            journey.native_implementation,
            "evaluate_implementation",
            return_value=blocked,
        ):
            with self.assertRaises(journey.NativeCumulativeJourneyError):
                journey.run_main_journey("full")

    def test_handoff_cannot_claim_real_user_acceptance(self) -> None:
        result = journey.run_main_journey("full")
        envelope = json.loads(result.handoff_document)
        envelope["payload"]["real_user_acceptance_claimed"] = True
        payload_text = json.dumps(
            envelope["payload"],
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
        import hashlib

        envelope["digest"] = "sha256:" + hashlib.sha256(
            payload_text.encode("utf-8")
        ).hexdigest()
        with self.assertRaises(journey.NativeCumulativeJourneyError):
            journey.recover_handoff(
                json.dumps(envelope), session_id="independent-session"
            )


if __name__ == "__main__":
    unittest.main()
