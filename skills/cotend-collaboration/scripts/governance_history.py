#!/usr/bin/env python3
"""Read-only health, integrity, and bounded lookup for governance history."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, Literal


LOCATOR_CONTRACT = "cotend.governance-history-locator.v1"
INDEX_CONTRACT = "cotend.governance-history-index.v1"
HEALTH_CONTRACT = "cotend.governance-history-health.v1"
VALIDATION_CONTRACT = "cotend.governance-history-validation.v1"
SELECTION_CONTRACT = "cotend.governance-history-selection.v1"
ERROR_CONTRACT = "cotend.governance-history-error.v1"

DEFAULT_MAX_BYTES = 256 * 1024
DEFAULT_MAX_RECORDS = 500
DEFAULT_MAX_RECORD_BYTES = 64 * 1024
DEFAULT_MAX_ATTENTION_RECORDS = 100
MAX_SELECTION_RESULTS = 3

LOCATOR_FIELDS = {
    "contract",
    "schema_version",
    "carrier_id",
    "index_path",
    "index_sha256",
    "latest_chunk_id",
    "active_ids",
    "current_ids",
    "pending_ids",
    "unresolved_ids",
}
INDEX_FIELDS = {
    "contract",
    "schema_version",
    "carrier_id",
    "active_path",
    "latest_chunk_id",
    "migration_state",
    "chunks",
}
CHUNK_FIELDS = {
    "chunk_id",
    "path",
    "sha256",
    "state",
    "record_count",
    "first_id",
    "last_id",
    "date_from",
    "date_to",
    "tags",
    "records",
}
ARCHIVE_RECORD_FIELDS = {"id", "date", "tags", "status"}
ACTIVE_RECORD_FIELDS = {"id", "date", "tags", "states"}

ACTIVE_STATES = {"active", "current", "pending", "recent", "unresolved"}
ARCHIVE_STATUSES = {"archived", "resolved", "superseded"}
LOCATOR_PATTERN = re.compile(
    rb"<!-- cotend-history-locator\r?\n(?P<body>\{[^\r\n]*\})\r?\n-->",
    re.MULTILINE,
)
RECORD_PATTERN = re.compile(
    rb"^<!-- cotend-history-record (?P<body>\{[^\r\n]*\}) -->[ \t]*(?:\r?\n|$)",
    re.MULTILINE,
)
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}")
CARRIER_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}")
SHA256 = re.compile(r"[0-9a-f]{64}")
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
READ_BLOCK_BYTES = 1024 * 1024
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
    "COM¹",
    "COM²",
    "COM³",
    "LPT¹",
    "LPT²",
    "LPT³",
}


@dataclass(frozen=True)
class RootToken:
    """Resolved project root bound to the directory inspected by the caller."""

    path: Path
    identity: tuple[int, int, int, int]


@dataclass(frozen=True)
class PathToken:
    """Pre-open identity for every component of one canonical project path."""

    root: RootToken
    relative: str
    resolved: Path
    field: str
    components: tuple[tuple[Path, tuple[int, int, int, int]], ...]
    final_state: tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class FileSnapshot:
    """One race-checked read-only file observation."""

    relative: str
    resolved: Path
    size: int
    bytes_read: int
    sha256: str | None
    raw: bytes | None
    file_state: tuple[int, int, int, int, int, int, int]
    path_identities: tuple[tuple[int, int, int, int], ...]


class GovernanceHistoryError(ValueError):
    """Fail-closed lifecycle or query error."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise GovernanceHistoryError(code, message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, "duplicate_json_key", f"duplicate JSON key: {key}")
        value[key] = item
    return value


def reject_json_constant(value: str) -> None:
    raise GovernanceHistoryError(
        "invalid_json", f"non-standard JSON constant is forbidden: {value}"
    )


def strict_json_bytes(raw: bytes, *, label: str) -> Any:
    try:
        text = raw.decode("utf-8", errors="strict")
        return json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=reject_json_constant,
        )
    except GovernanceHistoryError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise GovernanceHistoryError(
            "invalid_json", f"{label} is not strict UTF-8 JSON: {exc}"
        ) from exc


def exact_fields(value: Any, expected: set[str], *, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), "schema_drift", f"{label} must be an object")
    actual = set(value)
    require(
        actual == expected,
        "schema_drift",
        f"{label} fields differ: missing={sorted(expected - actual)}, "
        f"unknown={sorted(actual - expected)}",
    )
    return value


def positive_int(value: Any, *, field: str) -> int:
    require(
        type(value) is int and value > 0,
        "invalid_threshold",
        f"{field} must be a positive integer",
    )
    return value


def non_negative_int(value: Any, *, field: str) -> int:
    require(
        type(value) is int and value >= 0,
        "schema_drift",
        f"{field} must be a non-negative integer",
    )
    return value


def schema_version_one(value: Any, *, field: str) -> int:
    require(
        type(value) is int and value == 1,
        "schema_drift",
        f"{field} must be integer 1",
    )
    return value


