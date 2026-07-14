from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_isolated_codex_plugin as lifecycle  # noqa: E402
import verify_remote_github_marketplace as remote  # noqa: E402


class RemoteGitHubMarketplaceTests(unittest.TestCase):
    def setUp(self) -> None:
        remote.PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = Path(
            tempfile.mkdtemp(prefix="L55-unit-", dir=remote.PRIVATE_ROOT)
        )

    def tearDown(self) -> None:
        if self.root.exists():
            remote.local_carrier.remove_tree_with_readonly_retry(self.root)

    def test_l55_root_guard_rejects_other_private_directory(self) -> None:
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.guarded_run_root(remote.PRIVATE_ROOT / "L54-not-l55")
        self.assertEqual(remote.guarded_run_root(self.root), self.root.resolve())

    def test_remote_source_is_exact_and_not_file_url(self) -> None:
        self.assertEqual(remote.validate_remote_slug(remote.REMOTE_SLUG), remote.REMOTE_SLUG)
        self.assertEqual(
            remote.REMOTE_URL,
            "https://github.com/lhh1301506137/CoTend.git",
        )
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_remote_slug("file:///tmp/CoTend")

    def test_network_env_is_write_isolated_and_credential_free(self) -> None:
        proxy_env = {
            key: "http://127.0.0.1:9876" for key in remote.PROXY_KEYS
        }
        with mock.patch.dict(remote.os.environ, proxy_env, clear=True):
            env = remote.build_network_isolated_env(self.root)
        remote.validate_network_isolated_env(self.root, env)
        self.assertEqual(set(remote.validated_loopback_proxy_env(env)), set(remote.PROXY_KEYS))
        self.assertNotIn("NO_PROXY", env)
        self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(env["GCM_INTERACTIVE"], "Never")
        self.assertTrue(Path(env["GIT_CONFIG_GLOBAL"]).is_relative_to(self.root))
        self.assertNotIn("GITHUB_TOKEN", env)
        unsafe = dict(env)
        unsafe["HTTP_PROXY"] = "http://user:password@127.0.0.1:9"
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_network_isolated_env(self.root, unsafe)

    def test_network_env_allows_direct_connection_without_proxy(self) -> None:
        with mock.patch.dict(remote.os.environ, {}, clear=True):
            env = remote.build_network_isolated_env(self.root)
        remote.validate_network_isolated_env(self.root, env)
        self.assertFalse(set(remote.PROXY_KEYS) & set(env))
        self.assertEqual(remote.validated_loopback_proxy_env(env), {})

    def test_marketplace_add_requires_exact_isolated_clone_root(self) -> None:
        payload = {
            "marketplaceName": "cotend",
            "installedRoot": str(remote.expected_clone_root(self.root)),
            "alreadyAdded": False,
        }
        self.assertEqual(
            remote.validate_marketplace_add_payload(payload, self.root),
            remote.expected_clone_root(self.root),
        )
        payload["installedRoot"] = str(self.root.parent / "escape")
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_marketplace_add_payload(payload, self.root)

    def test_marketplace_list_requires_git_provenance(self) -> None:
        payload = {
            "marketplaces": [
                {
                    "name": "cotend",
                    "root": str(remote.expected_clone_root(self.root)),
                    "marketplaceSource": {
                        "sourceType": "git",
                        "source": remote.REMOTE_URL,
                    },
                }
            ]
        }
        remote.validate_marketplace_list_payload(payload, self.root, present=True)
        payload["marketplaces"][0]["marketplaceSource"]["source"] = "./"
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_marketplace_list_payload(payload, self.root, present=True)

    def test_remote_git_state_is_bound_to_full_expected_commit(self) -> None:
        head = "a" * 40
        self.assertEqual(
            remote.validate_remote_git_state(remote.REMOTE_URL, head, head)["head"],
            head,
        )
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_remote_git_state(remote.REMOTE_URL, "b" * 40, head)
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_expected_head("abc123")
        metadata = {
            "source_type": "git",
            "source": remote.REMOTE_URL,
            "ref_name": None,
            "sparse_paths": [],
            "revision": head,
        }
        (self.root / remote.INSTALL_METADATA_NAME).write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        self.assertEqual(
            remote.validate_install_metadata(self.root, head)["path"],
            remote.INSTALL_METADATA_NAME,
        )
        metadata["revision"] = "b" * 40
        (self.root / remote.INSTALL_METADATA_NAME).write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_install_metadata(self.root, head)

    def test_remote_plugin_list_requires_git_marketplace_source(self) -> None:
        payload = {
            "installed": [],
            "available": [
                {
                    "pluginId": "cotend@cotend",
                    "name": "cotend",
                    "marketplaceName": "cotend",
                    "version": None,
                    "installed": False,
                    "enabled": False,
                    "source": {
                        "source": "git",
                        "url": str(remote.expected_clone_root(self.root)),
                    },
                    "marketplaceSource": {
                        "sourceType": "git",
                        "source": remote.REMOTE_URL,
                    },
                    "installPolicy": "AVAILABLE",
                    "authPolicy": "ON_INSTALL",
                }
            ],
        }
        remote.validate_remote_plugin_list_payload(
            payload, self.root, installed=False, available=True
        )
        payload["available"][0]["marketplaceSource"]["sourceType"] = "local"
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_remote_plugin_list_payload(
                payload, self.root, installed=False, available=True
            )

    def test_upgrade_payload_requires_no_errors_and_exact_clone(self) -> None:
        clone = remote.expected_clone_root(self.root)
        remote.validate_upgrade_payload(
            {
                "selectedMarketplaces": ["cotend"],
                "upgradedRoots": [str(clone)],
                "errors": [],
            },
            clone,
        )
        with self.assertRaises(lifecycle.PluginFixtureError):
            remote.validate_upgrade_payload(
                {
                    "selectedMarketplaces": ["cotend"],
                    "upgradedRoots": [str(clone)],
                    "errors": ["network failure"],
                },
                clone,
            )

    def test_external_project_root_is_guarded_and_removable(self) -> None:
        root = remote.create_external_project_root()
        try:
            (root / "sentinel.txt").write_text("fixture\n", encoding="utf-8")
            self.assertEqual(remote.guarded_external_project_root(root), root)
            with self.assertRaises(lifecycle.PluginFixtureError):
                remote.guarded_external_project_root(Path(tempfile.gettempdir()))
        finally:
            remote.remove_external_project_root(root)
        self.assertFalse(root.exists())

    def test_cleanup_attempts_external_root_when_runtime_purge_fails(self) -> None:
        external = Path(tempfile.gettempdir()) / (
            remote.EXTERNAL_PROJECT_PREFIX + "unit-cleanup"
        )
        with (
            mock.patch.object(
                remote.local_carrier,
                "purge_isolated_write_roots",
                side_effect=lifecycle.PluginFixtureError("injected purge failure"),
            ),
            mock.patch.object(remote, "remove_external_project_root") as remove,
        ):
            with self.assertRaisesRegex(
                lifecycle.PluginFixtureError, "injected purge failure"
            ):
                remote.cleanup_scenario(self.root, {}, external)
        remove.assert_called_once_with(external)

        def fail_after_partial_environment(fixture: Path) -> dict[str, str]:
            (fixture / "partial-environment").mkdir(parents=True)
            raise lifecycle.PluginFixtureError("injected environment failure")

        with mock.patch.object(
            remote,
            "build_network_isolated_env",
            side_effect=fail_after_partial_environment,
        ):
            with self.assertRaisesRegex(
                lifecycle.PluginFixtureError, "injected environment failure"
            ):
                remote.prepare_scenario(self.root, {})
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
