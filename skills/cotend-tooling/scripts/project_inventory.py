#!/usr/bin/env python3
"""Read-only CoTend capability-evidence inventory and reconciliation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


RESULT_CONTRACT = "cotend.project-capability-inventory-scan.v1"
CHECKPOINT_CONTRACT = "cotend.project-capability-inventory-checkpoint.v1"
REQUESTED_MODES = {"bootstrap_full", "incremental_reconcile", "forced_full"}
EXCLUDED_DIRECTORIES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "venv",
}
ALLOWED_HIDDEN_EVIDENCE_ROOTS = {".claude", ".codex", ".github", ".vscode"}
EXACT_EVIDENCE_NAMES = {
    ".mcp.json",
    ".nvmrc",
    ".python-version",
    ".tool-versions",
    "agents.md",
    "bun.lock",
    "bun.lockb",
    "cargo.lock",
    "cargo.toml",
    "composer.json",
    "composer.lock",
    "deno.json",
    "deno.lock",
    "dockerfile",
    "flake.lock",
    "flake.nix",
    "gemfile",
    "gemfile.lock",
    "go.mod",
    "go.sum",
    "justfile",
    "makefile",
    "mcp.json",
    "package-lock.json",
    "package.json",
    "pipfile",
    "pipfile.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "project-capabilities.md",
    "project-decision-log.md",
    "project-knowledge-changelog.md",
    "project-plan-tree.md",
    "pyproject.toml",
    "quality-signals.md",
    "requirements.in",
    "requirements.txt",
    "review-log.md",
    "status.md",
    "taskfile.yml",
    "taskfile.yaml",
    "tox.ini",
    "upstream-sources.md",
    "uv.lock",
    "yarn.lock",
}
SCRIPT_SUFFIXES = {".bat", ".cmd", ".js", ".mjs", ".ps1", ".py", ".rb", ".sh", ".ts"}
CONFIG_SUFFIXES = {".json", ".toml", ".yaml", ".yml"}
TOOL_SIGNAL = re.compile(
    rb"(?i)(?:\bskill\b|\bmcp\b|\bcli\b|\blibrar(?:y|ies)\b|"
    rb"\bdependenc(?:y|ies)\b|\btool(?:ing|s)?\b|\bservice\b|"
    rb"\bplugin\b|\bpackage manager\b|\xe5\xb7\xa5\xe5\x85\xb7|"
    rb"\xe4\xbe\x9d\xe8\xb5\x96|\xe6\x8a\x80\xe8\x83\xbd|\xe6\x9c\x8d\xe5\x8a\xa1)"
)
HEX_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OBJECT_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
CHECKPOINT_FIELDS = {
    "contract",
    "vcs_anchor",
    "relevant_surface_digest",
    "working_evidence_digest",
    "evidence_manifest",
    "integrity_digest",
}


class InventoryError(ValueError):
    """Fail-closed inventory input or evidence error."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InventoryError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_strict_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8", errors="strict"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InventoryError(f"cannot read strict JSON {path}: {exc}") from exc


