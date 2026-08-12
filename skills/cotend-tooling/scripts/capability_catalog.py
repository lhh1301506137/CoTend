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
    "canonical_source_field",
    "identity_field",
    "license",
    "license_claim",
    "license_spdx",
    "lookup_method",
    "release_channel",
    "release_source",
    "update_locator",
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

UPDATE_LOCATOR_FIELDS = {
    "canonical_source_field",
    "release_source",
    "release_channel",
    "lookup_method",
    "identity_field",
}
RELEASE_SOURCES = {
    "article",
    "not_checked",
    "platform",
    "registry",
    "repository",
    "self_maintained",
}
RELEASE_CHANNELS = {
    "default_branch",
    "not_checked",
    "not_versioned",
    "platform_managed",
    "prerelease",
    "self_managed",
    "stable",
}
LOOKUP_METHODS = {
    "git_default_branch",
    "git_release_or_tag",
    "manual_source_recheck",
    "not_checked",
    "platform_runtime",
    "registry_dist_tag",
    "repository_path_git_tree",
}
UPDATE_LOCATOR_COMBINATIONS = {
    ("article", "not_versioned", "manual_source_recheck"),
    ("not_checked", "not_checked", "not_checked"),
    ("platform", "platform_managed", "platform_runtime"),
    ("registry", "prerelease", "registry_dist_tag"),
    ("registry", "stable", "registry_dist_tag"),
    ("repository", "default_branch", "git_default_branch"),
    ("repository", "prerelease", "git_release_or_tag"),
    ("repository", "stable", "git_release_or_tag"),
    ("self_maintained", "self_managed", "repository_path_git_tree"),
}

