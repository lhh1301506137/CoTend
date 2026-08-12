#!/usr/bin/env python3
"""Validate and resolve the CoTend framework impact index without project writes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


INDEX_SCHEMA = "cotend.framework-impact-index"
RESOLUTION_CONTRACT = "cotend.framework-update-resolution.v2"
FRAMEWORK_STATE_CONTRACT = "cotend.framework-update-state.v2"
LEGACY_FRAMEWORK_STATE_CONTRACT = "legacy_applied_through"
FRAMEWORK_STATE_CONTRACTS = {
    FRAMEWORK_STATE_CONTRACT,
    LEGACY_FRAMEWORK_STATE_CONTRACT,
}
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = SKILL_ROOT / "references" / "framework-impact-index.json"

SCOPE_ORDER = (
    "none",
    "trigger_only",
    "named_carrier",
    "active_path",
    "affected_domain",
    "full_current_mvp",
    "legacy_bounded_audit",
)
REPLAY_POLICIES = {
    "none",
    "future_trigger_only",
    "once_per_project",
    "once_if_absent",
}
EXECUTION_POLICIES = {"merged", "ordered_migration"}
STATE_RELIABILITIES = {"reliable", "unreliable", "conflict"}
INVENTORY_STATUSES = {"absent", "initialized", "degraded"}
GUARD_STATUSES = {"clear", "human_needed", "blocked", "unknown"}
REQUIRED_RECEIPT_SCOPES = {"full_current_mvp"}
PROJECT_ACTIONS = {
    "ensure_governance_language_resolution",
    "activate_actual_byte_gate_on_next_governance_write",
    "defer_same_primary_handoff_until_explicit_trigger",
    "require_literal_session_handoff_invocation",
    "apply_current_execution_authorization_contract",
    "normalize_continuous_risk_selection",
    "reconstruct_current_mvp_once",
    "defer_failure_memory_until_relevant_failure_trigger",
    "defer_provider_and_failure_contract_until_trigger",
    "use_thinner_current_framework_contract",
    "maintain_project_agents_router_block",
    "defer_tooling_reuse_decision_until_concrete_need",
    "defer_solution_adequacy_until_material_route_trigger",
    "delegate_tooling_inventory_once_if_absent",
    "apply_coherence_sized_execution_on_active_route",
    "apply_outcome_triggered_governance_on_active_route",
    "defer_traceable_tooling_refresh_until_actual_trigger",
    "defer_adaptive_development_experience_until_actual_trigger",
    "defer_project_intelligence_design_refresh_until_actual_trigger",
    "defer_governance_carrier_lifecycle_until_actual_trigger",
    "use_converged_init_contract",
    "use_current_managed_skill_inventory",
    "use_framework_compatibility_receipt_v2",
    "use_scoped_collaboration_authority",
    "defer_project_intelligence_until_actual_trigger",
    "defer_execution_closure_successor_until_actual_trigger",
    "defer_adapter_and_mode_shards_until_actual_trigger",
    "defer_understanding_interface_until_material_trigger",
    "defer_understanding_artifact_validation_until_material_trigger",
    "defer_understanding_artifact_v3_until_material_trigger",
    "defer_understanding_artifact_v4_until_material_trigger",
}

TOP_LEVEL_FIELDS = {
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
VERSION_RE = re.compile(r"^v([1-9][0-9]*)\.([0-9]+)$")
ID_RE = re.compile(r"^v[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")


class ImpactContractError(ValueError):
    """Fail-closed impact-index or resolution error."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ImpactContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_strict_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8", errors="strict"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ImpactContractError(f"cannot read strict JSON {path}: {exc}") from exc


