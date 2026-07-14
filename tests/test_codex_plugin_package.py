from __future__ import annotations

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

import build_codex_plugin as package  # noqa: E402


class CodexPluginPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        private_root = ROOT / ".private-provenance"
        private_root.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="L44-unit-", dir=private_root))

    def tearDown(self) -> None:
        if self.root.exists():
            package.reject_link_tree(self.root, label="L44 unit fixture")
            shutil.rmtree(self.root)

    def output(self, name: str) -> Path:
        return self.root / name / package.PLUGIN_NAME

    def build(self, name: str = "base") -> Path:
        output = self.output(name)
        package.build_package(output)
        return output

    def test_manifest_and_lock_define_skills_candidate_with_brand_assets(self) -> None:
        contract = package.validate_contract()
        manifest = contract["manifest"]
        lock = contract["lock"]
        self.assertEqual(manifest["name"], "cotend")
        self.assertEqual(manifest["version"], "0.1.0-rc.1")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["interface"]["brandColor"], "#139C98")
        self.assertEqual(
            manifest["interface"]["composerIcon"], "./assets/cotend-logo.png"
        )
        self.assertEqual(manifest["interface"]["logo"], "./assets/cotend-logo.png")
        self.assertEqual(
            manifest["interface"]["logoDark"], "./assets/cotend-logo-dark.png"
        )
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("hooks", manifest)
        self.assertEqual(lock["status"], "production_candidate_not_published")
        self.assertEqual(lock["schema_version"], 2)
        self.assertEqual(len(lock["package"]["brand_assets"]), 4)
        self.assertNotIn("assets", lock["package"]["forbidden_components"])
        self.assertFalse(lock["authority"]["candidate_identity_only"])
        self.assertTrue(lock["authority"]["final_plugin_identity_confirmed"])
        self.assertFalse(lock["authority"]["release_or_publish_authorized"])

    def test_two_builds_are_byte_deterministic(self) -> None:
        first = self.build("first")
        second = self.build("second")
        first_manifest = package.path_hash_manifest(first)
        second_manifest = package.path_hash_manifest(second)
        self.assertEqual(first_manifest, second_manifest)
        self.assertEqual(len(first_manifest), 41)
        self.assertEqual(
            package.path_hash_manifest_sha256(first_manifest),
            "18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f",
        )

    def test_output_must_stay_in_repository_build_roots(self) -> None:
        outside = Path(tempfile.gettempdir()).resolve() / package.PLUGIN_NAME
        with self.assertRaises(package.PluginPackageError):
            package.build_package(outside)
        with self.assertRaises(package.PluginPackageError):
            package.build_package(ROOT / "skills" / package.PLUGIN_NAME)
        with self.assertRaises(package.PluginPackageError):
            package.build_package(self.root / "wrong-name")

    def test_package_drift_is_rejected(self) -> None:
        base = self.build()

        def extra_file(root: Path) -> None:
            (root / "EXTRA.md").write_text("unexpected\n", encoding="utf-8")

        def missing_skill(root: Path) -> None:
            (root / "skills" / "cotend-init" / "SKILL.md").unlink()

        def skill_drift(root: Path) -> None:
            path = root / "skills" / "cotend-init" / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")

        def license_drift(root: Path) -> None:
            (root / "LICENSE").write_text("wrong license\n", encoding="utf-8")

        def manifest_drift(root: Path) -> None:
            path = root / ".codex-plugin" / "plugin.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["version"] = "9.9.9"
            path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

        def undeclared_app(root: Path) -> None:
            (root / ".app.json").write_text("{}\n", encoding="utf-8")

        def hooks_directory(root: Path) -> None:
            (root / "hooks").mkdir()

        def marketplace_file(root: Path) -> None:
            path = root / ".agents" / "plugins" / "marketplace.json"
            path.parent.mkdir(parents=True)
            path.write_text("{}\n", encoding="utf-8")

        def missing_brand_asset(root: Path) -> None:
            (root / "assets" / "cotend-logo.png").unlink()

        def brand_asset_drift(root: Path) -> None:
            path = root / "assets" / "cotend-logo-dark.png"
            path.write_bytes(path.read_bytes() + b"drift")

        def extra_brand_asset(root: Path) -> None:
            (root / "assets" / "unexpected.png").write_bytes(b"unexpected")

        def manifest_logo_path_drift(root: Path) -> None:
            path = root / ".codex-plugin" / "plugin.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["interface"]["logo"] = "./assets/unexpected.png"
            path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

        mutations = {
            "extra_file": extra_file,
            "missing_skill": missing_skill,
            "skill_drift": skill_drift,
            "license_drift": license_drift,
            "manifest_drift": manifest_drift,
            "undeclared_app": undeclared_app,
            "hooks_directory": hooks_directory,
            "marketplace_file": marketplace_file,
            "missing_brand_asset": missing_brand_asset,
            "brand_asset_drift": brand_asset_drift,
            "extra_brand_asset": extra_brand_asset,
            "manifest_logo_path_drift": manifest_logo_path_drift,
        }
        for case_id, mutate in mutations.items():
            with self.subTest(case_id=case_id):
                candidate = self.output(case_id)
                candidate.parent.mkdir(parents=True)
                shutil.copytree(base, candidate)
                mutate(candidate)
                with self.assertRaises(package.PluginPackageError):
                    package.verify_package(candidate)

    def test_existing_invalid_output_is_not_overwritten(self) -> None:
        output = self.output("invalid-existing")
        output.mkdir(parents=True)
        sentinel = output / "USER-DATA.txt"
        sentinel.write_text("must remain\n", encoding="utf-8")
        with self.assertRaises(package.PluginPackageError):
            package.build_package(output)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "must remain\n")

    def test_linklike_package_member_is_rejected(self) -> None:
        output = self.build("link-classification")
        linked_path = output / "skills"
        original = package._is_linklike

        def classify(path: Path) -> bool:
            return path == linked_path or original(path)

        with mock.patch.object(package, "_is_linklike", side_effect=classify):
            with self.assertRaises(package.PluginPackageError):
                package.verify_package(output)

    def test_n3_display_metadata_and_prompt_limits_are_preserved(self) -> None:
        output = self.build("display")
        result = package.verify_package(output)
        self.assertEqual(result["friendly_display_names"], 5)
        self.assertEqual(result["relative_notice_links"], 4)
        self.assertEqual(result["brand_assets"], 4)
        manifest = json.loads(
            (output / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        prompts = manifest["interface"]["defaultPrompt"]
        self.assertEqual(len(prompts), 3)
        self.assertTrue(all(len(prompt) <= 128 for prompt in prompts))
        self.assertEqual(
            package.sha256_file(output / "assets" / "cotend-mark.svg"),
            "27c5a8566bb4d7800f9250715aef649adf5806b35784955a093cc37cf477238a",
        )

    def test_valid_existing_output_rebuild_is_idempotent(self) -> None:
        output = self.build("idempotent")
        before = package.path_hash_manifest(output)
        package.build_package(output)
        after = package.path_hash_manifest(output)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