HEX_OBJECT = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
QUOTED_IDENTITY = re.compile(r"`[^`\s]{1,128}`")
UNVERIFIABLE_IDENTITY_MARKERS = (
    "no direct upstream pinned",
    "not a versioned",
    "not applicable",
    "not checked",
    "not_checked",
    "source_review_pending",
    "unknown",
)

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
        raw = path.read_bytes()
        return json.loads(
            raw.decode("utf-8", errors="strict"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CatalogError(f"cannot read strict JSON catalog {path}: {exc}") from exc


def _require_exact_fields(
    value: dict[str, Any],
    expected: set[str],
    *,
    label: str,
) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise CatalogError(
            f"{label} fields mismatch: missing={missing}, unknown={unknown}"
        )


def normalize_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    normalized = normalized.replace("_", "-").replace(" ", "-")
    return re.sub(r"-+", "-", normalized).strip("-")


def _require_slug(value: Any, *, label: str) -> str:
    if not isinstance(value, str):
        raise CatalogError(f"{label} must be a string slug")
    normalized = normalize_slug(value)
    if value != normalized or not SLUG.fullmatch(value):
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
    if len(value) != len(set(value)):
        raise CatalogError(f"{label} contains duplicate values")
    if value != sorted(value):
        raise CatalogError(f"{label} must be sorted")
    for item in value:
        if allowed is None:
            _require_slug(item, label=f"{label} item")
        elif item not in allowed:
            raise CatalogError(f"{label} item must be one of {sorted(allowed)}")
    return list(value)


def _safe_relative_path(value: str, *, prefix: str, label: str) -> Path:
    path = Path(value)
    if (
        not value.strip()
        or path.is_absolute()
        or value.startswith(("/", "\\"))
        or ".." in path.parts
        or (prefix and not value.replace("\\", "/").startswith(prefix))
    ):
        raise CatalogError(f"{label} must stay under {prefix}")
    return path


def _authority_sections(authority_root: Path) -> dict[str, str]:
    authority = authority_root / "UPSTREAM-SOURCES.md"
    if not authority.is_file():
        raise CatalogError(f"missing source authority: {authority}")
    try:
        text = authority.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise CatalogError(f"cannot read source authority {authority}: {exc}") from exc
    sections: dict[str, list[str]] = {}
    heading: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            if not heading:
                raise CatalogError("source authority contains an empty heading")
            if heading in sections:
                raise CatalogError(
                    f"source authority contains duplicate heading: {heading}"
                )
            sections[heading] = []
        elif heading is not None:
            sections[heading].append(line)
    return {name: "\n".join(lines) for name, lines in sections.items()}


def validate_update_locator(
    authority_record: str,
    *,
    label: str = "authority record",
) -> dict[str, str]:
    """Validate one compact authority-owned release/update locator."""

    lines = authority_record.splitlines()
    locator_indexes = [
        index for index, line in enumerate(lines) if line == "update_locator:"
    ]
    if len(locator_indexes) != 1:
        qualifier = "missing" if not locator_indexes else "duplicated"
        raise CatalogError(f"{label} update_locator is {qualifier}")

    locator: dict[str, str] = {}
    index = locator_indexes[0] + 1
    while index < len(lines) and lines[index].startswith("  "):
        match = re.fullmatch(r"  ([a-z_]+): ([a-z_]+)", lines[index])
        if match is None:
            raise CatalogError(f"{label} update_locator contains an invalid field")
        key, value = match.groups()
        if key in locator:
            raise CatalogError(f"{label} update_locator duplicates {key}")
        locator[key] = value
        index += 1

    _require_exact_fields(
        locator,
        UPDATE_LOCATOR_FIELDS,
        label=f"{label}.update_locator",
    )
    if locator["canonical_source_field"] != "upstream":
        raise CatalogError(
            f"{label}.update_locator.canonical_source_field must be upstream"
        )
    if locator["identity_field"] != "upstream_version_or_commit":
        raise CatalogError(
            f"{label}.update_locator.identity_field must be "
            "upstream_version_or_commit"
        )
    _require_enum(
        locator["release_source"],
        RELEASE_SOURCES,
        label=f"{label}.update_locator.release_source",
    )
    _require_enum(
        locator["release_channel"],
        RELEASE_CHANNELS,
        label=f"{label}.update_locator.release_channel",
    )
    _require_enum(
        locator["lookup_method"],
        LOOKUP_METHODS,
        label=f"{label}.update_locator.lookup_method",
    )
    combination = (
        locator["release_source"],
        locator["release_channel"],
        locator["lookup_method"],
    )
    if combination not in UPDATE_LOCATOR_COMBINATIONS:
        raise CatalogError(f"{label} update_locator combination is invalid")
    return locator


def _authority_scalar(
    authority_record: str,
    field: str,
    *,
    label: str,
) -> str:
    matches = re.findall(
        rf"(?m)^{re.escape(field)}:[ \t]*(.*)$",
        authority_record,
    )
    if len(matches) != 1:
        qualifier = "missing" if not matches else "duplicated"
        raise CatalogError(f"{label} {field} is {qualifier}")
    return matches[0].strip()


def _authority_field_block(
    authority_record: str,
    field: str,
    *,
    label: str,
) -> str:
    lines = authority_record.splitlines()
    indexes = [
        index
        for index, line in enumerate(lines)
        if re.match(rf"^{re.escape(field)}:[ \t]*", line)
    ]
    if len(indexes) != 1:
        qualifier = "missing" if not indexes else "duplicated"
        raise CatalogError(f"{label} {field} is {qualifier}")
    index = indexes[0]
    values = [lines[index].split(":", 1)[1].strip()]
    index += 1
    while index < len(lines) and lines[index].startswith("- "):
        values.append(lines[index][2:].strip())
        index += 1
    return "\n".join(value for value in values if value)


def authority_source_status(
    authority_record: str,
    locator: dict[str, str],
    *,
    label: str = "authority record",
) -> str:
    """Classify whether the locator's canonical source is concrete enough to use."""

    source = _authority_field_block(
        authority_record,
        locator["canonical_source_field"],
        label=label,
    )
    method = locator["lookup_method"]
    if method in {"git_default_branch", "git_release_or_tag"}:
        return "checkable" if re.search(r"https://[^\s`]+", source) else "unverifiable"
    if method == "registry_dist_tag":
        registry_markers = {
            "crates.io",
            "maven",
            "npm",
            "nuget",
            "packagist",
            "pypi",
            "rubygems",
        }
        return (
            "checkable"
            if any(marker in source.casefold() for marker in registry_markers)
            else "unverifiable"
        )
    if method == "platform_runtime":
        return "checkable" if source else "unverifiable"
    if method == "repository_path_git_tree":
        path_matches = re.findall(r"`([^`]+)`", source)
        if len(path_matches) != 1:
            return "unverifiable"
        try:
            _safe_relative_path(
                path_matches[0],
                prefix="",
                label=f"{label}.upstream repository path",
            )
        except CatalogError:
            return "unverifiable"
        return "checkable"
    if method == "manual_source_recheck":
        return "checkable" if "https://" in source else "unverifiable"
    return "unverifiable"


def authority_identity_status(
    authority_record: str,
    locator: dict[str, str],
    *,
    label: str = "authority record",
) -> str:
    """Classify whether the declared identity is concrete enough to recheck."""

    identity = _authority_scalar(
        authority_record,
        locator["identity_field"],
        label=label,
    )
    normalized = identity.casefold()
    if not identity or any(
        marker in normalized for marker in UNVERIFIABLE_IDENTITY_MARKERS
    ):
        return "unverifiable"

    method = locator["lookup_method"]
    if method in {"git_default_branch", "git_release_or_tag"}:
        return "checkable" if HEX_OBJECT.search(normalized) else "unverifiable"
    if method == "registry_dist_tag":
        return "checkable" if QUOTED_IDENTITY.search(identity) else "unverifiable"
    if method == "platform_runtime":
        return (
            "checkable"
            if HEX_OBJECT.search(normalized) or QUOTED_IDENTITY.search(identity)
            else "unverifiable"
        )
    if method == "repository_path_git_tree":
        has_tree = re.search(r"\btree\s+`[0-9a-f]{40}`", normalized) is not None
        has_commit = re.search(r"\bcommit\s+`[0-9a-f]{40}`", normalized) is not None
        return "checkable" if has_tree and has_commit else "unverifiable"
    return "unverifiable"


def update_locator_status(locator: dict[str, str]) -> str:
    """Return the explicit traceability class without checking a network."""

    release_source = locator["release_source"]
    release_channel = locator["release_channel"]
    if release_source == "not_checked":
        return "not_checked"
    if release_channel == "not_versioned":
        return "not_versioned"
    if release_source == "platform":
        return "platform_managed"
    if release_source == "self_maintained":
        return "self_maintained"
    return "traceable"


def _validate_record(
    record: Any,
    *,
    index: int,
    authority_root: Path | None,
    authority_sections: dict[str, str] | None,
) -> dict[str, Any]:
    label = f"record[{index}]"
    if not isinstance(record, dict):
        raise CatalogError(f"{label} must be an object")
    forbidden = sorted(set(record) & FORBIDDEN_AUTHORITY_FIELDS)
    if forbidden:
        raise CatalogError(
            f"{label} catalog must not own license/version/source URL claims: "
            f"{forbidden}"
        )
    _require_exact_fields(record, RECORD_FIELDS, label=label)

    record_id = _require_slug(record["id"], label=f"{label}.id")
    if not isinstance(record["name"], str) or not record["name"].strip():
        raise CatalogError(f"{label}.name must be a non-empty string")
    if record["name"] != record["name"].strip():
        raise CatalogError(f"{label}.name must not have surrounding whitespace")

    _require_enum(record["kind"], KINDS, label=f"{label}.kind")
    _require_slug_list(record["tasks"], label=f"{label}.tasks")
    _require_slug_list(record["capabilities"], label=f"{label}.capabilities")
    _require_slug_list(record["stacks"], label=f"{label}.stacks")
    _require_slug_list(record["platforms"], label=f"{label}.platforms")
    _require_enum(record["relationship"], RELATIONSHIPS, label=f"{label}.relationship")
    _require_slug_list(
        record["eligible_routes"],
        label=f"{label}.eligible_routes",
        allowed=ELIGIBLE_ROUTES,
    )
    review_state = _require_enum(
        record["review_state"], REVIEW_STATES, label=f"{label}.review_state"
    )
    adoption = _require_enum(
        record["adoption_disposition"],
        ADOPTION_DISPOSITIONS,
        label=f"{label}.adoption_disposition",
    )
    runtime_state = _require_enum(
        record["runtime_state"], RUNTIME_STATES, label=f"{label}.runtime_state"
    )
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
    _require_enum(
        record["rollback_band"], ROLLBACK_BANDS, label=f"{label}.rollback_band"
    )

    source_pointer = record["source_pointer"]
    if not isinstance(source_pointer, dict):
        raise CatalogError(f"{label}.source_pointer must be an object")
    _require_exact_fields(
        source_pointer,
        SOURCE_POINTER_FIELDS,
        label=f"{label}.source_pointer",
    )
    if source_pointer["path"] != "UPSTREAM-SOURCES.md":
        raise CatalogError(f"{label}.source_pointer.path must be UPSTREAM-SOURCES.md")
    heading = source_pointer["heading"]
    if not isinstance(heading, str) or not heading.strip():
        raise CatalogError(f"{label}.source_pointer.heading must be non-empty")
    if authority_sections is not None:
        if heading not in authority_sections:
            raise CatalogError(
                f"{label}.source_pointer heading not found in authority: {heading}"
            )
        authority_record = authority_sections[heading]
        for required_field in (
            "upstream",
            "upstream_version_or_commit",
            "license",
            "authority_boundary",
        ):
            if not re.search(
                rf"(?m)^{re.escape(required_field)}:",
                authority_record,
            ):
                raise CatalogError(
                    f"{label}.source_pointer authority record missing "
                    f"{required_field}: {heading}"
                )
        locator = validate_update_locator(
            authority_record,
            label=f"{label}.source_pointer authority record",
        )
        identity_status = authority_identity_status(
            authority_record,
            locator,
            label=f"{label}.source_pointer authority record",
        )
        source_status = authority_source_status(
            authority_record,
            locator,
            label=f"{label}.source_pointer authority record",
        )
        if record["freshness"] == "current" and (
            update_locator_status(locator) in {"not_checked", "not_versioned"}
            or source_status != "checkable"
            or identity_status != "checkable"
        ):
            raise CatalogError(
                f"{label}.freshness current requires a checkable locator, "
                "source, and verifiable identity"
            )

    research = record["research_pointers"]
    if not isinstance(research, list) or not all(
        isinstance(item, str) for item in research
    ):
        raise CatalogError(f"{label}.research_pointers must be a string list")
    if len(research) != len(set(research)) or research != sorted(research):
        raise CatalogError(f"{label}.research_pointers must be unique and sorted")
    for item in research:
        relative = _safe_relative_path(
            item,
            prefix="OPEN-SOURCE-REFERENCES/",
            label=f"{label}.research_pointers item",
        )
        if authority_root is not None and not (authority_root / relative).is_file():
            raise CatalogError(f"{label} missing research pointer target: {item}")

    evidence_set = set(evidence)
    if review_state == "lead":
        if not evidence_set <= {"article_claim", "readme_claim"}:
            raise CatalogError(f"{label} lead may contain claim evidence only")
        if adoption not in {"unreviewed", "defer"}:
            raise CatalogError(f"{label} lead cannot be adopted")
        if runtime_state not in {"not_installed", "not_applicable", "unknown"}:
            raise CatalogError(f"{label} lead cannot claim an active runtime")
    if (
        review_state == "source_behavior_checked"
        and "source_proven" not in evidence_set
    ):
        raise CatalogError(f"{label} source_behavior_checked requires source_proven")
    if (
        review_state == "local_validation_checked"
        and "local_validation" not in evidence_set
    ):
        raise CatalogError(
            f"{label} local_validation_checked requires local_validation"
        )
    if (
        review_state == "project_evidence_checked"
        and "project_evidence" not in evidence_set
    ):
        raise CatalogError(
            f"{label} project_evidence_checked requires project_evidence"
        )
    if adoption in {"adopt_full", "adopt_partial"} and review_state == "lead":
        raise CatalogError(f"{label} adopted disposition cannot remain a lead")
    if record["relationship"] == "source_review_pending" and adoption not in {
        "unreviewed",
        "defer",
    }:
        raise CatalogError(
            f"{label} source_review_pending must remain unreviewed or defer"
        )

    result = dict(record)
    result["id"] = record_id
    return result


def validate_catalog_data(
    catalog: Any,
    *,
    authority_root: Path | None = None,
) -> dict[str, Any]:
    if not isinstance(catalog, dict):
        raise CatalogError("catalog must be an object")
    _require_exact_fields(catalog, TOP_LEVEL_FIELDS, label="catalog")
    if catalog["schema"] != CATALOG_SCHEMA:
        raise CatalogError(f"catalog.schema must be {CATALOG_SCHEMA}")
    if type(catalog["schema_version"]) is not int or catalog["schema_version"] != 1:
        raise CatalogError("catalog.schema_version must be 1")
    records = catalog["records"]
    if not isinstance(records, list) or not records:
        raise CatalogError("catalog.records must be a non-empty list")

    resolved_root = authority_root.resolve() if authority_root is not None else None
    sections = _authority_sections(resolved_root) if resolved_root is not None else None
    validated = [
        _validate_record(
            record,
            index=index,
            authority_root=resolved_root,
            authority_sections=sections,
        )
        for index, record in enumerate(records)
    ]
    ids = [record["id"] for record in validated]
    if len(ids) != len(set(ids)):
        raise CatalogError("catalog contains duplicate ids")
    if ids != sorted(ids):
        raise CatalogError("catalog records must be sorted by id")
    return {
        "schema": CATALOG_SCHEMA,
        "schema_version": 1,
        "records": validated,
    }


def validate_catalog(
    catalog_path: Path = DEFAULT_CATALOG,
    *,
    authority_root: Path | None = None,
) -> dict[str, Any]:
    return validate_catalog_data(
        read_strict_json(catalog_path),
        authority_root=authority_root,
    )


def _normalized_query(values: Iterable[str]) -> set[str]:
    return {
        normalized
        for value in values
        if (normalized := normalize_slug(value)) and SLUG.fullmatch(normalized)
    }


def _compatible(requested: set[str], offered: set[str]) -> bool:
    return not requested or "any" in offered or bool(requested & offered)


def select_candidates(
    *,
    catalog: dict[str, Any],
    ids: Iterable[str] = (),
    tasks: Iterable[str] = (),
    capabilities: Iterable[str] = (),
    stacks: Iterable[str] = (),
    platforms: Iterable[str] = (),
    max_risk: str | None = None,
    max_maintenance: str | None = None,
    allowed_costs: Iterable[str] = (),
    allowed_rollbacks: Iterable[str] = (),
    include_retired: bool = False,
    limit: int = 3,
) -> dict[str, Any]:
    if type(limit) is not int or not 1 <= limit <= 3:
        raise CatalogError("limit must be an integer from 1 to 3")
    validated = validate_catalog_data(catalog)

    query_ids = _normalized_query(ids)
    query_tasks = _normalized_query(tasks) - GENERIC_QUERY_TERMS
    query_capabilities = _normalized_query(capabilities) - GENERIC_QUERY_TERMS
    query_stacks = _normalized_query(stacks)
    query_platforms = _normalized_query(platforms)
    query_costs = _normalized_query(allowed_costs)
    query_rollbacks = _normalized_query(allowed_rollbacks)

    if max_risk is not None and max_risk not in RISK_BANDS:
        raise CatalogError(f"max_risk must be one of {sorted(RISK_BANDS)}")
    if max_maintenance is not None and max_maintenance not in MAINTENANCE_BANDS:
        raise CatalogError(
            f"max_maintenance must be one of {sorted(MAINTENANCE_BANDS)}"
        )
    if not query_costs <= COST_BANDS:
        raise CatalogError(f"allowed_costs must use {sorted(COST_BANDS)}")
    if not query_rollbacks <= ROLLBACK_BANDS:
        raise CatalogError(f"allowed_rollbacks must use {sorted(ROLLBACK_BANDS)}")

    specific_need = bool(query_ids or query_tasks or query_capabilities)
    candidates: list[dict[str, Any]] = []
    if specific_need:
        records = validated["records"]
        rank_bases = (
            max(len(record["tasks"]) for record in records) + 1,
            max(len(record["capabilities"]) for record in records) + 1,
            max(len(record["stacks"]) for record in records) + 1,
            max(len(record["platforms"]) for record in records) + 1,
        )
        for record in records:
            if record["runtime_state"] == "retired" and not include_retired:
                continue

            record_tasks = set(record["tasks"])
            record_capabilities = set(record["capabilities"])
            record_stacks = set(record["stacks"])
            record_platforms = set(record["platforms"])
            id_match = record["id"] in query_ids
            task_matches = sorted(query_tasks & record_tasks)
            capability_matches = sorted(query_capabilities & record_capabilities)
            if not (id_match or task_matches or capability_matches):
                continue
            if not _compatible(query_stacks, record_stacks):
                continue
            if not _compatible(query_platforms, record_platforms):
                continue
            if max_risk is not None and (
                RISK_ORDER[record["risk_band"]] > RISK_ORDER[max_risk]
            ):
                continue
            if max_maintenance is not None and (
                MAINTENANCE_ORDER[record["maintenance_burden"]]
                > MAINTENANCE_ORDER[max_maintenance]
            ):
                continue
            if query_costs and record["cost_band"] not in query_costs:
                continue
            if query_rollbacks and record["rollback_band"] not in query_rollbacks:
                continue

            stack_matches = sorted(query_stacks & record_stacks)
            platform_matches = sorted(query_platforms & record_platforms)
            rank_components = (
                int(id_match),
                len(task_matches),
                len(capability_matches),
                len(stack_matches),
                len(platform_matches),
            )
            score = rank_components[0]
            for component, base in zip(rank_components[1:], rank_bases, strict=True):
                score = score * base + component

            why: list[str] = []
            if id_match:
                why.append(f"id:{record['id']}")
            for match in task_matches:
                why.append(f"task:{match}")
            for match in capability_matches:
                why.append(f"capability:{match}")
            for match in stack_matches:
                why.append(f"stack:{match}")
            for match in platform_matches:
                why.append(f"platform:{match}")

            candidates.append(
                {
                    "id": record["id"],
                    "name": record["name"],
                    "kind": record["kind"],
                    "score": score,
                    "why_matched": why,
                    "eligible_routes": record["eligible_routes"],
                    "review_state": record["review_state"],
                    "adoption_disposition": record["adoption_disposition"],
                    "runtime_state": record["runtime_state"],
                    "freshness": record["freshness"],
                    "risk_band": record["risk_band"],
                    "maintenance_burden": record["maintenance_burden"],
                    "cost_band": record["cost_band"],
                    "rollback_band": record["rollback_band"],
                    "source_pointer": record["source_pointer"],
                    "research_pointers": record["research_pointers"],
                }
            )

    candidates.sort(key=lambda item: (-item["score"], item["id"]))
    selected = candidates[:limit]
    return {
        "contract": SELECTION_CONTRACT,
        "catalog_schema": CATALOG_SCHEMA,
        "query_status": "specific_need" if specific_need else "no_specific_need",
        "query": {
            "ids": sorted(query_ids),
            "tasks": sorted(query_tasks),
            "capabilities": sorted(query_capabilities),
            "stacks": sorted(query_stacks),
            "platforms": sorted(query_platforms),
            "max_risk": max_risk,
            "max_maintenance": max_maintenance,
            "allowed_costs": sorted(query_costs),
            "allowed_rollbacks": sorted(query_rollbacks),
            "include_retired": include_retired,
            "limit": limit,
        },
        "selected_count": len(selected),
        "candidates": selected,
        "full_catalog_emitted": False,
        "detail_record_limit": 3,
    }


def _add_find_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--task", action="append", default=[])
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--stack", action="append", default=[])
    parser.add_argument("--platform", action="append", default=[])
    parser.add_argument("--max-risk", choices=sorted(RISK_BANDS))
    parser.add_argument("--max-maintenance", choices=sorted(MAINTENANCE_BANDS))
    parser.add_argument("--allowed-cost", action="append", default=[])
    parser.add_argument("--allowed-rollback", action="append", default=[])
    parser.add_argument("--include-retired", action="store_true")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--authority-root", type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and query the CoTend capability catalog."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate")
    validate.add_argument("--authority-root", type=Path, required=True)

    find = commands.add_parser("find")
    _add_find_arguments(find)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        authority_root = getattr(args, "authority_root", None)
        catalog = validate_catalog(
            args.catalog.resolve(),
            authority_root=authority_root.resolve()
            if authority_root is not None
            else None,
        )
        if args.command == "validate":
            output: dict[str, Any] = {
                "contract": "cotend.capability-catalog-validation.v1",
                "status": "valid",
                "catalog": str(args.catalog.resolve()),
                "record_count": len(catalog["records"]),
                "update_locator_count": len(catalog["records"]),
                "authority_root": str(args.authority_root.resolve()),
            }
        else:
            output = select_candidates(
                catalog=catalog,
                ids=args.id,
                tasks=args.task,
                capabilities=args.capability,
                stacks=args.stack,
                platforms=args.platform,
                max_risk=args.max_risk,
                max_maintenance=args.max_maintenance,
                allowed_costs=args.allowed_cost,
                allowed_rollbacks=args.allowed_rollback,
                include_retired=args.include_retired,
                limit=args.limit,
            )
    except CatalogError as exc:
        print(f"capability catalog error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