def _require_exact_fields(
    value: dict[str, Any], expected: set[str], *, label: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ImpactContractError(
            f"{label} fields mismatch: "
            f"missing={sorted(expected - actual)}, unknown={sorted(actual - expected)}"
        )


def _parse_version(value: Any, *, label: str) -> tuple[int, int]:
    if not isinstance(value, str):
        raise ImpactContractError(f"{label} must be a vMAJOR.MINOR string")
    match = VERSION_RE.fullmatch(value)
    if match is None:
        raise ImpactContractError(f"{label} must be a vMAJOR.MINOR string: {value!r}")
    return int(match.group(1)), int(match.group(2))


def _require_string_list(value: Any, *, label: str, allow_empty: bool) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a list" if allow_empty else "a non-empty list"
        raise ImpactContractError(f"{label} must be {qualifier}")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ImpactContractError(f"{label} must contain non-empty strings")
    if len(value) != len(set(value)):
        raise ImpactContractError(f"{label} must not contain duplicates")
    return value


def _validate_no_order_cycle(entries: list[dict[str, Any]]) -> None:
    edges = {entry["id"]: set(entry["ordered_after"]) for entry in entries}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ImpactContractError("ordered_after contains a cycle")
        if node in visited:
            return
        visiting.add(node)
        for dependency in edges[node]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in edges:
        visit(node)


def validate_index_data(value: Any, *, fce_path: Path | None = None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ImpactContractError("impact index root must be an object")
    _require_exact_fields(value, TOP_LEVEL_FIELDS, label="impact index")
    if value["schema"] != INDEX_SCHEMA:
        raise ImpactContractError(f"impact index schema must be {INDEX_SCHEMA}")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ImpactContractError("impact index schema_version must be 1")
    if value["fce_owner"] != "FRAMEWORK-CHANGE-EVAL.md":
        raise ImpactContractError("fce_owner must remain FRAMEWORK-CHANGE-EVAL.md")
    if value["scope_order"] != list(SCOPE_ORDER):
        raise ImpactContractError(
            "scope_order must preserve the canonical scope lattice"
        )

    supported_from = _parse_version(value["supported_from"], label="supported_from")
    indexed_through = _parse_version(value["indexed_through"], label="indexed_through")
    entries = value["entries"]
    if not isinstance(entries, list) or not entries:
        raise ImpactContractError("entries must be a non-empty list")

    ids: set[str] = set()
    versions: list[tuple[int, int]] = []
    anchors: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    positions: dict[str, int] = {}
    for position, entry in enumerate(entries):
        label = f"entries[{position}]"
        if not isinstance(entry, dict):
            raise ImpactContractError(f"{label} must be an object")
        _require_exact_fields(entry, ENTRY_FIELDS, label=label)
        entry_id = entry["id"]
        if not isinstance(entry_id, str) or ID_RE.fullmatch(entry_id) is None:
            raise ImpactContractError(f"{label}.id must be a stable normalized id")
        if entry_id in ids:
            raise ImpactContractError(f"duplicate entry id: {entry_id}")
        ids.add(entry_id)
        by_id[entry_id] = entry
        positions[entry_id] = position

        version = _parse_version(entry["version"], label=f"{label}.version")
        versions.append(version)
        if not supported_from <= version <= indexed_through:
            raise ImpactContractError(f"{entry_id} version is outside index bounds")
        anchor = entry["fce_anchor"]
        if not isinstance(anchor, str) or not anchor.startswith("## "):
            raise ImpactContractError(f"{entry_id}.fce_anchor must be an exact heading")
        if anchor in anchors:
            raise ImpactContractError(f"duplicate fce_anchor: {anchor}")
        anchors.add(anchor)

        if entry["minimum_scope"] not in SCOPE_ORDER:
            raise ImpactContractError(f"{entry_id}.minimum_scope is invalid")
        if entry["project_action"] not in PROJECT_ACTIONS:
            raise ImpactContractError(f"{entry_id}.project_action is not recognized")
        owner = entry["canonical_owner"]
        if (
            not isinstance(owner, str)
            or not owner
            or "\\" in owner
            or ".." in owner.split("/")
            or owner.startswith(("/", "~"))
        ):
            raise ImpactContractError(f"{entry_id}.canonical_owner must be a safe path")

        _require_string_list(
            entry["named_carriers"],
            label=f"{entry_id}.named_carriers",
            allow_empty=True,
        )
        _require_string_list(
            entry["acceptance"],
            label=f"{entry_id}.acceptance",
            allow_empty=False,
        )
        _require_string_list(
            entry["supersedes"],
            label=f"{entry_id}.supersedes",
            allow_empty=True,
        )
        _require_string_list(
            entry["ordered_after"],
            label=f"{entry_id}.ordered_after",
            allow_empty=True,
        )
        if entry["replay_policy"] not in REPLAY_POLICIES:
            raise ImpactContractError(f"{entry_id}.replay_policy is invalid")
        if entry["execution"] not in EXECUTION_POLICIES:
            raise ImpactContractError(f"{entry_id}.execution is invalid")
        if entry["replay_policy"] == "none" and entry["minimum_scope"] != "none":
            raise ImpactContractError(f"{entry_id} replay none requires scope none")
        if (
            entry["replay_policy"] == "future_trigger_only"
            and entry["minimum_scope"] != "trigger_only"
        ):
            raise ImpactContractError(
                f"{entry_id} future_trigger_only requires scope trigger_only"
            )
        if (
            entry["replay_policy"] == "once_if_absent"
            and entry["project_action"] != "delegate_tooling_inventory_once_if_absent"
        ):
            raise ImpactContractError(
                f"{entry_id} once_if_absent is reserved for capability inventory"
            )
        if entry["execution"] == "ordered_migration" and not entry["ordered_after"]:
            raise ImpactContractError(
                f"{entry_id} ordered_migration requires ordered_after"
            )
        if (
            entry["minimum_scope"] in REQUIRED_RECEIPT_SCOPES
            and entry["replay_policy"] != "once_per_project"
        ):
            raise ImpactContractError(
                f"{entry_id} {entry['minimum_scope']} requires once_per_project"
            )

    if versions != sorted(versions):
        raise ImpactContractError("entries must be sorted by version")
    if versions[0] != supported_from:
        raise ImpactContractError("supported_from must match the first indexed version")
    if versions[-1] != indexed_through:
        raise ImpactContractError("indexed_through must match the last indexed version")
    for predecessor, successor in zip(versions, versions[1:]):
        same_major_next_minor = (
            successor[0] == predecessor[0]
            and successor[1] == predecessor[1] + 1
        )
        next_major_zero = (
            successor[0] == predecessor[0] + 1 and successor[1] == 0
        )
        if not (same_major_next_minor or next_major_zero):
            raise ImpactContractError(
                "entries must provide contiguous version coverage from "
                "supported_from through indexed_through"
            )

    scope_ranks = {scope: index for index, scope in enumerate(SCOPE_ORDER)}
    superseded_by: dict[str, str] = {}
    for entry in entries:
        entry_version = _parse_version(entry["version"], label=entry["id"])
        for relation in (*entry["supersedes"], *entry["ordered_after"]):
            if relation == entry["id"] or relation not in by_id:
                raise ImpactContractError(
                    f"{entry['id']} references missing/self relation {relation}"
                )
            relation_version = _parse_version(
                by_id[relation]["version"], label=relation
            )
            if relation_version > entry_version:
                raise ImpactContractError(
                    f"{entry['id']} relation {relation} points to a later version"
                )
            if positions[relation] >= positions[entry["id"]]:
                raise ImpactContractError(
                    f"{entry['id']} relation {relation} must point to an earlier entry"
                )
        for relation in entry["supersedes"]:
            existing_superseder = superseded_by.get(relation)
            if existing_superseder is not None:
                raise ImpactContractError(
                    f"{relation} has multiple superseders: "
                    f"{existing_superseder}, {entry['id']}"
                )
            superseded_by[relation] = entry["id"]
            if (
                scope_ranks[entry["minimum_scope"]]
                < scope_ranks[by_id[relation]["minimum_scope"]]
            ):
                raise ImpactContractError(
                    f"{entry['id']} cannot supersede {relation} with a smaller scope"
                )
        if entry["execution"] == "ordered_migration":
            for dependency in entry["ordered_after"]:
                if by_id[dependency]["replay_policy"] in {
                    "none",
                    "future_trigger_only",
                }:
                    raise ImpactContractError(
                        f"{entry['id']} ordered dependency {dependency} is not a "
                        "project migration"
                    )
    _validate_no_order_cycle(entries)

    if fce_path is not None:
        try:
            fce = fce_path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as exc:
            raise ImpactContractError(f"cannot read FCE {fce_path}: {exc}") from exc
        fce_lines = fce.splitlines()
        for anchor in anchors:
            if fce_lines.count(anchor) != 1:
                raise ImpactContractError(
                    f"FCE anchor must occur exactly once: {anchor}"
                )
    return value


def validate_index(path: Path, *, fce_path: Path | None = None) -> dict[str, Any]:
    return validate_index_data(read_strict_json(path), fce_path=fce_path)


def _scope_max(scopes: Iterable[str]) -> str:
    ranks = {scope: index for index, scope in enumerate(SCOPE_ORDER)}
    return max(scopes, key=ranks.__getitem__, default="none")


def _apply_requested_scope(
    minimum: str,
    requested: str | None,
    widened_scope_reason: str | None,
) -> tuple[str, str]:
    effective = minimum if requested is None else requested
    if effective not in SCOPE_ORDER:
        raise ImpactContractError(f"requested_scope is invalid: {effective}")
    ranks = {scope: index for index, scope in enumerate(SCOPE_ORDER)}
    if ranks[effective] < ranks[minimum]:
        raise ImpactContractError(
            f"requested scope cannot narrow index minimum {minimum} to {effective}"
        )
    reason = (widened_scope_reason or "none").strip() or "none"
    if ranks[effective] > ranks[minimum] and reason.casefold() == "none":
        raise ImpactContractError("widening the index scope requires project evidence")
    if ranks[effective] == ranks[minimum] and reason.casefold() != "none":
        raise ImpactContractError(
            "widened_scope_reason is allowed only for a wider scope"
        )
    return effective, reason


def _inventory_bootstrap_required(
    index: dict[str, Any], *, target: str, inventory_status: str
) -> bool:
    if inventory_status != "absent":
        return False
    target_version = _parse_version(target, label="to_version")
    return any(
        entry["replay_policy"] == "once_if_absent"
        and _parse_version(entry["version"], label=entry["id"]) <= target_version
        for entry in index["entries"]
    )


def _apply_guard_status(result: dict[str, Any], *, guard_status: str) -> dict[str, Any]:
    result["guard_status"] = guard_status
    result["guard_stop"] = guard_status != "clear"
    result["guard_owner_resolution_required"] = guard_status != "clear"
    result["stop_reason"] = (
        "none" if guard_status == "clear" else f"existing_guard_{guard_status}"
    )
    if guard_status != "clear":
        result["advance_allowed"] = False
        result["fast_path_no_migration"] = False
    return result


def _framework_state_before(
    *,
    framework_state_contract: str,
    compatibility_checked_through: str,
    last_material_project_migration: str,
) -> dict[str, str]:
    if framework_state_contract not in FRAMEWORK_STATE_CONTRACTS:
        raise ImpactContractError(
            "framework_state_contract is invalid: " f"{framework_state_contract!r}"
        )
    if compatibility_checked_through != "unknown":
        compatibility = _parse_version(
            compatibility_checked_through,
            label="compatibility_checked_through",
        )
    else:
        compatibility = None
    if last_material_project_migration != "unknown":
        material = _parse_version(
            last_material_project_migration,
            label="last_material_project_migration",
        )
        if compatibility is None:
            raise ImpactContractError(
                "a material migration anchor requires a known compatibility anchor"
            )
        if material > compatibility:
            raise ImpactContractError(
                "last_material_project_migration cannot be newer than "
                "compatibility_checked_through"
            )
        material_basis = (
            "canonical_v2_state"
            if framework_state_contract == FRAMEWORK_STATE_CONTRACT
            else "legacy_verified_migration_receipt"
        )
    else:
        material_basis = "unknown"
    return {
        "contract": framework_state_contract,
        "compatibility_checked_through": compatibility_checked_through,
        "compatibility_basis": (
            "canonical_v2_state"
            if framework_state_contract == FRAMEWORK_STATE_CONTRACT
            else "legacy_applied_through"
        ),
        "last_material_project_migration": last_material_project_migration,
        "material_migration_basis": material_basis,
    }


def _finalize_framework_state_transition(
    result: dict[str, Any],
    *,
    framework_state_contract: str,
    last_material_project_migration: str,
) -> dict[str, Any]:
    state_before = _framework_state_before(
        framework_state_contract=framework_state_contract,
        compatibility_checked_through=result["from_version"],
        last_material_project_migration=last_material_project_migration,
    )
    material_required = (
        result["status"] == "routed" and result["project_migration_required"]
    )
    transition_required = (
        framework_state_contract != FRAMEWORK_STATE_CONTRACT
        or result["from_version"] != result["to_version"]
        or material_required
    )
    guard_clear = result["guard_status"] == "clear"
    routed = result["status"] == "routed"

    if not guard_clear:
        receipt_status = "blocked"
        checked_range_status = "blocked"
        write_ready = False
        advance_condition = "resolve_existing_stop_before_state_transition"
    elif not routed:
        receipt_status = "audit_required"
        checked_range_status = "audit_required"
        write_ready = False
        advance_condition = "complete_bounded_audit_then_resolve_again"
    elif material_required:
        receipt_status = "deferred_until_material_migration_and_acceptance"
        checked_range_status = "checked"
        write_ready = False
        advance_condition = (
            "complete_selected_actions_acceptance_and_actual_byte_validation"
        )
    elif not result["advance_allowed"]:
        receipt_status = "deferred_until_scope_validation"
        checked_range_status = "checked"
        write_ready = False
        advance_condition = (
            "complete_widened_scope_validation_and_actual_byte_validation"
        )
    elif transition_required:
        receipt_status = "write_required"
        checked_range_status = "checked"
        write_ready = True
        advance_condition = "persist_and_validate_actual_compatibility_receipt_bytes"
        result["advance_allowed"] = False
        result["advance_requires_acceptance"] = True
    else:
        receipt_status = "already_current"
        checked_range_status = "already_current"
        write_ready = False
        advance_condition = "none"

    result["framework_loaded"] = result["to_version"]
    result["checked_range"] = {
        "from_exclusive": result["from_version"],
        "through_inclusive": result["to_version"],
        "status": checked_range_status,
    }
    result["framework_state_before"] = state_before
    result["material_project_changes"] = (
        "required" if material_required else "pending_audit" if not routed else "none"
    )
    result["compatibility_receipt"] = {
        "contract": FRAMEWORK_STATE_CONTRACT,
        "status": receipt_status,
        "transition_required": transition_required,
        "write_ready": write_ready,
        "existing_carrier_only": True,
        "compatibility_checked_through_on_success": (
            result["to_version"] if routed and guard_clear else result["from_version"]
        ),
        "last_material_project_migration_on_success": (
            result["to_version"]
            if material_required and guard_clear
            else last_material_project_migration
        ),
        "advance_condition": advance_condition,
    }
    return result


def _legacy_resolution(
    *,
    index: dict[str, Any],
    from_version: str,
    to_version: str,
    reason: str,
    requested_scope: str | None,
    widened_scope_reason: str | None,
    inventory_status: str,
    guard_status: str,
) -> dict[str, Any]:
    effective, widen_reason = _apply_requested_scope(
        "legacy_bounded_audit", requested_scope, widened_scope_reason
    )
    inventory_required = _inventory_bootstrap_required(
        index, target=to_version, inventory_status=inventory_status
    )
    result = {
        "contract": RESOLUTION_CONTRACT,
        "status": "legacy_bounded_audit",
        "from_version": from_version,
        "to_version": to_version,
        "impact_index_schema": index["schema_version"],
        "required_scope": effective,
        "widened_scope_reason": widen_reason,
        "fallback_reason": reason,
        "advance_allowed": False,
        "advance_requires_acceptance": True,
        "project_migration_required": True,
        "fast_path_no_migration": False,
        "inventory_bootstrap_required": inventory_required,
        "inventory_bootstrap_timing": (
            "after_legacy_audit_and_existing_guards"
            if inventory_required
            else "not_applicable"
        ),
        "preflight_reads": [
            "compact framework_update, capability_inventory, canonical language, and pending-gate state in STATUS.md|mapped carrier",
            "cotend-project-init/references/framework-impact-index.json",
        ],
        "project_reads": [
            "bounded active truth, current-MVP owners, pending gates, and version evidence"
        ],
        "loaded_owners": [
            "cotend-project-init/references/framework-update-routing.md"
        ],
        "framework_only_changes": [],
        "deferred_triggers": [],
        "skipped_changes": [],
        "merged_actions": [],
        "ordered_actions": [],
        "full_adaptive_result_invariant": True,
    }
    return _apply_guard_status(result, guard_status=guard_status)


def _unique(items: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _topologically_order_entries(
    entries: list[dict[str, Any]],
    *,
    effective_dependencies: dict[str, list[str]],
) -> list[dict[str, Any]]:
    ordered_ids = {entry["id"] for entry in entries}
    remaining = list(entries)
    emitted: set[str] = set()
    result: list[dict[str, Any]] = []
    while remaining:
        ready = [
            entry
            for entry in remaining
            if all(
                dependency not in ordered_ids or dependency in emitted
                for dependency in effective_dependencies[entry["id"]]
            )
        ]
        if not ready:
            raise ImpactContractError(
                "ordered migrations cannot be topologically sorted"
            )
        for entry in ready:
            result.append(entry)
            emitted.add(entry["id"])
            remaining.remove(entry)
    return result


def resolve_update(
    index: dict[str, Any],
    *,
    from_version: str,
    to_version: str | None = None,
    completed_once: Iterable[str] = (),
    inventory_status: str = "absent",
    state_reliability: str = "reliable",
    guard_status: str = "unknown",
    framework_state_contract: str = LEGACY_FRAMEWORK_STATE_CONTRACT,
    last_material_project_migration: str = "unknown",
    requested_scope: str | None = None,
    widened_scope_reason: str | None = None,
) -> dict[str, Any]:
    validate_index_data(index)
    target = to_version or index["indexed_through"]
    if inventory_status not in INVENTORY_STATUSES:
        raise ImpactContractError(f"inventory_status is invalid: {inventory_status}")
    if state_reliability not in STATE_RELIABILITIES:
        raise ImpactContractError(f"state_reliability is invalid: {state_reliability}")
    if guard_status not in GUARD_STATUSES:
        raise ImpactContractError(f"guard_status is invalid: {guard_status}")
    _framework_state_before(
        framework_state_contract=framework_state_contract,
        compatibility_checked_through=from_version,
        last_material_project_migration=last_material_project_migration,
    )

    def finalize(result: dict[str, Any]) -> dict[str, Any]:
        return _finalize_framework_state_transition(
            result,
            framework_state_contract=framework_state_contract,
            last_material_project_migration=last_material_project_migration,
        )

    def legacy(**kwargs: Any) -> dict[str, Any]:
        return finalize(_legacy_resolution(**kwargs))

    target_version = _parse_version(target, label="to_version")
    if state_reliability != "reliable":
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason=f"framework_update_state_{state_reliability}",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )
    if from_version == "unknown":
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason="from_version_unknown",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )

    source_version = _parse_version(from_version, label="from_version")
    supported = _parse_version(index["supported_from"], label="supported_from")
    indexed = _parse_version(index["indexed_through"], label="indexed_through")
    known_versions = {
        _parse_version(entry["version"], label=entry["id"])
        for entry in index["entries"]
    }
    if source_version < supported:
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason="from_version_before_supported_baseline",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )
    if source_version not in known_versions or target_version not in known_versions:
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason="version_not_covered_by_index",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )
    if source_version > target_version or target_version > indexed:
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason="version_anchor_conflict",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )

    completed = set(completed_once)
    known_ids = {entry["id"] for entry in index["entries"]}
    unknown_receipts = sorted(completed - known_ids)
    if unknown_receipts:
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason="completed_once_receipt_not_in_index",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )
    once_per_project_ids = {
        entry["id"]
        for entry in index["entries"]
        if entry["replay_policy"] == "once_per_project"
    }
    invalid_policy_receipts = sorted(completed - once_per_project_ids)
    if invalid_policy_receipts:
        return legacy(
            index=index,
            from_version=from_version,
            to_version=target,
            reason="completed_once_receipt_not_once_per_project",
            requested_scope=requested_scope,
            widened_scope_reason=widened_scope_reason,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )

    selected = [
        entry
        for entry in index["entries"]
        if source_version
        < _parse_version(entry["version"], label=entry["id"])
        <= target_version
    ]
    if inventory_status == "absent":
        selected_ids = {entry["id"] for entry in selected}
        selected.extend(
            entry
            for entry in index["entries"]
            if entry["replay_policy"] == "once_if_absent"
            and _parse_version(entry["version"], label=entry["id"]) <= target_version
            and entry["id"] not in selected_ids
        )
        selected.sort(
            key=lambda entry: _parse_version(entry["version"], label=entry["id"])
        )
    selected_ids = {entry["id"] for entry in selected}
    selected.extend(
        entry
        for entry in index["entries"]
        if entry["replay_policy"] == "once_per_project"
        and entry["minimum_scope"] in REQUIRED_RECEIPT_SCOPES
        and _parse_version(entry["version"], label=entry["id"]) <= target_version
        and entry["id"] not in completed
        and entry["id"] not in selected_ids
    )
    selected.sort(key=lambda entry: _parse_version(entry["version"], label=entry["id"]))
    superseded_by_selected = {
        superseded_id: entry["id"]
        for entry in selected
        for superseded_id in entry["supersedes"]
    }
    superseded = set(superseded_by_selected)

    def canonical_selected_change(change_id: str) -> str:
        seen: set[str] = set()
        current = change_id
        while current in superseded_by_selected:
            if current in seen:
                raise ImpactContractError(
                    "selected supersedes relation contains a cycle"
                )
            seen.add(current)
            current = superseded_by_selected[current]
        return current

    selected = [entry for entry in selected if entry["id"] not in superseded]

    framework_only: list[str] = []
    deferred: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = [
        {"change_id": change_id, "reason": "superseded_by_later_index_entry"}
        for change_id in sorted(superseded)
    ]
    actionable: list[dict[str, Any]] = []
    for entry in selected:
        replay = entry["replay_policy"]
        if replay == "none":
            framework_only.append(entry["id"])
        elif replay == "future_trigger_only":
            deferred.append(
                {
                    "change_id": entry["id"],
                    "owner": entry["canonical_owner"],
                    "future_action": entry["project_action"],
                    "ordered_after": entry["ordered_after"],
                    "acceptance": entry["acceptance"],
                }
            )
        elif replay == "once_per_project" and entry["id"] in completed:
            skipped.append(
                {"change_id": entry["id"], "reason": "completed_once_receipt"}
            )
        elif replay == "once_if_absent" and inventory_status != "absent":
            skipped.append(
                {
                    "change_id": entry["id"],
                    "reason": f"capability_inventory_marker_{inventory_status}",
                }
            )
        else:
            actionable.append(entry)

    minimum_scope = _scope_max(
        [entry["minimum_scope"] for entry in actionable]
        + (["trigger_only"] if deferred else [])
    )
    effective_scope, widen_reason = _apply_requested_scope(
        minimum_scope, requested_scope, widened_scope_reason
    )
    if effective_scope == "legacy_bounded_audit":
        audit = _legacy_resolution(
            index=index,
            from_version=from_version,
            to_version=target,
            reason=(
                "project_evidence_requires_legacy_bounded_audit"
                if widen_reason != "none"
                else "impact_index_requires_legacy_bounded_audit"
            ),
            requested_scope=None,
            widened_scope_reason=None,
            inventory_status=inventory_status,
            guard_status=guard_status,
        )
        audit["widened_scope_reason"] = widen_reason
        return finalize(audit)

    raw_ordered_entries = [
        entry for entry in actionable if entry["execution"] == "ordered_migration"
    ]
    effective_dependencies = {
        entry["id"]: _unique(
            canonical_selected_change(dependency)
            for dependency in entry["ordered_after"]
        )
        for entry in raw_ordered_entries
    }
    ordered_entries = _topologically_order_entries(
        raw_ordered_entries,
        effective_dependencies=effective_dependencies,
    )
    merged_entries = [entry for entry in actionable if entry["execution"] == "merged"]
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in merged_entries:
        groups.setdefault(entry["canonical_owner"], []).append(entry)
    merged_actions = [
        {
            "canonical_owner": owner,
            "change_ids": [entry["id"] for entry in entries],
            "minimum_scope": _scope_max(entry["minimum_scope"] for entry in entries),
            "project_actions": [entry["project_action"] for entry in entries],
            "named_carriers": _unique(
                carrier for entry in entries for carrier in entry["named_carriers"]
            ),
            "acceptance": _unique(
                item for entry in entries for item in entry["acceptance"]
            ),
        }
        for owner, entries in groups.items()
    ]
    actionable_ids = {entry["id"] for entry in actionable}
    ordered_actions = [
        {
            "canonical_owner": entry["canonical_owner"],
            "change_id": entry["id"],
            "minimum_scope": entry["minimum_scope"],
            "project_action": entry["project_action"],
            "named_carriers": entry["named_carriers"],
            "acceptance": entry["acceptance"],
            "ordered_after": entry["ordered_after"],
            "effective_ordered_after": effective_dependencies[entry["id"]],
            "dependency_status": {
                original_dependency: (
                    f"superseded_by_selected_action:{dependency}"
                    if dependency != original_dependency
                    and dependency in actionable_ids
                    else f"superseded_by_completed_receipt:{dependency}"
                    if dependency != original_dependency and dependency in completed
                    else "selected_action"
                    if dependency in actionable_ids
                    else "completed_once_receipt"
                    if dependency in completed
                    else "applied_through_baseline"
                )
                for original_dependency, dependency in (
                    (
                        original_dependency,
                        canonical_selected_change(original_dependency),
                    )
                    for original_dependency in entry["ordered_after"]
                )
            },
        }
        for entry in ordered_entries
    ]
    carriers = _unique(
        carrier for entry in actionable for carrier in entry["named_carriers"]
    )
    project_reads = list(carriers)
    if effective_scope in {"active_path", "affected_domain", "full_current_mvp"}:
        project_reads.append(
            {
                "active_path": "current leaf and direct upstream/downstream",
                "affected_domain": "affected L1/L2 domain and dependency path",
                "full_current_mvp": "current-MVP active truth and direct dependencies",
            }[effective_scope]
        )
    loaded_owners = _unique([entry["canonical_owner"] for entry in actionable])
    work_required = bool(actionable) or effective_scope not in {
        "none",
        "trigger_only",
    }
    inventory_required = _inventory_bootstrap_required(
        index, target=target, inventory_status=inventory_status
    )
    result = {
        "contract": RESOLUTION_CONTRACT,
        "status": "routed",
        "from_version": from_version,
        "to_version": target,
        "impact_index_schema": index["schema_version"],
        "required_scope": effective_scope,
        "index_minimum_scope": minimum_scope,
        "widened_scope_reason": widen_reason,
        "fallback_reason": "none",
        "advance_allowed": not work_required,
        "advance_requires_acceptance": work_required,
        "project_migration_required": bool(actionable),
        "fast_path_no_migration": not actionable
        and effective_scope in {"none", "trigger_only"},
        "inventory_bootstrap_required": inventory_required,
        "inventory_bootstrap_timing": (
            "selected_action" if inventory_required else "not_applicable"
        ),
        "preflight_reads": [
            "compact framework_update, capability_inventory, canonical language, and pending-gate state in STATUS.md|mapped carrier",
            "cotend-project-init/references/framework-impact-index.json",
        ],
        "project_reads": project_reads,
        "loaded_owners": loaded_owners,
        "framework_only_changes": framework_only,
        "deferred_triggers": deferred,
        "skipped_changes": skipped,
        "merged_actions": merged_actions,
        "ordered_actions": ordered_actions,
        "full_adaptive_result_invariant": True,
    }
    return finalize(_apply_guard_status(result, guard_status=guard_status))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate or resolve the read-only CoTend framework impact index."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    validate.add_argument("--fce", type=Path)

    resolve = commands.add_parser("resolve")
    resolve.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    resolve.add_argument("--from-version", required=True)
    resolve.add_argument("--to-version")
    resolve.add_argument("--completed-once", action="append", default=[])
    resolve.add_argument(
        "--inventory-status", choices=sorted(INVENTORY_STATUSES), default="absent"
    )
    resolve.add_argument(
        "--state-reliability",
        choices=sorted(STATE_RELIABILITIES),
        default="reliable",
    )
    resolve.add_argument(
        "--guard-status",
        choices=sorted(GUARD_STATUSES),
        required=True,
        help=(
            "Existing compact language/human/safety/integrity guard state; "
            "missing fields are unknown, never clear."
        ),
    )
    resolve.add_argument(
        "--framework-state-contract",
        choices=sorted(FRAMEWORK_STATE_CONTRACTS),
        default=LEGACY_FRAMEWORK_STATE_CONTRACT,
        help=(
            "Use the canonical v2 contract when the project already stores both "
            "anchors; omitted legacy state treats --from-version only as the "
            "compatibility seed."
        ),
    )
    resolve.add_argument(
        "--last-material-project-migration",
        default="unknown",
        help=(
            "A vMAJOR.MINOR anchor backed by canonical v2 state or a separate "
            "legacy migration receipt; never infer it from applied_through."
        ),
    )
    resolve.add_argument("--requested-scope", choices=SCOPE_ORDER)
    resolve.add_argument("--widened-scope-reason")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        index = validate_index(
            args.index,
            fce_path=args.fce if args.command == "validate" else None,
        )
        if args.command == "validate":
            result: dict[str, Any] = {
                "contract": INDEX_SCHEMA,
                "status": "valid",
                "schema_version": index["schema_version"],
                "supported_from": index["supported_from"],
                "indexed_through": index["indexed_through"],
                "entry_count": len(index["entries"]),
                "fce_anchors_checked": args.fce is not None,
            }
        else:
            result = resolve_update(
                index,
                from_version=args.from_version,
                to_version=args.to_version,
                completed_once=args.completed_once,
                inventory_status=args.inventory_status,
                state_reliability=args.state_reliability,
                guard_status=args.guard_status,
                framework_state_contract=args.framework_state_contract,
                last_material_project_migration=(args.last_material_project_migration),
                requested_scope=args.requested_scope,
                widened_scope_reason=args.widened_scope_reason,
            )
    except ImpactContractError as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
