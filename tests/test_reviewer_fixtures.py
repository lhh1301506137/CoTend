from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
import uuid
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import prepare_reviewer_fixtures as fixtures  # noqa: E402


class ReviewerFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.output = ROOT / "dist" / "reviewer-fixture-tests" / uuid.uuid4().hex
        self.contract = json.loads(
            fixtures.FIXTURE_CONTRACT_PATH.read_text(encoding="utf-8")
        )

    def tearDown(self) -> None:
        if self.output.exists():
            fixtures.remove_generated_tree(self.output)

    def test_fixture_contract_matches_five_plus_three_reviewer_cases(self) -> None:
        result = fixtures.validate_fixture_contract(self.contract)
        self.assertEqual(result["case_count"], 8)
        self.assertEqual(result["positive_count"], 5)
        self.assertEqual(result["negative_count"], 3)
        self.assertEqual(result["preflight_count"], 5)

    def test_materialized_fixtures_are_clean_git_repositories(self) -> None:
        result = fixtures.prepare_fixtures(self.output)
        self.assertFalse(result["model_execution_performed"])
        for case_id in fixtures.EXPECTED_CASE_IDS:
            case_root = self.output / case_id
            self.assertTrue((case_root / ".git").is_dir())
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=case_root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertEqual(status, "")

    def test_preflight_results_preserve_pass_and_expected_failure_cases(self) -> None:
        result = fixtures.prepare_fixtures(self.output)
        self.assertEqual(result["preflight_count"], 5)
        self.assertEqual(result["preflight_passed"], 3)
        self.assertEqual(result["preflight_expected_failures"], 2)

    def test_existing_unowned_output_is_not_overwritten(self) -> None:
        self.output.mkdir(parents=True)
        sentinel = self.output / "USER-DATA.txt"
        sentinel.write_text("preserve\n", encoding="utf-8")
        with self.assertRaises(fixtures.ReviewerFixtureError):
            fixtures.prepare_fixtures(self.output)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve\n")

    def test_path_escape_and_private_content_are_rejected(self) -> None:
        path_escape = copy.deepcopy(self.contract)
        path_escape["cases"][1]["files"]["../escape.txt"] = "escape\n"
        with self.assertRaises(fixtures.ReviewerFixtureError):
            fixtures.validate_fixture_contract(path_escape)

        private_text = copy.deepcopy(self.contract)
        private_text["cases"][1]["files"]["PRIVATE.txt"] = (
            "Read " + "C" + ":/private/file.\n"
        )
        with self.assertRaises(fixtures.ReviewerFixtureError):
            fixtures.validate_fixture_contract(private_text)

    def test_output_rejects_simulated_linked_generation_root(self) -> None:
        original = fixtures.package._is_linklike
        dist_root = ROOT / "dist"

        def classify(path: Path) -> bool:
            return path == dist_root or original(path)

        with mock.patch.object(
            fixtures.package, "_is_linklike", side_effect=classify
        ):
            with self.assertRaises(fixtures.ReviewerFixtureError):
                fixtures.guarded_output(dist_root / "reviewer-fixtures")

    def test_repeated_materialization_is_idempotent_for_working_files(self) -> None:
        fixtures.prepare_fixtures(self.output)
        first = {
            case_id: fixtures._working_files(self.output / case_id)
            for case_id in fixtures.EXPECTED_CASE_IDS
        }
        fixtures.prepare_fixtures(self.output)
        second = {
            case_id: fixtures._working_files(self.output / case_id)
            for case_id in fixtures.EXPECTED_CASE_IDS
        }
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
