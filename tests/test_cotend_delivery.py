from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cotend_delivery import Artifact, DeliveryError, DeliveryManager  # noqa: E402


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_manifest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class DeliveryLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.temp_root = Path(self.temp.name)
        self.project = self.temp_root / "project"
        self.project.mkdir()
        (self.project / "README.md").write_text("user readme\n", encoding="utf-8")
        (self.project / "USER-NOTES.md").write_text("keep me\n", encoding="utf-8")
        (self.project / "STATUS.md").write_text("project truth\n", encoding="utf-8")
        unrelated = self.project / ".agents" / "skills" / "user-skill"
        unrelated.mkdir(parents=True)
        (unrelated / "SKILL.md").write_text("user-owned skill\n", encoding="utf-8")
        self.protected = {
            relative: file_sha256(self.project / relative)
            for relative in (
                "README.md",
                "USER-NOTES.md",
                "STATUS.md",
                ".agents/skills/user-skill/SKILL.md",
            )
        }
        self.artifact = Artifact.from_repository(ROOT)
        self.manager = DeliveryManager(self.project)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_protected_unchanged(self) -> None:
        for relative, expected in self.protected.items():
            self.assertEqual(file_sha256(self.project / relative), expected, relative)

    def make_updated_artifact(self) -> Artifact:
        source = self.temp_root / "artifact-v2"
        shutil.copytree(ROOT / "codex-skills", source)
        changed = source / "cotend-init" / "SKILL.md"
        changed.write_text(
            changed.read_text(encoding="utf-8") + "\n<!-- delivery-test-v2 -->\n",
            encoding="utf-8",
        )
        return Artifact.from_directory(
            source,
            source_release_id=self.artifact.source_release_id,
            artifact_id="cotend-codex-r000002",
            revision=2,
            protocol=self.artifact.protocol,
        )

    def install(self) -> None:
        result = self.manager.execute("install", self.artifact, apply=True)
        self.assertTrue(result["applied"])

    def load_receipt(self) -> dict[str, object]:
        return json.loads(self.manager.receipt_path.read_text(encoding="utf-8"))

    def write_legacy_receipt(self, *, artifact_id: str | None = None) -> dict[str, object]:
        mapping = self.artifact.legacy_receipt_mappings[0]
        receipt = self.load_receipt()
        legacy = {
            key: value
            for key, value in receipt.items()
            if key not in {"source_release_id", "artifact_lineage", "target_revision"}
        }
        legacy.update(
            {
                "schema_version": 1,
                "artifact_id": artifact_id or mapping.artifact_id,
                "protocol": mapping.protocol,
                "manifest_sha256": mapping.manifest_sha256,
            }
        )
        self.manager.receipt_path.write_text(
            json.dumps(legacy, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return legacy

    def managed_payload_manifest(self) -> dict[str, str]:
        return {
            relative: digest
            for relative, digest in tree_manifest(self.project).items()
            if relative.startswith(".agents/skills/")
            and not relative.startswith(".agents/skills/user-skill/")
        }

    def test_artifact_identity_dry_run_and_idempotent_install(self) -> None:
        self.assertEqual(len(self.artifact.skills), 7)
        self.assertEqual(len(self.artifact.files), 30)
        self.assertEqual(self.artifact.source_release_id, "2026.07.11.3")
        self.assertEqual(self.artifact.artifact_id, "cotend-codex-r000001")
        self.assertEqual(self.artifact.revision, 1)
        before = tree_manifest(self.project)

        preview = self.manager.execute("install", self.artifact)
        self.assertEqual(preview["status"], "planned")
        self.assertFalse(preview["applied"])
        self.assertEqual(tree_manifest(self.project), before)

        self.install()
        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(state["enablement"], "enabled")
        self.assertEqual(state["candidate_relation"], "same_as_current")
        self.assertEqual(state["managed_files"], 30)
        receipt = self.load_receipt()
        self.assertEqual(receipt["schema_version"], 2)
        self.assertEqual(receipt["source_release_id"], self.artifact.source_release_id)
        self.assertEqual(receipt["artifact_lineage"], self.artifact.lineage)
        self.assertEqual(receipt["target_revision"], self.artifact.revision)

        repeated = self.manager.execute("install", self.artifact, apply=True)
        self.assertEqual(repeated["status"], "current_no_change")
        self.assertFalse(repeated["applied"])
        self.assert_protected_unchanged()

    def test_disable_enable_preserves_unrelated_project_content(self) -> None:
        self.install()
        disabled = self.manager.execute("disable", self.artifact, apply=True)
        self.assertEqual(disabled["state_after"]["enablement"], "disabled")
        self.assertTrue((self.project / ".agents" / "skills" / "user-skill").is_dir())

        enabled = self.manager.execute("enable", self.artifact, apply=True)
        self.assertEqual(enabled["state_after"]["enablement"], "enabled")
        self.assert_protected_unchanged()

    def test_disabled_lifecycle_preserves_enablement(self) -> None:
        self.install()
        self.manager.execute("disable", self.artifact, apply=True)
        managed = (
            self.project
            / ".agents"
            / ".cotend-delivery"
            / "disabled-skills"
            / "cotend-init"
            / "SKILL.md"
        )
        managed.write_text("damaged while disabled\n", encoding="utf-8")

        repaired = self.manager.execute("repair", self.artifact, apply=True)
        self.assertEqual(repaired["state_after"]["enablement"], "disabled")
        updated_artifact = self.make_updated_artifact()
        updated = self.manager.execute("update", updated_artifact, apply=True)
        self.assertEqual(updated["state_after"]["enablement"], "disabled")
        update_rollback = self.manager.execute(
            "rollback",
            updated_artifact,
            apply=True,
        )
        self.assertEqual(update_rollback["state_after"]["enablement"], "disabled")

        self.manager.execute("uninstall", apply=True)
        uninstall_rollback = self.manager.execute("rollback", apply=True)
        self.assertEqual(
            uninstall_rollback["state_after"]["enablement"],
            "disabled",
        )
        self.assert_protected_unchanged()

    def test_update_and_one_step_rollback(self) -> None:
        self.install()
        updated_artifact = self.make_updated_artifact()

        updated = self.manager.execute("update", updated_artifact, apply=True)
        self.assertEqual(updated["state_after"]["artifact_id"], updated_artifact.artifact_id)
        self.assertEqual(updated["state_after"]["candidate_relation"], "same_as_current")

        rolled_back = self.manager.execute("rollback", updated_artifact, apply=True)
        self.assertEqual(rolled_back["state_after"]["artifact_id"], self.artifact.artifact_id)
        self.assertEqual(
            rolled_back["state_after"]["candidate_relation"],
            "update_available",
        )
        self.assert_protected_unchanged()

    def test_same_artifact_id_with_different_bytes_is_blocked(self) -> None:
        self.install()
        updated_artifact = self.make_updated_artifact()
        conflicting_artifact = Artifact.from_directory(
            updated_artifact.root,
            source_release_id=self.artifact.source_release_id,
            artifact_id=self.artifact.artifact_id,
            revision=self.artifact.revision,
            protocol=self.artifact.protocol,
        )

        state = self.manager.inspect(conflicting_artifact)
        self.assertEqual(state["candidate_relation"], "incompatible")
        self.assertIn("artifact_identity_conflict", state["diagnostics"])
        with self.assertRaisesRegex(DeliveryError, "update is blocked"):
            self.manager.execute("update", conflicting_artifact, apply=True)
        current = self.manager.inspect(self.artifact)
        self.assertEqual(current["candidate_relation"], "same_as_current")
        self.assert_protected_unchanged()

    def test_lower_revision_is_not_mislabeled_as_update(self) -> None:
        self.install()
        updated_artifact = self.make_updated_artifact()
        self.manager.execute("update", updated_artifact, apply=True)

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["candidate_relation"], "downgrade_candidate")
        self.assertEqual(state["recommended_operation"], "manual_resolution")
        with self.assertRaisesRegex(DeliveryError, "update is blocked"):
            self.manager.execute("update", self.artifact, apply=True)
        self.assertEqual(
            self.manager.inspect(updated_artifact)["candidate_relation"],
            "same_as_current",
        )
        self.assert_protected_unchanged()

    def test_protocol_change_is_incompatible_even_at_higher_revision(self) -> None:
        self.install()
        candidate = Artifact.from_directory(
            self.artifact.root,
            source_release_id=self.artifact.source_release_id,
            artifact_id="cotend-codex-r000002",
            revision=2,
            protocol="cotend-collaboration-v99",
        )

        state = self.manager.inspect(candidate)
        self.assertEqual(state["candidate_relation"], "incompatible")
        self.assertIn("protocol_incompatible", state["diagnostics"])
        with self.assertRaisesRegex(DeliveryError, "update is blocked"):
            self.manager.execute("update", candidate, apply=True)
        self.assert_protected_unchanged()

    def test_legacy_identity_migration_is_receipt_only_and_reversible(self) -> None:
        self.install()
        legacy_receipt = self.write_legacy_receipt()
        payload_before = self.managed_payload_manifest()
        tree_before_preview = tree_manifest(self.project)

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["candidate_relation"], "identity_migration_available")
        self.assertEqual(state["recommended_operation"], "migrate_identity")
        preview = self.manager.execute("migrate_identity", self.artifact)
        self.assertEqual(preview["status"], "planned")
        self.assertEqual(tree_manifest(self.project), tree_before_preview)

        migrated = self.manager.execute(
            "migrate_identity",
            self.artifact,
            apply=True,
        )
        self.assertEqual(migrated["state_after"]["candidate_relation"], "same_as_current")
        self.assertEqual(self.load_receipt()["schema_version"], 2)
        self.assertEqual(self.managed_payload_manifest(), payload_before)
        checkpoint = json.loads(
            (self.manager.rollback_path / "checkpoint.json").read_text(encoding="utf-8")
        )
        self.assertEqual(checkpoint["payload_mode"], "preserve_existing")
        self.assertFalse((self.manager.rollback_path / "enabled-skills").exists())

        rolled_back = self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(
            rolled_back["state_after"]["candidate_relation"],
            "identity_migration_available",
        )
        self.assertEqual(self.load_receipt(), legacy_receipt)
        self.assertEqual(self.managed_payload_manifest(), payload_before)
        self.assert_protected_unchanged()

    def test_unmapped_legacy_identity_cannot_migrate_or_repair(self) -> None:
        self.install()
        self.write_legacy_receipt(artifact_id="unmapped-legacy-artifact")
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("damaged legacy payload\n", encoding="utf-8")

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["candidate_relation"], "incompatible")
        self.assertIn("legacy_identity_unmapped", state["diagnostics"])
        with self.assertRaisesRegex(DeliveryError, "migrate_identity is blocked"):
            self.manager.execute("migrate_identity", self.artifact, apply=True)
        with self.assertRaisesRegex(DeliveryError, "repair is blocked"):
            self.manager.execute("repair", self.artifact, apply=True)
        self.assertEqual(managed.read_text(encoding="utf-8"), "damaged legacy payload\n")
        self.assert_protected_unchanged()

    def test_damaged_mapped_legacy_receipt_repairs_and_migrates(self) -> None:
        self.install()
        self.write_legacy_receipt()
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("damaged mapped legacy payload\n", encoding="utf-8")

        before = self.manager.inspect(self.artifact)
        self.assertEqual(before["installation"], "damaged")
        self.assertEqual(before["candidate_relation"], "identity_migration_available")
        repaired = self.manager.execute("repair", self.artifact, apply=True)
        self.assertEqual(repaired["state_after"]["installation"], "complete")
        self.assertEqual(repaired["state_after"]["candidate_relation"], "same_as_current")
        self.assertEqual(self.load_receipt()["schema_version"], 2)
        self.assertEqual(file_sha256(managed), self.artifact.files["cotend-init/SKILL.md"])
        self.assert_protected_unchanged()

    def test_preserved_migration_checkpoint_rejects_payload_drift(self) -> None:
        self.install()
        self.write_legacy_receipt()
        self.manager.execute("migrate_identity", self.artifact, apply=True)
        receipt_before = self.load_receipt()
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("changed after identity migration\n", encoding="utf-8")

        with self.assertRaisesRegex(DeliveryError, "Preserved checkpoint payload"):
            self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(self.load_receipt(), receipt_before)
        self.assertEqual(managed.read_text(encoding="utf-8"), "changed after identity migration\n")
        self.assert_protected_unchanged()

    def test_legacy_snapshot_checkpoint_remains_readable(self) -> None:
        self.install()
        legacy_receipt = self.write_legacy_receipt()
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("legacy checkpoint damage\n", encoding="utf-8")
        self.manager.execute("repair", self.artifact, apply=True)
        checkpoint_path = self.manager.rollback_path / "checkpoint.json"
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        checkpoint["schema_version"] = 1
        checkpoint.pop("payload_mode")
        checkpoint_path.write_text(
            json.dumps(checkpoint, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        rolled_back = self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(rolled_back["state_after"]["installation"], "damaged")
        self.assertEqual(self.load_receipt(), legacy_receipt)
        self.assertEqual(managed.read_text(encoding="utf-8"), "legacy checkpoint damage\n")
        self.assert_protected_unchanged()

    def test_legacy_receipt_rejects_schema_v2_identity_fields(self) -> None:
        self.install()
        mapping = self.artifact.legacy_receipt_mappings[0]
        hybrid = self.load_receipt()
        hybrid.update(
            {
                "schema_version": 1,
                "artifact_id": mapping.artifact_id,
                "protocol": mapping.protocol,
                "manifest_sha256": mapping.manifest_sha256,
            }
        )
        self.manager.receipt_path.write_text(
            json.dumps(hybrid, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        state = self.manager.inspect(self.artifact)
        self.assertFalse(state["receipt_valid"])
        self.assertEqual(state["candidate_relation"], "unknown")
        self.assertIn("receipt_invalid", state["diagnostics"])
        with self.assertRaisesRegex(DeliveryError, "migrate_identity is blocked"):
            self.manager.execute("migrate_identity", self.artifact, apply=True)
        self.assert_protected_unchanged()

    def test_legacy_checkpoint_rejects_schema_v2_operation(self) -> None:
        self.install()
        checkpoint_path = self.manager.rollback_path / "checkpoint.json"
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        checkpoint["schema_version"] = 1
        checkpoint["operation"] = "migrate_identity"
        checkpoint.pop("payload_mode")
        checkpoint_path.write_text(
            json.dumps(checkpoint, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        receipt_before = self.manager.receipt_path.read_bytes()

        with self.assertRaisesRegex(DeliveryError, "checkpoint metadata is invalid"):
            self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(self.manager.receipt_path.read_bytes(), receipt_before)
        self.assert_protected_unchanged()

    def test_schema_v2_checkpoint_requires_explicit_payload_mode(self) -> None:
        self.install()
        checkpoint_path = self.manager.rollback_path / "checkpoint.json"
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        checkpoint.pop("payload_mode")
        checkpoint_path.write_text(
            json.dumps(checkpoint, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        receipt_before = self.manager.receipt_path.read_bytes()

        with self.assertRaisesRegex(DeliveryError, "checkpoint metadata is invalid"):
            self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(self.manager.receipt_path.read_bytes(), receipt_before)
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "complete")
        self.assert_protected_unchanged()

    def test_target_lock_manifest_drift_is_rejected(self) -> None:
        repository = self.temp_root / "repository"
        shutil.copytree(ROOT / "codex-skills", repository / "codex-skills")
        shutil.copytree(ROOT / "upstream", repository / "upstream")
        target_lock = repository / "delivery" / "codex-artifact.lock.json"
        target_lock.parent.mkdir()
        shutil.copy2(ROOT / "delivery" / "codex-artifact.lock.json", target_lock)
        value = json.loads(target_lock.read_text(encoding="utf-8"))
        value["target"]["manifest_sha256"] = "0" * 64
        target_lock.write_text(
            json.dumps(value, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(DeliveryError, "Target artifact inventory"):
            Artifact.from_repository(repository)

    def test_repair_restores_modified_and_missing_owned_files(self) -> None:
        self.install()
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("damaged\n", encoding="utf-8")
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "damaged")

        repaired = self.manager.execute("repair", self.artifact, apply=True)
        self.assertEqual(repaired["state_after"]["installation"], "complete")
        self.assertEqual(file_sha256(managed), self.artifact.files["cotend-init/SKILL.md"])

        managed.unlink()
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "partial")
        self.manager.execute("repair", self.artifact, apply=True)
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "complete")

        missing_skill = self.project / ".agents" / "skills" / "grill-me"
        shutil.rmtree(missing_skill)
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "partial")
        self.manager.execute("repair", self.artifact, apply=True)
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "complete")
        self.assert_protected_unchanged()

    def test_repair_failure_restores_exact_damaged_state(self) -> None:
        self.install()
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("damaged before repair\n", encoding="utf-8")

        with mock.patch.object(
            self.manager,
            "_write_receipt",
            side_effect=OSError("injected repair failure"),
        ):
            with self.assertRaisesRegex(DeliveryError, "prior checkpoint was restored"):
                self.manager.execute("repair", self.artifact, apply=True)

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "damaged")
        self.assertEqual(state["transition"], "recovery_required")
        self.assertEqual(state["transition_artifacts"], [])
        self.assertEqual(managed.read_text(encoding="utf-8"), "damaged before repair\n")
        self.assert_protected_unchanged()

    def test_repair_rollback_restores_exact_damaged_state(self) -> None:
        self.install()
        managed = self.project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        managed.write_text("damage to restore\n", encoding="utf-8")
        self.manager.execute("repair", self.artifact, apply=True)

        rolled_back = self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(rolled_back["state_after"]["installation"], "damaged")
        self.assertEqual(
            rolled_back["state_after"]["transition"],
            "recovery_required",
        )
        self.assertEqual(managed.read_text(encoding="utf-8"), "damage to restore\n")
        self.assert_protected_unchanged()

    def test_unexpected_file_blocks_repair_and_uninstall(self) -> None:
        self.install()
        unexpected = (
            self.project
            / ".agents"
            / "skills"
            / "cotend-init"
            / "USER-EXTENSION.md"
        )
        unexpected.write_text("do not delete\n", encoding="utf-8")
        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "damaged")
        self.assertIn("cotend-init/USER-EXTENSION.md", state["unexpected"])

        with self.assertRaisesRegex(DeliveryError, "repair is blocked"):
            self.manager.execute("repair", self.artifact, apply=True)
        with self.assertRaisesRegex(DeliveryError, "uninstall is blocked"):
            self.manager.execute("uninstall", self.artifact, apply=True)
        with self.assertRaisesRegex(DeliveryError, "rollback is blocked"):
            self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(unexpected.read_text(encoding="utf-8"), "do not delete\n")
        self.assert_protected_unchanged()

    def test_shadow_payload_blocks_mutation(self) -> None:
        self.install()
        shadow = (
            self.project
            / ".agents"
            / ".cotend-delivery"
            / "disabled-skills"
            / "cotend-init"
        )
        shadow.mkdir(parents=True)
        shadow_file = shadow / "USER-EXTENSION.md"
        shadow_file.write_text("preserve me\n", encoding="utf-8")

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "damaged")
        self.assertIn(
            ".agents/.cotend-delivery/disabled-skills/cotend-init",
            state["unexpected"],
        )
        with self.assertRaisesRegex(DeliveryError, "rollback is blocked"):
            self.manager.execute("rollback", self.artifact, apply=True)
        with self.assertRaisesRegex(DeliveryError, "uninstall is blocked"):
            self.manager.execute("uninstall", self.artifact, apply=True)
        self.assertEqual(shadow_file.read_text(encoding="utf-8"), "preserve me\n")
        self.assert_protected_unchanged()

    def test_uninstall_removes_only_owned_files_and_can_rollback(self) -> None:
        self.install()
        uninstalled = self.manager.execute("uninstall", self.artifact, apply=True)
        self.assertEqual(uninstalled["state_after"]["installation"], "absent")
        self.assertTrue(uninstalled["state_after"]["rollback_available"])
        self.assertTrue((self.project / ".agents" / "skills" / "user-skill").is_dir())
        self.assert_protected_unchanged()

        restored = self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(restored["state_after"]["installation"], "complete")
        self.assertEqual(restored["state_after"]["artifact_id"], self.artifact.artifact_id)
        self.assert_protected_unchanged()

    def test_unowned_collision_blocks_install(self) -> None:
        collision_project = self.temp_root / "collision-project"
        collision = collision_project / ".agents" / "skills" / "cotend-init"
        collision.mkdir(parents=True)
        collision_file = collision / "SKILL.md"
        collision_file.write_text("user collision\n", encoding="utf-8")
        manager = DeliveryManager(collision_project)

        with self.assertRaisesRegex(DeliveryError, "install is blocked"):
            manager.execute("install", self.artifact, apply=True)
        self.assertEqual(collision_file.read_text(encoding="utf-8"), "user collision\n")

    def test_invalid_receipt_blocks_mutation_but_allows_rollback(self) -> None:
        self.install()
        receipt = self.project / ".agents" / ".cotend-delivery" / "receipt.json"
        receipt.write_text("{broken", encoding="utf-8")
        self.assertEqual(self.manager.inspect(self.artifact)["installation"], "unknown")

        with self.assertRaisesRegex(DeliveryError, "update is blocked"):
            self.manager.execute("update", self.make_updated_artifact(), apply=True)
        rolled_back = self.manager.execute("rollback", self.artifact, apply=True)
        self.assertEqual(rolled_back["state_after"]["installation"], "absent")
        self.assert_protected_unchanged()

    def test_corrupt_checkpoint_is_rejected_before_mutation(self) -> None:
        self.install()
        updated_artifact = self.make_updated_artifact()
        self.manager.execute("update", updated_artifact, apply=True)
        current_before = tree_manifest(self.project)
        checkpoint_file = (
            self.project
            / ".agents"
            / ".cotend-delivery"
            / "rollback"
            / "enabled-skills"
            / "cotend-init"
            / "SKILL.md"
        )
        checkpoint_file.write_text("corrupt checkpoint\n", encoding="utf-8")

        with self.assertRaisesRegex(DeliveryError, "integrity verification failed"):
            self.manager.execute("rollback", updated_artifact, apply=True)
        current_after = tree_manifest(self.project)
        changed = {
            path
            for path in set(current_before) | set(current_after)
            if current_before.get(path) != current_after.get(path)
        }
        self.assertEqual(
            changed,
            {
                ".agents/.cotend-delivery/rollback/enabled-skills/"
                "cotend-init/SKILL.md"
            },
        )
        state = self.manager.inspect(updated_artifact)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(state["artifact_id"], updated_artifact.artifact_id)
        self.assert_protected_unchanged()

    def test_failed_update_restores_prior_state_and_prior_rollback(self) -> None:
        self.install()
        updated_artifact = self.make_updated_artifact()

        def fail_receipt_write(_receipt: dict[str, object]) -> None:
            self.manager.receipt_temp_path.write_text(
                "incomplete receipt\n",
                encoding="utf-8",
            )
            raise OSError("injected receipt failure")

        with mock.patch.object(
            self.manager,
            "_write_receipt",
            side_effect=fail_receipt_write,
        ):
            with self.assertRaisesRegex(DeliveryError, "prior checkpoint was restored"):
                self.manager.execute("update", updated_artifact, apply=True)

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(state["enablement"], "enabled")
        self.assertEqual(state["transition"], "stable")
        self.assertEqual(state["transition_artifacts"], [])
        self.assertEqual(state["artifact_id"], self.artifact.artifact_id)
        self.assertTrue(state["rollback_available"])
        self.assert_protected_unchanged()

    def test_commit_cleanup_failure_restores_prior_state(self) -> None:
        self.install()
        updated_artifact = self.make_updated_artifact()
        with mock.patch.object(
            self.manager,
            "_commit_checkpoint",
            side_effect=OSError("injected commit cleanup failure"),
        ):
            with self.assertRaisesRegex(DeliveryError, "prior checkpoint was restored"):
                self.manager.execute("update", updated_artifact, apply=True)

        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(state["artifact_id"], self.artifact.artifact_id)
        self.assertEqual(state["transition"], "stable")
        self.assertTrue(state["rollback_available"])
        self.assert_protected_unchanged()

    def test_cli_defaults_to_dry_run(self) -> None:
        before = tree_manifest(self.project)
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "cotend_delivery.py"),
                "install",
                "--project",
                str(self.project),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "planned")
        self.assertFalse(result["applied"])
        self.assertEqual(tree_manifest(self.project), before)

    def test_candidate_free_operations_ignore_missing_repository(self) -> None:
        self.install()
        missing_repository = self.temp_root / "missing-repository"
        for operation in ("disable", "enable", "uninstall", "rollback"):
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "cotend_delivery.py"),
                    operation,
                    "--project",
                    str(self.project),
                    "--repository",
                    str(missing_repository),
                    "--apply",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertTrue(json.loads(completed.stdout)["applied"])
        state = self.manager.inspect(self.artifact)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(state["enablement"], "enabled")
        self.assert_protected_unchanged()

    def test_inspect_reports_current_state_when_repository_is_missing(self) -> None:
        self.install()
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "cotend_delivery.py"),
                "inspect",
                "--project",
                str(self.project),
                "--repository",
                str(self.temp_root / "missing-repository"),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["state"]["installation"], "complete")
        self.assertEqual(result["state"]["candidate_relation"], "none")
        self.assertEqual(
            result["candidate_diagnostic"]["error"],
            "framework_lock_invalid",
        )
        self.assert_protected_unchanged()

    def test_invalid_disabled_carrier_boundary_is_rejected(self) -> None:
        self.install()
        disabled_root = (
            self.project / ".agents" / ".cotend-delivery" / "disabled-skills"
        )
        disabled_root.write_text("not a directory\n", encoding="utf-8")
        with self.assertRaisesRegex(DeliveryError, "must be a directory"):
            self.manager.inspect(self.artifact)
        self.assert_protected_unchanged()

    def test_unowned_delivery_state_blocks_install(self) -> None:
        project = self.temp_root / "state-residue-project"
        project.mkdir()
        state_root = project / ".agents" / ".cotend-delivery"
        state_root.mkdir(parents=True)
        residue = state_root / "unknown.json"
        residue.write_text("{}\n", encoding="utf-8")
        manager = DeliveryManager(project)

        with self.assertRaisesRegex(DeliveryError, "install is blocked"):
            manager.execute("install", self.artifact, apply=True)
        self.assertEqual(residue.read_text(encoding="utf-8"), "{}\n")


if __name__ == "__main__":
    unittest.main()