def identifier(value: Any, *, field: str) -> str:
    require(
        isinstance(value, str) and IDENTIFIER.fullmatch(value) is not None,
        "invalid_identifier",
        f"{field} is not a stable identifier",
    )
    return value


def carrier_id(value: Any, *, field: str) -> str:
    require(
        isinstance(value, str) and CARRIER_ID.fullmatch(value) is not None,
        "invalid_carrier_id",
        f"{field} is invalid",
    )
    return value


def sha256_value(value: Any, *, field: str) -> str:
    require(
        isinstance(value, str) and SHA256.fullmatch(value) is not None,
        "invalid_hash",
        f"{field} must be a lowercase SHA-256",
    )
    return value


def iso_date(value: Any, *, field: str) -> str:
    require(isinstance(value, str), "invalid_date", f"{field} must be a date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise GovernanceHistoryError("invalid_date", f"{field} is invalid") from exc
    require(parsed.isoformat() == value, "invalid_date", f"{field} is not canonical")
    return value


def unique_strings(
    value: Any,
    *,
    field: str,
    allow_empty: bool = True,
    maximum_items: int = 10_000,
    maximum_length: int = 128,
) -> list[str]:
    require(
        isinstance(value, list)
        and (allow_empty or bool(value))
        and len(value) <= maximum_items
        and all(
            isinstance(item, str) and item and len(item) <= maximum_length
            for item in value
        ),
        "schema_drift",
        f"{field} must be a bounded string list",
    )
    require(len(set(value)) == len(value), "duplicate_id", f"{field} has duplicates")
    return value


def id_list(value: Any, *, field: str) -> list[str]:
    values = unique_strings(value, field=field)
    for position, item in enumerate(values):
        identifier(item, field=f"{field}[{position}]")
    return values


def tags(value: Any, *, field: str) -> list[str]:
    values = unique_strings(
        value,
        field=field,
        maximum_items=64,
        maximum_length=80,
    )
    require(values == sorted(values), "schema_drift", f"{field} must be sorted")
    return values


def safe_relative(value: Any, *, field: str) -> str:
    require(
        isinstance(value, str)
        and value
        and "\\" not in value
        and "\x00" not in value
        and ":" not in value
        and re.search(r'[<>"|?*]', value) is None
        and not any(ord(character) < 32 for character in value),
        "unsafe_path",
        f"{field} must be a POSIX-relative path",
    )
    require(
        "://" not in value and not re.match(r"^[A-Za-z]:", value),
        "unsafe_path",
        f"{field} must not be absolute or URI-like",
    )
    pure = PurePosixPath(value)
    require(
        not pure.is_absolute()
        and bool(pure.parts)
        and value not in {".", ".."}
        and all(part not in {"", ".", ".."} for part in pure.parts)
        and pure.as_posix() == value,
        "unsafe_path",
        f"{field} contains traversal or normalization drift",
    )
    for part in pure.parts:
        stem = part.split(".", 1)[0].rstrip(" .").upper()
        require(
            not part.endswith((" ", ".")) and stem not in WINDOWS_RESERVED_NAMES,
            "unsafe_path",
            f"{field} is not cross-platform canonical",
        )
    return value


def _linklike(path: Path) -> bool:
    info = path.lstat()
    return _linklike_info(info)


def _linklike_info(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & FILE_ATTRIBUTE_REPARSE_POINT)


def _stat_identity(info: os.stat_result) -> tuple[int, int, int, int]:
    return (
        info.st_dev,
        info.st_ino,
        stat.S_IFMT(info.st_mode),
        getattr(info, "st_file_attributes", 0),
    )


def _file_state(info: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        *_stat_identity(info),
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _open_binding_state(info: os.stat_result) -> tuple[int, int, int, int, int, int]:
    # Windows path-stat and handle-stat can report different creation/ctime
    # precision for the same file, so bind identity, size, and mtime here. The
    # handle-to-handle and transaction checks below still compare full state.
    return (*_stat_identity(info), info.st_size, info.st_mtime_ns)


def _revalidate_root(root: RootToken) -> None:
    try:
        info = root.path.lstat()
        require(
            stat.S_ISDIR(info.st_mode) and not _linklike_info(info),
            "path_race",
            "project root became a link or non-directory",
        )
        require(
            _stat_identity(info) == root.identity,
            "path_race",
            "project root identity changed",
        )
    except GovernanceHistoryError:
        raise
    except OSError as exc:
        raise GovernanceHistoryError(
            "path_race", f"cannot revalidate project root: {exc}"
        ) from exc


def project_root(root: Path) -> RootToken:
    try:
        require(os.path.lexists(root), "missing_path", "project root is missing")
        before = root.lstat()
        require(
            stat.S_ISDIR(before.st_mode),
            "unsafe_path",
            "project root must be a directory",
        )
        require(not _linklike_info(before), "link_forbidden", "project root is a link")
        resolved = root.resolve(strict=True)
        resolved_info = resolved.lstat()
        require(
            _stat_identity(resolved_info) == _stat_identity(before),
            "path_race",
            "project root changed while resolving",
        )
        token = RootToken(path=resolved, identity=_stat_identity(resolved_info))
        _revalidate_root(token)
        return token
    except GovernanceHistoryError:
        raise
    except OSError as exc:
        raise GovernanceHistoryError(
            "path_error", f"cannot inspect project root: {exc}"
        ) from exc


def _regular_file_token(root: RootToken, relative: str, *, field: str) -> PathToken:
    safe_relative(relative, field=field)
    current = root.path
    components: list[tuple[Path, tuple[int, int, int, int]]] = []
    try:
        root_info = current.lstat()
        require(
            not _linklike_info(root_info), "link_forbidden", "project root is a link"
        )
        require(stat.S_ISDIR(root_info.st_mode), "unsafe_path", "project root changed")
        require(
            _stat_identity(root_info) == root.identity,
            "path_race",
            "project root identity changed",
        )
        components.append((current, _stat_identity(root_info)))
        parts = PurePosixPath(relative).parts
        for position, part in enumerate(parts):
            current = current / part
            require(os.path.lexists(current), "missing_path", f"{field} is missing")
            info = current.lstat()
            require(
                not _linklike_info(info),
                "link_forbidden",
                f"{field} crosses a link",
            )
            if position + 1 < len(parts):
                require(
                    stat.S_ISDIR(info.st_mode),
                    "unsafe_path",
                    f"{field} crosses a non-directory",
                )
            else:
                require(
                    stat.S_ISREG(info.st_mode),
                    "unsafe_path",
                    f"{field} is not a regular file",
                )
            components.append((current, _stat_identity(info)))
        resolved = current.resolve(strict=True)
        try:
            resolved.relative_to(root.path)
        except ValueError as exc:
            raise GovernanceHistoryError(
                "unsafe_path", f"{field} resolves outside the project"
            ) from exc
        return PathToken(
            root=root,
            relative=relative,
            resolved=resolved,
            field=field,
            components=tuple(components),
            final_state=_open_binding_state(info),
        )
    except GovernanceHistoryError:
        raise
    except OSError as exc:
        raise GovernanceHistoryError(
            "path_error", f"cannot inspect {field}: {exc}"
        ) from exc


def _revalidate_path_token(token: PathToken) -> None:
    try:
        for path, expected_identity in token.components:
            require(os.path.lexists(path), "path_race", f"{token.field} changed")
            info = path.lstat()
            require(
                not _linklike_info(info),
                "link_forbidden",
                f"{token.field} crosses a link",
            )
            require(
                _stat_identity(info) == expected_identity,
                "path_race",
                f"{token.field} identity changed during inspection",
            )
        resolved = token.components[-1][0].resolve(strict=True)
        require(
            resolved == token.resolved,
            "path_race",
            f"{token.field} target changed during inspection",
        )
        try:
            resolved.relative_to(token.root.path)
        except ValueError as exc:
            raise GovernanceHistoryError(
                "unsafe_path", f"{token.field} resolves outside the project"
            ) from exc
    except GovernanceHistoryError:
        raise
    except OSError as exc:
        raise GovernanceHistoryError(
            "path_race", f"cannot revalidate {token.field}: {exc}"
        ) from exc


def snapshot_regular_file(
    root: RootToken,
    relative: str,
    *,
    field: str,
    mode: Literal["metadata", "hash", "bytes"],
) -> FileSnapshot:
    """Open read-only, bind the handle to the checked path, then recheck it."""

    token = _regular_file_token(root, relative, field=field)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(token.resolved, flags)
    except OSError as exc:
        raise GovernanceHistoryError(
            "path_race", f"cannot open stable {field}: {exc}"
        ) from exc
    try:
        opened_before = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened_before.st_mode) and not _linklike_info(opened_before),
            "link_forbidden",
            f"{field} opened as a link or non-regular file",
        )
        require(
            _open_binding_state(opened_before) == token.final_state,
            "path_race",
            f"{field} changed before its read-only handle opened",
        )
        _revalidate_path_token(token)

        chunks: list[bytes] | None = [] if mode == "bytes" else None
        digest = hashlib.sha256() if mode in {"hash", "bytes"} else None
        bytes_read = 0
        if mode != "metadata":
            while True:
                block = os.read(descriptor, READ_BLOCK_BYTES)
                if not block:
                    break
                bytes_read += len(block)
                assert digest is not None
                digest.update(block)
                if chunks is not None:
                    chunks.append(block)

        opened_after = os.fstat(descriptor)
        require(
            _file_state(opened_after) == _file_state(opened_before),
            "path_race",
            f"{field} changed while it was being read",
        )
        if mode != "metadata":
            require(
                bytes_read == opened_before.st_size,
                "path_race",
                f"{field} byte count changed while it was being read",
            )
        _revalidate_path_token(token)
        return FileSnapshot(
            relative=relative,
            resolved=token.resolved,
            size=opened_before.st_size,
            bytes_read=bytes_read,
            sha256=digest.hexdigest() if digest is not None else None,
            raw=b"".join(chunks) if chunks is not None else None,
            file_state=_file_state(opened_before),
            path_identities=tuple(identity for _, identity in token.components),
        )
    except GovernanceHistoryError:
        raise
    except OSError as exc:
        raise GovernanceHistoryError(
            "path_race", f"cannot read stable {field}: {exc}"
        ) from exc
    finally:
        os.close(descriptor)


