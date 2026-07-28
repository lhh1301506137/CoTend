from __future__ import annotations

import hashlib
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_INIT = ROOT / "skills" / "cotend-project-init"
CHECKER = PROJECT_INIT / "scripts" / "check_cotend_governance_language.py"
VALIDATOR = PROJECT_INIT / "scripts" / "validate_governance_language.py"


class CoTendGovernanceLanguageTests(unittest.TestCase):
    def run_checker(
        self, normalized_tag: str, text: str
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, Any], bytes]:
        with tempfile.TemporaryDirectory(prefix="cotend-language-checker-") as temporary:
            path = Path(temporary) / "STATUS.md"
            data = text.encode("utf-8")
            path.write_bytes(data)
            result = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER),
                    "--normalized-tag",
                    normalized_tag,
                    "--path",
                    str(path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            payload = json.loads(result.stdout)
            return result, payload, data

    def prepare_project(self, normalized_tag: str, body: str) -> Path:
        root = Path(tempfile.mkdtemp(prefix="cotend-language-validator-"))
        subprocess.run(
            ["git", "init", "--quiet", "--initial-branch=main", str(root)],
            check=True,
            capture_output=True,
        )
        (root / "STATUS.md").write_text(
            (
                f"{body}\n\n"
                "user_facing_language_resolution:\n"
                "  contract: cotend.user-facing-language-resolution.v1\n"
                "  status: resolved\n"
                f"  normalized_tag: {normalized_tag}\n"
            ),
            encoding="utf-8",
        )
        return root

    def run_validator(
        self,
        project: Path,
        *,
        expected_tag: str,
        checker: Path = CHECKER,
        runtime_profile: str | None = None,
        write_receipts: tuple[str, ...] = ("STATUS.md",),
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
        command = [
            sys.executable,
            str(VALIDATOR),
            "--project-root",
            str(project),
            "--status-carrier",
            "STATUS.md",
            "--expected-normalized-tag",
            expected_tag,
            "--checker",
            str(checker),
        ]
        for receipt in write_receipts:
            command.extend(["--write-receipt", receipt])
        if runtime_profile is not None:
            command.extend(["--runtime-profile", runtime_profile])
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        return result, json.loads(result.stdout)

    def test_checker_accepts_english_default_and_binds_actual_sha(self) -> None:
        result, payload, data = self.run_checker(
            "en", "# Project Status\n\nInitialization is complete and safe to resume."
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["checker"], "cotend-governance-language.v1")
        self.assertEqual(payload["body_result"], "match")
        self.assertTrue(payload["actual_bytes_checked"])
        self.assertEqual(payload["sha256"], hashlib.sha256(data).hexdigest())
        self.assertNotIn("private", payload["reason"])

    def test_checker_accepts_explicit_simplified_and_traditional_chinese(self) -> None:
        for tag, text in (
            ("zh-CN", "# 项目状态\n\n初始化已完成，可以安全继续当前路线。"),
            ("zh-TW", "# 專案狀態\n\n初始化已完成，可以安全繼續目前路線。"),
        ):
            with self.subTest(tag=tag):
                result, payload, _ = self.run_checker(tag, text)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(payload["normalized_tag"], tag)
                self.assertEqual(payload["body_result"], "match")

    def test_checker_rejects_opposite_language_bodies(self) -> None:
        for tag, text in (
            ("en", "# 项目状态\n\n初始化已经完成，可以继续。"),
            ("zh-CN", "# Project Status\n\nInitialization is complete and ready."),
            ("zh-TW", "# Project Status\n\nInitialization is complete and ready."),
        ):
            with self.subTest(tag=tag):
                _, payload, _ = self.run_checker(tag, text)
                self.assertEqual(payload["body_result"], "mismatch")
                self.assertEqual(payload["user_visible_prose"], "present")

    def test_checker_accepts_concrete_technical_only_body(self) -> None:
        _, payload, _ = self.run_checker(
            "en",
            (
                "```yaml\n"
                "status: current\n"
                "revision: 13\n"
                "```\n"
                "git status --short\n"
                "manifest_sha256: "
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
            ),
        )
        self.assertEqual(payload["body_result"], "technical_only")
        self.assertEqual(payload["user_visible_prose"], "absent")
        self.assertIn("code", payload["excluded_technical_segments"])

    def test_checker_excludes_relative_paths_and_identifiers_from_prose(self) -> None:
        _, technical, _ = self.run_checker(
            "en",
            (
                "- skills/cotend-project-init/SKILL.md\n"
                "- delivery/codex-artifact.lock.json\n"
                "- cotend_workflow.state\n"
                "- v1.67-full\n"
            ),
        )
        self.assertEqual(technical["body_result"], "technical_only")
        self.assertEqual(technical["user_visible_prose"], "absent")
        self.assertIn("path", technical["excluded_technical_segments"])
        self.assertIn("identifier", technical["excluded_technical_segments"])

        _, chinese, _ = self.run_checker(
            "zh-CN",
            (
                "# 项目状态\n\n"
                "初始化已完成，可以安全继续当前路线。\n\n"
                "- skills/cotend-project-init/SKILL.md\n"
                "- delivery/codex-artifact.lock.json\n"
                "- upstream/FRAMEWORK-CANDIDATE.json\n"
                "- cotend_workflow.runtime_profile\n"
                "- cotend.user-facing-language-resolution.v1\n"
                "- delegated_pair\n"
            ),
        )
        self.assertEqual(chinese["body_result"], "match")

    def test_validator_passes_actual_bytes_and_is_profile_equivalent(self) -> None:
        project = self.prepare_project(
            "en", "# Project Status\n\nInitialization is complete and safe to resume."
        )
        try:
            full_result, full = self.run_validator(
                project, expected_tag="en", runtime_profile="full"
            )
            adaptive_result, adaptive = self.run_validator(
                project, expected_tag="en", runtime_profile="adaptive"
            )
            self.assertEqual(full_result.returncode, 0)
            self.assertEqual(adaptive_result.returncode, 0)
            self.assertEqual(full, adaptive)
            self.assertEqual(
                full["contract"], "cotend.governance-language-pre-handback.v1"
            )
            self.assertEqual(full["result"], "pass")
            self.assertEqual(full["repair"]["max_same_turn_repairs"], 1)
            self.assertEqual(full["repair"]["max_same_turn_rechecks"], 1)
            self.assertEqual(len(full["files"]), 1)
            status_bytes = (project / "STATUS.md").read_bytes()
            self.assertEqual(
                full["files"][0]["sha256"], hashlib.sha256(status_bytes).hexdigest()
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)

    def test_validator_fails_mismatched_body_with_one_repair_budget(self) -> None:
        project = self.prepare_project(
            "zh-CN", "# Project Status\n\nInitialization is complete and ready."
        )
        try:
            result, payload = self.run_validator(project, expected_tag="zh-CN")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(payload["result"], "fail")
            self.assertTrue(payload["repair"]["permitted"])
            self.assertIn(
                "governance_body_mismatch:STATUS.md", payload["reasons"]
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)

    def test_validator_blocks_checker_sha_mismatch(self) -> None:
        project = self.prepare_project(
            "en", "# Project Status\n\nInitialization is complete and ready."
        )
        checker = project / "wrong_sha_checker.py"
        checker.write_text(
            (
                "import argparse,json\n"
                "p=argparse.ArgumentParser();"
                "p.add_argument('--normalized-tag');p.add_argument('--path');a=p.parse_args()\n"
                "print(json.dumps({'checker':'fixture.v1','path':a.path,"
                "'normalized_tag':a.normalized_tag,'sha256':'0'*64,"
                "'actual_bytes_checked':True,'user_visible_prose':'present',"
                "'body_result':'match'}))\n"
            ),
            encoding="utf-8",
        )
        try:
            result, payload = self.run_validator(
                project, expected_tag="en", checker=checker
            )
            self.assertEqual(result.returncode, 3)
            self.assertEqual(payload["result"], "blocked")
            self.assertIn(
                "adapter_checker_sha256_mismatch:STATUS.md", payload["reasons"]
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)

    def test_validator_blocks_file_mutation_during_checker_execution(self) -> None:
        project = self.prepare_project(
            "en", "# Project Status\n\nInitialization is complete and ready."
        )
        checker = project / "mutating_checker.py"
        checker.write_text(
            (
                "import argparse,hashlib,json,pathlib\n"
                "p=argparse.ArgumentParser();"
                "p.add_argument('--normalized-tag');p.add_argument('--path');a=p.parse_args()\n"
                "path=pathlib.Path(a.path);data=path.read_bytes();"
                "path.write_bytes(data+b'\\nmutation\\n')\n"
                "print(json.dumps({'checker':'fixture.v1','path':str(path),"
                "'normalized_tag':a.normalized_tag,"
                "'sha256':hashlib.sha256(data).hexdigest(),"
                "'actual_bytes_checked':True,'user_visible_prose':'present',"
                "'body_result':'match'}))\n"
            ),
            encoding="utf-8",
        )
        try:
            result, payload = self.run_validator(
                project, expected_tag="en", checker=checker
            )
            self.assertEqual(result.returncode, 3)
            self.assertEqual(payload["result"], "blocked")
            self.assertIn(
                "changed_file_changed_during_validation:STATUS.md",
                payload["reasons"],
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)

    def test_validator_blocks_canonical_drift_before_per_file_check(self) -> None:
        project = self.prepare_project(
            "en", "# Project Status\n\nInitialization is complete and ready."
        )
        try:
            validator = runpy.run_path(
                str(VALIDATOR),
                run_name="cotend_governance_validator_under_test",
            )
            validate = validator["validate"]
            original_read = validate.__globals__["read_utf8"]
            canonical = (project / "STATUS.md").resolve()
            first_status_read = True

            def drift_after_canonical_read(path: Path) -> Any:
                nonlocal first_status_read
                result = original_read(path)
                if path == canonical and first_status_read:
                    first_status_read = False
                    canonical.write_text(
                        canonical.read_text(encoding="utf-8") + "\nrevision: 14\n",
                        encoding="utf-8",
                    )
                return result

            args = Namespace(
                project_root=str(project),
                status_carrier="STATUS.md",
                expected_normalized_tag="en",
                checker=str(CHECKER),
                write_receipt=["STATUS.md"],
                runtime_profile=None,
            )
            validate.__globals__["read_utf8"] = drift_after_canonical_read
            try:
                payload = validate(args)
            finally:
                validate.__globals__["read_utf8"] = original_read
            self.assertEqual(payload["result"], "blocked")
            self.assertIn(
                "canonical_status_changed_during_validation:STATUS.md",
                payload["reasons"],
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)

    def test_validator_unions_vcs_changes_with_ignored_write_receipts(self) -> None:
        project = self.prepare_project(
            "en", "# Project Status\n\nInitialization is complete and ready."
        )
        try:
            (project / ".gitignore").write_text("REVIEW-LOG.md\n", encoding="utf-8")
            (project / "REVIEW-LOG.md").write_text(
                "# Review Log\n\nThe initialization evidence is ready.\n",
                encoding="utf-8",
            )
            result, payload = self.run_validator(
                project,
                expected_tag="en",
                write_receipts=("STATUS.md", "REVIEW-LOG.md"),
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["result"], "pass")
            self.assertEqual(
                payload["changed_file_set"]["source"],
                "vcs_diff_plus_write_receipts",
            )
            self.assertEqual(
                payload["changed_file_set"]["files"],
                ["REVIEW-LOG.md", "STATUS.md"],
            )
            self.assertEqual(
                [item["path"] for item in payload["files"]],
                ["REVIEW-LOG.md", "STATUS.md"],
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)

    def test_validator_blocks_unlisted_canonical_drift_while_checking_review(
        self,
    ) -> None:
        project = self.prepare_project(
            "en", "# Project Status\n\nInitialization is complete and ready."
        )
        try:
            subprocess.run(
                ["git", "-C", str(project), "add", "STATUS.md"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(project),
                    "-c",
                    "user.name=CoTend Test",
                    "-c",
                    "user.email=cotend-test@example.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "baseline",
                ],
                check=True,
                capture_output=True,
            )
            (project / ".gitignore").write_text("REVIEW-LOG.md\n", encoding="utf-8")
            (project / "REVIEW-LOG.md").write_text(
                "# Review Log\n\nThe initialization evidence is ready.\n",
                encoding="utf-8",
            )
            validator = runpy.run_path(
                str(VALIDATOR),
                run_name="cotend_governance_validator_review_drift_test",
            )
            validate = validator["validate"]
            original_read = validate.__globals__["read_utf8"]
            canonical = (project / "STATUS.md").resolve()
            first_status_read = True

            def drift_after_canonical_read(path: Path) -> Any:
                nonlocal first_status_read
                result = original_read(path)
                if path == canonical and first_status_read:
                    first_status_read = False
                    canonical.write_text(
                        canonical.read_text(encoding="utf-8") + "\nrevision: 14\n",
                        encoding="utf-8",
                    )
                return result

            args = Namespace(
                project_root=str(project),
                status_carrier="STATUS.md",
                expected_normalized_tag="en",
                checker=str(CHECKER),
                write_receipt=["REVIEW-LOG.md"],
                runtime_profile=None,
            )
            validate.__globals__["read_utf8"] = drift_after_canonical_read
            try:
                payload = validate(args)
            finally:
                validate.__globals__["read_utf8"] = original_read
            self.assertEqual(payload["result"], "blocked")
            self.assertEqual(
                payload["changed_file_set"]["files"],
                ["REVIEW-LOG.md"],
            )
            self.assertIn(
                "canonical_status_changed_during_validation:STATUS.md",
                payload["reasons"],
            )
        finally:
            shutil.rmtree(project, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
