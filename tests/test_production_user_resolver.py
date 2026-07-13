from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cotend_delivery import (  # noqa: E402
    DeliveryError,
    inspect_production_user_layout,
    resolve_production_user_layout,
)
from cotend_delivery.production_cli import main as production_cli_main  # noqa: E402


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


class ProductionUserResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.isolation = Path(self.temp.name)
        self.home = self.isolation / "private-user-name"
        self.codex_home = self.isolation / "codex-home"
        self.home.mkdir()
        self.codex_home.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def layout(self, *, codex_home: Path | None = None):
        return resolve_production_user_layout(
            home=self.home,
            codex_home=codex_home or self.codex_home,
        )

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = production_cli_main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_resolves_official_roots_and_home_owned_state(self) -> None:
        layout = self.layout()
        self.assertEqual(layout.canonical_root, self.home / ".agents" / "skills")
        self.assertEqual(layout.compatibility_root, self.codex_home / "skills")
        self.assertEqual(
            layout.state_root,
            self.home / ".agents" / ".cotend-delivery",
        )
        self.assertFalse(layout.state_root.is_relative_to(self.codex_home))

    def test_same_home_multiple_codex_home_shares_installation_identity(self) -> None:
        first = self.layout()
        second = self.layout(codex_home=self.isolation / "other-codex-home")
        self.assertEqual(first.state_root, second.state_root)
        self.assertEqual(first.installation_id, second.installation_id)
        self.assertNotEqual(first.layout_fingerprint, second.layout_fingerprint)
        before = tree_snapshot(self.isolation)
        changed = inspect_production_user_layout(
            second,
            expected_layout_fingerprint=first.layout_fingerprint,
        )
        self.assertEqual(changed["layout_context"]["status"], "changed")
        self.assertIn("layout_context_changed", changed["blockers"])
        self.assertEqual(
            changed["migration_status"],
            "explicit_layout_context_migration_required",
        )
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_identity_does_not_expose_user_or_absolute_path(self) -> None:
        layout = self.layout()
        identities = f"{layout.installation_id} {layout.layout_fingerprint}"
        self.assertNotIn("private-user-name", identities)
        self.assertNotIn(str(self.home), identities)
        self.assertRegex(layout.installation_id, r"^cotend-user-[0-9a-f]{24}$")
        self.assertRegex(layout.layout_fingerprint, r"^cotend-layout-[0-9a-f]{24}$")

    def test_environment_codex_home_is_used_when_not_injected(self) -> None:
        selected = self.isolation / "environment-codex-home"
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(selected)}):
            layout = resolve_production_user_layout(home=self.home)
        self.assertEqual(layout.codex_home, selected)

    def test_relative_empty_and_overlapping_roots_are_rejected(self) -> None:
        with self.assertRaisesRegex(DeliveryError, "absolute path"):
            resolve_production_user_layout(home=Path("relative-home"))
        with self.assertRaisesRegex(DeliveryError, "cannot be empty"):
            resolve_production_user_layout(home=self.home, codex_home="")
        with self.assertRaisesRegex(DeliveryError, "overlaps"):
            resolve_production_user_layout(
                home=self.home,
                codex_home=self.home / ".agents",
            )
        with self.assertRaisesRegex(DeliveryError, "fingerprint is invalid"):
            inspect_production_user_layout(
                self.layout(),
                expected_layout_fingerprint="not-a-layout-fingerprint",
            )
        (self.home / ".agents").write_text("not a directory\n", encoding="utf-8")
        with self.assertRaisesRegex(DeliveryError, "must identify a directory"):
            self.layout()

    def test_linked_codex_home_is_rejected(self) -> None:
        target = self.isolation / "linked-target"
        target.mkdir()
        linked = self.isolation / "linked-codex-home"
        if not create_directory_link(linked, target):
            self.skipTest("directory link unavailable")
        with self.assertRaisesRegex(DeliveryError, "link or junction"):
            resolve_production_user_layout(home=self.home, codex_home=linked)

    def test_resolve_and_absent_inspection_are_zero_write(self) -> None:
        before = tree_snapshot(self.isolation)
        layout = self.layout()
        result = inspect_production_user_layout(layout)
        self.assertEqual(result["state"]["status"], "absent")
        self.assertEqual(result["migration_status"], "none")
        self.assertEqual(result["blockers"], [])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_cli_dry_run_is_structured_and_zero_write(self) -> None:
        expected_fingerprint = self.layout().layout_fingerprint
        before = tree_snapshot(self.isolation)
        code, stdout, stderr = self.run_cli(
            "install",
            "--home",
            str(self.home),
            "--codex-home",
            str(self.codex_home),
            "--expected-layout-fingerprint",
            expected_fingerprint,
        )
        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        result = json.loads(stdout)
        self.assertEqual(result["status"], "preview")
        self.assertEqual(result["operation"], "install")
        self.assertEqual(result["layout_context"]["status"], "current")
        self.assertFalse(result["production_apply"]["available"])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_cli_apply_rejects_before_path_resolution_and_zero_write(self) -> None:
        before = tree_snapshot(self.isolation)
        code, stdout, stderr = self.run_cli(
            "install",
            "--home",
            str(self.isolation / "missing-home"),
            "--apply",
        )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(json.loads(stderr)["error"], "production_apply_forbidden")
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_schema_v3_receipt_requires_explicit_migration(self) -> None:
        layout = self.layout()
        layout.state_root.mkdir(parents=True)
        (layout.state_root / "receipt.json").write_text(
            json.dumps(
                {
                    "schema": "cotend.delivery-receipt",
                    "schema_version": 3,
                    "scope": "user",
                }
            ),
            encoding="utf-8",
        )
        before = tree_snapshot(self.isolation)
        result = inspect_production_user_layout(layout)
        self.assertEqual(
            result["migration_status"],
            "explicit_receipt_migration_required",
        )
        self.assertIn("explicit_receipt_migration_required", result["blockers"])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_unknown_state_blocks_without_cleanup(self) -> None:
        layout = self.layout()
        layout.state_root.mkdir(parents=True)
        (layout.state_root / "receipt.json").write_text("not-json\n", encoding="utf-8")
        (layout.state_root / "unknown.bin").write_bytes(b"keep")
        before = tree_snapshot(self.isolation)
        result = inspect_production_user_layout(layout)
        self.assertEqual(result["migration_status"], "blocked_unknown_state")
        self.assertIn("unknown_state", result["blockers"])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_first_party_compatibility_residue_requires_migration(self) -> None:
        layout = self.layout()
        residue = layout.compatibility_root / "cotend-init"
        residue.mkdir(parents=True)
        (residue / "SKILL.md").write_text("existing\n", encoding="utf-8")
        before = tree_snapshot(self.isolation)
        result = inspect_production_user_layout(layout)
        self.assertEqual(
            result["migration_status"],
            "explicit_first_party_migration_required",
        )
        self.assertIn("first_party_compatibility_residue", result["blockers"])
        self.assertEqual(tree_snapshot(self.isolation), before)

    def test_unowned_canonical_residue_requires_migration(self) -> None:
        layout = self.layout()
        residue = layout.canonical_root / "cotend-init"
        residue.mkdir(parents=True)
        before = tree_snapshot(self.isolation)
        result = inspect_production_user_layout(layout)
        self.assertIn("first_party_canonical_residue", result["blockers"])
        self.assertEqual(tree_snapshot(self.isolation), before)


if __name__ == "__main__":
    unittest.main()
