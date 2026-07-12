from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", ROOT / "scripts"):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from cotend_delivery import Artifact  # noqa: E402
import verify_delivered_codex_runtime as bridge  # noqa: E402
import verify_isolated_codex_carrier as carrier  # noqa: E402


class DeliveredCodexRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        bridge.PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        self.fixture = Path(
            tempfile.mkdtemp(prefix="L25-unit-", dir=bridge.PRIVATE_ROOT)
        )

    def tearDown(self) -> None:
        if self.fixture.exists():
            bridge.remove_fixture_tree(self.fixture)

    def test_unrelated_static_skill_requires_explicit_tolerance(self) -> None:
        carrier.prepare_fixture(self.fixture)
        bridge.write_unrelated_skill(self.fixture)

        with self.assertRaises(carrier.CarrierError):
            carrier.verify_static(self.fixture)
        result = carrier.verify_static(
            self.fixture,
            allow_unrelated_skills=True,
        )
        self.assertEqual(result["skills"], 7)
        self.assertEqual(result["files"], 30)
        self.assertEqual(result["unrelated_skills"], [bridge.UNRELATED_SKILL])

    def test_delivery_preflight_uses_receipt_and_exact_artifact(self) -> None:
        artifact = Artifact.from_repository(ROOT)
        bridge.remove_fixture_tree(self.fixture)
        shutil.copytree(carrier.TEMPLATE_ROOT, self.fixture)
        bridge.write_unrelated_skill(self.fixture)
        bridge.initialize_nested_repository(self.fixture)
        manager = bridge.DeliveryManager(self.fixture)
        installed = manager.execute("install", artifact, apply=True)
        state = bridge.validate_delivery_state(manager, artifact)
        static = carrier.verify_static(
            self.fixture,
            allow_unrelated_skills=True,
        )

        self.assertEqual(installed["status"], "applied")
        self.assertEqual(state["artifact_id"], artifact.artifact_id)
        self.assertEqual(static["unrelated_skills"], ["user-skill"])

    def test_discovery_contract_rejects_missing_or_wrong_scope(self) -> None:
        valid = bridge.valid_discovery_sample()
        bridge.validate_bridge_discovery(
            valid,
            expected_unrelated={bridge.UNRELATED_SKILL},
        )

        missing = bridge.valid_discovery_sample()
        missing["fixture_skills"] = missing["fixture_skills"][1:]
        missing["fixture_skill_count"] -= 1
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_bridge_discovery(
                missing,
                expected_unrelated={bridge.UNRELATED_SKILL},
            )

        wrong_scope = bridge.valid_discovery_sample()
        wrong_scope["fixture_skills"][0]["scope"] = "user"
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_bridge_discovery(
                wrong_scope,
                expected_unrelated={bridge.UNRELATED_SKILL},
            )


if __name__ == "__main__":
    unittest.main()
