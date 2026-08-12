#!/usr/bin/env python3
"""Validate and retrieve bounded CoTend adaptive-development reasoning cues."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG = SKILL_ROOT / "references" / "development-experience-catalog.json"

CATALOG_SCHEMA = "cotend.development-experience-catalog.v1"
SELECTION_CONTRACT = "cotend.development-experience-selection.v1"
CARD_ID = re.compile(r"AEP-[0-9]{3,}")
MAX_ORDINARY_RESULTS = 3

TRIGGER_SIGNALS = {
    "conditions_changed",
    "method_goal_mismatch",
    "comparable_prior_strategy",
    "evidence_backed_improvement",
    "explicit_experience_request",
}
LIFECYCLES = {"candidate", "active", "distilled", "archived"}
ORDINARY_LIFECYCLES = {"active", "distilled"}
RETIREMENT_REASONS = {
    "none",
    "narrowed",
    "superseded",
    "contradicted",
    "stale",
}
GENERIC_ROOT_SKILLS = {"cotend-collaboration"}
TOP_LEVEL_FIELDS = {
    "schema",
    "schema_version",
    "source_of_truth",
    "record_count",
    "cards",
}
CARD_FIELDS = {
    "id",
    "title",
    "kind",
    "lifecycle",
    "lifecycle_evidence_ref",
    "retirement",
    "areas",
    "trigger_tags",
    "related_skills",
    "applicability_conditions",
    "counter_conditions",
    "reasoning_cue",
    "evidence_refs",
}
RETIREMENT_FIELDS = {"reason", "evidence_ref"}


class DevelopmentExperienceError(ValueError):
    """Fail-closed catalog or query error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DevelopmentExperienceError(message)


def normalize(value: str) -> str:
    return value.strip().casefold()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_strict_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8", errors="strict"),
            object_pairs_hook=strict_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DevelopmentExperienceError(
            f"cannot read strict catalog {path}: {exc}"
        ) from exc


def require_exact_fields(
    value: dict[str, Any], expected: set[str], *, label: str
) -> None:
    actual = set(value)
    require(
        actual == expected,
        f"{label} fields mismatch: missing={sorted(expected - actual)}, "
        f"unknown={sorted(actual - expected)}",
    )


def string_value(value: Any, *, field: str, maximum: int = 400) -> str:
    require(isinstance(value, str) and value.strip(), f"{field} must be non-empty")
    require(len(value) <= maximum, f"{field} is too long")
    return value.strip()


def evidence_ref_value(value: Any, *, field: str, allow_none: bool = False) -> str:
    cleaned = string_value(value, field=field)
    require(
        allow_none or normalize(cleaned) != "none",
        f"{field} must identify evidence",
    )
    path_part = cleaned.split("#", 1)[0].replace("\\", "/").casefold()
    task_marker = "project-plan-nodes/"
    if task_marker in path_part:
        task_suffix = path_part.split(task_marker, 1)[1]
        require(
            task_suffix.startswith("archive/"),
            f"{field} must not reference an active CoTend Plan node path",
        )
    return cleaned


def string_list(
    value: Any,
    *,
    field: str,
    maximum_items: int,
    maximum_item_length: int = 240,
) -> list[str]:
    require(
        isinstance(value, list)
        and value
        and len(value) <= maximum_items
        and all(isinstance(item, str) and item.strip() for item in value),
        f"{field} must be a non-empty string list of at most {maximum_items} items",
    )
    cleaned = [item.strip() for item in value]
    require(
        all(len(item) <= maximum_item_length for item in cleaned),
        f"{field} contains an overlong item",
    )
    normalized = [normalize(item) for item in cleaned]
    require(len(normalized) == len(set(normalized)), f"{field} contains duplicates")
    return cleaned