def pending_marker_path(root: RootToken, index_relative: str) -> Path:
    marker_relative = f"{index_relative}.migration-pending"
    safe_relative(marker_relative, field="migration_pending_marker")
    return root.path.joinpath(*PurePosixPath(marker_relative).parts)


def parse_locator(raw: bytes) -> dict[str, Any]:
    matches = list(LOCATOR_PATTERN.finditer(raw))
    require(
        len(matches) == 1 and raw.count(b"<!-- cotend-history-locator") == 1,
        "locator_missing_or_ambiguous",
        "active carrier must contain exactly one canonical locator",
    )
    value = exact_fields(
        strict_json_bytes(matches[0].group("body"), label="history locator"),
        LOCATOR_FIELDS,
        label="history locator",
    )
    require(
        value["contract"] == LOCATOR_CONTRACT, "schema_drift", "wrong locator contract"
    )
    schema_version_one(value["schema_version"], field="locator.schema_version")
    carrier_id(value["carrier_id"], field="locator.carrier_id")
    safe_relative(value["index_path"], field="locator.index_path")
    sha256_value(value["index_sha256"], field="locator.index_sha256")
    if value["latest_chunk_id"] is not None:
        identifier(value["latest_chunk_id"], field="locator.latest_chunk_id")
    for field in ("active_ids", "current_ids", "pending_ids", "unresolved_ids"):
        value[field] = id_list(value[field], field=f"locator.{field}")
    return value


