#!/usr/bin/env python3
"""Read-only governance-language pre-handback validator.

This helper validates persisted state and actual changed file bytes. It never
resolves language, writes project files, repairs prose, or trusts model
self-report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


CONTRACT = "cotend.governance-language-pre-handback.v1"
RESOLUTION_CONTRACT = "cotend.user-facing-language-resolution.v1"
PARENT_RE = re.compile(
    r"^(?P<indent> *)user_facing_language_resolution\s*:\s*(?:#.*)?$"
)
CHILD_RE = re.compile(r"^(?P<indent> +)(?P<key>[A-Za-z0-9_]+)\s*:\s*(?P<value>.*?)\s*$")
TAG_RE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
ALIASES = {
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh-hans": "zh-CN",
    "中文": "zh-CN",
    "简体中文": "zh-CN",
    "zh-tw": "zh-TW",
    "繁體中文": "zh-TW",
    "繁体中文": "zh-TW",
    "en": "en",
    "english": "en",
    "英文": "en",
    "英语": "en",
}
GOVERNANCE_BASENAMES = {
    "AGENTS.md",
    "COLLAB-CONTEXT.md",
    "COLLAB-HANDOFF.md",
    "COLLAB-TASK-INDEX.md",
    "PROJECT-DECISION-LOG.md",
    "PROJECT-KNOWLEDGE-CHANGELOG.md",
    "PROJECT-PLAN-TREE.md",
    "QUALITY-SIGNALS.md",
    "REVIEW-LOG.md",
    "STATUS.md",
}
GOVERNANCE_DIRS = {
    "PROJECT-PLAN-NODES",
    "PROJECT-UNDERSTANDING",
}
ALLOWED_BODY_RESULTS = {"match", "mismatch", "technical_only", "unchecked"}
ALLOWED_PROSE_RESULTS = {"present", "absent"}
ALLOWED_EVALUATION_SCOPES = {
    "whole_file_no_git",
    "whole_file_outside_git_root",
    "git_untracked_whole_file",
    "git_unborn_whole_file",
    "whole_file_no_git_delta",
    "git_added_lines",
    "git_added_lines_unavailable",
}


def normalize_tag(raw: str) -> str:
    value = raw.strip().replace("_", "-")
    alias = ALIASES.get(value.casefold())
    if alias:
        return alias
    if not TAG_RE.fullmatch(value):
        raise ValueError(f"invalid language tag: {raw!r}")
    parts = value.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif (len(part) == 2 and part.isalpha()) or (
            len(part) == 3 and part.isdigit()
        ):
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def canonical_root(raw: str) -> Path:
    try:
        root = Path(raw).expanduser().resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError("project_root_unresolvable") from exc
    if not root.is_dir():
        raise ValueError("project_root_missing_or_not_directory")
    return root


def resolve_inside(root: Path, raw: str) -> Path:
    try:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        resolved = candidate.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError(f"path_unresolvable:{raw}") from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path_outside_project_root:{raw}") from exc
    return resolved


def relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def is_governance_path(path: str, status_carrier: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    if normalized == status_carrier:
        return True
    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return False
    basename = parts[-1]
    if basename in GOVERNANCE_BASENAMES:
        return True
    if basename.startswith("COLLAB-") and basename.endswith((".md", ".txt")):
        return True
    return any(part in GOVERNANCE_DIRS for part in parts[:-1]) and basename.endswith(
        (".md", ".txt")
    )


def run_git_paths(root: Path) -> tuple[bool, set[str], str | None]:
    try:
        probe = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            check=False,
        )
    except OSError:
        return False, set(), None
    if probe.returncode != 0 or probe.stdout.strip() != b"true":
        return False, set(), None

    paths: set[str] = set()
    commands = (
        [
            "git",
            "-C",
            str(root),
            "diff",
            "--relative",
            "--name-only",
            "-z",
            "--",
            ".",
        ],
        [
            "git",
            "-C",
            str(root),
            "diff",
            "--cached",
            "--relative",
            "--name-only",
            "-z",
            "--",
            ".",
        ],
        [
            "git",
            "-C",
            str(root),
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            ".",
        ],
    )
    for command in commands:
        try:
            result = subprocess.run(command, capture_output=True, check=False)
        except OSError:
            return True, set(), "vcs_changed_set_unavailable"
        if result.returncode != 0:
            return True, set(), "vcs_changed_set_unavailable"
        for raw_path in result.stdout.split(b"\0"):
            if raw_path:
                paths.add(os.fsdecode(raw_path).replace("\\", "/"))
    return True, paths, None


def parse_resolution(text: str) -> tuple[int, dict[str, str], list[str]]:
    lines = text.splitlines()
    matches: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = PARENT_RE.fullmatch(line)
        if match:
            matches.append((index, len(match.group("indent"))))

    if len(matches) != 1:
        return len(matches), {}, []

    start, parent_indent = matches[0]
    block_rows: list[tuple[int, str]] = []
    child_rows: list[tuple[int, str, str]] = []
    for line in lines[start + 1 :]:
        if not line.strip():
            continue
        leading = len(line) - len(line.lstrip(" "))
        if leading <= parent_indent:
            break
        block_rows.append((leading, line))
        child = CHILD_RE.fullmatch(line)
        if child:
            child_rows.append(
                (leading, child.group("key"), child.group("value").strip())
            )

    if not block_rows:
        return 1, {}, []

    # Only direct children of the canonical parent count. Without this boundary,
    # a nested wrapper could smuggle contract/status/tag fields into an invalid
    # shape while still satisfying a line-oriented parser.
    direct_indent = min(row[0] for row in block_rows)
    values: dict[str, str] = {}
    duplicate_keys: list[str] = []
    for leading, key, value in child_rows:
        if leading != direct_indent:
            continue
        if key in values:
            duplicate_keys.append(key)
        else:
            values[key] = value.strip("\"'")
    return 1, values, sorted(set(duplicate_keys))


def read_utf8(path: Path) -> tuple[bytes | None, str | None, str | None]:
    try:
        data = path.read_bytes()
    except OSError:
        return None, None, "unreadable_bytes"
    try:
        return data, data.decode("utf-8"), None
    except UnicodeDecodeError:
        return data, None, "invalid_utf8"


def invoke_checker(
    checker: Path,
    *,
    root: Path,
    normalized_tag: str,
    path: Path,
    expected_sha256: str,
    expected_byte_count: int,
) -> tuple[dict[str, Any] | None, str | None]:
    command = (
        [sys.executable, str(checker)]
        if checker.suffix.casefold() == ".py"
        else [str(checker)]
    )
    command.extend(["--normalized-tag", normalized_tag, "--path", str(path)])
    try:
        result = subprocess.run(
            command,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return None, "adapter_checker_timeout"
    except (OSError, UnicodeError):
        return None, "adapter_checker_failed"
    if result.returncode != 0:
        return None, "adapter_checker_failed"
    try:
        payload = json.loads(result.stdout)
    except (json.JSONDecodeError, TypeError):
        return None, "adapter_checker_invalid_json"
    if not isinstance(payload, dict):
        return None, "adapter_checker_invalid_json"
    try:
        reported_raw = str(payload["path"])
        reported_candidate = Path(reported_raw).expanduser()
        if not reported_candidate.is_absolute():
            reported_candidate = root / reported_candidate
        reported_path = reported_candidate.resolve()
    except (KeyError, OSError, RuntimeError, ValueError):
        return None, "adapter_checker_path_missing_or_invalid"
    if reported_path != path.resolve():
        return None, "adapter_checker_path_mismatch"
    if payload.get("normalized_tag") != normalized_tag:
        return None, "adapter_checker_tag_mismatch"
    if payload.get("actual_bytes_checked") is not True:
        return None, "adapter_checker_did_not_check_bytes"
    if payload.get("sha256") != expected_sha256:
        return None, "adapter_checker_sha256_mismatch"
    if not isinstance(payload.get("checker"), str) or not payload["checker"].strip():
        return None, "adapter_checker_identity_missing"
    if payload.get("body_result") not in ALLOWED_BODY_RESULTS:
        return None, "adapter_checker_body_result_invalid"
    if payload.get("user_visible_prose") not in ALLOWED_PROSE_RESULTS:
        return None, "adapter_checker_prose_result_invalid"
    if (
        payload["body_result"] == "technical_only"
        and payload["user_visible_prose"] != "absent"
    ) or (
        payload["body_result"] != "technical_only"
        and payload["user_visible_prose"] != "present"
    ):
        return None, "adapter_checker_body_prose_inconsistent"

    scope_fields = {
        "evaluation_scope",
        "git_added_line_count",
        "whole_file_sha256_checked",
        "whole_file_byte_count",
        "evaluated_text_byte_count",
    }
    if scope_fields.intersection(payload):
        if not scope_fields.issubset(payload):
            return None, "adapter_checker_scope_evidence_incomplete"
        if payload["evaluation_scope"] not in ALLOWED_EVALUATION_SCOPES:
            return None, "adapter_checker_evaluation_scope_invalid"
        if payload["whole_file_sha256_checked"] is not True:
            return None, "adapter_checker_whole_file_hash_unchecked"
        whole_file_bytes = payload["whole_file_byte_count"]
        if (
            not isinstance(whole_file_bytes, int)
            or isinstance(whole_file_bytes, bool)
            or whole_file_bytes != expected_byte_count
        ):
            return None, "adapter_checker_whole_file_byte_count_mismatch"
        evaluated_bytes = payload["evaluated_text_byte_count"]
        if not isinstance(evaluated_bytes, int) or isinstance(evaluated_bytes, bool):
            return None, "adapter_checker_evaluated_byte_count_invalid"
        if evaluated_bytes < 0 or evaluated_bytes > expected_byte_count:
            return None, "adapter_checker_evaluated_byte_count_invalid"
        added_count = payload["git_added_line_count"]
        if added_count is not None and (
            not isinstance(added_count, int)
            or isinstance(added_count, bool)
            or added_count < 0
        ):
            return None, "adapter_checker_added_line_count_invalid"
        if payload["evaluation_scope"] == "git_added_lines" and added_count is None:
            return None, "adapter_checker_added_line_count_missing"
    return payload, None


def base_packet() -> dict[str, Any]:
    return {
        "contract": CONTRACT,
        "result": "blocked",
        "canonical_resolution": {
            "pointer": None,
            "parent_count": None,
            "contract": None,
            "status": None,
            "normalized_tag": None,
            "expected_normalized_tag": None,
        },
        "changed_file_set": {
            "source": None,
            "vcs_available": False,
            "write_receipts": [],
            "files": [],
        },
        "files": [],
        "reasons": [],
        "repair": {
            "permitted": False,
            "max_same_turn_repairs": 1,
            "max_same_turn_rechecks": 1,
        },
    }


def emit(packet: dict[str, Any]) -> int:
    packet["reasons"] = sorted(set(packet["reasons"]))
    packet["changed_file_set"]["write_receipts"] = sorted(
        set(packet["changed_file_set"]["write_receipts"])
    )
    packet["changed_file_set"]["files"] = sorted(
        set(packet["changed_file_set"]["files"])
    )
    packet["files"] = sorted(packet["files"], key=lambda item: item["path"])
    sys.stdout.write(
        json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    )
    return {"pass": 0, "not_applicable": 0, "fail": 2, "blocked": 3}[
        packet["result"]
    ]


def validate(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet()
    try:
        root = canonical_root(args.project_root)
        status_path = resolve_inside(root, args.status_carrier)
        status_relative = relative_path(root, status_path)
    except (OSError, RuntimeError, ValueError) as exc:
        packet["reasons"].append(str(exc))
        return packet

    packet["canonical_resolution"]["pointer"] = (
        f"{status_relative}#user_facing_language_resolution"
    )
    packet["canonical_resolution"]["expected_normalized_tag"] = (
        args.expected_normalized_tag
    )

    vcs_available, vcs_paths, vcs_error = run_git_paths(root)
    packet["changed_file_set"]["vcs_available"] = vcs_available
    if vcs_error:
        packet["reasons"].append(vcs_error)
        return packet

    receipts: set[str] = set()
    for raw in args.write_receipt:
        try:
            receipt_path = resolve_inside(root, raw)
            receipt_relative = relative_path(root, receipt_path)
        except ValueError as exc:
            packet["reasons"].append(str(exc))
            return packet
        if not receipt_path.is_file():
            packet["reasons"].append(f"write_receipt_missing:{receipt_relative}")
            return packet
        receipts.add(receipt_relative)

    classified_vcs = {
        path
        for path in vcs_paths
        if is_governance_path(path, status_relative)
    }
    changed = classified_vcs | receipts
    packet["changed_file_set"]["write_receipts"] = sorted(receipts)
    packet["changed_file_set"]["files"] = sorted(changed)

    if vcs_available and receipts:
        source = "vcs_diff_plus_write_receipts"
    elif vcs_available:
        source = "vcs_diff" if changed else "established_empty"
    elif receipts:
        source = "write_receipts_no_vcs"
    else:
        packet["reasons"].append("changed_file_set_unestablished")
        return packet
    packet["changed_file_set"]["source"] = source

    if not changed:
        packet["result"] = "not_applicable"
        return packet

    if not args.expected_normalized_tag:
        packet["reasons"].append("expected_normalized_tag_missing")
        return packet
    try:
        expected = normalize_tag(args.expected_normalized_tag)
    except ValueError:
        packet["reasons"].append("expected_normalized_tag_invalid")
        return packet
    if expected != args.expected_normalized_tag:
        packet["reasons"].append("expected_normalized_tag_not_normalized")
        return packet

    if not status_path.is_file():
        packet["reasons"].append("canonical_status_carrier_missing")
        return packet
    status_bytes, status_text, status_error = read_utf8(status_path)
    if status_error or status_bytes is None or status_text is None:
        packet["reasons"].append(f"canonical_status_carrier_{status_error}")
        return packet
    parent_count, resolution, duplicate_keys = parse_resolution(status_text)
    packet["canonical_resolution"]["parent_count"] = parent_count
    for key in ("contract", "status", "normalized_tag"):
        packet["canonical_resolution"][key] = resolution.get(key)
    if parent_count == 0:
        packet["reasons"].append("canonical_parent_missing")
        return packet
    if parent_count > 1:
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        packet["reasons"].append("canonical_parent_duplicate")
        return packet
    if duplicate_keys:
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        packet["reasons"].extend(
            f"canonical_child_duplicate:{key}" for key in duplicate_keys
        )
        return packet
    if resolution.get("contract") != RESOLUTION_CONTRACT:
        packet["reasons"].append("canonical_contract_missing_or_invalid")
        return packet
    if resolution.get("status") != "resolved":
        packet["reasons"].append("canonical_resolution_not_resolved")
        return packet
    canonical_tag = resolution.get("normalized_tag")
    if not canonical_tag:
        packet["reasons"].append("canonical_normalized_tag_missing")
        return packet
    try:
        normalized_canonical = normalize_tag(canonical_tag)
    except ValueError:
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        packet["reasons"].append("canonical_normalized_tag_invalid")
        return packet
    if normalized_canonical != canonical_tag:
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        packet["reasons"].append("canonical_normalized_tag_not_normalized")
        return packet
    if canonical_tag != expected:
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        packet["reasons"].append("canonical_tag_mismatch")
        return packet

    if not args.checker:
        packet["reasons"].append("adapter_checker_missing")
        return packet
    try:
        checker = Path(args.checker).expanduser().resolve()
    except (OSError, RuntimeError, ValueError):
        packet["reasons"].append("adapter_checker_unavailable")
        return packet
    if not checker.is_file():
        packet["reasons"].append("adapter_checker_unavailable")
        return packet

    any_mismatch = False
    for relative in sorted(changed):
        try:
            path = resolve_inside(root, relative)
        except ValueError as exc:
            packet["reasons"].append(str(exc))
            return packet
        data, text, error = read_utf8(path)
        if error or data is None or text is None:
            packet["files"].append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(data).hexdigest()
                    if data is not None
                    else None,
                    "actual_bytes_checked": data is not None,
                    "user_visible_prose": "absent",
                    "body_result": "unchecked",
                    "checker": None,
                }
            )
            packet["reasons"].append(f"changed_file_{error}:{relative}")
            return packet
        if path == status_path and data != status_bytes:
            packet["files"].append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "actual_bytes_checked": True,
                    "user_visible_prose": "absent",
                    "body_result": "unchecked",
                    "checker": None,
                }
            )
            packet["reasons"].append(
                f"canonical_status_changed_during_validation:{relative}"
            )
            return packet
        digest = hashlib.sha256(data).hexdigest()
        checker_payload, checker_error = invoke_checker(
            checker,
            root=root,
            normalized_tag=canonical_tag,
            path=path,
            expected_sha256=digest,
            expected_byte_count=len(data),
        )
        if checker_error or checker_payload is None:
            packet["files"].append(
                {
                    "path": relative,
                    "sha256": digest,
                    "actual_bytes_checked": True,
                    "user_visible_prose": "absent",
                    "body_result": "unchecked",
                    "checker": None,
                }
            )
            packet["reasons"].append(f"{checker_error}:{relative}")
            return packet
        data_after, _, stability_error = read_utf8(path)
        if stability_error or data_after != data:
            packet["files"].append(
                {
                    "path": relative,
                    "sha256": digest,
                    "actual_bytes_checked": True,
                    "user_visible_prose": "absent",
                    "body_result": "unchecked",
                    "checker": checker_payload.get("checker"),
                }
            )
            packet["reasons"].append(
                f"changed_file_changed_during_validation:{relative}"
            )
            return packet
        body_result = checker_payload["body_result"]
        file_evidence = {
            "path": relative,
            "sha256": digest,
            "actual_bytes_checked": True,
            "user_visible_prose": checker_payload["user_visible_prose"],
            "body_result": body_result,
            "checker": checker_payload.get("checker"),
            "excluded_technical_segments": checker_payload.get(
                "excluded_technical_segments", []
            ),
            "metrics": checker_payload.get("metrics", {}),
            "reason": checker_payload.get("reason"),
        }
        for field in (
            "evaluation_scope",
            "git_added_line_count",
            "whole_file_sha256_checked",
            "whole_file_byte_count",
            "evaluated_text_byte_count",
        ):
            if field in checker_payload:
                file_evidence[field] = checker_payload[field]
        packet["files"].append(file_evidence)
        if body_result in {"mismatch", "unchecked"}:
            any_mismatch = True
            packet["reasons"].append(f"governance_body_{body_result}:{relative}")

    if len(packet["files"]) != len(changed):
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        packet["reasons"].append("changed_governance_file_omitted")
        return packet
    if any_mismatch:
        packet["result"] = "fail"
        packet["repair"]["permitted"] = True
        return packet

    status_bytes_after, _, status_stability_error = read_utf8(status_path)
    if status_stability_error or status_bytes_after != status_bytes:
        packet["reasons"].append(
            f"canonical_status_changed_during_validation:{status_relative}"
        )
        return packet

    packet["result"] = "pass"
    return packet


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate actual governance bytes before Project Init handback."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--status-carrier", required=True)
    parser.add_argument("--expected-normalized-tag")
    parser.add_argument("--checker")
    parser.add_argument("--write-receipt", action="append", default=[])
    parser.add_argument(
        "--runtime-profile",
        choices=("full", "adaptive"),
        help="Parity witness only; never changes validation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    # Profile is deliberately not used or emitted. Identical bytes must produce
    # identical evidence under Full and Adaptive.
    return emit(validate(args))


if __name__ == "__main__":
    raise SystemExit(main())
