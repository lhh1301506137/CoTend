#!/usr/bin/env python3
"""Validate and resolve CoTend's impact-directed framework update route."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any


INDEX_SCHEMA = "cotend.framework-impact-index"
RESULT_CONTRACT = "cotend.framework-update-resolution.v1"
DEFAULT_INDEX = Path(__file__).resolve().parents[1] / "references" / "framework-impact-index.json"
SCOPE_ORDER = [
    "none",
    "trigger_only",
    "named_carrier",
    "active_path",
    "affected_domain",
    "full_current_mvp",
    "legacy_bounded_audit",
]
TOP_FIELDS = {
    "schema",
    "schema_version",
    "fce_owner",
    "supported_from",
    "indexed_through",
    "scope_order",
    "entries",
}
ENTRY_FIELDS = {
    "id",
    "version",
    "fce_anchor",
    "minimum_scope",
    "project_action",
    "canonical_owner",
    "named_carriers",
    "acceptance",
    "replay_policy",
    "execution",
    "supersedes",
    "ordered_after",
}
REPLAY_POLICIES = {"none", "future_trigger_only", "once_per_project", "once_if_absent"}
EXECUTION_POLICIES = {"merged", "ordered_migration"}
VERSION_RE = re.compile(r"^v1\.(\d+)$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class UpdateResolutionError(ValueError):
    """Fail-closed update-index or resolver input error."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise UpdateResolutionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_strict_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8", errors="strict"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UpdateResolutionError(f"cannot read impact index {path}: {exc}") from exc


def _version_number(value: str, *, allow_unknown: bool = False) -> int | None:
    if allow_unknown and value == "unknown":
        return None
    if not isinstance(value, str):
        raise UpdateResolutionError("version must be a string")
    match = VERSION_RE.fullmatch(value)
    if match is None:
        raise UpdateResolutionError(f"unsupported version identity: {value}")
    return int(match.group(1))


