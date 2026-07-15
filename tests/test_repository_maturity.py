from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_repository_maturity as maturity  # noqa: E402


class RepositoryMaturityTests(unittest.TestCase):
    def test_required_public_entry_points_are_present_and_linked(self) -> None:
        result = maturity.validate_public_entry_points()
        self.assertEqual(result["community_policies"], 6)
        self.assertEqual(result["issue_forms"], 2)
        self.assertGreaterEqual(result["required_files"], 28)

    def test_ci_is_cross_platform_and_read_only(self) -> None:
        result = maturity.validate_ci_workflow()
        self.assertEqual(result["operating_systems"], 2)
        self.assertEqual(result["python_versions"], 2)
        self.assertEqual(result["matrix_jobs"], 3)
        self.assertEqual(result["pinned_ci_dependencies"], 1)

    def test_ci_installs_exactly_pinned_yaml_dependency(self) -> None:
        original = maturity.CI_PATH.read_text(encoding="utf-8")
        install = (
            "python -m pip install --disable-pip-version-check "
            "--requirement requirements-ci.txt"
        )
        with self.assertRaises(maturity.RepositoryMaturityError):
            maturity.validate_ci_workflow(original.replace(install, ""))
        with self.assertRaises(maturity.RepositoryMaturityError):
            maturity.validate_ci_workflow(
                original,
                requirements_text="PyYAML>=6.0\n",
            )

    def test_release_workflow_is_manual_tag_bound_and_draft_only(self) -> None:
        result = maturity.validate_release_workflow()
        self.assertTrue(result["manual_only"])
        self.assertTrue(result["existing_tag_required"])
        self.assertTrue(result["draft_only"])
        self.assertFalse(result["publish_supported"])

    def test_release_workflow_rejects_automatic_or_publish_behavior(self) -> None:
        original = maturity.RELEASE_WORKFLOW_PATH.read_text(encoding="utf-8")
        automatic = original.replace("  workflow_dispatch:", "  push:\n  workflow_dispatch:")
        with self.assertRaises(maturity.RepositoryMaturityError):
            maturity.validate_release_workflow(automatic)

        publishing = original + "\n# gh release edit v0.1.0-rc.1 --draft=false\n"
        with self.assertRaises(maturity.RepositoryMaturityError):
            maturity.validate_release_workflow(publishing)

    def test_repository_settings_define_exact_metadata_and_public_url_candidates(self) -> None:
        result = maturity.validate_repository_settings()
        self.assertEqual(result["topics"], 7)
        self.assertEqual(result["public_url_candidates"], 4)
        self.assertTrue(result["external_application_required"])

    def test_all_relative_markdown_links_resolve(self) -> None:
        result = maturity.validate_relative_markdown_links()
        self.assertGreaterEqual(result["markdown_files"], 70)
        self.assertGreaterEqual(result["relative_links"], 40)

    def test_static_maturity_contract_preserves_external_boundaries(self) -> None:
        result = maturity.validate_repository_maturity(build_artifacts=False)
        self.assertEqual(
            result["status"],
            "repository_internal_maturity_ready_external_state_not_checked",
        )
        self.assertFalse(result["external_state_checked"])
        self.assertEqual(result["external_state_source"], "GitHub")
        self.assertIsNone(result["public_push_performed"])
        self.assertIsNone(result["github_settings_applied"])
        self.assertIsNone(result["tag_created"])
        self.assertIsNone(result["release_created"])
        self.assertFalse(result["reviewer_fixtures"]["model_execution_performed"])


if __name__ == "__main__":
    unittest.main()
