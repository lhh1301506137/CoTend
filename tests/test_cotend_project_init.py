from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_cotend_project_init as project_init  # noqa: E402


class CoTendProjectInitContractTests(unittest.TestCase):
    def test_repository_has_concise_core_ten_references_and_three_scripts(self) -> None:
        result = project_init.load_project_init_contract()
        self.assertEqual(result["status"], "cotend_project_init_topology_verified")
        self.assertEqual(result["file_count"], 15)
        self.assertEqual(result["reference_count"], 10)
        self.assertEqual(result["script_count"], 3)
        self.assertLessEqual(result["core_lines"], 260)
        self.assertIn(
            "cotend.governance-language-pre-handback.v1", result["combined"]
        )
        self.assertIn('CONTRACT = "cotend.project-router.v1"', result["router"])
        self.assertIn("$cotend-collaboration", result["router"])
        self.assertIn("$cotend-session-handoff", result["router"])

    def test_nested_project_init_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cotend-project-init-topology-") as temp:
            root = Path(temp)
            target = root / "skills" / "cotend-project-init"
            shutil.copytree(ROOT / "skills" / "cotend-project-init", target)
            reference = target / "references" / project_init.EXPECTED_REFERENCES[0]
            reference.write_text(
                reference.read_text(encoding="utf-8")
                + "\nLoad `references/reporting-and-handback.md`.\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                project_init.ProjectInitContractError, "nested"
            ):
                project_init.load_project_init_contract(root)

    def test_private_checker_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cotend-project-init-checker-") as temp:
            root = Path(temp)
            target = root / "skills" / "cotend-project-init"
            shutil.copytree(ROOT / "skills" / "cotend-project-init", target)
            checker = target / "scripts" / "check_cotend_governance_language.py"
            checker.write_text(
                checker.read_text(encoding="utf-8")
                + '\nPRIVATE_REASON = "private_dual_chinese_body_threshold_met"\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                project_init.ProjectInitContractError, "private-Dual"
            ):
                project_init.load_project_init_contract(root)


if __name__ == "__main__":
    unittest.main()
