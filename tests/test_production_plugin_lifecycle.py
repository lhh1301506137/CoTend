from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import verify_isolated_codex_plugin as fixture  # noqa: E402
import verify_production_plugin_lifecycle as production  # noqa: E402


class ProductionPluginLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        production.PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        self.root = Path(
            tempfile.mkdtemp(prefix="L46-unit-", dir=production.PRIVATE_ROOT)
        )

    def tearDown(self) -> None:
        if self.root.exists():
            fixture.remove_fixture_tree(self.root)

    def test_production_identity_is_separate_from_fixture_default(self) -> None:
        self.assertEqual(production.PRODUCTION_IDENTITY.plugin_version, "0.1.0-rc.1")
        self.assertEqual(
            production.PRODUCTION_IDENTITY.marketplace_name,
            "cotend-production-candidate-local",
        )
        self.assertNotEqual(
            production.PRODUCTION_IDENTITY.plugin_version,
            fixture.FIXTURE_LIFECYCLE_IDENTITY.plugin_version,
        )
        self.assertNotEqual(
            production.PRODUCTION_IDENTITY.marketplace_name,
            fixture.FIXTURE_LIFECYCLE_IDENTITY.marketplace_name,
        )

    def test_l46_root_guard_rejects_other_private_directory(self) -> None:
        with self.assertRaises(fixture.PluginFixtureError):
            production.guarded_run_root(production.PRIVATE_ROOT / "unrelated")
        self.assertEqual(production.guarded_run_root(self.root), self.root.resolve())

    def test_marketplace_is_local_only_and_not_part_of_package(self) -> None:
        manifest = production.marketplace_manifest()
        source = manifest["plugins"][0]["source"]
        self.assertEqual(source["source"], "local")
        self.assertEqual(source["path"], "./plugins/cotend")
        self.assertEqual(manifest["name"], production.MARKETPLACE_NAME)
        self.assertNotIn(
            ".agents/plugins/marketplace.json", package.expected_package_manifest()
        )

    def test_materialized_package_matches_l44_digest(self) -> None:
        scenario = self.root / "materialized"
        scenario.mkdir()
        result = production.materialize_scenario(scenario)
        package_result = package.verify_package(result["plugin_root"])
        self.assertEqual(package_result["package_files"], 37)
        self.assertEqual(
            package_result["package_manifest_sha256"],
            production.EXPECTED_PACKAGE_DIGEST,
        )
        self.assertTrue(
            (
                result["marketplace_root"]
                / ".agents"
                / "plugins"
                / "marketplace.json"
            ).is_file()
        )

    def test_parameterized_payload_rejects_fixture_identity(self) -> None:
        installed_path = (
            self.root
            / "codex-home"
            / "plugins"
            / "cache"
            / "cotend"
            / production.MARKETPLACE_NAME
            / package.PLUGIN_VERSION
        )
        payload = {
            "pluginId": production.PRODUCTION_IDENTITY.selector,
            "name": package.PLUGIN_NAME,
            "marketplaceName": production.MARKETPLACE_NAME,
            "version": package.PLUGIN_VERSION,
            "authPolicy": "ON_INSTALL",
            "installedPath": str(installed_path),
        }
        fixture.validate_plugin_add_payload(
            payload, self.root, production.PRODUCTION_IDENTITY
        )
        with self.assertRaises(fixture.PluginFixtureError):
            fixture.validate_plugin_add_payload(
                payload, self.root, fixture.FIXTURE_LIFECYCLE_IDENTITY
            )

    def test_fail_after_plugin_add_is_deterministic(self) -> None:
        marketplace_root = self.root / "source-marketplace"
        installed_path = (
            self.root
            / "codex-home"
            / "plugins"
            / "cache"
            / "cotend"
            / production.MARKETPLACE_NAME
            / package.PLUGIN_VERSION
        )
        source = {
            "source": "local",
            "path": str(marketplace_root / "plugins" / package.PLUGIN_NAME),
        }
        available = {
            "pluginId": production.PRODUCTION_IDENTITY.selector,
            "name": package.PLUGIN_NAME,
            "marketplaceName": production.MARKETPLACE_NAME,
            "version": package.PLUGIN_VERSION,
            "installed": False,
            "enabled": False,
            "source": source,
            "installPolicy": "AVAILABLE",
            "authPolicy": "ON_INSTALL",
        }
        payloads = [
            {
                "marketplaceName": production.MARKETPLACE_NAME,
                "installedRoot": str(marketplace_root),
                "alreadyAdded": False,
            },
            {"marketplaces": [{"name": production.MARKETPLACE_NAME}]},
            {"installed": [], "available": [available]},
            {
                "pluginId": production.PRODUCTION_IDENTITY.selector,
                "name": package.PLUGIN_NAME,
                "marketplaceName": production.MARKETPLACE_NAME,
                "version": package.PLUGIN_VERSION,
                "authPolicy": "ON_INSTALL",
                "installedPath": str(installed_path),
            },
        ]
        with mock.patch.object(fixture, "run_cli_step", side_effect=payloads) as run:
            with self.assertRaisesRegex(
                fixture.PluginFixtureError,
                "injected lifecycle failure after plugin_add",
            ):
                fixture.run_phase_a(
                    self.root,
                    {},
                    {},
                    {},
                    identity=production.PRODUCTION_IDENTITY,
                    fail_after_step="plugin_add",
                )
        self.assertEqual(run.call_count, 4)

    def test_purge_removes_only_isolated_runtime_roots(self) -> None:
        env = fixture.build_isolated_env(self.root)
        sentinel = self.root / "source-marketplace" / "KEEP.txt"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_text("keep\n", encoding="utf-8")
        result = production.purge_isolated_write_roots(self.root, env)
        self.assertTrue(result["all_write_roots_absent"])
        self.assertEqual(result["write_root_keys"], 15)
        self.assertTrue(sentinel.is_file())
        self.assertTrue(
            all(not Path(env[key]).exists() for key in fixture.WRITE_ROOT_ENV_KEYS)
        )


if __name__ == "__main__":
    unittest.main()