def parse_active_records(raw: bytes) -> list[dict[str, Any]]:
    matches = list(RECORD_PATTERN.finditer(raw))
    require(
        raw.count(b"<!-- cotend-history-record") == len(matches),
        "missing_or_malformed_record_id",
        "every declared active record marker must be canonical",
    )
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for position, match in enumerate(matches):
        value = exact_fields(
            strict_json_bytes(match.group("body"), label=f"active record {position}"),
            ACTIVE_RECORD_FIELDS,
            label=f"active record {position}",
        )
        record_id = identifier(value["id"], field=f"active record {position}.id")
        require(
            record_id not in seen, "duplicate_id", f"duplicate active ID: {record_id}"
        )
        seen.add(record_id)
        iso_date(value["date"], field=f"active record {record_id}.date")
        value["tags"] = tags(value["tags"], field=f"active record {record_id}.tags")
        states = unique_strings(
            value["states"],
            field=f"active record {record_id}.states",
            allow_empty=False,
            maximum_items=len(ACTIVE_STATES),
            maximum_length=16,
        )
        require(
            states == sorted(states) and set(states) <= ACTIVE_STATES,
            "schema_drift",
            f"active record {record_id}.states are invalid",
        )
        records.append(value)
    return records


def active_record_metrics(raw: bytes, records: list[dict[str, Any]]) -> dict[str, Any]:
    matches = list(RECORD_PATTERN.finditer(raw))
    lengths = [
        (matches[position + 1].start() if position + 1 < len(matches) else len(raw))
        - match.start()
        for position, match in enumerate(matches)
    ]
    state_ids = {
        state: [record["id"] for record in records if state in record["states"]]
        for state in ACTIVE_STATES
    }
    attention_ids = {
        record_id
        for state in ("active", "pending", "unresolved")
        for record_id in state_ids[state]
    }
    return {
        "record_count": len(records),
        "longest_record_bytes": max(lengths, default=0),
        "state_counts": {
            state: len(state_ids[state]) for state in sorted(ACTIVE_STATES)
        },
        "attention_record_count": len(attention_ids),
        "state_ids": state_ids,
    }


def validate_locator_against_active(
    locator: dict[str, Any], records: list[dict[str, Any]]
) -> None:
    state_ids = {
        state: [record["id"] for record in records if state in record["states"]]
        for state in ACTIVE_STATES
    }
    for state, field in (
        ("active", "active_ids"),
        ("current", "current_ids"),
        ("pending", "pending_ids"),
        ("unresolved", "unresolved_ids"),
    ):
        require(
            locator[field] == state_ids[state],
            "active_pointer_mismatch",
            f"locator.{field} differs from active record states",
        )


