from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def stat_only_snapshot(root: Path) -> tuple[tuple[str, str, int, int, int], ...]:
    records: list[tuple[str, str, int, int, int]] = []

    def visit(path: Path, relative: str) -> None:
        try:
            stat = path.lstat()
        except FileNotFoundError:
            records.append((relative, "missing", 0, 0, 0))
            return
        except OSError as exc:
            records.append((relative, f"error:{exc.errno}", 0, 0, 0))
            return
        is_junction = getattr(path, "is_junction", lambda: False)
        if path.is_symlink() or is_junction():
            kind = "link"
        elif path.is_dir():
            kind = "directory"
        elif path.is_file():
            kind = "file"
        else:
            kind = "special"
        records.append((relative, kind, stat.st_mode, stat.st_size, stat.st_mtime_ns))
        if kind != "directory":
            return
        try:
            entries = sorted(os.scandir(path), key=lambda entry: entry.name)
        except OSError as exc:
            records.append((f"{relative}/<scan>", f"error:{exc.errno}", 0, 0, 0))
            return
        for entry in entries:
            child_relative = f"{relative}/{entry.name}" if relative else entry.name
            visit(Path(entry.path), child_relative)

    visit(root, ".")
    return tuple(records)


def protected_boundaries() -> dict[str, Path]:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    return {
        "canonical_user_skills": home / ".agents" / "skills",
        "compatibility_user_skills": codex_home / "skills",
        "codex_config": codex_home / "config.toml",
        "codex_auth": codex_home / "auth.json",
        "plugin_cache": codex_home / "plugins" / "cache",
        "personal_marketplace": home / ".agents" / "plugins" / "marketplace.json",
    }


def main() -> int:
    boundaries = protected_boundaries()
    before = {label: stat_only_snapshot(path) for label, path in boundaries.items()}

    suite = unittest.defaultTestLoader.loadTestsFromName(
        "tests.test_user_skill_delivery"
    )
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        return 1

    after = {label: stat_only_snapshot(path) for label, path in boundaries.items()}
    changed = sorted(label for label in boundaries if before[label] != after[label])
    if changed:
        print(f"USER_SKILL_DELIVERY_BOUNDARY_CHANGED labels={','.join(changed)}")
        return 2

    print(
        "USER_SKILL_DELIVERY_OK "
        f"tests={result.testsRun} skipped={len(result.skipped)} "
        f"protected_boundaries={len(boundaries)} unchanged=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