def validate_catalog_data(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "catalog root must be an object")
    require_exact_fields(value, TOP_LEVEL_FIELDS, label="catalog")
    require(value["schema"] == CATALOG_SCHEMA, "wrong catalog schema")
    require(type(value["schema_version"]) is int, "schema_version must be an integer")
    require(value["schema_version"] == 1, "unsupported schema_version")
    string_value(value["source_of_truth"], field="source_of_truth")
    cards = value["cards"]
    require(isinstance(cards, list), "cards must be a list")
    require(type(value["record_count"]) is int, "record_count must be an integer")
    require(value["record_count"] == len(cards), "record_count differs from cards")

    seen: set[str] = set()
    for position, card in enumerate(cards):
        label = f"cards[{position}]"
        require(isinstance(card, dict), f"{label} must be an object")
        require_exact_fields(card, CARD_FIELDS, label=label)
        card_id = card["id"]
        require(
            isinstance(card_id, str) and CARD_ID.fullmatch(card_id),
            f"{label}.id is invalid",
        )
        require(card_id not in seen, f"duplicate card id: {card_id}")
        seen.add(card_id)
        string_value(card["title"], field=f"{card_id}.title", maximum=120)
        require(
            card["kind"] == "reasoning_cue", f"{card_id}.kind must be reasoning_cue"
        )
        require(
            isinstance(card["lifecycle"], str) and card["lifecycle"] in LIFECYCLES,
            f"{card_id}.lifecycle is invalid",
        )
        card["lifecycle_evidence_ref"] = evidence_ref_value(
            card["lifecycle_evidence_ref"],
            field=f"{card_id}.lifecycle_evidence_ref",
        )

        retirement = card["retirement"]
        require(isinstance(retirement, dict), f"{card_id}.retirement must be an object")
        require_exact_fields(
            retirement, RETIREMENT_FIELDS, label=f"{card_id}.retirement"
        )
        reason = retirement["reason"]
        require(
            isinstance(reason, str) and reason in RETIREMENT_REASONS,
            f"{card_id}.retirement.reason is invalid",
        )
        evidence_ref = evidence_ref_value(
            retirement["evidence_ref"],
            field=f"{card_id}.retirement.evidence_ref",
            allow_none=True,
        )
        retirement["evidence_ref"] = evidence_ref
        if card["lifecycle"] == "archived":
            require(
                reason != "none", f"{card_id} archived card needs a retirement reason"
            )
            require(
                evidence_ref != "none",
                f"{card_id} archived card needs retirement evidence",
            )
        else:
            require(reason == "none", f"{card_id} non-archived card cannot be retired")
            require(
                evidence_ref == "none",
                f"{card_id} non-archived retirement evidence must be none",
            )

        card["areas"] = string_list(
            card["areas"],
            field=f"{card_id}.areas",
            maximum_items=8,
            maximum_item_length=80,
        )
        card["trigger_tags"] = string_list(
            card["trigger_tags"],
            field=f"{card_id}.trigger_tags",
            maximum_items=10,
            maximum_item_length=80,
        )
        card["related_skills"] = string_list(
            card["related_skills"],
            field=f"{card_id}.related_skills",
            maximum_items=8,
            maximum_item_length=80,
        )
        card["applicability_conditions"] = string_list(
            card["applicability_conditions"],
            field=f"{card_id}.applicability_conditions",
            maximum_items=4,
        )
        card["counter_conditions"] = string_list(
            card["counter_conditions"],
            field=f"{card_id}.counter_conditions",
            maximum_items=4,
        )
        string_value(card["reasoning_cue"], field=f"{card_id}.reasoning_cue")
        evidence_refs = string_list(
            card["evidence_refs"],
            field=f"{card_id}.evidence_refs",
            maximum_items=4,
        )
        card["evidence_refs"] = [
            evidence_ref_value(item, field=f"{card_id}.evidence_refs")
            for item in evidence_refs
        ]
    return value


def validate_catalog(path: Path = CATALOG) -> dict[str, Any]:
    return validate_catalog_data(read_strict_json(path))


def normalize_triggers(values: Iterable[str]) -> set[str]:
    triggers = {normalize(value) for value in values if value.strip()}
    unknown = sorted(triggers - TRIGGER_SIGNALS)
    require(not unknown, f"unknown trigger signal: {unknown}")
    return triggers


def empty_result(*, trigger_gate_met: bool, catalog_loaded: bool) -> dict[str, Any]:
    return {
        "contract": SELECTION_CONTRACT,
        "trigger_gate_met": trigger_gate_met,
        "catalog_loaded": catalog_loaded,
        "ordinary_lifecycle_filter": sorted(ORDINARY_LIFECYCLES),
        "hard_result_cap": MAX_ORDINARY_RESULTS,
        "selected_count": 0,
        "full_records_loaded_into_output": False,
        "cards": [],
    }