def parse_index(raw: bytes) -> dict[str, Any]:
    value = exact_fields(
        strict_json_bytes(raw, label="history index"),
        INDEX_FIELDS,
        label="history index",
    )
    require(value["contract"] == INDEX_CONTRACT, "schema_drift", "wrong index contract")
    schema_version_one(value["schema_version"], field="index.schema_version")
    carrier_id(value["carrier_id"], field="index.carrier_id")
    safe_relative(value["active_path"], field="index.active_path")
    require(
        value["migration_state"] == "complete",
        "half_migration",
        "history index is not in complete state",
    )
    require(
        isinstance(value["chunks"], list), "schema_drift", "index.chunks must be a list"
    )

    chunk_ids: set[str] = set()
    chunk_paths: set[str] = set()
    archive_ids: set[str] = set()
    for chunk_position, chunk_value in enumerate(value["chunks"]):
        chunk = exact_fields(
            chunk_value,
            CHUNK_FIELDS,
            label=f"index.chunks[{chunk_position}]",
        )
        chunk_id = identifier(
            chunk["chunk_id"], field=f"chunk {chunk_position}.chunk_id"
        )
        require(
            chunk_id not in chunk_ids, "duplicate_id", f"duplicate chunk ID: {chunk_id}"
        )
        chunk_ids.add(chunk_id)
        chunk_path = safe_relative(chunk["path"], field=f"chunk {chunk_id}.path")
        chunk_path_key = chunk_path.casefold()
        require(
            chunk_path_key not in chunk_paths,
            "duplicate_path",
            f"duplicate or case-colliding chunk path: {chunk_path}",
        )
        chunk_paths.add(chunk_path_key)
        sha256_value(chunk["sha256"], field=f"chunk {chunk_id}.sha256")
        require(
            chunk["state"] == "sealed",
            "half_migration",
            f"chunk {chunk_id} is not sealed",
        )
        require(
            isinstance(chunk["records"], list) and chunk["records"],
            "schema_drift",
            f"chunk {chunk_id}.records must be non-empty",
        )
        non_negative_int(chunk["record_count"], field=f"chunk {chunk_id}.record_count")
        require(
            chunk["record_count"] == len(chunk["records"]),
            "record_count_mismatch",
            f"chunk {chunk_id} record count differs",
        )

        record_ids: list[str] = []
        record_dates: list[str] = []
        record_tags: set[str] = set()
        for record_position, record_value in enumerate(chunk["records"]):
            record = exact_fields(
                record_value,
                ARCHIVE_RECORD_FIELDS,
                label=f"chunk {chunk_id}.records[{record_position}]",
            )
            record_id = identifier(record["id"], field=f"chunk {chunk_id} record ID")
            require(
                record_id not in archive_ids,
                "duplicate_id",
                f"duplicate archive ID: {record_id}",
            )
            archive_ids.add(record_id)
            record_ids.append(record_id)
            record_dates.append(
                iso_date(record["date"], field=f"archive record {record_id}.date")
            )
            record["tags"] = tags(
                record["tags"], field=f"archive record {record_id}.tags"
            )
            record_tags.update(record["tags"])
            require(
                isinstance(record["status"], str)
                and record["status"] in ARCHIVE_STATUSES,
                "schema_drift",
                f"archive record {record_id}.status is invalid",
            )

        identifier(chunk["first_id"], field=f"chunk {chunk_id}.first_id")
        identifier(chunk["last_id"], field=f"chunk {chunk_id}.last_id")
        require(
            chunk["first_id"] == record_ids[0] and chunk["last_id"] == record_ids[-1],
            "id_range_mismatch",
            f"chunk {chunk_id} ID range differs",
        )
        require(
            iso_date(chunk["date_from"], field=f"chunk {chunk_id}.date_from")
            == min(record_dates),
            "date_range_mismatch",
            f"chunk {chunk_id} date_from differs",
        )
        require(
            iso_date(chunk["date_to"], field=f"chunk {chunk_id}.date_to")
            == max(record_dates),
            "date_range_mismatch",
            f"chunk {chunk_id} date_to differs",
        )
        chunk["tags"] = tags(chunk["tags"], field=f"chunk {chunk_id}.tags")
        require(
            chunk["tags"] == sorted(record_tags),
            "tag_range_mismatch",
            f"chunk {chunk_id} tags differ",
        )

    expected_latest = value["chunks"][-1]["chunk_id"] if value["chunks"] else None
    if value["latest_chunk_id"] is not None:
        identifier(value["latest_chunk_id"], field="index.latest_chunk_id")
    require(
        value["latest_chunk_id"] == expected_latest,
        "current_pointer_mismatch",
        "index latest chunk is not the final sealed chunk",
    )
    return value


def snapshot_evidence(snapshot: FileSnapshot) -> dict[str, Any]:
    return {
        "path": snapshot.relative,
        "bytes_read": snapshot.bytes_read,
        "sha256": snapshot.sha256,
    }


def require_snapshot_unchanged(
    root: RootToken, snapshot: FileSnapshot, *, field: str
) -> None:
    current = snapshot_regular_file(
        root, snapshot.relative, field=field, mode="metadata"
    )
    require(
        current.file_state == snapshot.file_state
        and current.path_identities == snapshot.path_identities,
        "path_race",
        f"{field} or its directory chain changed across the validation transaction",
    )


