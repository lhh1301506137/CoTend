from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_requirements_clarification as clarification  # noqa: E402


class NativeRequirementsClarificationTests(unittest.TestCase):
    def test_repository_contract_and_eight_scenarios_pass(self) -> None:
        result = clarification.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 8)
        self.assertEqual(result["max_questions_per_scenario"], 1)
        self.assertFalse(result["external_route_owner"])
        self.assertFalse(result["parallel_truth_created"])

    def test_clear_request_does_not_create_a_question(self) -> None:
        result = clarification.evaluate_clarification("clear")
        self.assertEqual(result.route, "continue_existing_cotend_route")
        self.assertEqual(result.question_count, 0)

    def test_fuzzy_request_asks_exactly_one_question(self) -> None:
        result = clarification.evaluate_clarification("fuzzy")
        self.assertEqual(result.route_owner, "cotend_semantic_alignment")
        self.assertEqual(result.question_count, 1)

    def test_init_only_hands_back(self) -> None:
        result = clarification.evaluate_clarification(
            "fuzzy",
            entry_point="init",
        )
        self.assertEqual(result.route, "handback_to_cotend_semantic_alignment")
        self.assertEqual(result.question_count, 0)

    def test_init_cannot_consume_a_product_answer(self) -> None:
        with self.assertRaises(clarification.NativeClarificationError):
            clarification.evaluate_clarification(
                "pending_answer",
                entry_point="init",
                reply="recommended_1",
                question_kind="decision_worthy",
            )

    def test_bare_continue_does_not_select_pending_answer(self) -> None:
        result = clarification.evaluate_clarification(
            "pending_answer",
            reply="continue",
            question_kind="decision_worthy",
        )
        self.assertFalse(result.answer_selected)
        self.assertFalse(result.decision_log_required)
        self.assertEqual(result.question_count, 1)

    def test_recommended_one_is_persisted_before_route_effect(self) -> None:
        result = clarification.evaluate_clarification(
            "pending_answer",
            reply="recommended_1",
            question_kind="decision_worthy",
        )
        self.assertTrue(result.answer_selected)
        self.assertTrue(result.decision_log_required)
        self.assertTrue(result.persist_before_route_effect)

    def test_factual_answer_avoids_decision_log_noise(self) -> None:
        result = clarification.evaluate_clarification(
            "pending_answer",
            reply="explicit_answer",
            question_kind="factual",
        )
        self.assertTrue(result.answer_selected)
        self.assertFalse(result.decision_log_required)

    def test_external_evidence_never_owns_route(self) -> None:
        aligned = clarification.evaluate_clarification(
            "fuzzy",
            external_state="aligned",
        )
        conflict = clarification.evaluate_clarification(
            "fuzzy",
            external_state="conflict",
        )
        self.assertEqual(aligned.external_classification, "reference_only")
        self.assertEqual(conflict.external_classification, "conflict")
        self.assertFalse(aligned.external_route_owner)
        self.assertFalse(conflict.external_route_owner)

    def test_grill_me_adopted_blob_is_unchanged(self) -> None:
        result = clarification.verify_repository()
        self.assertEqual(
            result["grill_me_sha256"],
            clarification.EXPECTED_GRILL_ME_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
