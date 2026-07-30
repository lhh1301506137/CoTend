#!/usr/bin/env python3
"""Read-only CoTend checker for user-facing governance prose."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


CHECKER_ID = "cotend-governance-language.v2"
SUPPORTED_TAGS = {"en", "zh-CN", "zh-TW"}
MIN_VISIBLE_LETTERS = 4
MIN_ENGLISH_SHARE = 0.80
MIN_CHINESE_SHARE = 0.20

CJK_CHARACTER = re.compile(r"[\u3400-\u9fff]")
LATIN_LETTER = re.compile(r"[A-Za-z]")
FENCE = re.compile(r"^\s*```")
MARKDOWN_PREFIX = re.compile(r"^\s{0,3}(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+)")
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")
HEX_DIGEST = re.compile(r"(?i)(?:sha256:)?[0-9a-f]{40,64}")
WINDOWS_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|\\\\)[^\s]+")
POSIX_PATH = re.compile(r"(?<!\w)(?:\./|\.\./|/)[^\s]+")
RELATIVE_PATH = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Za-z0-9_.-]+[\\/])+[A-Za-z0-9_.-]+"
)
COMMAND_LINE = re.compile(
    r"^\s*(?:git|python|py|pwsh|powershell|node|npm|pnpm|yarn|cargo|go)\s+\S+"
)
KEY_VALUE = re.compile(
    r"^\s*(?:-\s*)?(?P<key>[A-Za-z_][A-Za-z0-9_.-]*)\s*:\s*(?P<value>.*)$"
)
MACHINE_VALUE = re.compile(
    r"^[A-Za-z0-9_.:/|+\-]+(?: [A-Za-z0-9_.:/|+\-]+){0,2}$"
)
TECHNICAL_ATOM = re.compile(r"^[A-Za-z0-9_.:/\\|+\-]+$")
TECHNICAL_SIGNAL = re.compile(r"[0-9_./:\\|+]")
MACHINE_TOKEN = re.compile(r"(?=.*[0-9_.:/|+\-])[A-Za-z0-9_.:/|+\-]+")
TABLE_DELIMITER_CELL = re.compile(r"^:?-{3,}:?$")


def run_git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(path), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=15,
    )


def resolve_evaluation_text(path: Path, full_text: str) -> tuple[str, dict[str, Any]]:
    """Prefer operation-owned Git additions while hashing the whole file."""

    try:
        root_result = run_git(path.parent, "rev-parse", "--show-toplevel")
    except (OSError, subprocess.TimeoutExpired):
        root_result = None
    if root_result is None or root_result.returncode != 0:
        return full_text, {
            "evaluation_scope": "whole_file_no_git",
            "git_added_line_count": None,
        }

    try:
        root = Path(root_result.stdout.strip()).resolve()
        relative = path.resolve().relative_to(root).as_posix()
    except (OSError, RuntimeError, ValueError):
        return full_text, {
            "evaluation_scope": "whole_file_outside_git_root",
            "git_added_line_count": None,
        }

    try:
        tracked = run_git(root, "ls-files", "--error-unmatch", "--", relative)
    except (OSError, subprocess.TimeoutExpired):
        tracked = None
    if tracked is None or tracked.returncode != 0:
        return full_text, {
            "evaluation_scope": "git_untracked_whole_file",
            "git_added_line_count": len(full_text.splitlines()),
        }

    try:
        head = run_git(root, "rev-parse", "--verify", "HEAD")
    except (OSError, subprocess.TimeoutExpired):
        head = None
    if head is None or head.returncode != 0:
        return full_text, {
            "evaluation_scope": "git_unborn_whole_file",
            "git_added_line_count": len(full_text.splitlines()),
        }

    try:
        diff = run_git(
            root,
            "diff",
            "--no-ext-diff",
            "--no-color",
            "--no-renames",
            "--unified=0",
            "HEAD",
            "--",
            relative,
        )
    except (OSError, subprocess.TimeoutExpired):
        diff = None
    if diff is None or diff.returncode != 0:
        return "", {
            "evaluation_scope": "git_added_lines_unavailable",
            "git_added_line_count": None,
            "scope_error": "git_diff_failed",
        }

    added_lines = [
        line[1:]
        for line in diff.stdout.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    if not diff.stdout.strip():
        return full_text, {
            "evaluation_scope": "whole_file_no_git_delta",
            "git_added_line_count": 0,
        }
    return "\n".join(added_lines), {
        "evaluation_scope": "git_added_lines",
        "git_added_line_count": len(added_lines),
    }


def markdown_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def is_machine_table_cell(line: str) -> bool:
    value = line.strip().strip("`")
    if not value or TABLE_DELIMITER_CELL.fullmatch(value):
        return True
    tokens = [token for token in value.split() if token not in {"/", "|", "+", "-"}]
    return bool(tokens) and all(MACHINE_TOKEN.fullmatch(token) for token in tokens)


def _without_technical_fragments(value: str, exclusions: set[str]) -> str:
    text = MARKDOWN_LINK.sub(r"\1", value)
    substitutions = (
        (URL, "url"),
        (INLINE_CODE, "code"),
        (HEX_DIGEST, "hash"),
        (WINDOWS_PATH, "path"),
        (POSIX_PATH, "path"),
        (RELATIVE_PATH, "path"),
    )
    for pattern, label in substitutions:
        if pattern.search(text):
            text = pattern.sub("", text)
            exclusions.add(label)
    return MARKDOWN_PREFIX.sub("", text).strip()


def visible_governance_prose(text: str) -> tuple[str, list[str]]:
    """Return prose that a user reads, excluding deterministic technical forms."""

    visible: list[str] = []
    exclusions: set[str] = set()
    inside_fence = False

    for raw_line in text.splitlines():
        if FENCE.match(raw_line):
            inside_fence = not inside_fence
            exclusions.add("code")
            continue
        if inside_fence:
            exclusions.add("code")
            continue

        stripped = raw_line.strip()
        if not stripped:
            continue

        table_cells = markdown_table_cells(raw_line)
        candidates = table_cells if table_cells is not None else [raw_line]
        if table_cells is not None:
            exclusions.add("markdown_table_structure")

        for raw_candidate in candidates:
            candidate = raw_candidate.strip()
            if not candidate:
                continue
            if COMMAND_LINE.match(candidate):
                exclusions.add("command")
                continue

            key_value = KEY_VALUE.match(raw_candidate)
            if key_value:
                candidate = key_value.group("value").strip().strip("\"'")
                if not candidate or MACHINE_VALUE.fullmatch(candidate):
                    exclusions.add("machine_field")
                    continue
                exclusions.add("schema_key")

            candidate = _without_technical_fragments(candidate, exclusions)
            if not candidate:
                continue
            if table_cells is not None and is_machine_table_cell(candidate):
                exclusions.add("machine_table_cell")
                continue
            if TECHNICAL_ATOM.fullmatch(candidate) and TECHNICAL_SIGNAL.search(
                candidate
            ):
                exclusions.add("identifier")
                continue
            if not CJK_CHARACTER.search(candidate) and not LATIN_LETTER.search(
                candidate
            ):
                exclusions.add("identifier")
                continue
            visible.append(candidate)

    return "\n".join(visible), sorted(exclusions) or ["none"]


def evaluate(normalized_tag: str, text: str) -> dict[str, Any]:
    prose, exclusions = visible_governance_prose(text)
    cjk_count = len(CJK_CHARACTER.findall(prose))
    latin_count = len(LATIN_LETTER.findall(prose))
    total_letters = cjk_count + latin_count
    cjk_share = cjk_count / total_letters if total_letters else 0.0
    latin_share = latin_count / total_letters if total_letters else 0.0

    if total_letters == 0:
        body_result = "technical_only"
        prose_state = "absent"
        reason = "cotend_no_user_visible_prose_after_technical_exclusions"
    elif normalized_tag == "en":
        body_result = (
            "match"
            if latin_count >= MIN_VISIBLE_LETTERS
            and latin_share >= MIN_ENGLISH_SHARE
            else "mismatch"
        )
        prose_state = "present"
        reason = (
            "cotend_english_governance_prose_matches"
            if body_result == "match"
            else "cotend_english_governance_prose_mismatch"
        )
    elif normalized_tag in {"zh-CN", "zh-TW"}:
        body_result = (
            "match"
            if cjk_count >= MIN_VISIBLE_LETTERS
            and cjk_share >= MIN_CHINESE_SHARE
            else "mismatch"
        )
        prose_state = "present"
        reason = (
            "cotend_chinese_governance_prose_matches"
            if body_result == "match"
            else "cotend_chinese_governance_prose_mismatch"
        )
    else:
        body_result = "unchecked"
        prose_state = "present"
        reason = "cotend_normalized_tag_not_supported"

    return {
        "checker": CHECKER_ID,
        "normalized_tag": normalized_tag,
        "actual_bytes_checked": True,
        "user_visible_prose": prose_state,
        "body_result": body_result,
        "excluded_technical_segments": exclusions,
        "metrics": {
            "cjk_count": cjk_count,
            "latin_count": latin_count,
            "cjk_share": round(cjk_share, 6),
            "latin_share": round(latin_share, 6),
        },
        "reason": reason,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check actual CoTend governance bytes against a normalized tag."
    )
    parser.add_argument("--normalized-tag", required=True)
    parser.add_argument("--path", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.path).expanduser().resolve()
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        sys.stderr.write(
            json.dumps(
                {
                    "checker": CHECKER_ID,
                    "error": "cotend_actual_bytes_unreadable_or_not_utf8",
                    "detail": type(exc).__name__,
                    "path": str(path),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        )
        return 3

    evaluation_text, scope = resolve_evaluation_text(path, text)
    if scope.get("scope_error"):
        payload = {
            "checker": CHECKER_ID,
            "normalized_tag": args.normalized_tag,
            "actual_bytes_checked": True,
            "user_visible_prose": "present",
            "body_result": "unchecked",
            "excluded_technical_segments": ["none"],
            "metrics": {},
            "reason": scope["scope_error"],
        }
    else:
        payload = evaluate(args.normalized_tag, evaluation_text)
    payload.update(scope)
    payload["whole_file_sha256_checked"] = True
    payload["whole_file_byte_count"] = len(data)
    payload["evaluated_text_byte_count"] = len(evaluation_text.encode("utf-8"))
    payload["path"] = str(path)
    payload["sha256"] = hashlib.sha256(data).hexdigest()
    sys.stdout.write(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
