from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_native_zero_runtime_dependency as zero_runtime  # noqa: E402


class NativeZeroRuntimeDependencyTests(unittest.TestCase):
    def copied_skills(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="cotend-g05-test-")
        skills = Path(temporary.name) / "skills"
        shutil.copytree(ROOT / "skills", skills)
        return temporary, skills

    def test_repository_contract_and_no_regression_baseline(self) -> None:
        result = zero_runtime.verify_repository()
        self.assertEqual(
            result["status"], "native_zero_runtime_dependency_verified"
        )
        self.assertEqual(result["source_runtime_mentions"], 0)
        self.assertEqual(result["packaged_runtime_mentions"], 0)
        self.assertEqual(result["runtime_commands"], 0)
        self.assertEqual(result["runtime_state_paths"], 0)
        self.assertEqual(result["external_task_spec_authority"], 0)
        self.assertEqual(result["native_capabilities"], 8)
        self.assertEqual(result["dual_capabilities"], 19)
        self.assertEqual(result["mapped_skill_roles"], 8)
        self.assertEqual(result["target_artifact"], "cotend-codex-r000012")
        self.assertEqual(result["predecessor_target"], "cotend-codex-r000010")
        self.assertFalse(result["real_project_claimed"])
        self.assertFalse(result["real_user_acceptance_claimed"])
        self.assertFalse(result["rc3_built"])
        self.assertFalse(result["public_action"])

    def test_source_runtime_and_disposable_copy_are_identical_and_clean(self) -> None:
        scan = zero_runtime.scan_runtime(ROOT / "skills")
        zero_runtime.assert_runtime_scan_clean(scan, "source")
        result = zero_runtime.verify_disposable_runtime()
        self.assertEqual(result["skill_files"], 40)
        self.assertEqual(
            result["manifest_sha256"], zero_runtime.EXPECTED_TARGET_MANIFEST
        )

    def test_specific_framework_name_mutation_is_rejected(self) -> None:
        temporary, skills = self.copied_skills()
        try:
            path = skills / "cotend-init" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8") + "\nTrellis runtime fallback.\n",
                encoding="utf-8",
            )
            scan = zero_runtime.scan_runtime(skills)
            self.assertTrue(scan["name_hits"])
            with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
                zero_runtime.assert_runtime_scan_clean(scan, "mutation")
        finally:
            temporary.cleanup()

    def test_specific_framework_command_mutation_is_rejected(self) -> None:
        temporary, skills = self.copied_skills()
        try:
            path = skills / "cotend-init" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8") + "\nRun /trellis-start.\n",
                encoding="utf-8",
            )
            scan = zero_runtime.scan_runtime(skills)
            self.assertTrue(scan["command_hits"])
            with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
                zero_runtime.assert_runtime_scan_clean(scan, "mutation")
        finally:
            temporary.cleanup()

    def test_specific_framework_state_path_mutation_is_rejected(self) -> None:
        temporary, skills = self.copied_skills()
        try:
            path = skills / "cotend-init" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8") + "\nRead .trellis/config.yaml.\n",
                encoding="utf-8",
            )
            scan = zero_runtime.scan_runtime(skills)
            self.assertTrue(scan["state_path_hits"])
            with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
                zero_runtime.assert_runtime_scan_clean(scan, "mutation")
        finally:
            temporary.cleanup()

    def test_external_framework_authority_mutation_is_rejected(self) -> None:
        mutations = (
            "The external-framework task is the binding route owner.",
            "The binding route owner is the external-framework task.",
            (
                "The external-framework task is not the route owner; "
                "the external-framework task is the binding route owner."
            ),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                temporary, skills = self.copied_skills()
                try:
                    path = skills / "cotend-init" / "SKILL.md"
                    path.write_text(
                        path.read_text(encoding="utf-8") + f"\n{mutation}\n",
                        encoding="utf-8",
                    )
                    scan = zero_runtime.scan_runtime(skills)
                    self.assertTrue(scan["external_authority_hits"])
                    with self.assertRaises(
                        zero_runtime.NativeZeroRuntimeDependencyError
                    ):
                        zero_runtime.assert_runtime_scan_clean(scan, "mutation")
                finally:
                    temporary.cleanup()

    def test_retained_capability_marker_deletion_is_rejected(self) -> None:
        for relative, markers in zero_runtime.REQUIRED_RUNTIME_CAPABILITY_MARKERS.items():
            for marker in markers:
                with self.subTest(relative=relative, marker=marker):
                    temporary, skills = self.copied_skills()
                    try:
                        path = skills / relative
                        text = path.read_text(encoding="utf-8")
                        self.assertIn(marker, text)
                        path.write_text(
                            text.replace(marker, "removed capability marker", 1),
                            encoding="utf-8",
                        )
                        scan = zero_runtime.scan_runtime(skills)
                        self.assertTrue(scan["missing_capability_markers"])
                        with self.assertRaises(
                            zero_runtime.NativeZeroRuntimeDependencyError
                        ):
                            zero_runtime.assert_runtime_scan_clean(scan, "mutation")
                    finally:
                        temporary.cleanup()

    def test_r10_predecessor_mutation_is_rejected(self) -> None:
        lock = json.loads(zero_runtime.TARGET_LOCK_PATH.read_text(encoding="utf-8"))
        changed = copy.deepcopy(lock)
        changed["predecessor_targets"][0]["manifest_sha256"] = "0" * 64
        with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
            zero_runtime.validate_target_lock(
                changed,
                manifest_sha256=zero_runtime.EXPECTED_TARGET_MANIFEST,
                skill_file_count=40,
            )

    def test_current_manifest_mutation_is_rejected(self) -> None:
        lock = json.loads(zero_runtime.TARGET_LOCK_PATH.read_text(encoding="utf-8"))
        changed = copy.deepcopy(lock)
        changed["target"]["manifest_sha256"] = "0" * 64
        with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
            zero_runtime.validate_target_lock(
                changed,
                manifest_sha256=zero_runtime.EXPECTED_TARGET_MANIFEST,
                skill_file_count=40,
            )

    def test_frozen_rc2_mutation_is_rejected(self) -> None:
        lock = json.loads(zero_runtime.PACKAGE_LOCK_PATH.read_text(encoding="utf-8"))
        changed = copy.deepcopy(lock)
        changed["package"]["path_hash_manifest_sha256"] = "0" * 64
        with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
            zero_runtime.validate_frozen_rc2_lock(changed)

    def test_native_capability_regression_is_rejected(self) -> None:
        baseline = zero_runtime.native_negative_recovery.verify_repository()
        changed = dict(baseline)
        changed["native_capabilities_composed"] = 7
        with mock.patch.object(
            zero_runtime.native_negative_recovery,
            "verify_repository",
            return_value=changed,
        ):
            with self.assertRaises(zero_runtime.NativeZeroRuntimeDependencyError):
                zero_runtime.verify_no_regression()


if __name__ == "__main__":
    unittest.main()
