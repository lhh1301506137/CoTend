#!/usr/bin/env python3
"""Validate and query the bounded CoTend capability catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable


CATALOG_SCHEMA = "cotend.capability-catalog"
SELECTION_CONTRACT = "cotend.capability-selection.v1"
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = SKILL_ROOT / "references" / "capability-catalog.json"

TOP_LEVEL_FIELDS = {"schema", "schema_version", "records"}
RECORD_FIELDS = {
    "id",
    "name",
    "kind",
    "tasks",
    "capabilities",
    "stacks",
    "platforms",
    "relationship",
    "eligible_routes",
    "review_state",
    "adoption_disposition",
    "runtime_state",
    "freshness",
    "evidence_levels",
    "risk_band",
    "maintenance_burden",
    "cost_band",
    "rollback_band",
    "source_pointer",
    "research_pointers",
}
SOURCE_POINTER_FIELDS = {"path", "heading"}
FORBIDDEN_AUTHORITY_FIELDS = {
    "license",
    "license_claim",
    "license_spdx",
    "version",
    "version_or_commit",
    "commit",
    "url",
    "source_url",
    "canonical_url",
}

KINDS = {
    "article",
    "cli",
    "framework",
    "github_project",
    "library",
    "mcp",
    "plugin",
    "service",
    "skill",
}
RELATIONSHIPS = {
    "bundled_or_adapted",
    "external_runtime",
    "reference_only",
    "self_maintained",
    "source_evidence",
    "source_review_pending",
}
ELIGIBLE_ROUTES = {"adapt", "call", "compose"}
REVIEW_STATES = {
    "lead",
    "canonical_source_checked",
    "source_behavior_checked",
    "local_validation_checked",
    "project_evidence_checked",
}
ADOPTION_DISPOSITIONS = {
    "unreviewed",
    "adopt_full",
    "adopt_partial",
    "defer",
    "reject",
}
RUNTIME_STATES = {
    "not_installed",
    "installed_disabled",
    "available",
    "enabled",
    "not_applicable",
    "retired",
    "unknown",
}
FRESHNESS_STATES = {"unknown", "current", "review_due", "stale"}
EVIDENCE_LEVELS = {
    "article_claim",
    "readme_claim",
    "source_proven",
    "local_validation",
    "project_evidence",
}
RISK_BANDS = {"low", "medium", "high", "unknown"}
MAINTENANCE_BANDS = {"low", "medium", "high", "unknown"}
COST_BANDS = {"free", "paid", "mixed", "unknown"}
ROLLBACK_BANDS = {"easy", "bounded", "hard", "unknown"}
GENERIC_QUERY_TERMS = {
    "ai",
    "build",
    "capability",
    "code",
    "development",
    "framework",
    "library",
    "project",
    "software",
    "tool",
    "tooling",
    "workflow",
}
SLUG = re.compile(r"^[a-z0-9][a-z0-9.+#-]*$")
RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "unknown": 3}
MAINTENANCE_ORDER = {"low": 0, "medium": 1, "high": 2, "unknown": 3}


class CatalogError(ValueError):
    """Fail-closed catalog validation error."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_strict_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8", errors="strict"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CatalogError(f"cannot read strict JSON catalog {path}: {exc}") from exc


