#!/usr/bin/env python3
"""Validate, index, and retrieve bounded CoTend failure-pattern guards."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
PATTERN_ROOT = REFERENCES / "failure-patterns"
CATALOG = REFERENCES / "failure-pattern-catalog.json"

PATTERN_SCHEMA = "cotend.failure-pattern.v1"
CATALOG_SCHEMA = "cotend.failure-catalog.v1"
SELECTION_CONTRACT = "cotend.failure-selection.v1"
PATTERN_ID = re.compile(r"AFP-[0-9]{3,}")
DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
METADATA_BLOCK = re.compile(
    r"^# .+?\n\n```json\n(?P<body>\{.*?\})\n```",
    re.DOTALL,
)

LIFECYCLES = {
    "candidate",
    "active",
    "guarded",
    "verified",
    "archived",
    "reopened",
}
ORDINARY_LIFECYCLES = {"active", "guarded", "reopened"}
SEVERITIES = {"low", "medium", "high", "critical"}
CAUSE_CLASSES = {
    "model_behavior",
    "framework_gap_or_ambiguity",
    "stale_or_conflicting_project_truth",
    "tool_or_environment",
}
REQUIRED_SECTIONS = {
    "Context",
    "Observable Failure",
    "Mistaken Claim Versus Actual State",
    "Cause And Impact",
    "Missed Detection",
    "Correction",
    "Reusable Guard",
    "Validation",
    "Lifecycle History",
}
CATALOG_FIELDS = (
    "id",
    "title",
    "lifecycle",
    "severity",
    "cause_class",
    "areas",
    "trigger_tags",
    "related_skills",
    "confirmed_occurrences",
    "post_guard_recurrences",
    "first_seen",
    "last_seen",
    "guard_summary",
    "guard_owner",
    "evidence_refs",
)
SEVERITY_SCORE = {"low": 0, "medium": 2, "high": 5, "critical": 9}
LIFECYCLE_SCORE = {"guarded": 2, "active": 4, "reopened": 8}
MAX_ORDINARY_RESULTS = 3


class FailureMemoryError(RuntimeError):
    """Raised when failure-memory source or retrieval is invalid."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FailureMemoryError(message)


def normalize(value: str) -> str:
    return value.strip().casefold()


def string_list(value: Any, *, field: str) -> list[str]:
    require(
        isinstance(value, list)
        and value
        and all(isinstance(item, str) and item.strip() for item in value),
        f"{field} must be a non-empty string list",
    )
    normalized = [normalize(item) for item in value]
    require(len(set(normalized)) == len(normalized), f"{field} contains duplicates")
    return [item.strip() for item in value]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pattern_paths(root: Path = PATTERN_ROOT) -> list[Path]:
    return sorted(path for path in root.rglob("AFP-*.md") if path.is_file())


def parse_pattern(path: Path, *, root: Path = PATTERN_ROOT) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="strict")
    match = METADATA_BLOCK.search(text)
    require(match is not None, f"missing leading JSON metadata block: {path}")
    try:
        metadata = json.loads(match.group("body"))
    except json.JSONDecodeError as exc:
        raise FailureMemoryError(f"invalid pattern JSON: {path}: {exc}") from exc

    require(isinstance(metadata, dict), f"pattern metadata must be an object: {path}")
    require(metadata.get("schema") == PATTERN_SCHEMA, f"wrong pattern schema: {path}")
    require(set(CATALOG_FIELDS) | {"schema"} == set(metadata), f"wrong fields: {path}")

    pattern_id = metadata.get("id")
    require(
        isinstance(pattern_id, str) and PATTERN_ID.fullmatch(pattern_id),
        f"invalid pattern id: {path}",
    )
    require(path.stem == pattern_id, f"pattern id/path mismatch: {path}")
    for field in ("title", "guard_summary", "guard_owner"):
        require(
            isinstance(metadata.get(field), str) and metadata[field].strip(),
            f"{field} must be non-empty: {path}",
        )
    require(len(metadata["guard_summary"]) <= 280, f"guard_summary too long: {path}")

    lifecycle = metadata.get("lifecycle")
    require(lifecycle in LIFECYCLES, f"invalid lifecycle: {path}")
    relative = path.relative_to(root).as_posix()
    archived_path = relative.startswith("archive/")
    require(
        (lifecycle == "archived") == archived_path,
        f"archived lifecycle/path mismatch: {path}",
    )
    require(metadata.get("severity") in SEVERITIES, f"invalid severity: {path}")
    require(
        metadata.get("cause_class") in CAUSE_CLASSES,
        f"invalid cause_class: {path}",
    )

    for field in ("areas", "trigger_tags", "related_skills", "evidence_refs"):
        metadata[field] = string_list(metadata.get(field), field=field)
    for field in ("confirmed_occurrences", "post_guard_recurrences"):
        require(
            isinstance(metadata.get(field), int) and metadata[field] >= 0,
            f"{field} must be a non-negative integer: {path}",
        )
    require(
        metadata["confirmed_occurrences"] >= metadata["post_guard_recurrences"],
        f"post-guard recurrence exceeds occurrences: {path}",
    )
    for field in ("first_seen", "last_seen"):
        require(
            isinstance(metadata.get(field), str) and DATE.fullmatch(metadata[field]),
            f"invalid {field}: {path}",
        )
    require(
        metadata["first_seen"] <= metadata["last_seen"],
        f"first_seen is after last_seen: {path}",
    )

    headings = set(re.findall(r"^## ([^\n]+)$", text, re.MULTILINE))
    missing = REQUIRED_SECTIONS - headings
    require(not missing, f"missing full-record sections in {path}: {sorted(missing)}")
    return metadata