def require_pending_marker_absent(root: RootToken, index_relative: str) -> None:
    _revalidate_root(root)
    marker = pending_marker_path(root, index_relative)
    marker_absent = not os.path.lexists(marker)
    _revalidate_root(root)
    require(marker_absent, "half_migration", "migration pending marker exists")


def revalidate_loaded_state(state: dict[str, Any]) -> None:
    require_snapshot_unchanged(state["root"], state["active_snapshot"], field="active")
    require_snapshot_unchanged(
        state["root"], state["index_snapshot"], field="locator.index_path"
    )
    for chunk in state["index"]["chunks"]:
        require_snapshot_unchanged(
            state["root"],
            state["chunk_snapshots_by_id"][chunk["chunk_id"]],
            field=f"chunk {chunk['chunk_id']}.path",
        )
    require_pending_marker_absent(state["root"], state["locator"]["index_path"])


def _load_validated(
    root: Path, active_relative: str, *, validate_all_chunks: bool
) -> dict[str, Any]:
    resolved_root = project_root(root)
    active_relative = safe_relative(active_relative, field="active")
    active_snapshot = snapshot_regular_file(
        resolved_root,
        active_relative,
        field="active",
        mode="bytes",
    )
    assert active_snapshot.raw is not None
    active_raw = active_snapshot.raw
    locator = parse_locator(active_raw)
    active_records = parse_active_records(active_raw)
    validate_locator_against_active(locator, active_records)

    require(
        locator["index_path"].casefold() != active_relative.casefold(),
        "path_conflict",
        "history index must differ from the active carrier",
    )
    require_pending_marker_absent(resolved_root, locator["index_path"])
    index_snapshot = snapshot_regular_file(
        resolved_root,
        locator["index_path"],
        field="locator.index_path",
        mode="bytes",
    )
    require_pending_marker_absent(resolved_root, locator["index_path"])
    assert index_snapshot.raw is not None and index_snapshot.sha256 is not None
    index_raw = index_snapshot.raw
    require(
        index_snapshot.sha256 == locator["index_sha256"],
        "hash_drift",
        "history index hash differs from locator",
    )
    index = parse_index(index_raw)

    require(
        index["carrier_id"] == locator["carrier_id"],
        "carrier_mismatch",
        "locator/index carrier IDs differ",
    )
    require(
        index["active_path"] == active_relative,
        "carrier_mismatch",
        "index active path differs",
    )
    require(
        index["latest_chunk_id"] == locator["latest_chunk_id"],
        "current_pointer_mismatch",
        "locator/index latest chunk IDs differ",
    )

    archive_records = [
        record for chunk in index["chunks"] for record in chunk["records"]
    ]
    active_ids = {record["id"] for record in active_records}
    archive_ids = {record["id"] for record in archive_records}
    superseded = {
        record["id"] for record in archive_records if record["status"] == "superseded"
    }
    require(
        not (set(locator["current_ids"]) & superseded),
        "current_points_to_superseded",
        "current pointer targets superseded history",
    )
    overlap = active_ids & archive_ids
    require(
        not overlap,
        "active_archive_conflict",
        f"active IDs also exist in archive: {sorted(overlap)}",
    )
    for field in ("active_ids", "current_ids", "pending_ids", "unresolved_ids"):
        missing = set(locator[field]) - active_ids
        require(
            not missing,
            "active_pointer_missing",
            f"locator.{field} exists only outside active carrier",
        )

    chunk_snapshots_by_id: dict[str, FileSnapshot] = {}
    authority_path_keys = {
        active_relative.casefold(),
        locator["index_path"].casefold(),
    }
    for chunk in index["chunks"]:
        require(
            chunk["path"].casefold() not in authority_path_keys,
            "path_conflict",
            f"chunk {chunk['chunk_id']} collides with an authority-bearing file",
        )
        chunk_snapshot = snapshot_regular_file(
            resolved_root,
            chunk["path"],
            field=f"chunk {chunk['chunk_id']}.path",
            mode="hash" if validate_all_chunks else "metadata",
        )
        chunk_snapshots_by_id[chunk["chunk_id"]] = chunk_snapshot
        if validate_all_chunks:
            require(
                chunk_snapshot.sha256 == chunk["sha256"],
                "hash_drift",
                f"chunk hash differs: {chunk['chunk_id']}",
            )
    require_pending_marker_absent(resolved_root, locator["index_path"])

    return {
        "root": resolved_root,
        "active_relative": active_relative,
        "active_raw": active_raw,
        "active_snapshot": active_snapshot,
        "active_records": active_records,
        "locator": locator,
        "index": index,
        "index_snapshot": index_snapshot,
        "chunk_snapshots_by_id": chunk_snapshots_by_id,
    }


