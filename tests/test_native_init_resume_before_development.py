from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_init_resume_before_development as native_entry  # noqa: E402


class NativeInitResumeBeforeDevelopmentTests(unittest.TestCase):
    def test_repository_contract_and_exact_runtime_inventory(self) -> None:
        result = native_entry.verify_repository()
        self.assertEqual(result["status"], "native_parity_verified")
        self.assertEqual(result["runtime_mentions"], 0)
        self.assertEqual(result["runtime_files"], 0)
        self.assertEqual(result["td02_commands"], 0)
        self.assertEqual(result["remaining_commands"], 0)
        self.assertEqual(result["target_artifact"], "cotend-codex-r000013")

    def test_all_entry_modes_and_stops_are_covered(self) -> None:
        result = native_entry.verify_repository()
        self.assertEqual(len(result["entry_scenarios"]), 13)
        self.assertEqual(
            {
                payload["auto_mode"]
                for payload in result["entry_scenarios"].values()
            },
            {
                "fresh_init",
                "legacy_update",
                "partial_repair",
                "current_resume",
                "blocked_human_decision",
            },
        )

    def test_explicit_init_never_starts_product_work(self) -> None:
        for contract in native_entry.ENTRY_SCENARIOS.values():
            result = native_entry.evaluate_entry(**contract["kwargs"])
            self.assertFalse(result.same_response_product_work_started)

    def test_bare_continue_only_matches_generic_handback(self) -> None:
        generic = native_entry.evaluate_entry("current")
        specialized = native_entry.evaluate_entry(
            "current",
            pending_specialized_decision=True,
        )
        self.assertTrue(generic.bare_continue_allowed)
        self.assertFalse(specialized.bare_continue_allowed)
        self.assertTrue(specialized.specialized_decision_preserved)

    def test_repeated_initialization_is_a_no_op(self) -> None:
        first = native_entry.evaluate_entry("absent")
        repeated = native_entry.evaluate_entry("current")
        self.assertTrue(first.write_performed)
        self.assertFalse(repeated.write_performed)
        self.assertEqual(repeated.write_actions, ())

    def test_predevelopment_loads_truth_before_code_context(self) -> None:
        result = native_entry.evaluate_predevelopment()
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.load_order, native_entry.LOAD_ORDER)
        self.assertLess(
            result.load_order.index("current_truth"),
            result.load_order.index("code_context_provider_and_impact"),
        )
        self.assertTrue(result.truth_loaded_before_code_context)

    def test_codegraph_fallback_is_recorded(self) -> None:
        result = native_entry.evaluate_predevelopment(
            provider_state="codegraph_missing"
        )
        self.assertEqual(result.provider, "rg_fallback")
        self.assertEqual(result.provider_action, "record_fallback")
        self.assertTrue(result.broad_edits_allowed)

    def test_ambiguous_root_and_pending_decision_fail_closed(self) -> None:
        ambiguous = native_entry.evaluate_predevelopment(
            canonical_root_clear=False
        )
        pending = native_entry.evaluate_predevelopment(
            specialized_decision_pending=True
        )
        self.assertEqual(ambiguous.blocking_reason, "canonical_root_ambiguous")
        self.assertEqual(pending.blocking_reason, "specialized_decision_required")
        self.assertFalse(ambiguous.broad_edits_allowed)
        self.assertFalse(pending.broad_edits_allowed)

    def test_repeated_predevelopment_preserves_scope_and_stops_writing(self) -> None:
        first = native_entry.evaluate_predevelopment(
            provider_state="codegraph_unindexed"
        )
        repeated = native_entry.evaluate_predevelopment(
            provider_state="codegraph_fresh"
        )
        self.assertTrue(first.generated_index_write)
        self.assertFalse(repeated.generated_index_write)
        self.assertEqual(first.scope_signature, repeated.scope_signature)

    def test_td02_commands_and_all_remaining_compatibility_commands_are_removed(self) -> None:
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "skills").rglob("*"))
            if path.is_file()
        )
        for command in native_entry.REMOVED_TD02_COMMANDS:
            self.assertNotIn(command, text)
        for command in native_entry.REQUIRED_REMAINING_COMMANDS:
            self.assertIn(command, text)


if __name__ == "__main__":
    unittest.main()
