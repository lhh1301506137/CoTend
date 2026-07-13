from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_plugin_submission_materials as submission  # noqa: E402
import verify_submission_prerequisites as prerequisites  # noqa: E402


NEGATIVE_MUTATION_COUNT = 14


class SubmissionPrerequisiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = json.loads(
            prerequisites.PREREQUISITES_PATH.read_text(encoding="utf-8")
        )
        self.submission = json.loads(
            submission.SUBMISSION_PATH.read_text(encoding="utf-8")
        )

    def validate(
        self,
        packet: dict[str, Any] | None = None,
        submission_contract: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return prerequisites.validate_submission_prerequisites(
            self.packet if packet is None else packet,
            self.submission if submission_contract is None else submission_contract,
        )

    def test_valid_packet_binds_exact_candidate_and_submission_contract(self) -> None:
        result = self.validate()
        self.assertEqual(result["status"], "awaiting_owner_decisions")
        self.assertEqual(result["prerequisites"], 10)
        self.assertEqual(result["decisions"], 7)
        self.assertEqual(result["active_decision"], "Q02-final-plugin-identity")
        self.assertEqual(
            result["package_digest"],
            self.submission["package"]["path_hash_manifest_sha256"],
        )
        q02 = self.packet["decisions"][1]
        self.assertIn("尚未验证", q02["options"][0]["impact_zh"])
        self.assertIn("重新打开 Q02", q02["options"][0]["impact_zh"])

    def test_prerequisites_exactly_map_ten_canonical_blockers(self) -> None:
        canonical = [blocker["id"] for blocker in self.submission["blockers"]]
        packet_ids = [item["id"] for item in self.packet["prerequisites"]]
        self.assertEqual(packet_ids, canonical)
        self.assertEqual(packet_ids, submission.EXPECTED_BLOCKER_IDS)
        covered = [
            blocker_id
            for decision in self.packet["decisions"]
            for blocker_id in decision["blocker_ids"]
        ]
        self.assertEqual(sorted(covered), sorted(canonical))

    def test_decision_graph_is_acyclic_and_one_at_a_time(self) -> None:
        seen: set[str] = set()
        awaiting: list[str] = []
        for decision in self.packet["decisions"]:
            self.assertTrue(set(decision["depends_on"]).issubset(seen))
            if decision["status"] == "awaiting_user_decision":
                awaiting.append(decision["id"])
            seen.add(decision["id"])
        self.assertEqual(awaiting, ["Q02-final-plugin-identity"])
        self.assertFalse(
            self.packet["decision_policy"]["ordinary_continue_answers_decision"]
        )

    def test_policy_attestations_are_the_final_gate(self) -> None:
        policy = self.packet["prerequisites"][-1]
        self.assertEqual(policy["id"], "policy_attestations")
        self.assertEqual(policy["depends_on"], submission.EXPECTED_BLOCKER_IDS[:-1])
        self.assertTrue(policy["openai_platform_required"])
        self.assertFalse(policy["repository_can_prepare"])

    def test_repository_and_external_responsibilities_are_explicit(self) -> None:
        by_id = {item["id"]: item for item in self.packet["prerequisites"]}
        self.assertTrue(by_id["production_logo"]["repository_can_prepare"])
        self.assertFalse(by_id["verified_publisher_identity"]["repository_can_prepare"])
        self.assertTrue(
            by_id["verified_publisher_identity"]["external_action_required"]
        )
        self.assertEqual(by_id["website_url"]["completion_location"], "public_web")
        self.assertTrue(
            all(len(item["completion_evidence_zh"]) >= 2 for item in by_id.values())
        )

    def test_q01_route_is_recorded_but_external_authority_remains_unset(self) -> None:
        self.assertTrue(
            all(
                item["status"] == "unresolved" and item["value"] is None
                for item in self.packet["prerequisites"]
            )
        )
        q01, *remaining = self.packet["decisions"]
        self.assertEqual(q01["status"], "answered")
        self.assertEqual(q01["answer"], "1")
        self.assertEqual(q01["evidence"]["evidence_type"], "user_explicit")
        self.assertTrue(
            all(
                decision["answer"] is None and decision["evidence"] is None
                for decision in remaining
            )
        )
        authority = self.packet["authority"]
        self.assertTrue(authority["repository_preparation_only"])
        self.assertTrue(authority["publisher_mode_selected"])
        self.assertTrue(
            all(
                value is False
                for key, value in authority.items()
                if key not in {"repository_preparation_only", "publisher_mode_selected"}
            )
        )

    def test_q01_explains_publisher_mode_tradeoff_in_chinese(self) -> None:
        q01 = self.packet["decisions"][0]
        self.assertEqual(q01["id"], "Q01-publisher-mode")
        self.assertEqual(q01["status"], "answered")
        self.assertEqual(q01["answer"], "1")
        self.assertEqual(q01["recommended_option_id"], "1")
        self.assertEqual([option["id"] for option in q01["options"]], ["1", "2", "3"])
        self.assertIn("个人身份", q01["options"][0]["label_zh"])
        self.assertIn("企业身份", q01["options"][1]["label_zh"])
        self.assertIn("个人名称", q01["options"][0]["impact_zh"])

    def test_fourteen_negative_mutations_are_rejected(self) -> None:
        def mutate_packet(
            callback: Callable[[dict[str, Any]], None],
        ) -> tuple[dict[str, Any], dict[str, Any]]:
            packet = copy.deepcopy(self.packet)
            callback(packet)
            return packet, copy.deepcopy(self.submission)

        mutations = {
            "schema_drift": mutate_packet(
                lambda value: value.__setitem__("schema", "invalid")
            ),
            "ready_claim": mutate_packet(
                lambda value: value.__setitem__("status", "ready")
            ),
            "package_digest_drift": mutate_packet(
                lambda value: value["package"].__setitem__(
                    "path_hash_manifest_sha256", "0" * 64
                )
            ),
            "missing_prerequisite": mutate_packet(
                lambda value: value["prerequisites"].pop()
            ),
            "reordered_prerequisites": mutate_packet(
                lambda value: value["prerequisites"].reverse()
            ),
            "resolved_without_evidence": mutate_packet(
                lambda value: value["prerequisites"][0].__setitem__(
                    "status", "resolved"
                )
            ),
            "invented_identity": mutate_packet(
                lambda value: value["prerequisites"][1].__setitem__(
                    "value", "Invented Publisher"
                )
            ),
            "filled_owner_answer": mutate_packet(
                lambda value: value["decisions"][1].__setitem__("answer", "1")
            ),
            "two_active_decisions": mutate_packet(
                lambda value: value["decisions"][2].__setitem__(
                    "status", "awaiting_user_decision"
                )
            ),
            "decision_cycle": mutate_packet(
                lambda value: value["decisions"][0].__setitem__(
                    "depends_on", ["Q07-policy-attestations"]
                )
            ),
            "duplicate_blocker_mapping": mutate_packet(
                lambda value: value["decisions"][1].__setitem__(
                    "blocker_ids", ["verified_publisher_identity"]
                )
            ),
            "policy_not_last": mutate_packet(
                lambda value: value["prerequisites"][-1].__setitem__("depends_on", [])
            ),
            "portal_opened_claim": mutate_packet(
                lambda value: value["authority"].__setitem__("portal_opened", True)
            ),
            "wrong_next_action": mutate_packet(
                lambda value: value["next_action"].__setitem__(
                    "decision_id", "Q03-public-web-presence"
                )
            ),
        }
        self.assertEqual(len(mutations), NEGATIVE_MUTATION_COUNT)
        for case_id, (packet, submission_contract) in mutations.items():
            with self.subTest(case_id=case_id):
                with self.assertRaises(prerequisites.SubmissionPrerequisiteError):
                    self.validate(packet, submission_contract)


if __name__ == "__main__":
    unittest.main()
