from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
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
    IsolatedUserSkillDeliveryManager,
)


FIRST_PARTY = (
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-init",
    "cotend-model-upgrade",
    "cotend-project-init",
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


def create_directory_link(link: Path, target: Path) -> bool:
    try:
        link.symlink_to(target, target_is_directory=True)
        return True
    except OSError:
        if os.name != "nt":
            return False
    created = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    return created.returncode == 0


class IsolatedUserSkillDeliveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.isolation = Path(self.temp.name)
        self.home = self.isolation / "home"
        self.codex_home = self.isolation / "codex-home"
        self.home.mkdir()
        self.codex_home.mkdir()
        self.state_root = self.isolation / "delivery-state"
        self.artifact = Artifact.from_repository(ROOT)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @property
    def canonical(self) -> Path:
        return self.home / ".agents" / "skills"

    @property
    def compatibility(self) -> Path:
        return self.codex_home / "skills"

    def manager(self, artifact: Artifact | None = None) -> IsolatedUserSkillDeliveryManager:
        return IsolatedUserSkillDeliveryManager(
            artifact or self.artifact,
            isolation_root=self.isolation,
            home=self.home,
            codex_home=self.codex_home,
            state_root=self.state_root,
        )

    def add_external(
        self,
        skill: str,
        *,
        root: str = "compatibility",
        portable_newlines: bool = False,
    ) -> Path:
        destination_root = self.compatibility if root == "compatibility" else self.canonical
        destination = destination_root / skill
        shutil.copytree(self.artifact.root / skill, destination)
        if portable_newlines:
            entry = destination / "SKILL.md"
            data = entry.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            entry.write_bytes(b"\xef\xbb\xbf" + data)
        return destination

    def updated_artifact(self, *, change_companion: bool = False) -> Artifact:
        source = self.isolation / (
            "artifact-companion-v2" if change_companion else "artifact-v2"
        )
        shutil.copytree(self.artifact.root, source)
        skill = "grill-me" if change_companion else "cotend-init"
        entry = source / skill / "SKILL.md"
        entry.write_text(
            entry.read_text(encoding="utf-8") + "\n<!-- isolated-user-v2 -->\n",
            encoding="utf-8",
        )
        return Artifact.from_directory(
            source,
            source_release_id=self.artifact.source_release_id,
            artifact_id="cotend-codex-r000002",
            revision=2,
            protocol=self.artifact.protocol,
        )

    def receipt(self, manager: IsolatedUserSkillDeliveryManager) -> dict[str, object]:
        return json.loads(manager.receipt_path.read_text(encoding="utf-8"))

    def test_absent_companions_are_owned_through_full_lifecycle(self) -> None:
        manager = self.manager()
        before = tree_snapshot(self.isolation)
        preview = manager.execute("install")
        self.assertEqual(preview["status"], "planned")
        self.assertEqual(tree_snapshot(self.isolation), before)

        installed = manager.execute("install", apply=True)
        self.assertEqual(installed["state_after"]["installation"], "complete")
        receipt = self.receipt(manager)
        self.assertEqual(receipt["schema_version"], 3)
        self.assertEqual(receipt["scope"], "user")
        self.assertEqual(receipt["owned_skills"], list(self.artifact.skills))

        manager.execute("disable", apply=True)
        self.assertFalse(any((self.canonical / skill).exists() for skill in self.artifact.skills))
        manager.execute("enable", apply=True)
        manager.execute("uninstall", apply=True)
        self.assertFalse(any((self.canonical / skill).exists() for skill in self.artifact.skills))

    def test_compatible_existing_companions_are_external_and_preserved(self) -> None:
        for skill in COMPANIONS:
            self.add_external(skill)
        external_before = tree_snapshot(self.compatibility)
        manager = self.manager()

        installed = manager.execute("install", apply=True)
        self.assertEqual(installed["state_after"]["managed_skills"], list(FIRST_PARTY))
        receipt = self.receipt(manager)
        self.assertEqual(receipt["owned_skills"], list(FIRST_PARTY))
        for skill in COMPANIONS:
            self.assertEqual(
                receipt["components"][skill]["disposition"],
                "external_shared",
            )

        manager.execute("disable", apply=True)
        manager.execute("enable", apply=True)
        updated = self.updated_artifact()
        manager.execute("update", updated, apply=True)
        manager.execute("rollback", updated, apply=True)
        manager.execute("uninstall", apply=True)
        self.assertEqual(tree_snapshot(self.compatibility), external_before)

        restored = manager.execute("rollback", apply=True)
        self.assertEqual(restored["state_after"]["installation"], "complete")
        self.assertEqual(tree_snapshot(self.compatibility), external_before)

    def test_mixed_owned_and_external_companions_are_recorded_per_component(self) -> None:
        self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        receipt = self.receipt(manager)
        self.assertEqual(receipt["components"]["grill-me"]["disposition"], "external_shared")
        self.assertEqual(receipt["components"]["karpathy-guidelines"]["disposition"], "owned")
        self.assertIn("karpathy-guidelines", receipt["owned_skills"])

        manager.execute("uninstall", apply=True)
        self.assertTrue((self.compatibility / "grill-me" / "SKILL.md").is_file())
        self.assertFalse((self.canonical / "karpathy-guidelines").exists())

    def test_portable_bom_and_crlf_companion_is_compatible(self) -> None:
        self.add_external("grill-me", portable_newlines=True)
        manager = self.manager()
        state = manager.inspect()
        self.assertEqual(
            state["components"]["grill-me"]["disposition"],
            "external_shared",
        )
        manager.execute("install", apply=True)
        self.assertFalse((self.canonical / "grill-me").exists())

    def test_compatible_duplicate_warns_without_creating_third_copy(self) -> None:
        self.add_external("grill-me", root="canonical")
        self.add_external("grill-me", root="compatibility")
        manager = self.manager()
        preview = manager.inspect()
        self.assertIn("compatible_duplicate:grill-me", preview["warnings"])
        manager.execute("install", apply=True)
        self.assertEqual(
            self.receipt(manager)["components"]["grill-me"]["observed_roots"],
            ["canonical", "compatibility"],
        )
        manager.execute("uninstall", apply=True)
        self.assertTrue((self.canonical / "grill-me" / "SKILL.md").is_file())
        self.assertTrue((self.compatibility / "grill-me" / "SKILL.md").is_file())

    def test_incompatible_companion_blocks_before_any_write(self) -> None:
        external = self.add_external("grill-me")
        (external / "SKILL.md").write_text("incompatible\n", encoding="utf-8")
        before = tree_snapshot(self.isolation)
        manager = self.manager()
        state = manager.inspect()
        self.assertIn("companion_content_incompatible", state["diagnostics"])
        with self.assertRaisesRegex(DeliveryError, "install is blocked"):
            manager.execute("install", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_extra_companion_file_blocks_before_any_write(self) -> None:
        external = self.add_external("grill-me")
        (external / "extra.txt").write_text("unexpected\n", encoding="utf-8")
        before = tree_snapshot(self.isolation)
        manager = self.manager()
        self.assertIn("companion_inventory_incompatible", manager.inspect()["diagnostics"])
        with self.assertRaises(DeliveryError):
            manager.execute("install", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_first_party_collision_in_compatibility_root_blocks(self) -> None:
        collision = self.compatibility / "cotend-init"
        shutil.copytree(self.artifact.root / "cotend-init", collision)
        before = tree_snapshot(self.isolation)
        manager = self.manager()
        self.assertIn("unowned_collision", manager.inspect()["diagnostics"])
        with self.assertRaises(DeliveryError):
            manager.execute("install", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_external_shared_disappearance_blocks_mutation_without_takeover(self) -> None:
        external = self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        shutil.rmtree(external)
        before = tree_snapshot(self.isolation)
        state = manager.inspect()
        self.assertIn("external_shared_missing:grill-me", state["unexpected"])
        with self.assertRaisesRegex(DeliveryError, "uninstall is blocked"):
            manager.execute("uninstall", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)
        self.assertTrue((self.canonical / "cotend-init" / "SKILL.md").is_file())

    def test_external_shared_candidate_version_drift_blocks_update(self) -> None:
        self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        changed = self.updated_artifact(change_companion=True)
        before = tree_snapshot(self.isolation)
        state = manager.inspect(changed)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(state["transition"], "stable")
        self.assertEqual(state["candidate_relation"], "incompatible")
        self.assertIn(
            "external_shared_candidate_incompatible:grill-me",
            state["diagnostics"],
        )
        with self.assertRaises(DeliveryError):
            manager.execute("update", changed, apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_failed_repair_rolls_back_owned_payload_and_preserves_external(self) -> None:
        self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        owned = self.canonical / "cotend-init" / "SKILL.md"
        owned.write_text("damaged\n", encoding="utf-8")
        before = tree_snapshot(self.isolation)
        external_before = tree_snapshot(self.compatibility)

        with mock.patch.object(
            manager,
            "_write_receipt",
            side_effect=OSError("injected receipt failure"),
        ):
            with self.assertRaisesRegex(DeliveryError, "prior checkpoint was restored"):
                manager.execute("repair", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)
        self.assertEqual(tree_snapshot(self.compatibility), external_before)

    def test_mutation_lock_blocks_second_user_scope_writer(self) -> None:
        self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        external_before = tree_snapshot(self.compatibility)
        lease = manager._acquire_mutation_lock("update")
        try:
            contender = self.manager()
            state = contender.inspect()
            self.assertTrue(state["mutation_lock"]["present"])
            with self.assertRaisesRegex(DeliveryError, "update is blocked"):
                contender.execute("update", self.updated_artifact(), apply=True)
            self.assertEqual(tree_snapshot(self.compatibility), external_before)
        finally:
            manager._release_mutation_lock(lease)

    def test_recovery_restores_interrupted_user_update_without_touching_external(self) -> None:
        self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        baseline_receipt = self.receipt(manager)
        external_before = tree_snapshot(self.compatibility)
        updated = self.updated_artifact()

        lease = manager._acquire_mutation_lock("update")
        manager._update_mutation_phase(lease, "checkpointing")
        manager._create_checkpoint("update")
        manager._update_mutation_phase(lease, "mutating")
        manager._replace_with_artifact(updated, enabled=True)
        metadata = json.loads(manager.mutation_owner_path.read_text(encoding="utf-8"))
        metadata.update({"process_id": 2_147_483_647, "phase": "mutating"})
        manager.mutation_owner_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        recovery_manager = self.manager(updated)
        preview = recovery_manager.execute("recover")
        plan_id = preview["plan"]["recovery"]["recovery_plan_id"]
        recovered = recovery_manager.execute(
            "recover",
            apply=True,
            confirm_recovery_plan_id=plan_id,
        )
        self.assertEqual(recovered["branch"], "rollback_interrupted_transition")
        self.assertEqual(self.receipt(recovery_manager), baseline_receipt)
        self.assertEqual(tree_snapshot(self.compatibility), external_before)
        self.assertFalse(recovery_manager.mutation_lock_path.exists())
        self.assertFalse(recovery_manager.recovery_lock_path.exists())

    def test_recovery_blocks_external_drift_before_owned_payload_write(self) -> None:
        external = self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        updated = self.updated_artifact()

        lease = manager._acquire_mutation_lock("update")
        manager._update_mutation_phase(lease, "checkpointing")
        manager._create_checkpoint("update")
        manager._update_mutation_phase(lease, "mutating")
        manager._replace_with_artifact(updated, enabled=True)
        metadata = json.loads(manager.mutation_owner_path.read_text(encoding="utf-8"))
        metadata.update({"process_id": 2_147_483_647, "phase": "mutating"})
        manager.mutation_owner_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (external / "SKILL.md").write_text("external drift\n", encoding="utf-8")
        before = tree_snapshot(self.isolation)

        recovery_manager = self.manager(updated)
        preview = recovery_manager.plan("recover")
        self.assertFalse(preview["allowed"])
        self.assertEqual(preview["reason"], "external_shared_state_changed")
        with self.assertRaisesRegex(DeliveryError, "recover is blocked"):
            recovery_manager.execute("recover", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_user_receipt_ownership_tamper_is_rejected(self) -> None:
        self.add_external("grill-me")
        manager = self.manager()
        manager.execute("install", apply=True)
        receipt = self.receipt(manager)
        receipt["owned_skills"].append("grill-me")
        manager.receipt_path.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        state = manager.inspect()
        self.assertFalse(state["receipt_valid"])
        self.assertIn("receipt_invalid", state["diagnostics"])

    def test_layout_rejects_escape_and_live_home(self) -> None:
        with self.assertRaisesRegex(DeliveryError, "outside the explicit isolation root"):
            IsolatedUserSkillDeliveryManager(
                self.artifact,
                isolation_root=self.isolation,
                home=self.home,
                codex_home=self.codex_home,
                state_root=self.isolation.parent / "escaped-state",
            )
        with self.assertRaisesRegex(DeliveryError, "isolated user roots only"):
            IsolatedUserSkillDeliveryManager(
                self.artifact,
                isolation_root=self.isolation,
                home=Path.home(),
                codex_home=self.codex_home,
                state_root=self.state_root,
            )

    def test_layout_rejects_state_and_skill_root_overlap(self) -> None:
        before = tree_snapshot(self.isolation)
        with self.assertRaisesRegex(DeliveryError, "Delivery state overlaps"):
            IsolatedUserSkillDeliveryManager(
                self.artifact,
                isolation_root=self.isolation,
                home=self.home,
                codex_home=self.codex_home,
                state_root=self.canonical,
            )
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_layout_rejects_linked_user_root(self) -> None:
        target = self.isolation / "linked-home-target"
        target.mkdir()
        linked_home = self.isolation / "linked-home"
        if not create_directory_link(linked_home, target):
            self.skipTest("directory link unavailable")
        with self.assertRaisesRegex(DeliveryError, "roots cannot be links"):
            IsolatedUserSkillDeliveryManager(
                self.artifact,
                isolation_root=self.isolation,
                home=linked_home,
                codex_home=self.codex_home,
                state_root=self.state_root,
            )

    def test_linked_companion_is_rejected_when_platform_allows_link_creation(self) -> None:
        self.compatibility.mkdir(parents=True)
        link = self.compatibility / "grill-me"
        if not create_directory_link(link, self.artifact.root / "grill-me"):
            self.skipTest("directory link unavailable")
        before = tree_snapshot(self.isolation)
        manager = self.manager()
        self.assertIn("symlink_boundary", manager.inspect()["diagnostics"])
        with self.assertRaises(DeliveryError):
            manager.execute("install", apply=True)
        self.assertEqual(tree_snapshot(self.isolation), before)


if __name__ == "__main__":
    unittest.main()
