from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cotend_delivery import (  # noqa: E402
    Artifact,
    DeliveryError,
    IsolatedProductionUserSkillDeliveryManager,
    IsolatedUserSkillDeliveryManager,
    ProductionUserDeliveryBridge,
    inspect_production_user_layout,
    resolve_production_user_layout,
)


COMPANIONS = ("grill-me", "karpathy-guidelines")


def tree_snapshot(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        is_junction = getattr(path, "is_junction", lambda: False)
        if path.is_symlink() or is_junction():
            snapshot[relative] = f"link:{os.readlink(path)}"
        elif path.is_file():
            snapshot[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            snapshot[relative] = "directory"
    return snapshot


class IsolatedProductionUserReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.isolation = Path(self.temp.name)
        self.home = self.isolation / "home"
        self.codex_home = self.isolation / "codex-home"
        self.home.mkdir()
        self.codex_home.mkdir()
        self.artifact = Artifact.from_repository(ROOT)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @property
    def canonical(self) -> Path:
        return self.home / ".agents" / "skills"

    @property
    def compatibility(self) -> Path:
        return self.codex_home / "skills"

    @property
    def state_root(self) -> Path:
        return self.home / ".agents" / ".cotend-delivery"

    def production_manager(
        self,
        artifact: Artifact | None = None,
        *,
        codex_home: Path | None = None,
    ) -> IsolatedProductionUserSkillDeliveryManager:
        return IsolatedProductionUserSkillDeliveryManager(
            artifact or self.artifact,
            isolation_root=self.isolation,
            home=self.home,
            codex_home=codex_home or self.codex_home,
        )

    def legacy_manager(self) -> IsolatedUserSkillDeliveryManager:
        return IsolatedUserSkillDeliveryManager(
            self.artifact,
            isolation_root=self.isolation,
            home=self.home,
            codex_home=self.codex_home,
            state_root=self.state_root,
        )

    def receipt(self) -> dict[str, object]:
        return json.loads((self.state_root / "receipt.json").read_text(encoding="utf-8"))

    def write_receipt(self, receipt: dict[str, object]) -> None:
        (self.state_root / "receipt.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def add_external(self, skill: str) -> Path:
        destination = self.compatibility / skill
        shutil.copytree(self.artifact.root / skill, destination)
        return destination

    def updated_artifact(self) -> Artifact:
        source = self.isolation / "artifact-v2"
        shutil.copytree(self.artifact.root, source)
        entry = source / "cotend-init" / "SKILL.md"
        entry.write_text(
            entry.read_text(encoding="utf-8") + "\n<!-- production-v2 -->\n",
            encoding="utf-8",
        )
        return Artifact.from_directory(
            source,
            source_release_id=self.artifact.source_release_id,
            artifact_id="cotend-codex-r000002",
            revision=2,
            protocol=self.artifact.protocol,
        )

    def test_fresh_install_writes_schema_v4_bound_to_resolved_identity(self) -> None:
        manager = self.production_manager()
        preview_before = tree_snapshot(self.isolation)
        preview = manager.execute("install")
        self.assertEqual(preview["status"], "planned")
        self.assertEqual(tree_snapshot(self.isolation), preview_before)

        installed = manager.execute("install", apply=True)
        receipt = self.receipt()
        self.assertEqual(installed["state_after"]["installation"], "complete")
        self.assertEqual(receipt["schema_version"], 4)
        self.assertEqual(receipt["installation_id"], manager.production_layout.installation_id)
        self.assertEqual(
            receipt["layout_fingerprint"],
            manager.production_layout.layout_fingerprint,
        )
        self.assertNotIn(str(self.home), json.dumps(receipt))

    def test_schema_v4_full_lifecycle_preserves_external_companions(self) -> None:
        for skill in COMPANIONS:
            self.add_external(skill)
        external_before = tree_snapshot(self.compatibility)
        manager = self.production_manager()
        manager.execute("install", apply=True)
        self.assertEqual(self.receipt()["schema_version"], 4)

        manager.execute("disable", apply=True)
        manager.execute("enable", apply=True)
        updated = self.updated_artifact()
        manager.execute("update", updated, apply=True)
        manager.execute("rollback", updated, apply=True)
        manager.execute("uninstall", apply=True)
        self.assertEqual(tree_snapshot(self.compatibility), external_before)

        manager.execute("rollback", apply=True)
        self.assertEqual(self.receipt()["schema_version"], 4)
        self.assertEqual(tree_snapshot(self.compatibility), external_before)

    def test_schema_v3_migration_is_previewable_receipt_only_and_reversible(self) -> None:
        legacy = self.legacy_manager()
        legacy.execute("install", apply=True)
        legacy_receipt_bytes = legacy.receipt_path.read_bytes()
        payload_before = tree_snapshot(self.canonical)
        manager = self.production_manager()
        state = manager.inspect()
        self.assertEqual(state["candidate_relation"], "identity_migration_available")
        self.assertEqual(state["identity_migration_kind"], "production_receipt_binding")

        before_preview = tree_snapshot(self.isolation)
        preview = manager.execute("migrate_identity")
        self.assertEqual(preview["status"], "planned")
        self.assertEqual(tree_snapshot(self.isolation), before_preview)

        migrated = manager.execute("migrate_identity", apply=True)
        receipt = self.receipt()
        self.assertEqual(migrated["state_after"]["receipt_schema_version"], 4)
        self.assertEqual(tree_snapshot(self.canonical), payload_before)
        checkpoint = json.loads(
            (manager.rollback_path / "checkpoint.json").read_text(encoding="utf-8")
        )
        self.assertEqual(checkpoint["payload_mode"], "preserve_existing")
        self.assertFalse((manager.rollback_path / "enabled-skills").exists())
        self.assertEqual(receipt["installation_id"], manager.production_layout.installation_id)

        manager.execute("rollback", apply=True)
        self.assertEqual(legacy.receipt_path.read_bytes(), legacy_receipt_bytes)
        self.assertEqual(tree_snapshot(self.canonical), payload_before)

    def test_schema_v3_ownership_tamper_is_rejected_before_migration(self) -> None:
        self.add_external("grill-me")
        legacy = self.legacy_manager()
        legacy.execute("install", apply=True)
        receipt = self.receipt()
        receipt["owned_skills"].append("grill-me")  # type: ignore[union-attr]
        self.write_receipt(receipt)

        before = tree_snapshot(self.isolation)
        state = self.production_manager().inspect()
        self.assertFalse(state["receipt_valid"])
        self.assertIn("receipt_invalid", state["diagnostics"])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_schema_v3_payload_drift_blocks_migration_and_combined_repair(self) -> None:
        self.legacy_manager().execute("install", apply=True)
        target = self.canonical / "cotend-init" / "SKILL.md"
        target.write_text("drift\n", encoding="utf-8")
        manager = self.production_manager()
        before = tree_snapshot(self.isolation)

        migration = manager.plan("migrate_identity")
        repair = manager.plan("repair")
        self.assertFalse(migration["allowed"])
        self.assertFalse(repair["allowed"])
        self.assertEqual(
            repair["reason"],
            "production_identity_migration_requires_complete_verified_payload",
        )
        with self.assertRaises(DeliveryError):
            manager.execute("migrate_identity", apply=True)
        with self.assertRaises(DeliveryError):
            manager.execute("repair", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_schema_v3_external_shared_drift_blocks_migration_without_takeover(self) -> None:
        external = self.add_external("grill-me")
        self.legacy_manager().execute("install", apply=True)
        (external / "SKILL.md").write_text("external drift\n", encoding="utf-8")
        manager = self.production_manager()
        before = tree_snapshot(self.isolation)

        state = manager.inspect()
        self.assertIn("external_shared_missing:grill-me", state["unexpected"])
        self.assertIn("companion_content_incompatible:grill-me", state["unexpected"])
        with self.assertRaises(DeliveryError):
            manager.execute("migrate_identity", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_schema_v3_hybrid_production_identity_fields_are_rejected(self) -> None:
        self.legacy_manager().execute("install", apply=True)
        receipt = self.receipt()
        layout = resolve_production_user_layout(
            home=self.home,
            codex_home=self.codex_home,
        )
        receipt["installation_id"] = layout.installation_id
        receipt["layout_fingerprint"] = layout.layout_fingerprint
        self.write_receipt(receipt)

        state = self.production_manager().inspect()
        self.assertFalse(state["receipt_valid"])
        self.assertIn("receipt_invalid", state["diagnostics"])

    def test_schema_v4_installation_identity_tamper_is_rejected(self) -> None:
        manager = self.production_manager()
        manager.execute("install", apply=True)
        receipt = self.receipt()
        receipt["installation_id"] = "cotend-user-000000000000000000000000"
        self.write_receipt(receipt)

        before = tree_snapshot(self.isolation)
        state = manager.inspect()
        self.assertFalse(state["receipt_valid"])
        self.assertIn("receipt_installation_identity_mismatch", state["diagnostics"])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_layout_context_rebind_is_receipt_only_and_reversible(self) -> None:
        original = self.production_manager()
        original.execute("install", apply=True)
        old_receipt_bytes = original.receipt_path.read_bytes()
        payload_before = tree_snapshot(self.canonical)
        other_codex_home = self.isolation / "other-codex-home"
        other_codex_home.mkdir()
        rebound = self.production_manager(codex_home=other_codex_home)

        state = rebound.inspect()
        self.assertEqual(state["candidate_relation"], "identity_migration_available")
        self.assertEqual(state["identity_migration_kind"], "layout_context_rebind")
        before_preview = tree_snapshot(self.isolation)
        rebound.execute("migrate_identity")
        self.assertEqual(tree_snapshot(self.isolation), before_preview)

        rebound.execute("migrate_identity", apply=True)
        receipt = self.receipt()
        self.assertEqual(
            receipt["layout_fingerprint"],
            rebound.production_layout.layout_fingerprint,
        )
        self.assertEqual(tree_snapshot(self.canonical), payload_before)
        rebound.execute("rollback", apply=True)
        self.assertEqual(original.receipt_path.read_bytes(), old_receipt_bytes)
        self.assertEqual(tree_snapshot(self.canonical), payload_before)

    def test_layout_context_change_blocks_artifact_update_until_rebound(self) -> None:
        self.production_manager().execute("install", apply=True)
        updated = self.updated_artifact()
        other_codex_home = self.isolation / "other-codex-home"
        other_codex_home.mkdir()
        changed = self.production_manager(updated, codex_home=other_codex_home)
        before = tree_snapshot(self.isolation)

        state = changed.inspect()
        self.assertEqual(state["candidate_relation"], "incompatible")
        self.assertIn(
            "layout_context_migration_required_before_artifact_change",
            state["diagnostics"],
        )
        with self.assertRaises(DeliveryError):
            changed.execute("update", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

        rebound = self.production_manager(codex_home=other_codex_home)
        rebound.execute("migrate_identity", apply=True)
        changed.execute("update", apply=True)
        self.assertEqual(self.receipt()["target_revision"], 2)

    def test_production_bridge_is_hard_disabled_and_never_creates_state(self) -> None:
        bridge = ProductionUserDeliveryBridge(
            home=self.home,
            codex_home=self.codex_home,
        )
        before = tree_snapshot(self.isolation)
        preview = bridge.execute("install")
        self.assertEqual(preview["transaction_bridge"]["state"], "hard_disabled")
        self.assertFalse(preview["transaction_bridge"]["manager_available"])
        self.assertEqual(preview["transaction_bridge"]["receipt_schema_version"], 4)
        self.assertEqual(tree_snapshot(self.isolation), before)
        with self.assertRaisesRegex(DeliveryError, "read-only"):
            bridge.execute("install", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)
        self.assertFalse(self.state_root.exists())

    def test_isolated_production_manager_rejects_escape_and_simulated_live_home(self) -> None:
        before = tree_snapshot(self.isolation)
        with self.assertRaisesRegex(DeliveryError, "outside the explicit isolation root"):
            IsolatedProductionUserSkillDeliveryManager(
                self.artifact,
                isolation_root=self.home,
                home=self.home,
                codex_home=self.codex_home,
            )
        with mock.patch.object(Path, "home", return_value=self.home):
            with self.assertRaisesRegex(DeliveryError, "isolated user roots only"):
                self.production_manager()
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_resolver_recognizes_current_changed_and_foreign_v4_envelopes(self) -> None:
        manager = self.production_manager()
        manager.execute("install", apply=True)
        current_layout = manager.production_layout
        current = inspect_production_user_layout(current_layout)
        self.assertEqual(current["state"]["receipt_status"], "current_envelope")
        self.assertEqual(current["migration_status"], "none")

        other_codex_home = self.isolation / "other-codex-home"
        other_codex_home.mkdir()
        changed_layout = resolve_production_user_layout(
            home=self.home,
            codex_home=other_codex_home,
        )
        changed = inspect_production_user_layout(changed_layout)
        self.assertEqual(
            changed["migration_status"],
            "explicit_layout_context_migration_required",
        )
        self.assertIn("layout_context_changed", changed["blockers"])

        receipt = self.receipt()
        receipt["installation_id"] = "cotend-user-000000000000000000000000"
        self.write_receipt(receipt)
        foreign = inspect_production_user_layout(current_layout)
        self.assertEqual(
            foreign["migration_status"],
            "blocked_installation_identity_mismatch",
        )
        self.assertIn("installation_identity_mismatch", foreign["blockers"])


if __name__ == "__main__":
    unittest.main()