def health(
    root: Path,
    active_relative: str,
    *,
    deep: bool = False,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_records: int = DEFAULT_MAX_RECORDS,
    max_record_bytes: int = DEFAULT_MAX_RECORD_BYTES,
    max_attention_records: int = DEFAULT_MAX_ATTENTION_RECORDS,
) -> dict[str, Any]:
    thresholds = {
        "max_bytes": positive_int(max_bytes, field="max_bytes"),
        "max_records": positive_int(max_records, field="max_records"),
        "max_record_bytes": positive_int(max_record_bytes, field="max_record_bytes"),
        "max_attention_records": positive_int(
            max_attention_records, field="max_attention_records"
        ),
    }
    resolved_root = project_root(root)
    active_relative = safe_relative(active_relative, field="active")
    active_snapshot = snapshot_regular_file(
        resolved_root,
        active_relative,
        field="active",
        mode="metadata",
    )
    size = active_snapshot.size
    violations = ["total_bytes"] if size > max_bytes else []
    should_deep = deep or bool(violations)
    result: dict[str, Any] = {
        "contract": HEALTH_CONTRACT,
        "schema_version": 1,
        "active_path": active_relative,
        "total_bytes": size,
        "inspection": "deep" if should_deep else "stat_only",
        "deep_reason": "explicit"
        if deep
        else ("bytes_threshold" if violations else None),
        "thresholds": thresholds,
        "record_count": None,
        "longest_record_bytes": None,
        "state_counts": None,
        "attention_record_count": None,
        "violations": violations,
        "maintenance_candidate": True if violations else None,
        "index_read": False,
        "read_evidence": {
            "active": snapshot_evidence(active_snapshot),
            "index_bytes_read": 0,
            "chunk_bytes_read": 0,
            "total_bytes_read": 0,
        },
        "chunk_body_output": False,
        "semantic_conclusion": False,
        "migration_authorized": False,
    }
    if not should_deep:
        return result

    deep_snapshot = snapshot_regular_file(
        resolved_root,
        active_relative,
        field="active",
        mode="bytes",
    )
    require(
        deep_snapshot.file_state == active_snapshot.file_state,
        "path_race",
        "active carrier changed between stat and deep health",
    )
    assert deep_snapshot.raw is not None
    raw = deep_snapshot.raw
    locator = parse_locator(raw)
    records = parse_active_records(raw)
    validate_locator_against_active(locator, records)
    require_pending_marker_absent(resolved_root, locator["index_path"])
    metrics = active_record_metrics(raw, records)
    result.update(
        {
            "carrier_id": locator["carrier_id"],
            "record_count": metrics["record_count"],
            "longest_record_bytes": metrics["longest_record_bytes"],
            "state_counts": metrics["state_counts"],
            "attention_record_count": metrics["attention_record_count"],
            "read_evidence": {
                "active": snapshot_evidence(deep_snapshot),
                "index_bytes_read": 0,
                "chunk_bytes_read": 0,
                "total_bytes_read": deep_snapshot.bytes_read,
            },
        }
    )
    for code, actual, maximum in (
        ("record_count", metrics["record_count"], max_records),
        ("longest_record_bytes", metrics["longest_record_bytes"], max_record_bytes),
        (
            "attention_record_count",
            metrics["attention_record_count"],
            max_attention_records,
        ),
    ):
        if actual > maximum:
            result["violations"].append(code)
    result["maintenance_candidate"] = bool(result["violations"])
    return result


def validate(root: Path, active_relative: str) -> dict[str, Any]:
    state = _load_validated(root, active_relative, validate_all_chunks=True)
    metrics = active_record_metrics(state["active_raw"], state["active_records"])
    chunk_evidence = [
        snapshot_evidence(state["chunk_snapshots_by_id"][chunk["chunk_id"]])
        for chunk in state["index"]["chunks"]
    ]
    total_bytes_read = (
        state["active_snapshot"].bytes_read
        + state["index_snapshot"].bytes_read
        + sum(item["bytes_read"] for item in chunk_evidence)
    )
    revalidate_loaded_state(state)
    return {
        "contract": VALIDATION_CONTRACT,
        "schema_version": 1,
        "valid": True,
        "carrier_id": state["locator"]["carrier_id"],
        "active_path": state["active_relative"],
        "index_path": state["locator"]["index_path"],
        "latest_chunk_id": state["locator"]["latest_chunk_id"],
        "active_record_count": metrics["record_count"],
        "archive_record_count": sum(
            chunk["record_count"] for chunk in state["index"]["chunks"]
        ),
        "validated_chunk_count": len(state["index"]["chunks"]),
        "hashes_validated": True,
        "read_evidence": {
            "active": snapshot_evidence(state["active_snapshot"]),
            "index": snapshot_evidence(state["index_snapshot"]),
            "chunks": chunk_evidence,
            "total_bytes_read": total_bytes_read,
        },
        "chunk_body_output": False,
        "migration_performed": False,
    }


