from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_project_truth_authority as authority  # noqa: E402


class NativeProjectTruthAuthorityTests(unittest.TestCase):
    def test_repository_contract_and_six_scenarios_pass(self) -> None:
        result = authority.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["scenario_count"], 6)
        self.assertFalse(result["external_authority"])
        self.assertFalse(result["parallel_truth_created"])

    def test_aligned_external_artifact_is_reference_only(self) -> None:
        result = authority.evaluate_external_artifact("aligned")
        self.assertEqual(result.classification, "reference_only")
        self.assertEqual(result.action, "link_without_delegation")
        self.assertFalse(result.external_is_authority)

    def test_stale_external_artifact_is_historical(self) -> None:
        result = authority.evaluate_external_artifact("stale")
        self.assertEqual(result.classification, "historical")
        self.assertEqual(result.blocked_scope, "none")

    def test_protected_conflict_stops_only_affected_scope_for_user(self) -> None:
        result = authority.evaluate_external_artifact("conflict", "L0_L2")
        self.assertEqual(result.blocked_scope, "affected_semantic_scope")
        self.assertTrue(result.user_decision_required)
        self.assertIn("semantic_alignment", result.action)

    def test_execution_conflict_rebases_cotend_route_without_external_owner(self) -> None:
        result = authority.evaluate_external_artifact("conflict", "L3_L4")
        self.assertEqual(result.route_owner, "cotend_plan_tree")
        self.assertFalse(result.user_decision_required)
        self.assertFalse(result.external_is_authority)

    def test_unknown_impact_blocks_affected_dependencies_until_classified(self) -> None:
        result = authority.evaluate_external_artifact("unknown")
        self.assertEqual(result.classification, "conflict")
        self.assertEqual(result.blocked_scope, "affected_dependencies")

    def test_explicit_project_equivalent_avoids_second_route_tree(self) -> None:
        result = authority.evaluate_external_artifact(
            "aligned",
            has_plan_tree=False,
            has_project_equivalent_route=True,
        )
        self.assertEqual(result.route_owner, "project_equivalent_route")
        self.assertFalse(result.create_parallel_truth)

    def test_two_route_owners_are_rejected(self) -> None:
        with self.assertRaises(authority.NativeAuthorityError):
            authority.evaluate_external_artifact(
                "aligned",
                has_plan_tree=True,
                has_project_equivalent_route=True,
            )

    def test_legacy_external_authority_wording_is_rejected(self) -> None:
        sample = "Active Trellis owns task and spec lifecycle."
        self.assertTrue(
            authority.FORBIDDEN_AUTHORITY_PATTERNS["active_trellis_owns"].search(
                sample
            )
        )


if __name__ == "__main__":
    unittest.main()