def _require_string_list(value: Any, *, label: str, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise UpdateResolutionError(f"{label} must be a string list")
    if not all(isinstance(item, str) and item.strip() == item and item for item in value):
        raise UpdateResolutionError(f"{label} contains an invalid string")
    if len(value) != len(set(value)):
        raise UpdateResolutionError(f"{label} contains duplicates")
    return list(value)


def _validate_owner(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise UpdateResolutionError(f"{label} must be a POSIX owner path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise UpdateResolutionError(f"{label} escapes its owner root")
    return value


def validate_index(path: Path) -> dict[str, Any]:
    value = read_strict_json(path)
    if not isinstance(value, dict) or set(value) != TOP_FIELDS:
        raise UpdateResolutionError("impact index top-level fields mismatch")
    if value["schema"] != INDEX_SCHEMA or value["schema_version"] != 1:
        raise UpdateResolutionError("impact index schema identity is unsupported")
    if value["scope_order"] != SCOPE_ORDER:
        raise UpdateResolutionError("impact index scope lattice drifted")
    _validate_owner(value["fce_owner"], label="fce_owner")
    supported = _version_number(value["supported_from"])
    indexed = _version_number(value["indexed_through"])
    if supported is None or indexed is None or supported > indexed:
        raise UpdateResolutionError("impact index supported range is invalid")
    entries = value["entries"]
    if not isinstance(entries, list) or not entries:
        raise UpdateResolutionError("impact index entries must be non-empty")

    ids: set[str] = set()
    versions: list[int] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        label = f"entry[{index}]"
        if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
            raise UpdateResolutionError(f"{label} fields mismatch")
        entry_id = entry["id"]
        if not isinstance(entry_id, str) or ID_RE.fullmatch(entry_id) is None:
            raise UpdateResolutionError(f"{label}.id is invalid")
        if entry_id in ids:
            raise UpdateResolutionError(f"duplicate impact entry: {entry_id}")
        ids.add(entry_id)
        by_id[entry_id] = entry
        version = _version_number(entry["version"])
        assert version is not None
        versions.append(version)
        if version < supported or version > indexed:
            raise UpdateResolutionError(f"{label}.version is outside the indexed range")
        if not isinstance(entry["fce_anchor"], str) or not entry["fce_anchor"].strip():
            raise UpdateResolutionError(f"{label}.fce_anchor is invalid")
        if entry["minimum_scope"] not in SCOPE_ORDER:
            raise UpdateResolutionError(f"{label}.minimum_scope is invalid")
        if not isinstance(entry["project_action"], str) or ID_RE.fullmatch(entry["project_action"].replace("_", "-")) is None:
            raise UpdateResolutionError(f"{label}.project_action is invalid")
        _validate_owner(entry["canonical_owner"], label=f"{label}.canonical_owner")
        _require_string_list(entry["named_carriers"], label=f"{label}.named_carriers")
        _require_string_list(entry["acceptance"], label=f"{label}.acceptance", allow_empty=False)
        if entry["replay_policy"] not in REPLAY_POLICIES:
            raise UpdateResolutionError(f"{label}.replay_policy is invalid")
        if entry["execution"] not in EXECUTION_POLICIES:
            raise UpdateResolutionError(f"{label}.execution is invalid")
        _require_string_list(entry["supersedes"], label=f"{label}.supersedes")
        _require_string_list(entry["ordered_after"], label=f"{label}.ordered_after")

    if versions != sorted(versions):
        raise UpdateResolutionError("impact entries must be ordered by version")
    if versions[0] != supported or versions[-1] != indexed:
        raise UpdateResolutionError("impact entries do not cover supported endpoints")
    for entry in entries:
        current_version = _version_number(entry["version"])
        for field in ("supersedes", "ordered_after"):
            for related in entry[field]:
                if related not in by_id:
                    raise UpdateResolutionError(f"{entry['id']} references unknown {field}: {related}")
                related_version = _version_number(by_id[related]["version"])
                if related_version is not None and current_version is not None and related_version >= current_version:
                    raise UpdateResolutionError(f"{entry['id']} {field} must reference an earlier entry")
    return value


def _scope_max(scopes: list[str]) -> str:
    return max(scopes, key=SCOPE_ORDER.index) if scopes else "none"


def _entry_action(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "change_id": entry["id"],
        "version": entry["version"],
        "action": entry["project_action"],
        "owner": entry["canonical_owner"],
        "minimum_scope": entry["minimum_scope"],
        "named_carriers": entry["named_carriers"],
        "acceptance": entry["acceptance"],
        "execution": entry["execution"],
    }


def resolve_update(
    index: dict[str, Any],
    *,
    from_version: str,
    to_version: str,
    inventory_status: str,
    state_reliability: str,
    guard_status: str,
    completed_once: set[str],
) -> dict[str, Any]:
    if inventory_status not in {"absent", "initialized", "degraded"}:
        raise UpdateResolutionError("inventory_status is invalid")
    if state_reliability not in {"reliable", "unreliable", "conflict"}:
        raise UpdateResolutionError("state_reliability is invalid")
    if guard_status not in {"clear", "human_needed", "blocked", "unknown"}:
        raise UpdateResolutionError("guard_status is invalid")
    entries: list[dict[str, Any]] = index["entries"]
    by_id = {entry["id"]: entry for entry in entries}
    unknown_receipts = sorted(completed_once - set(by_id))
    if unknown_receipts:
        raise UpdateResolutionError(f"completed_once contains unknown ids: {unknown_receipts}")

    source = _version_number(from_version, allow_unknown=True)
    target = _version_number(to_version)
    supported = _version_number(index["supported_from"])
    indexed = _version_number(index["indexed_through"])
    assert target is not None and supported is not None and indexed is not None
    guard_stop = guard_status != "clear"
    fallback_reason = "none"
    legacy_audit = False
    if source is None:
        legacy_audit = True
        fallback_reason = "unknown_from_version"
    elif source > target:
        legacy_audit = True
        fallback_reason = "version_regression_or_conflict"
    elif source < supported or target > indexed:
        legacy_audit = True
        fallback_reason = "unindexed_version_range"
    elif state_reliability != "reliable":
        legacy_audit = True
        fallback_reason = f"state_{state_reliability}"

    inventory_entry = by_id.get("v179-project-capability-inventory")
    inventory_version = (
        _version_number(inventory_entry["version"]) if inventory_entry else None
    )
    inventory_bootstrap_required = bool(
        inventory_status == "absent"
        and inventory_version is not None
        and target >= inventory_version
    )

    selected: list[dict[str, Any]] = []
    if not legacy_audit and source is not None:
        selected = [
            entry
            for entry in entries
            if source < _version_number(entry["version"]) <= target
        ]
        if inventory_bootstrap_required and inventory_entry not in selected:
            selected.append(inventory_entry)
            selected.sort(key=lambda entry: _version_number(entry["version"]))

    superseded = {item for entry in selected for item in entry["supersedes"]}
    selected = [entry for entry in selected if entry["id"] not in superseded]
    future_triggers: list[str] = []
    skipped_receipts: list[str] = []
    action_entries: list[dict[str, Any]] = []
    for entry in selected:
        policy = entry["replay_policy"]
        if policy == "future_trigger_only":
            future_triggers.append(entry["id"])
            continue
        if policy == "none" or entry["minimum_scope"] == "none":
            continue
        if policy == "once_per_project" and entry["id"] in completed_once:
            skipped_receipts.append(entry["id"])
            continue
        if policy == "once_if_absent" and inventory_status != "absent":
            skipped_receipts.append(entry["id"])
            continue
        action_entries.append(entry)

    action_entries.sort(key=lambda entry: _version_number(entry["version"]))
    actions = [_entry_action(entry) for entry in action_entries]
    scopes = [entry["minimum_scope"] for entry in action_entries]
    required_scope = "legacy_bounded_audit" if legacy_audit else _scope_max(scopes)
    loaded_owners = sorted({entry["canonical_owner"] for entry in action_entries})
    project_reads = sorted(
        {carrier for entry in action_entries for carrier in entry["named_carriers"]}
    )
    if inventory_bootstrap_required and not legacy_audit:
        if "cotend-tooling/references/workflow.md" not in loaded_owners:
            loaded_owners.append("cotend-tooling/references/workflow.md")
            loaded_owners.sort()
        if required_scope == "none":
            required_scope = "named_carrier"

    migration_required = legacy_audit or bool(actions) or inventory_bootstrap_required
    fast_path = not migration_required and not guard_stop
    result_kind = "framework_update_only" if fast_path else "migration_required"
    if legacy_audit:
        result_kind = "legacy_bounded_audit_required"
    if guard_stop:
        result_kind = "blocked_by_existing_guard"
    advance_allowed = fast_path
    return {
        "contract": RESULT_CONTRACT,
        "status": "resolved",
        "result_kind": result_kind,
        "from_version": from_version,
        "to_version": to_version,
        "impact_index_schema": index["schema_version"],
        "minimum_scope": required_scope,
        "effective_scope": required_scope,
        "selected_entries": [entry["id"] for entry in selected],
        "actions": actions,
        "loaded_owners": loaded_owners,
        "project_reads": project_reads,
        "skipped_receipts": sorted(skipped_receipts),
        "future_trigger_entries": sorted(future_triggers),
        "guard_status": guard_status,
        "guard_stop": guard_stop,
        "inventory_status": inventory_status,
        "inventory_bootstrap_required": inventory_bootstrap_required,
        "inventory_owner": (
            "cotend-tooling/references/workflow.md"
            if inventory_bootstrap_required
            else "not_loaded"
        ),
        "state_reliability": state_reliability,
        "fallback_reason": fallback_reason,
        "fast_path_no_migration": fast_path,
        "advance_allowed": advance_allowed,
        "full_adaptive_semantics": "identical",
        "writes_performed": False,
        "network_calls": 0,
        "model_calls": 0,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    resolve = subparsers.add_parser("resolve")
    resolve.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    resolve.add_argument("--from-version", required=True)
    resolve.add_argument("--to-version", required=True)
    resolve.add_argument(
        "--inventory-status",
        choices=["absent", "initialized", "degraded"],
        required=True,
    )
    resolve.add_argument(
        "--state-reliability",
        choices=["reliable", "unreliable", "conflict"],
        required=True,
    )
    resolve.add_argument(
        "--guard-status",
        choices=["clear", "human_needed", "blocked", "unknown"],
        required=True,
    )
    resolve.add_argument("--completed-once", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        index = validate_index(args.index)
        if args.command == "validate":
            payload = {
                "status": "validated",
                "schema": INDEX_SCHEMA,
                "entry_count": len(index["entries"]),
                "supported_from": index["supported_from"],
                "indexed_through": index["indexed_through"],
                "writes_performed": False,
                "network_calls": 0,
            }
        else:
            payload = resolve_update(
                index,
                from_version=args.from_version,
                to_version=args.to_version,
                inventory_status=args.inventory_status,
                state_reliability=args.state_reliability,
                guard_status=args.guard_status,
                completed_once=set(args.completed_once),
            )
    except (UpdateResolutionError, OSError, TypeError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