def select(
    root: Path,
    active_relative: str,
    *,
    record_id: str | None = None,
    record_date: str | None = None,
    tag: str | None = None,
) -> dict[str, Any]:
    provided = [record_id is not None, record_date is not None, tag is not None]
    require(
        sum(provided) == 1,
        "invalid_selector",
        "select requires exactly one ID, date, or tag",
    )
    if record_id is not None:
        identifier(record_id, field="selector.id")
        selector = {"kind": "id", "value": record_id}
    elif record_date is not None:
        iso_date(record_date, field="selector.date")
        selector = {"kind": "date", "value": record_date}
    else:
        require(
            isinstance(tag, str) and 0 < len(tag) <= 80,
            "invalid_selector",
            "selector.tag is invalid",
        )
        selector = {"kind": "tag", "value": tag}

    state = _load_validated(root, active_relative, validate_all_chunks=False)
    matched_chunks: list[dict[str, Any]] = []
    for chunk in state["index"]["chunks"]:
        hit = False
        for record in chunk["records"]:
            if selector["kind"] == "id" and record["id"] == selector["value"]:
                hit = True
            elif selector["kind"] == "date" and record["date"] == selector["value"]:
                hit = True
            elif selector["kind"] == "tag" and selector["value"] in record["tags"]:
                hit = True
        if hit:
            matched_chunks.append(chunk)
    require(
        len(matched_chunks) <= MAX_SELECTION_RESULTS,
        "selector_result_limit_exceeded",
        f"selector matched {len(matched_chunks)} chunks; hard cap is "
        f"{MAX_SELECTION_RESULTS}",
    )
    matches: list[str] = []
    selected_evidence: list[dict[str, Any]] = []
    for chunk in matched_chunks:
        initial_snapshot = state["chunk_snapshots_by_id"][chunk["chunk_id"]]
        selected_snapshot = snapshot_regular_file(
            state["root"],
            chunk["path"],
            field=f"chunk {chunk['chunk_id']}.path",
            mode="hash",
        )
        require(
            selected_snapshot.file_state == initial_snapshot.file_state,
            "path_race",
            f"selected chunk changed after path validation: {chunk['chunk_id']}",
        )
        require(
            selected_snapshot.sha256 == chunk["sha256"],
            "hash_drift",
            f"selected chunk hash differs: {chunk['chunk_id']}",
        )
        matches.append(chunk["path"])
        selected_evidence.append(
            {
                **snapshot_evidence(selected_snapshot),
                "expected_sha256": chunk["sha256"],
            }
        )
    revalidate_loaded_state(state)
    total_bytes_read = (
        state["active_snapshot"].bytes_read
        + state["index_snapshot"].bytes_read
        + sum(item["bytes_read"] for item in selected_evidence)
    )
    return {
        "contract": SELECTION_CONTRACT,
        "schema_version": 1,
        "carrier_id": state["locator"]["carrier_id"],
        "selector": selector,
        "hard_result_cap": MAX_SELECTION_RESULTS,
        "selected_count": len(matches),
        "chunk_paths": matches,
        "index_validated": True,
        "selected_chunk_hashes_validated": True,
        "unselected_chunk_bodies_read": False,
        "read_evidence": {
            "active": snapshot_evidence(state["active_snapshot"]),
            "index": snapshot_evidence(state["index_snapshot"]),
            "selected_chunks": selected_evidence,
            "unselected_chunk_bytes_read": 0,
            "total_bytes_read": total_bytes_read,
        },
        "chunk_body_output": False,
        "migration_performed": False,
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Read-only governance history health, validation, and lookup"
    )
    commands = root.add_subparsers(dest="command", required=True)

    def common(command: argparse.ArgumentParser) -> None:
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--active", required=True)

    health_parser = commands.add_parser("health")
    common(health_parser)
    health_parser.add_argument("--deep", action="store_true")
    health_parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    health_parser.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS)
    health_parser.add_argument(
        "--max-record-bytes", type=int, default=DEFAULT_MAX_RECORD_BYTES
    )
    health_parser.add_argument(
        "--max-attention-records", type=int, default=DEFAULT_MAX_ATTENTION_RECORDS
    )

    validate_parser = commands.add_parser("validate")
    common(validate_parser)

    select_parser = commands.add_parser("select")
    common(select_parser)
    selectors = select_parser.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--id", dest="record_id")
    selectors.add_argument("--date", dest="record_date")
    selectors.add_argument("--tag")
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "health":
        result = health(
            args.root,
            args.active,
            deep=args.deep,
            max_bytes=args.max_bytes,
            max_records=args.max_records,
            max_record_bytes=args.max_record_bytes,
            max_attention_records=args.max_attention_records,
        )
    elif args.command == "validate":
        result = validate(args.root, args.active)
    else:
        result = select(
            args.root,
            args.active,
            record_id=args.record_id,
            record_date=args.record_date,
            tag=args.tag,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceHistoryError as exc:
        print(
            json.dumps(
                {
                    "contract": ERROR_CONTRACT,
                    "ok": False,
                    "error_code": exc.code,
                    "message": str(exc),
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
