from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_spec_change_route_rebase as route_rebase  # noqa: E402


class NativeSpecChangeRouteRebaseTests(unittest.TestCase):
    def test_repository_contract_and_ten_scenarios_pass(self) -> None:
        result = route_rebase.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 10)
        self.assertFalse(result["external_route_owner"])
        self.assertFalse(result["parallel_spec_tree_created"])
        self.assertTrue(result["old_decisions_preserved"])

    def test_ordinary_leaf_does_not_create_packet(self) -> None:
        result = route_rebase.evaluate_route_change("ordinary_leaf")
        self.assertFalse(result.packet_required)
        self.assertTrue(result.next_leaf_advance_allowed)

    def test_material_l3_l4_change_is_primary_owned(self) -> None:
        result = route_rebase.evaluate_route_change("material_l3_l4")
        self.assertEqual(result.route_owner, "cotend_plan_tree")
        self.assertFalse(result.user_decision_required)
        self.assertTrue(result.candidate_active)

    def test_l0_l2_candidate_waits_for_explicit_decision(self) -> None:
        result = route_rebase.evaluate_route_change("material_l0_l2")
        self.assertEqual(result.status, "pending_user_confirmation")
        self.assertTrue(result.user_decision_required)
        self.assertFalse(result.candidate_active)

    def test_bare_continue_does_not_accept_candidate(self) -> None:
        result = route_rebase.evaluate_route_change(
            "material_l0_l2",
            decision="continue",
        )
        self.assertFalse(result.answer_selected)
        self.assertFalse(result.candidate_active)
        self.assertEqual(result.status, "pending_user_confirmation")

    def test_acceptance_is_persisted_before_route_effect(self) -> None:
        result = route_rebase.evaluate_route_change(
            "material_l0_l2",
            decision="accept",
        )
        self.assertTrue(result.answer_selected)
        self.assertTrue(result.decision_persisted_before_route_effect)
        self.assertEqual(result.completion_evidence, "revalidation_required")

    def test_rejection_restores_previous_path_and_preserves_history(self) -> None:
        result = route_rebase.evaluate_route_change(
            "material_l0_l2",
            decision="reject",
        )
        self.assertEqual(result.resulting_path, "previous_path_restored_or_retained")
        self.assertEqual(result.history_disposition, "candidate_rejected_and_preserved")
        self.assertTrue(result.old_decisions_preserved)

    def test_unrelated_route_requires_positive_isolation(self) -> None:
        blocked = route_rebase.evaluate_route_change("material_l0_l2")
        isolated = route_rebase.evaluate_route_change(
            "material_l0_l2",
            dependency_isolated=True,
        )
        self.assertFalse(blocked.unaffected_route_can_continue)
        self.assertTrue(isolated.unaffected_route_can_continue)

    def test_changed_evidence_basis_never_inherits_completion(self) -> None:
        result = route_rebase.evaluate_route_change(
            "material_l3_l4",
            evidence_basis_changed=True,
        )
        self.assertEqual(result.completion_evidence, "revalidation_required")
        self.assertFalse(result.next_leaf_advance_allowed)

    def test_interrupted_apply_resumes_from_reliable_boundary(self) -> None:
        result = route_rebase.evaluate_route_change(
            "material_l3_l4",
            interrupted_at="applying",
        )
        self.assertEqual(result.status, "applying")
        self.assertEqual(
            result.reliable_resume_boundary,
            "earliest_jointly_trustworthy_boundary",
        )
        self.assertFalse(result.next_leaf_advance_allowed)

    def test_external_spec_conflict_never_owns_route(self) -> None:
        result = route_rebase.evaluate_route_change(
            "material_l3_l4",
            external_state="conflict",
        )
        self.assertEqual(result.status, "blocked")
        self.assertEqual(result.external_classification, "conflict")
        self.assertFalse(result.external_route_owner)

    def test_invalid_state_combinations_fail_closed(self) -> None:
        with self.assertRaises(route_rebase.NativeRouteRebaseError):
            route_rebase.evaluate_route_change(
                "ordinary_leaf",
                decision="accept",
            )
        with self.assertRaises(route_rebase.NativeRouteRebaseError):
            route_rebase.evaluate_route_change(
                "material_l3_l4",
                decision="accept",
            )
        with self.assertRaises(route_rebase.NativeRouteRebaseError):
            route_rebase.evaluate_route_change(
                "material_l0_l2",
                interrupted_at="applying",
            )


if __name__ == "__main__":
    unittest.main()
