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

import build_codex_plugin as package  # noqa: E402
import verify_plugin_submission_materials as submission  # noqa: E402


NEGATIVE_MUTATION_COUNT = 15


class PluginSubmissionMaterialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.materials = json.loads(
            submission.SUBMISSION_PATH.read_text(encoding="utf-8")
        )
        self.reviewer_tests = json.loads(
            submission.REVIEWER_TESTS_PATH.read_text(encoding="utf-8")
        )

    def validate(
        self,
        materials: dict[str, Any] | None = None,
        reviewer_tests: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return submission.validate_submission_materials(
            self.materials if materials is None else materials,
            self.reviewer_tests if reviewer_tests is None else reviewer_tests,
        )

    def test_valid_contract_binds_exact_production_candidate(self) -> None:
        result = self.validate()
        contract = package.validate_contract()
        self.assertEqual(result["status"], "draft_not_submitted")
        self.assertEqual(result["positive_cases"], 5)
        self.assertEqual(result["negative_cases"], 3)
        self.assertEqual(result["unresolved_blockers"], 9)
        self.assertEqual(
            result["package_digest"],
            package.path_hash_manifest_sha256(contract["expected_package_manifest"]),
        )
        self.assertEqual(self.materials["package"]["file_count"], 37)
        self.assertTrue(self.materials["package"]["final_identity_confirmed"])
        self.assertEqual(
            self.materials["package"]["identity_authority"],
            "initial_submission_identity_confirmed_not_release",
        )

    def test_listing_and_starter_prompts_match_plugin_manifest(self) -> None:
        manifest = package.validate_contract()["manifest"]
        interface = manifest["interface"]
        listing = self.materials["listing"]
        self.assertEqual(listing["plugin_name"], interface["displayName"])
        self.assertEqual(listing["short_description"], interface["shortDescription"])
        self.assertEqual(listing["long_description"], interface["longDescription"])
        self.assertEqual(self.materials["starter_prompts"], interface["defaultPrompt"])

    def test_reviewer_contract_has_exact_five_positive_three_negative(self) -> None:
        self.assertEqual(
            [case["id"] for case in self.reviewer_tests["positive_cases"]],
            submission.EXPECTED_POSITIVE_IDS,
        )
        self.assertEqual(
            [case["id"] for case in self.reviewer_tests["negative_cases"]],
            submission.EXPECTED_NEGATIVE_IDS,
        )
        self.assertTrue(
            all(
                case["execution_status"] == "contract_only_not_run"
                for case in self.reviewer_tests["positive_cases"]
                + self.reviewer_tests["negative_cases"]
            )
        )

    def test_reviewer_fixtures_are_public_and_self_contained(self) -> None:
        context = self.reviewer_tests["reviewer_context"]
        self.assertFalse(context["plugin_specific_authentication_required"])
        self.assertFalse(context["plugin_specific_account_required"])
        self.assertFalse(context["plugin_backend_required"])
        self.assertFalse(context["api_key_required"])
        self.assertFalse(context["demo_credentials_required"])
        self.assertFalse(context["private_network_required"])
        for case in (
            self.reviewer_tests["positive_cases"]
            + self.reviewer_tests["negative_cases"]
        ):
            self.assertFalse(case["fixture"]["plugin_specific_authentication_required"])
            self.assertFalse(case["fixture"]["external_fixture_network_required"])
            self.assertFalse(case["fixture"]["private_context_required"])

    def test_external_requirements_remain_real_blockers(self) -> None:
        self.assertEqual(
            [blocker["id"] for blocker in self.materials["blockers"]],
            submission.EXPECTED_BLOCKER_IDS,
        )
        identity, *external = self.materials["blockers"]
        self.assertEqual(identity["status"], "resolved")
        self.assertEqual(identity["value"], submission.EXPECTED_IDENTITY_VALUE)
        self.assertTrue(
            all(
                blocker["status"] == "unresolved" and blocker["value"] is None
                for blocker in external
            )
        )
        self.assertEqual(
            self.materials["readiness"]["unresolved_blocker_ids"],
            submission.EXPECTED_UNRESOLVED_BLOCKER_IDS,
        )
        self.assertEqual(
            self.materials["readiness"]["status"],
            "blocked_not_ready_for_portal_submission",
        )
        self.assertFalse(self.materials["readiness"]["portal_submission_ready"])
        self.assertEqual(self.materials["authority"], submission.EXPECTED_AUTHORITY)

    def test_release_notes_are_initial_draft_not_submission_claim(self) -> None:
        notes = self.materials["release_notes"]
        self.assertEqual(notes["status"], "draft_not_submitted")
        self.assertEqual(notes["submission_kind"], "initial_submission")
        self.assertIn("Initial submission", notes["initial_or_update"])
        self.assertIn("No CoTend account", notes["reviewer_setup"])

    def test_fifteen_negative_mutations_are_rejected(self) -> None:
        def mutate_materials(
            callback: Callable[[dict[str, Any]], None],
        ) -> tuple[dict[str, Any], dict[str, Any]]:
            materials = copy.deepcopy(self.materials)
            callback(materials)
            return materials, copy.deepcopy(self.reviewer_tests)

        def mutate_tests(
            callback: Callable[[dict[str, Any]], None],
        ) -> tuple[dict[str, Any], dict[str, Any]]:
            tests = copy.deepcopy(self.reviewer_tests)
            callback(tests)
            return copy.deepcopy(self.materials), tests

        mutations = {
            "submission_status": mutate_materials(
                lambda value: value.__setitem__("status", "submitted")
            ),
            "portal_draft_claim": mutate_materials(
                lambda value: value["authority"].__setitem__(
                    "portal_draft_created", True
                )
            ),
            "fake_publisher": mutate_materials(
                lambda value: value["publisher"].__setitem__(
                    "verified_identity", "Unverified Publisher"
                )
            ),
            "placeholder_website": mutate_materials(
                lambda value: value["listing"]["public_urls"].__setitem__(
                    "website_url", "https://example.com"
                )
            ),
            "resolved_without_evidence": mutate_materials(
                lambda value: value["blockers"][1].__setitem__("status", "resolved")
            ),
            "package_digest_drift": mutate_materials(
                lambda value: value["package"].__setitem__(
                    "path_hash_manifest_sha256", "0" * 64
                )
            ),
            "starter_prompt_drift": mutate_materials(
                lambda value: value["starter_prompts"].__setitem__(0, "Start.")
            ),
            "availability_claim": mutate_materials(
                lambda value: value["availability"].__setitem__("status", "selected")
            ),
            "missing_positive_case": mutate_tests(
                lambda value: value["positive_cases"].pop()
            ),
            "extra_negative_case": mutate_tests(
                lambda value: value["negative_cases"].append(
                    copy.deepcopy(value["negative_cases"][0])
                )
            ),
            "missing_expected_result": mutate_tests(
                lambda value: value["positive_cases"][0].pop("expected_result_shape")
            ),
            "executed_case_claim": mutate_tests(
                lambda value: value["positive_cases"][0].__setitem__(
                    "execution_status", "passed"
                )
            ),
            "private_fixture_path": mutate_tests(
                lambda value: value["negative_cases"][0]["fixture"].__setitem__(
                    "setup", "Read files from " + "C" + ":/private-project."
                )
            ),
            "empty_submission_object": (
                {},
                copy.deepcopy(self.reviewer_tests),
            ),
            "embedded_unapproved_url": mutate_materials(
                lambda value: value["release_notes"].__setitem__(
                    "what_plugin_does",
                    "Read setup details at https://invalid.test/setup before use.",
                )
            ),
        }
        self.assertEqual(len(mutations), NEGATIVE_MUTATION_COUNT)
        for case_id, (materials, tests) in mutations.items():
            with self.subTest(case_id=case_id):
                with self.assertRaises(submission.SubmissionMaterialError):
                    self.validate(materials, tests)


if __name__ == "__main__":
    unittest.main()