def select_cards(
    *,
    catalog: dict[str, Any],
    trigger_signals: Iterable[str],
    tags: Iterable[str],
    skills: Iterable[str],
    limit: int = MAX_ORDINARY_RESULTS,
) -> dict[str, Any]:
    validate_catalog_data(catalog)
    triggers = normalize_triggers(trigger_signals)
    require(1 <= limit <= MAX_ORDINARY_RESULTS, "ordinary result limit must be 1..3")
    if not triggers:
        return empty_result(trigger_gate_met=False, catalog_loaded=True)

    query_tags = {normalize(item) for item in tags if item.strip()}
    query_skills = {normalize(item) for item in skills if item.strip()}
    if not query_tags and not query_skills:
        return empty_result(trigger_gate_met=True, catalog_loaded=True)

    ranked: list[tuple[int, str, dict[str, Any], list[str]]] = []
    for card in catalog["cards"]:
        if card["lifecycle"] not in ORDINARY_LIFECYCLES:
            continue
        areas = {normalize(item) for item in card["areas"]}
        trigger_tags = {normalize(item) for item in card["trigger_tags"]}
        related_skills = {normalize(item) for item in card["related_skills"]}
        area_hits = sorted(query_tags & areas)
        tag_hits = sorted(query_tags & trigger_tags)
        skill_hits = sorted(query_skills & related_skills)
        specific_skill_hits = sorted(set(skill_hits) - GENERIC_ROOT_SKILLS)
        root_skill_hits = sorted(set(skill_hits) & GENERIC_ROOT_SKILLS)
        if not (area_hits or tag_hits or specific_skill_hits):
            continue
        lifecycle_score = 3 if card["lifecycle"] == "distilled" else 2
        score = (
            12 * len(tag_hits)
            + 10 * len(area_hits)
            + 9 * len(specific_skill_hits)
            + len(root_skill_hits)
            + lifecycle_score
        )
        why = [
            *(f"skill:{item}" for item in specific_skill_hits),
            *(f"root-skill-tiebreaker:{item}" for item in root_skill_hits),
            *(f"trigger-tag:{item}" for item in tag_hits),
            *(f"area:{item}" for item in area_hits),
        ]
        ranked.append((score, card["id"], card, why))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    cards = [
        {
            "id": card["id"],
            "title": card["title"],
            "kind": card["kind"],
            "lifecycle": card["lifecycle"],
            "match_score": score,
            "why_matched": why,
            "reasoning_cue": card["reasoning_cue"],
            "applicability_conditions": card["applicability_conditions"],
            "counter_conditions": card["counter_conditions"],
            "evidence_refs": card["evidence_refs"],
        }
        for score, _, card, why in ranked[:limit]
    ]
    result = empty_result(trigger_gate_met=True, catalog_loaded=True)
    result["selected_count"] = len(cards)
    result["cards"] = cards
    return result


def select_from_path(
    *,
    path: Path,
    trigger_signals: Iterable[str],
    tags: Iterable[str],
    skills: Iterable[str],
    limit: int = MAX_ORDINARY_RESULTS,
) -> dict[str, Any]:
    triggers = normalize_triggers(trigger_signals)
    require(1 <= limit <= MAX_ORDINARY_RESULTS, "ordinary result limit must be 1..3")
    if not triggers:
        return empty_result(trigger_gate_met=False, catalog_loaded=False)
    return select_cards(
        catalog=validate_catalog(path),
        trigger_signals=triggers,
        tags=tags,
        skills=skills,
        limit=limit,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate or select compact adaptive-development experience cues."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--catalog", type=Path, default=CATALOG)
    select = commands.add_parser("select")
    select.add_argument("--catalog", type=Path, default=CATALOG)
    select.add_argument("--trigger", action="append", default=[])
    select.add_argument("--tag", action="append", default=[])
    select.add_argument("--skill", action="append", default=[])
    select.add_argument("--limit", type=int, default=MAX_ORDINARY_RESULTS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "validate":
            catalog = validate_catalog(args.catalog)
            result: dict[str, Any] = {
                "contract": CATALOG_SCHEMA,
                "status": "valid",
                "record_count": catalog["record_count"],
            }
        else:
            result = select_from_path(
                path=args.catalog,
                trigger_signals=args.trigger,
                tags=args.tag,
                skills=args.skill,
                limit=args.limit,
            )
    except DevelopmentExperienceError as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