def _require_exact_fields(
    value: dict[str, Any], expected: set[str], *, label: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise CatalogError(
            f"{label} fields mismatch: missing={sorted(expected - actual)}, "
            f"unknown={sorted(actual - expected)}"
        )


def normalize_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    normalized = normalized.replace("_", "-").replace(" ", "-")
    return re.sub(r"-+", "-", normalized).strip("-")


def _require_slug(value: Any, *, label: str) -> str:
    if not isinstance(value, str):
        raise CatalogError(f"{label} must be a string slug")
    normalized = normalize_slug(value)
    if value != normalized or SLUG.fullmatch(value) is None:
        raise CatalogError(f"{label} must be a normalized lowercase slug: {value!r}")
    return value


def _require_enum(value: Any, allowed: set[str], *, label: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise CatalogError(f"{label} must be one of {sorted(allowed)}")
    return value


def _require_slug_list(
    value: Any,
    *,
    label: str,
    allowed: set[str] | None = None,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "a list" if allow_empty else "a non-empty list"
        raise CatalogError(f"{label} must be {qualifier}")
    if not all(isinstance(item, str) for item in value):
        raise CatalogError(f"{label} must contain only strings")
    if len(value) != len(set(value)) or value != sorted(value):
        raise CatalogError(f"{label} must be unique and sorted")
    for item in value:
        if allowed is None:
            _require_slug(item, label=f"{label} item")
        elif item not in allowed:
            raise CatalogError(f"{label} item must be one of {sorted(allowed)}")
    return list(value)


def _safe_public_research_path(value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise CatalogError("research pointer must be a POSIX relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.parts[0] != "docs":
        raise CatalogError("research pointer must stay under public docs/")
    return path


def _authority_sections(authority_root: Path) -> dict[str, str]:
    authority = authority_root / "UPSTREAM-SOURCES.md"
    if not authority.is_file() or authority.is_symlink():
        raise CatalogError(f"missing normal source authority: {authority}")
    try:
        text = authority.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise CatalogError(f"cannot read source authority {authority}: {exc}") from exc
    sections: dict[str, list[str]] = {}
    heading: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            if not heading or heading in sections:
                raise CatalogError(f"invalid or duplicate authority heading: {heading}")
            sections[heading] = []
        elif heading is not None:
            sections[heading].append(line)
    return {name: "\n".join(lines) for name, lines in sections.items()}


def _validate_record(
    record: Any,
    *,
    index: int,
    authority_root: Path | None,
    sections: dict[str, str] | None,
) -> dict[str, Any]:
    label = f"record[{index}]"
    if not isinstance(record, dict):
        raise CatalogError(f"{label} must be an object")
    forbidden = sorted(set(record) & FORBIDDEN_AUTHORITY_FIELDS)
    if forbidden:
        raise CatalogError(f"{label} owns forbidden authority facts: {forbidden}")
    _require_exact_fields(record, RECORD_FIELDS, label=label)
    _require_slug(record["id"], label=f"{label}.id")
    if not isinstance(record["name"], str) or record["name"] != record["name"].strip():
        raise CatalogError(f"{label}.name must be a trimmed non-empty string")
    _require_enum(record["kind"], KINDS, label=f"{label}.kind")
    for field in ("tasks", "capabilities", "stacks", "platforms"):
        _require_slug_list(record[field], label=f"{label}.{field}")
    _require_enum(record["relationship"], RELATIONSHIPS, label=f"{label}.relationship")
    _require_slug_list(
        record["eligible_routes"],
        label=f"{label}.eligible_routes",
        allowed=ELIGIBLE_ROUTES,
    )
    review = _require_enum(record["review_state"], REVIEW_STATES, label=f"{label}.review_state")
    adoption = _require_enum(
        record["adoption_disposition"],
        ADOPTION_DISPOSITIONS,
        label=f"{label}.adoption_disposition",
    )
    _require_enum(record["runtime_state"], RUNTIME_STATES, label=f"{label}.runtime_state")
    _require_enum(record["freshness"], FRESHNESS_STATES, label=f"{label}.freshness")
    evidence = _require_slug_list(
        record["evidence_levels"],
        label=f"{label}.evidence_levels",
        allowed=EVIDENCE_LEVELS,
    )
    _require_enum(record["risk_band"], RISK_BANDS, label=f"{label}.risk_band")
    _require_enum(
        record["maintenance_burden"],
        MAINTENANCE_BANDS,
        label=f"{label}.maintenance_burden",
    )
    _require_enum(record["cost_band"], COST_BANDS, label=f"{label}.cost_band")
    _require_enum(record["rollback_band"], ROLLBACK_BANDS, label=f"{label}.rollback_band")

    pointer = record["source_pointer"]
    if not isinstance(pointer, dict):
        raise CatalogError(f"{label}.source_pointer must be an object")
    _require_exact_fields(pointer, SOURCE_POINTER_FIELDS, label=f"{label}.source_pointer")
    if pointer["path"] != "UPSTREAM-SOURCES.md":
        raise CatalogError(f"{label}.source_pointer.path must be UPSTREAM-SOURCES.md")
    heading = pointer["heading"]
    if not isinstance(heading, str) or not heading.strip():
        raise CatalogError(f"{label}.source_pointer.heading must be non-empty")
    if sections is not None:
        if heading not in sections:
            raise CatalogError(f"{label} authority heading is missing: {heading}")
        block = sections[heading]
        for field in (
            "upstream",
            "upstream_version_or_commit",
            "license",
            "authority_boundary",
        ):
            if re.search(rf"(?m)^{re.escape(field)}:", block) is None:
                raise CatalogError(f"{label} authority heading lacks {field}: {heading}")

    research = record["research_pointers"]
    if not isinstance(research, list) or not all(isinstance(item, str) for item in research):
        raise CatalogError(f"{label}.research_pointers must be a string list")
    if len(research) != len(set(research)) or research != sorted(research):
        raise CatalogError(f"{label}.research_pointers must be unique and sorted")
    for item in research:
        relative = _safe_public_research_path(item)
        if authority_root is not None:
            target = authority_root / relative
            if not target.is_file() or target.is_symlink():
                raise CatalogError(f"{label} research pointer is unavailable: {item}")

    if review == "lead" and any(item not in {"article_claim", "readme_claim"} for item in evidence):
        raise CatalogError(f"{label} lead has evidence beyond claim level")
    requirements = {
        "source_behavior_checked": "source_proven",
        "local_validation_checked": "local_validation",
        "project_evidence_checked": "project_evidence",
    }
    if review in requirements and requirements[review] not in evidence:
        raise CatalogError(f"{label} review state lacks {requirements[review]}")
    if adoption in {"adopt_full", "adopt_partial"} and review == "lead":
        raise CatalogError(f"{label} cannot adopt a lead")
    return record


def validate_catalog(path: Path, authority_root: Path | None = None) -> list[dict[str, Any]]:
    value = read_strict_json(path)
    if not isinstance(value, dict):
        raise CatalogError("catalog must be an object")
    _require_exact_fields(value, TOP_LEVEL_FIELDS, label="catalog")
    if value["schema"] != CATALOG_SCHEMA or value["schema_version"] != 1:
        raise CatalogError("catalog schema identity is unsupported")
    if not isinstance(value["records"], list):
        raise CatalogError("catalog.records must be a list")
    sections = _authority_sections(authority_root) if authority_root else None
    records = [
        _validate_record(
            record,
            index=index,
            authority_root=authority_root,
            sections=sections,
        )
        for index, record in enumerate(value["records"])
    ]
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)) or ids != sorted(ids):
        raise CatalogError("catalog ids must be unique and sorted")
    return records


def _query_values(values: Iterable[str] | None) -> set[str]:
    return {normalize_slug(value) for value in values or [] if normalize_slug(value)}


def select_records(
    records: list[dict[str, Any]],
    *,
    ids: set[str],
    tasks: set[str],
    capabilities: set[str],
    stacks: set[str],
    platforms: set[str],
    max_risk: str | None,
    max_maintenance: str | None,
    cost: str | None,
    rollback: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    if not 1 <= limit <= 3:
        raise CatalogError("limit must be between 1 and 3")
    specific = ids | (tasks - GENERIC_QUERY_TERMS) | (capabilities - GENERIC_QUERY_TERMS)
    if not specific:
        return []
    ranked: list[tuple[tuple[int, int, int, int, int, str], dict[str, Any]]] = []
    for record in records:
        exact_id = int(record["id"] in ids)
        task_matches = len(tasks & set(record["tasks"]))
        capability_matches = len(capabilities & set(record["capabilities"]))
        if not (exact_id or task_matches or capability_matches):
            continue
        record_stacks = set(record["stacks"])
        record_platforms = set(record["platforms"])
        if stacks and "any" not in record_stacks and not (stacks & record_stacks):
            continue
        if platforms and "any" not in record_platforms and not (platforms & record_platforms):
            continue
        if max_risk and RISK_ORDER[record["risk_band"]] > RISK_ORDER[max_risk]:
            continue
        if max_maintenance and MAINTENANCE_ORDER[record["maintenance_burden"]] > MAINTENANCE_ORDER[max_maintenance]:
            continue
        if cost and record["cost_band"] != cost:
            continue
        if rollback and record["rollback_band"] != rollback:
            continue
        stack_matches = len(stacks & record_stacks)
        platform_matches = len(platforms & record_platforms)
        score = (
            -exact_id,
            -task_matches,
            -capability_matches,
            -stack_matches,
            -platform_matches,
            record["id"],
        )
        ranked.append((score, record))
    ranked.sort(key=lambda item: item[0])
    return [record for _, record in ranked[:limit]]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--authority-root", type=Path, required=True)
    find = subparsers.add_parser("find")
    find.add_argument("--authority-root", type=Path)
    find.add_argument("--id", action="append")
    find.add_argument("--task", action="append")
    find.add_argument("--capability", action="append")
    find.add_argument("--stack", action="append")
    find.add_argument("--platform", action="append")
    find.add_argument("--max-risk", choices=sorted(RISK_BANDS))
    find.add_argument("--max-maintenance", choices=sorted(MAINTENANCE_BANDS))
    find.add_argument("--cost", choices=sorted(COST_BANDS))
    find.add_argument("--rollback", choices=sorted(ROLLBACK_BANDS))
    find.add_argument("--limit", type=int, default=3)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records = validate_catalog(args.catalog, getattr(args, "authority_root", None))
        if args.command == "validate":
            payload = {
                "status": "validated",
                "schema": CATALOG_SCHEMA,
                "record_count": len(records),
                "writes_performed": False,
                "network_calls": 0,
            }
        else:
            selected = select_records(
                records,
                ids=_query_values(args.id),
                tasks=_query_values(args.task),
                capabilities=_query_values(args.capability),
                stacks=_query_values(args.stack),
                platforms=_query_values(args.platform),
                max_risk=args.max_risk,
                max_maintenance=args.max_maintenance,
                cost=args.cost,
                rollback=args.rollback,
                limit=args.limit,
            )
            payload = {
                "contract": SELECTION_CONTRACT,
                "status": "selected",
                "selected_count": len(selected),
                "records": selected,
                "adoption_authorized": False,
                "writes_performed": False,
                "network_calls": 0,
            }
    except (CatalogError, OSError, KeyError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