def build_catalog(root: Path = PATTERN_ROOT) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in pattern_paths(root):
        metadata = parse_pattern(path, root=root)
        require(metadata["id"] not in seen, f"duplicate pattern id: {metadata['id']}")
        seen.add(metadata["id"])
        record = {field: metadata[field] for field in CATALOG_FIELDS}
        record["record_path"] = path.relative_to(SKILL_ROOT).as_posix()
        record["record_sha256"] = sha256_file(path)
        records.append(record)
    records.sort(key=lambda item: item["id"])
    return {
        "schema": CATALOG_SCHEMA,
        "source_of_truth": "failure-pattern Markdown metadata",
        "record_count": len(records),
        "records": records,
    }


def write_catalog(path: Path = CATALOG) -> dict[str, Any]:
    catalog = build_catalog()
    path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return catalog


def read_catalog(path: Path = CATALOG) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FailureMemoryError(f"cannot read catalog: {path}: {exc}") from exc
    require(isinstance(value, dict), "catalog root must be an object")
    require(value.get("schema") == CATALOG_SCHEMA, "wrong catalog schema")
    require(
        isinstance(value.get("records"), list)
        and value.get("record_count") == len(value["records"]),
        "catalog count differs",
    )
    return value


def validate_catalog(path: Path = CATALOG) -> dict[str, Any]:
    actual = read_catalog(path)
    expected = build_catalog()
    require(actual == expected, "catalog differs from canonical pattern metadata")
    return actual


def select_cards(
    *,
    catalog: dict[str, Any],
    tags: list[str],
    skills: list[str],
    limit: int,
) -> dict[str, Any]:
    require(1 <= limit <= MAX_ORDINARY_RESULTS, "ordinary result limit must be 1..3")
    query_tags = {normalize(item) for item in tags if item.strip()}
    query_skills = {normalize(item) for item in skills if item.strip()}
    require(query_tags or query_skills, "selection requires at least one tag or skill")
    generic_root_skills = {"cotend-collaboration"}

    ranked: list[tuple[int, str, dict[str, Any], list[str]]] = []
    for record in catalog["records"]:
        if record.get("lifecycle") not in ORDINARY_LIFECYCLES:
            continue
        areas = {normalize(item) for item in record["areas"]}
        triggers = {normalize(item) for item in record["trigger_tags"]}
        related = {normalize(item) for item in record["related_skills"]}
        area_hits = sorted(query_tags & areas)
        trigger_hits = sorted(query_tags & triggers)
        skill_hits = sorted(query_skills & related)
        specific_skill_hits = sorted(set(skill_hits) - generic_root_skills)
        root_skill_hits = sorted(set(skill_hits) & generic_root_skills)
        admission_hits = area_hits or trigger_hits or specific_skill_hits
        if not admission_hits:
            continue

        score = (
            12 * len(specific_skill_hits)
            + len(root_skill_hits)
            + 10 * len(trigger_hits)
            + 8 * len(area_hits)
            + SEVERITY_SCORE[record["severity"]]
            + LIFECYCLE_SCORE[record["lifecycle"]]
            + min(record["post_guard_recurrences"], 3) * 6
            + min(record["confirmed_occurrences"], 5)
        )
        why = [
            *(f"skill:{value}" for value in specific_skill_hits),
            *(f"root-skill-tiebreaker:{value}" for value in root_skill_hits),
            *(f"trigger:{value}" for value in trigger_hits),
            *(f"area:{value}" for value in area_hits),
        ]
        ranked.append((score, record["id"], record, why))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    cards: list[dict[str, Any]] = []
    for score, _, record, why in ranked[:limit]:
        record_path = SKILL_ROOT / record["record_path"]
        require(record_path.is_file(), f"selected record missing: {record_path}")
        require(
            sha256_file(record_path) == record["record_sha256"],
            f"selected record hash differs: {record['id']}",
        )
        cards.append(
            {
                "id": record["id"],
                "title": record["title"],
                "lifecycle": record["lifecycle"],
                "severity": record["severity"],
                "match_score": score,
                "why_matched": why,
                "guard": record["guard_summary"],
                "guard_owner": record["guard_owner"],
                "confirmed_occurrences": record["confirmed_occurrences"],
                "post_guard_recurrences": record["post_guard_recurrences"],
                "full_record": record["record_path"],
                "record_sha256": record["record_sha256"],
            }
        )
    return {
        "contract": SELECTION_CONTRACT,
        "ordinary_lifecycle_filter": sorted(ORDINARY_LIFECYCLES),
        "hard_result_cap": MAX_ORDINARY_RESULTS,
        "selected_count": len(cards),
        "full_records_loaded_into_output": False,
        "cards": cards,
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("build-catalog")
    commands.add_parser("validate")
    select = commands.add_parser("select")
    select.add_argument("--tag", action="append", default=[])
    select.add_argument("--skill", action="append", default=[])
    select.add_argument("--limit", type=int, default=MAX_ORDINARY_RESULTS)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "build-catalog":
        result = write_catalog()
    elif args.command == "validate":
        result = validate_catalog()
    else:
        result = select_cards(
            catalog=validate_catalog(),
            tags=args.tag,
            skills=args.skill,
            limit=args.limit,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FailureMemoryError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc
