from __future__ import annotations

import json
import re
import shlex
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402


README_PATH = ROOT / "README.md"
SUBMISSION_PATH = (
    ROOT / "packaging" / "codex-plugin" / "submission-materials" / "submission.json"
)
EXPECTED_COMMANDS = {
    "python scripts/build_codex_plugin.py --output dist/cotend --json",
    "python scripts/verify_codex_plugin_package.py",
    "python scripts/verify_plugin_submission_materials.py",
    "python -m unittest discover -s tests",
    "python scripts/check_repository.py",
    "python scripts/verify_production_plugin_lifecycle.py",
}


class PublicReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = README_PATH.read_text(encoding="utf-8")

    def test_readme_is_english_and_novice_first(self) -> None:
        self.assertTrue(self.text.startswith("# CoTend\n"))
        self.assertIn("AI development governance framework", self.text)
        self.assertIn("people who do not read code", self.text)
        self.assertIn("The current pre-release adapter targets Codex", self.text)
        self.assertNotRegex(self.text, r"[\u3400-\u9fff]")

    def test_readme_declares_pre_release_and_no_public_install(self) -> None:
        for marker in (
            "Pre-release AI development governance framework",
            "CoTend is not yet available in the Public Plugin Directory.",
            "No supported end-user installation is available yet.",
            "The plugin has not been submitted for review and has not been published.",
            "Do not treat them as a supported end-user installation.",
        ):
            self.assertIn(marker, self.text)
        self.assertNotIn("Install CoTend from the Public Plugin Directory", self.text)
        self.assertNotIn("CoTend is production-ready", self.text)

    def test_readme_skill_catalog_matches_seven_packaged_skills(self) -> None:
        section = self.text.split("<!-- skill-catalog-start -->", 1)[1].split(
            "<!-- skill-catalog-end -->", 1
        )[0]
        ids = re.findall(r"^\| [^|]+ \| `([^`]+)` \|", section, re.MULTILINE)
        self.assertEqual(len(ids), 7)
        self.assertEqual(set(ids), set(package.EXPECTED_SKILLS))
        self.assertIn("`CoTend Init` is the normal start or resume entry", self.text)

    def test_readme_starter_prompts_match_submission_contract(self) -> None:
        submission = json.loads(SUBMISSION_PATH.read_text(encoding="utf-8"))
        prompts = submission["starter_prompts"]
        self.assertEqual(len(prompts), 3)
        for prompt in prompts:
            self.assertIn(f"`{prompt}`", self.text)

    def test_readme_relative_links_resolve(self) -> None:
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", self.text)
        relative_links = [
            link
            for link in links
            if not re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I)
            and not link.startswith("#")
        ]
        self.assertGreaterEqual(len(relative_links), 10)
        for link in relative_links:
            target = link.split("#", 1)[0]
            resolved = (ROOT / target).resolve()
            self.assertTrue(resolved.is_relative_to(ROOT.resolve()), link)
            self.assertTrue(resolved.exists(), link)

    def test_readme_maintainer_commands_are_safe_and_real(self) -> None:
        commands = {
            line.strip()
            for line in self.text.splitlines()
            if line.startswith("python ")
        }
        self.assertEqual(commands, EXPECTED_COMMANDS)
        joined = "\n".join(commands).lower()
        for forbidden in (
            "plugin install",
            "marketplace",
            "git push",
            "publish",
            "portal",
        ):
            self.assertNotIn(forbidden, joined)
        for command in commands:
            parts = shlex.split(command)
            if len(parts) > 1 and parts[1].startswith("scripts/"):
                self.assertTrue((ROOT / parts[1]).is_file(), command)


if __name__ == "__main__":
    unittest.main()