def _safe_relative_path(value: str, *, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise InventoryError(f"{label} must be a non-empty POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value.startswith("~"):
        raise InventoryError(f"{label} escapes the project root")
    normalized = path.as_posix()
    if normalized != value or normalized == ".":
        raise InventoryError(f"{label} is not normalized: {value!r}")
    return normalized


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _manifest_digest(manifest: dict[str, str]) -> str:
    payload = b"".join(
        path.encode("utf-8") + b"\0" + manifest[path].encode("ascii") + b"\0"
        for path in sorted(manifest)
    )
    return _sha256_bytes(payload)


def _checkpoint_integrity_digest(
    *,
    anchor: str | None,
    relevant_digest: str,
    working_digest: str,
    manifest: dict[str, str],
) -> str:
    payload = json.dumps(
        {
            "contract": CHECKPOINT_CONTRACT,
            "vcs_anchor": anchor,
            "relevant_surface_digest": relevant_digest,
            "working_evidence_digest": working_digest,
            "evidence_manifest": manifest,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return _sha256_bytes(payload)


def validate_checkpoint(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InventoryError("checkpoint must be an object")
    if set(value) != CHECKPOINT_FIELDS:
        raise InventoryError(
            "checkpoint fields mismatch: "
            f"missing={sorted(CHECKPOINT_FIELDS - set(value))}, "
            f"unknown={sorted(set(value) - CHECKPOINT_FIELDS)}"
        )
    if value["contract"] != CHECKPOINT_CONTRACT:
        raise InventoryError(f"checkpoint contract must be {CHECKPOINT_CONTRACT}")
    anchor = value["vcs_anchor"]
    if anchor is not None and (
        not isinstance(anchor, str) or GIT_OBJECT_RE.fullmatch(anchor) is None
    ):
        raise InventoryError("checkpoint.vcs_anchor must be a Git object id or null")
    for field in ("relevant_surface_digest", "working_evidence_digest", "integrity_digest"):
        if not isinstance(value[field], str) or HEX_DIGEST_RE.fullmatch(value[field]) is None:
            raise InventoryError(f"checkpoint.{field} must be a SHA-256 digest")
    manifest = value["evidence_manifest"]
    if not isinstance(manifest, dict):
        raise InventoryError("checkpoint.evidence_manifest must be an object")
    for path, digest in manifest.items():
        _safe_relative_path(path, label="checkpoint evidence path")
        if not isinstance(digest, str) or HEX_DIGEST_RE.fullmatch(digest) is None:
            raise InventoryError(f"checkpoint digest is invalid for {path}")
    if value["relevant_surface_digest"] != _manifest_digest(manifest):
        raise InventoryError("checkpoint relevant digest does not match its manifest")
    expected = _checkpoint_integrity_digest(
        anchor=anchor,
        relevant_digest=value["relevant_surface_digest"],
        working_digest=value["working_evidence_digest"],
        manifest=manifest,
    )
    if value["integrity_digest"] != expected:
        raise InventoryError("checkpoint integrity digest does not match its data")
    return value


def _parts(path: str) -> tuple[str, ...]:
    return tuple(part.casefold() for part in PurePosixPath(path).parts)


def _hidden_root_allowed(parts: tuple[str, ...]) -> bool:
    return not parts or not parts[0].startswith(".") or parts[0] in ALLOWED_HIDDEN_EVIDENCE_ROOTS


def is_evidence_path(path: str) -> bool:
    """Return whether a path belongs to the bounded capability-evidence surface."""

    normalized = _safe_relative_path(path, label="evidence path")
    parts = _parts(normalized)
    if not _hidden_root_allowed(parts):
        return False
    if any(part in EXCLUDED_DIRECTORIES for part in parts[:-1]):
        return False
    name = parts[-1]
    suffix = PurePosixPath(name).suffix.casefold()
    if name in EXACT_EVIDENCE_NAMES:
        return True
    if name.startswith("requirements") and name.endswith((".in", ".txt")):
        return True
    if name.startswith(("dockerfile", "compose", "docker-compose")):
        return True
    if name.startswith(("build.gradle", "settings.gradle")):
        return True
    if name.endswith((".config.js", ".config.mjs", ".config.ts")):
        return True
    if parts[0] in {"scripts", "tools", "bin"} and suffix in SCRIPT_SUFFIXES:
        return True
    if parts[0] == "skills" and name == "skill.md" and len(parts) >= 3:
        return True
    if parts[0] == ".github" and len(parts) >= 2 and parts[1] in {"actions", "workflows"}:
        return suffix in CONFIG_SUFFIXES or suffix in SCRIPT_SUFFIXES
    if parts[0] in {".codex", ".claude", ".vscode"}:
        return suffix in CONFIG_SUFFIXES
    return False


def _native_log_candidate(path: str) -> bool:
    parts = _parts(path)
    if not parts or not _hidden_root_allowed(parts):
        return False
    name = parts[-1]
    if len(parts) >= 2 and parts[0] == "project-plan-nodes" and name.endswith(".md"):
        return True
    return name.endswith(
        (
            "review-log.md",
            "quality-signals.md",
            "collab-context.md",
            "project-decision-log.md",
            "project-knowledge-changelog.md",
        )
    )


def _contains_tool_signal(path: Path) -> bool:
    try:
        if path.stat().st_size > 5 * 1024 * 1024:
            return False
        return TOOL_SIGNAL.search(path.read_bytes()) is not None
    except OSError as exc:
        raise InventoryError(f"cannot inspect evidence candidate {path}: {exc}") from exc


def _keep_directory(name: str) -> bool:
    lowered = name.casefold()
    if lowered in EXCLUDED_DIRECTORIES:
        return False
    if lowered.startswith(".") and lowered not in ALLOWED_HIDDEN_EVIDENCE_ROOTS:
        return False
    return True


def collect_evidence_manifest(project_root: Path) -> dict[str, str]:
    root = project_root.resolve(strict=True)
    if not root.is_dir():
        raise InventoryError("project_root must be a directory")
    manifest: dict[str, str] = {}
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        directory_names[:] = sorted(
            name
            for name in directory_names
            if _keep_directory(name) and not (Path(current) / name).is_symlink()
        )
        for name in sorted(file_names):
            absolute = Path(current) / name
            if absolute.is_symlink() or not absolute.is_file():
                continue
            relative = absolute.relative_to(root).as_posix()
            selected = is_evidence_path(relative)
            if not selected and _native_log_candidate(relative):
                selected = _contains_tool_signal(absolute)
            if selected:
                try:
                    manifest[relative] = _sha256_bytes(absolute.read_bytes())
                except OSError as exc:
                    raise InventoryError(f"cannot hash evidence file {relative}: {exc}") from exc
    return dict(sorted(manifest.items()))


def _git(project_root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    environment["LC_ALL"] = "C"
    return subprocess.run(
        ["git", "-C", str(project_root), *args],
        check=False,
        capture_output=True,
        env=environment,
    )


def _git_text(project_root: Path, *args: str) -> str | None:
    result = _git(project_root, *args)
    if result.returncode != 0:
        return None
    try:
        return result.stdout.decode("utf-8", errors="strict").strip()
    except UnicodeDecodeError as exc:
        raise InventoryError(f"Git output is not UTF-8 for {' '.join(args)}") from exc


def _git_available(project_root: Path) -> bool:
    try:
        return _git_text(project_root, "rev-parse", "--is-inside-work-tree") == "true"
    except OSError:
        return False


def _git_head(project_root: Path) -> str | None:
    value = _git_text(project_root, "rev-parse", "--verify", "HEAD")
    return value if value and GIT_OBJECT_RE.fullmatch(value) else None


def _anchor_relation(project_root: Path, anchor: str | None, head: str | None) -> str:
    if anchor is None or head is None:
        return "unavailable"
    if _git(project_root, "cat-file", "-e", f"{anchor}^{{commit}}").returncode != 0:
        return "unavailable"
    if anchor == head:
        return "current"
    ancestor = _git(project_root, "merge-base", "--is-ancestor", anchor, head)
    if ancestor.returncode == 0:
        return "ancestor"
    return "conflict" if ancestor.returncode == 1 else "unavailable"


def _working_evidence_digest(project_root: Path, manifest: dict[str, str]) -> str:
    result = _git(
        project_root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--",
        ".",
    )
    if result.returncode != 0:
        raise InventoryError("cannot calculate Git working evidence")
    records: list[str] = []
    for token in result.stdout.split(b"\0"):
        if len(token) < 4 or token[2:3] != b" ":
            continue
        try:
            status = token[:2].decode("ascii", errors="strict")
            path = token[3:].decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise InventoryError("Git working path is not UTF-8") from exc
        normalized = path.replace("\\", "/")
        if normalized in manifest or is_evidence_path(normalized):
            records.append(f"{status}\0{normalized}\0{manifest.get(normalized, 'missing')}")
    return _sha256_bytes("\n".join(sorted(records)).encode("utf-8"))


def _manifest_changes(previous: dict[str, str], current: dict[str, str]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for path in sorted(previous.keys() | current.keys()):
        if path not in previous:
            status = "added"
        elif path not in current:
            status = "deleted"
        elif previous[path] != current[path]:
            status = "modified"
        else:
            continue
        result.append({"status": status, "path": path})
    return result


def _full_rebuild_delta(current: dict[str, str], previous: dict[str, str]) -> list[dict[str, str]]:
    result = [{"status": "observed", "path": path} for path in sorted(current)]
    result.extend(
        {"status": "deleted", "path": path}
        for path in sorted(previous.keys() - current.keys())
    )
    return result


def _historical_evidence_paths(project_root: Path) -> tuple[list[str], str]:
    result = _git(project_root, "log", "--all", "--format=", "--name-only", "-z", "--", ".")
    if result.returncode != 0:
        return [], "unavailable"
    paths: set[str] = set()
    for token in result.stdout.split(b"\0"):
        token = token.strip(b"\r\n")
        if not token:
            continue
        try:
            path = token.decode("utf-8", errors="strict").replace("\\", "/")
        except UnicodeDecodeError as exc:
            raise InventoryError("Git history path is not UTF-8") from exc
        try:
            if is_evidence_path(path) or _native_log_candidate(path):
                paths.add(path)
        except InventoryError:
            continue
    return sorted(paths), "available"


def _checkpoint(
    *,
    head: str | None,
    relevant_digest: str,
    working_digest: str,
    manifest: dict[str, str],
) -> dict[str, Any]:
    checkpoint = {
        "contract": CHECKPOINT_CONTRACT,
        "vcs_anchor": head,
        "relevant_surface_digest": relevant_digest,
        "working_evidence_digest": working_digest,
        "evidence_manifest": manifest,
    }
    checkpoint["integrity_digest"] = _checkpoint_integrity_digest(
        anchor=head,
        relevant_digest=relevant_digest,
        working_digest=working_digest,
        manifest=manifest,
    )
    return checkpoint


def reconcile_project(
    project_root: Path,
    *,
    requested_mode: str,
    checkpoint: dict[str, Any] | None = None,
    checkpoint_error: str | None = None,
) -> dict[str, Any]:
    if requested_mode not in REQUESTED_MODES:
        raise InventoryError(f"requested_mode is invalid: {requested_mode}")
    root = project_root.resolve(strict=True)
    if not root.is_dir():
        raise InventoryError("project_root must be a directory")

    checkpoint_value: dict[str, Any] | None = None
    invalid_checkpoint = checkpoint_error
    if checkpoint is not None and invalid_checkpoint is None:
        try:
            checkpoint_value = validate_checkpoint(checkpoint)
        except InventoryError as exc:
            invalid_checkpoint = str(exc)

    manifest = collect_evidence_manifest(root)
    relevant_digest = _manifest_digest(manifest)
    git_available = _git_available(root)
    head = _git_head(root) if git_available else None
    working_digest = (
        _working_evidence_digest(root, manifest) if git_available else relevant_digest
    )
    previous_anchor = checkpoint_value["vcs_anchor"] if checkpoint_value else None
    relation = _anchor_relation(root, previous_anchor, head) if git_available else "unavailable"

    mode = requested_mode
    strategy = "bounded_evidence_surface_full"
    reliability = "reliable"
    fallback_reason = "none"
    history_paths: list[str] = []
    history_status = "not_requested"
    previous_manifest = checkpoint_value["evidence_manifest"] if checkpoint_value else {}

    if requested_mode == "bootstrap_full":
        delta = _full_rebuild_delta(manifest, {})
        if git_available:
            history_paths, history_status = _historical_evidence_paths(root)
    elif requested_mode == "forced_full":
        delta = _full_rebuild_delta(manifest, previous_manifest)
        fallback_reason = "explicit_forced_full"
        if git_available:
            history_paths, history_status = _historical_evidence_paths(root)
    elif invalid_checkpoint is not None:
        mode = "forced_full"
        reliability = "incomplete"
        fallback_reason = "checkpoint_invalid"
        delta = _full_rebuild_delta(manifest, previous_manifest)
        if git_available:
            history_paths, history_status = _historical_evidence_paths(root)
    elif checkpoint_value is None:
        mode = "forced_full"
        reliability = "bounded_fallback"
        fallback_reason = "checkpoint_missing"
        delta = _full_rebuild_delta(manifest, {})
        if git_available:
            history_paths, history_status = _historical_evidence_paths(root)
    elif git_available and relation in {"current", "ancestor"}:
        strategy = "git_anchor_and_evidence_digest_delta"
        delta = _manifest_changes(previous_manifest, manifest)
    elif not git_available and previous_anchor is None:
        if (
            checkpoint_value["relevant_surface_digest"] == relevant_digest
            and checkpoint_value["working_evidence_digest"] == working_digest
        ):
            strategy = "non_git_digest_unchanged"
            delta = []
        else:
            strategy = "non_git_bounded_evidence_rebuild"
            reliability = "bounded_fallback"
            fallback_reason = "non_git_digest_changed"
            delta = _manifest_changes(previous_manifest, manifest)
    else:
        mode = "forced_full"
        reliability = "bounded_fallback"
        fallback_reason = (
            f"git_anchor_{relation}" if git_available else "git_anchor_unavailable"
        )
        delta = _full_rebuild_delta(manifest, previous_manifest)
        if git_available:
            history_paths, history_status = _historical_evidence_paths(root)

    if history_status == "unavailable":
        reliability = "incomplete"
    reconcile_paths = sorted({change["path"] for change in delta})
    historical_only = sorted(set(history_paths) - set(manifest))
    return {
        "contract": RESULT_CONTRACT,
        "requested_mode": requested_mode,
        "mode": mode,
        "strategy": strategy,
        "inventory_initialized": True,
        "reliability": reliability,
        "fallback_reason": fallback_reason,
        "checkpoint_error": invalid_checkpoint or "none",
        "vcs": {
            "available": git_available,
            "previous_anchor": previous_anchor,
            "current_head": head,
            "anchor_relation": relation,
        },
        "relevant_surface_digest": relevant_digest,
        "working_evidence_digest": working_digest,
        "current_evidence_count": len(manifest),
        "delta_count": len(delta),
        "delta": delta,
        "reconcile_paths": reconcile_paths,
        "historical_evidence_paths": historical_only,
        "history_status": history_status,
        "new_checkpoint": _checkpoint(
            head=head,
            relevant_digest=relevant_digest,
            working_digest=working_digest,
            manifest=manifest,
        ),
        "semantic_inferences": [],
        "writes_performed": False,
        "network_calls": 0,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory bounded CoTend capability evidence without writes."
    )
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--mode", choices=sorted(REQUESTED_MODES), required=True)
    parser.add_argument("--checkpoint", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    checkpoint: dict[str, Any] | None = None
    checkpoint_error: str | None = None
    if args.checkpoint is not None:
        try:
            value = read_strict_json(args.checkpoint)
            checkpoint = value if isinstance(value, dict) else None
            if checkpoint is None:
                checkpoint_error = "checkpoint must be an object"
        except InventoryError as exc:
            checkpoint_error = str(exc)
    try:
        result = reconcile_project(
            args.project_root,
            requested_mode=args.mode,
            checkpoint=checkpoint,
            checkpoint_error=checkpoint_error,
        )
    except (InventoryError, OSError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
