from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_isolated_codex_plugin as plugin_fixture  # noqa: E402


class IsolatedCodexPluginTests(unittest.TestCase):
    def setUp(self) -> None:
        plugin_fixture.PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        self.fixture = Path(
            tempfile.mkdtemp(prefix="L31-unit-", dir=plugin_fixture.PRIVATE_ROOT)
        )

    def tearDown(self) -> None:
        if self.fixture.exists():
            plugin_fixture.remove_fixture_tree(self.fixture)

    def test_fixture_guard_rejects_private_root_and_escape(self) -> None:
        with self.assertRaises(plugin_fixture.PluginFixtureError):
            plugin_fixture.guarded_fixture(plugin_fixture.PRIVATE_ROOT)
        with self.assertRaises(plugin_fixture.PluginFixtureError):
            plugin_fixture.guarded_fixture(ROOT)
        with self.assertRaises(plugin_fixture.PluginFixtureError):
            plugin_fixture.assert_fixture_path(self.fixture, ROOT, "escape")

    def test_external_project_root_guard_and_cleanup(self) -> None:
        with self.assertRaises(plugin_fixture.PluginFixtureError):
            plugin_fixture.guarded_external_project_root(
                Path(tempfile.gettempdir())
            )
        with self.assertRaises(plugin_fixture.PluginFixtureError):
            plugin_fixture.guarded_external_project_root(
                Path(tempfile.gettempdir()) / "unowned-project-root"
            )

        root = plugin_fixture.create_external_project_root()
        try:
            marker = root / "project" / "marker.txt"
            marker.parent.mkdir()
            marker.write_text("owned fixture\n", encoding="utf-8")
            retries = plugin_fixture.remove_external_project_root(root)
            self.assertIsInstance(retries, int)
            self.assertFalse(root.exists())
        finally:
            if root.exists():
                plugin_fixture.remove_external_project_root(root)

    def test_isolated_environment_redirects_every_write_root(self) -> None:
        injected = {
            "EXAMPLE_API_KEY": "must-not-pass",
            "EXAMPLE_TOKEN": "must-not-pass",
        }
        with mock.patch.dict(os.environ, injected, clear=False):
            env = plugin_fixture.build_isolated_env(self.fixture)
        plugin_fixture.validate_isolated_env(self.fixture, env)
        for key in plugin_fixture.WRITE_ROOT_ENV_KEYS:
            resolved = Path(env[key]).resolve()
            self.assertTrue(resolved.is_relative_to(self.fixture.resolve()), key)
        self.assertNotIn("EXAMPLE_API_KEY", env)
        self.assertNotIn("EXAMPLE_TOKEN", env)

    def test_stat_only_snapshot_never_contains_content_digest(self) -> None:
        target = self.fixture / "opaque-config.toml"
        target.write_text("opaque-value\n", encoding="utf-8")
        snapshot = plugin_fixture.stat_only(target)
        self.assertEqual(set(snapshot), {"exists", "kind", "size", "mtime_ns"})
        self.assertNotIn("sha256", snapshot)
        self.assertNotIn("manifest", snapshot)

    def test_fixture_manifest_is_skills_only_and_non_release(self) -> None:
        manifest = plugin_fixture.plugin_manifest()
        self.assertEqual(manifest["name"], "cotend")
        self.assertEqual(manifest["version"], "0.0.0-dev.1+codex.fixture")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertNotIn("hooks", manifest)
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)

    def test_plugin_list_contract_requires_exact_install_state(self) -> None:
        source = {
            "source": "local",
            "path": str(
                self.fixture / "source-marketplace" / "plugins" / "cotend"
            ),
        }
        installed = {
            "pluginId": "cotend@cotend-fixture-local",
            "name": "cotend",
            "marketplaceName": "cotend-fixture-local",
            "version": "0.0.0-dev.1+codex.fixture",
            "installed": True,
            "enabled": True,
            "source": source,
            "installPolicy": "AVAILABLE",
            "authPolicy": "ON_INSTALL",
        }
        plugin_fixture.validate_plugin_list_payload(
            {"installed": [installed], "available": []},
            self.fixture,
            installed=True,
            available=False,
        )
        installed["enabled"] = False
        with self.assertRaises(plugin_fixture.PluginFixtureError):
            plugin_fixture.validate_plugin_list_payload(
                {"installed": [installed], "available": []},
                self.fixture,
                installed=True,
                available=False,
            )

    def test_discovery_separates_namespaced_repo_duplicate_by_path(self) -> None:
        project = self.fixture / "project"
        plugin_source = self.fixture / "plugin-source"
        standalone_source = self.fixture / "standalone-source"
        source_bytes = (
            plugin_fixture.SOURCE_SKILLS_ROOT
            / "cotend-init"
            / "SKILL.md"
        ).read_bytes()
        plugin_skill = plugin_source / "cotend-init" / "SKILL.md"
        standalone_skill = standalone_source / "cotend-init" / "SKILL.md"
        project_skill = (
            project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        )
        for path in (plugin_skill, standalone_skill, project_skill):
            path.parent.mkdir(parents=True)
            path.write_bytes(source_bytes)
        identity = plugin_fixture.PluginLifecycleIdentity(
            plugin_id="cotend",
            plugin_version="test",
            marketplace_name="test",
            expected_skills=("cotend-init",),
        )
        result = {
            "data": [
                {
                    "errors": [],
                    "skills": [
                        {
                            "name": "cotend:cotend-init",
                            "scope": "repo",
                            "enabled": True,
                            "path": str(project_skill),
                        },
                        {
                            "name": "cotend:cotend-init",
                            "scope": "user",
                            "enabled": True,
                            "path": str(plugin_skill),
                        },
                    ],
                }
            ]
        }
        with mock.patch.object(
            plugin_fixture,
            "app_server_request",
            return_value=result,
        ):
            discovered = plugin_fixture.discover_skills(
                self.fixture,
                {},
                project,
                expect_plugin=True,
                expect_standalone=True,
                identity=identity,
                plugin_source_root=plugin_source,
                standalone_source_root=standalone_source,
            )
        self.assertEqual(discovered["plugin_skill_count"], 1)
        self.assertEqual(discovered["standalone_skill_count"], 1)
        self.assertEqual(discovered["plugin_scopes"], ["user"])
        self.assertEqual(discovered["standalone_scopes"], ["repo"])
        self.assertEqual(discovered["standalone_names"], ["cotend-init"])

    def test_static_fixture_and_twelve_negative_mutations(self) -> None:
        plugin_fixture.materialize_fixture_payload(self.fixture)
        result = plugin_fixture.verify_static(self.fixture, run_official=False)
        self.assertEqual(result["skills"], 10)
        self.assertEqual(result["skill_files"], 104)
        self.assertEqual(result["undeclared_capabilities"], 0)
        negative = plugin_fixture.run_negative_mutations(self.fixture)
        self.assertEqual(negative["passed"], 12)
        self.assertEqual(negative["total"], 12)


if __name__ == "__main__":
    unittest.main()
