from __future__ import annotations

import copy
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import verify_github_marketplace_carrier as carrier  # noqa: E402
import verify_isolated_codex_plugin as lifecycle  # noqa: E402


class GitHubMarketplaceCarrierTests(unittest.TestCase):
    def setUp(self) -> None:
        carrier.PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = Path(
            tempfile.mkdtemp(prefix="L54-unit-", dir=carrier.PRIVATE_ROOT)
        )

    def tearDown(self) -> None:
        if self.root.exists():
            carrier.remove_tree_with_readonly_retry(self.root)

    def test_l54_root_guard_rejects_other_private_directory(self) -> None:
        with self.assertRaises(lifecycle.PluginFixtureError):
            carrier.guarded_run_root(carrier.PRIVATE_ROOT / "L46-not-l54")
        self.assertEqual(carrier.guarded_run_root(self.root), self.root.resolve())

    def test_carrier_manifest_is_exact_path_only_transform(self) -> None:
        production = package.validate_contract()["manifest"]
        unchanged = copy.deepcopy(production)
        actual = carrier.carrier_manifest()
        self.assertEqual(production, unchanged)
        expected = copy.deepcopy(production)
        for path, value in carrier.PATH_REWRITES.items():
            carrier._set_path(expected, path, value)
        self.assertEqual(actual, expected)
        self.assertEqual(
            carrier.validate_carrier_manifest(actual)["allowed_path_rewrites"], 3
        )
        actual["description"] = "independent metadata drift"
        with self.assertRaises(lifecycle.PluginFixtureError):
            carrier.validate_carrier_manifest(actual)

    def test_marketplace_uses_repository_root_url_source(self) -> None:
        manifest = carrier.marketplace_manifest()
        carrier.validate_marketplace_manifest(manifest)
        self.assertEqual(manifest["name"], "cotend")
        self.assertEqual(
            manifest["plugins"][0]["source"], {"source": "url", "url": "./"}
        )
        serialized = str(manifest).lower()
        self.assertNotIn("file://", serialized)
        self.assertNotIn("plugins/cotend", serialized)

    def test_materialized_carrier_has_one_skill_source_and_locked_assets(self) -> None:
        result = carrier.materialize_scenario(self.root)
        plugin_root = result["marketplace_root"]
        verified = carrier.verify_carrier_root(plugin_root)
        self.assertEqual(verified["skills"], 7)
        self.assertEqual(verified["skill_files"], 30)
        self.assertTrue(verified["source_bytes_identical"])
        self.assertFalse((plugin_root / "codex-skills").exists())
        self.assertTrue((plugin_root / "skills").is_dir())
        self.assertTrue(
            (
                plugin_root
                / "packaging"
                / "codex-plugin"
                / "cotend"
                / "assets"
                / "cotend-logo.png"
            ).is_file()
        )

    def test_root_source_validation_rejects_nested_package_source(self) -> None:
        self.assertEqual(
            carrier.validate_root_plugin_source(
                {"source": "url", "url": "./"}, self.root
            ),
            "url_relative_root",
        )
        self.assertEqual(
            carrier.validate_root_plugin_source(
                {"source": "local", "path": str(self.root / "source-marketplace")},
                self.root,
            ),
            "normalized_local_root",
        )
        self.assertEqual(
            carrier.validate_root_plugin_source(
                {"source": "git", "url": str(self.root / "source-marketplace")},
                self.root,
            ),
            "normalized_git_root",
        )
        with self.assertRaises(lifecycle.PluginFixtureError):
            carrier.validate_root_plugin_source(
                {
                    "source": "local",
                    "path": str(
                        self.root / "source-marketplace" / "plugins" / "cotend"
                    ),
                },
                self.root,
            )

    def test_repeat_add_and_local_refresh_require_known_outcomes(self) -> None:
        self.assertEqual(
            carrier.validate_repeat_add_observation(
                {
                    "returncode": 0,
                    "json": {
                        "marketplaceName": "cotend",
                        "alreadyAdded": True,
                    },
                }
            ),
            "idempotent_success",
        )
        self.assertEqual(
            carrier.validate_local_refresh_observation(
                {
                    "returncode": 1,
                    "stdout": "",
                    "stderr": (
                        "Error: marketplace `cotend` is not configured as a Git "
                        "marketplace"
                    ),
                }
            ),
            "local_marketplace_not_git_upgradeable",
        )
        with self.assertRaises(lifecycle.PluginFixtureError):
            carrier.validate_local_refresh_observation(
                {"returncode": 1, "stdout": "", "stderr": "unknown failure"}
            )

    def test_repository_carrier_requires_both_root_files(self) -> None:
        with self.assertRaises(lifecycle.PluginFixtureError):
            carrier.validate_carrier_manifest(
                carrier.carrier_manifest(), plugin_root=self.root
            )

    def test_cleanup_removes_readonly_git_objects_inside_fixture(self) -> None:
        target = self.root / "codex-home"
        git_object = target / "plugins" / "cache" / ".git" / "objects" / "aa"
        git_object.parent.mkdir(parents=True)
        git_object.write_text("fixture\n", encoding="utf-8")
        os.chmod(git_object, stat.S_IREAD)
        carrier.remove_tree_with_readonly_retry(target)
        self.assertFalse(target.exists())

    def test_git_environment_is_isolated_and_forces_lf(self) -> None:
        env = lifecycle.build_isolated_env(self.root)
        carrier.configure_isolated_git_env(self.root, env)
        config = Path(env["GIT_CONFIG_GLOBAL"])
        self.assertTrue(config.is_relative_to(self.root))
        self.assertEqual(env["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertIn("autocrlf = false", config.read_text(encoding="utf-8"))

    def test_external_project_root_is_exact_temp_child_and_removable(self) -> None:
        root = carrier.create_external_project_root()
        try:
            self.assertEqual(carrier.guarded_external_project_root(root), root)
            (root / "sentinel.txt").write_text("fixture\n", encoding="utf-8")
            with self.assertRaises(lifecycle.PluginFixtureError):
                carrier.guarded_external_project_root(Path(tempfile.gettempdir()))
        finally:
            carrier.remove_external_project_root(root)
        self.assertFalse(root.exists())

    def test_external_project_cleanup_retries_windows_handle_release(self) -> None:
        root = carrier.create_external_project_root()
        (root / "project-empty").mkdir()
        real_rmtree = carrier.shutil.rmtree
        calls = 0

        def busy_once(path: Path, *args: object, **kwargs: object) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                error = OSError("fixture directory is busy")
                error.winerror = 32  # type: ignore[attr-defined]
                raise error
            real_rmtree(path, *args, **kwargs)

        with mock.patch.object(carrier.shutil, "rmtree", side_effect=busy_once):
            retries = carrier.remove_external_project_root(
                root, timeout_seconds=1.0, retry_seconds=0.0
            )
        self.assertEqual(retries, 1)
        self.assertFalse(root.exists())

    def test_boundary_change_summary_never_includes_metadata_values(self) -> None:
        before = {"user_codex_root": {"mtime_ns": 1}, "auth": {"exists": True}}
        after = {"user_codex_root": {"mtime_ns": 2}, "auth": {"exists": True}}
        self.assertEqual(
            carrier.changed_boundary_labels(before, after), ["user_codex_root"]
        )


if __name__ == "__main__":
    unittest.main()
