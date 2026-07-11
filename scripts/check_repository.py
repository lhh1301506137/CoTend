from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CAPABILITIES = {f"C{number:02d}" for number in range(1, 20)}
EXPECTED_JOURNEYS = [f"J{number}" for number in range(1, 7)]
EXPECTED_NOVICE_STATUSES = {
    "draft_for_review",
    "reviewed_pending_user_confirmation",
    "active_user_confirmed",
}
EXPECTED_INTERFACE_DESIGN_STATUSES = {
    "unconfirmed",
    "baseline_user_confirmed",
}
EXPECTED_JOURNEY_RESULTS = [
    "success",
    "blocked",
    "failure",
    "deferred",
    "interrupted",
    "recovery_required",
]
EXPECTED_NOVICE_FIXTURES = {
    "F01": ("start", "question_or_confirmation", "yes", "framework"),
    "F02": ("start", "question_or_confirmation", "yes", "framework"),
    "F03": ("start", "question_or_confirmation", "yes", "framework"),
    "F04": ("start", "readiness_report", "no", "framework"),
    "F05": ("continue", "work_checkpoint", "no", "framework"),
    "F06": ("continue", "blocked_decision", "yes", "framework"),
    "F07": ("continue", "work_checkpoint", "yes", "framework"),
    "F08": ("continue", "failure_containment", "no", "framework"),
    "F09": ("change", "change_disposition", "yes", "framework"),
    "F10": ("change", "change_disposition", "no", "framework"),
    "F11": ("change", "interruption_checkpoint", "yes", "framework"),
    "F12": ("change", "change_disposition", "no", "framework"),
    "F13": ("recover", "recovery_report", "no", "framework"),
    "F14": ("recover", "recovery_report", "yes", "framework"),
    "F15": ("recover", "handoff_readiness", "no", "framework"),
    "F16": ("recover", "recovery_report", "no", "framework"),
    "F17": ("evaluate", "acceptance_walkthrough", "yes", "framework"),
    "F18": ("evaluate", "done_gate", "yes", "framework"),
    "F19": ("evaluate", "blocked_decision", "yes", "framework"),
    "F20": ("advanced", "diagnosis_report", "yes", "framework"),
    "F21": ("advanced", "model_options", "yes", "framework"),
    "F22": ("advanced", "learning_proposal", "yes", "framework"),
    "F23": ("advanced", "release_readiness", "yes", "framework"),
    "F24": ("advanced", "delivery_preflight", "yes", "framework"),
}
EXPECTED_NOVICE_PROMPT_SHA256 = "6852cad0c78a44e33b7f784e107165e6a59cb7f4afd04a52732d4efc4a3ba0f7"
EXPECTED_INTERFACE_GATES = [f"H{number}" for number in range(1, 9)]
EXPECTED_INTERFACE_CANDIDATES = [f"I{number}" for number in range(1, 7)]
EXPECTED_CONFIRMED_INTERFACE_CATALOG_SHA256 = (
    "0136eba98238743d9780f428a7acff03a26a8e211ebfb795ee0c68f754a20091"
)
EXPECTED_INTERFACE_DESTINATIONS = {
    "start": ("core", ("first", "confirmed", "route")),
    "continue": ("core", ("already current", "failure", "bounded", "verified")),
    "change": ("core", ("user correction", "new idea", "priority", "stop")),
    "recover": ("core", ("resume", "project truth", "hand")),
    "evaluate": ("core", ("test", "user's decision", "without implying acceptance")),
    "advanced:diagnosis": ("contextual", ("without editing", "repair", "user-authorized")),
    "advanced:model_roles": ("contextual", ("advice", "takeovers", "rollback", "cost", "data")),
    "advanced:framework_learning": (
        "contextual",
        ("repeated failures", "reversible", "improvement proposal"),
    ),
    "advanced:release": (
        "contextual",
        ("before", "push", "without performing the external action"),
    ),
    "advanced:platform_delivery": (
        "contextual",
        ("install", "update", "permissions", "state retention", "rollback"),
    ),
}
EXPECTED_INTERFACE_FIXTURE_DESTINATIONS = {
    **{f"F{number:02d}": "start" for number in range(1, 5)},
    **{f"F{number:02d}": "continue" for number in range(5, 9)},
    **{f"F{number:02d}": "change" for number in range(9, 13)},
    **{f"F{number:02d}": "recover" for number in range(13, 17)},
    **{f"F{number:02d}": "evaluate" for number in range(17, 20)},
    "F20": "advanced:diagnosis",
    "F21": "advanced:model_roles",
    "F22": "advanced:framework_learning",
    "F23": "advanced:release",
    "F24": "advanced:platform_delivery",
}
EXPECTED_PLATFORM_CLAIMS = [f"P{number:02d}" for number in range(1, 10)]

# checker-self-scan-allowlist-start
LOCAL_ONLY_PATHS = {
    "STATUS.md",
    "PROJECT-PLAN-NODES",
    "REVIEW-LOG.md",
    "docs/COMMAND-CONTRACTS.md",
    "QUALITY-SIGNALS.md",
    "PROJECT-UNDERSTANDING",
    "PROJECT-DECISION-LOG.md",
    "docs/V1-ARCHITECTURE.md",
    "PROJECT-KNOWLEDGE-CHANGELOG.md",
    "docs/PROJECT-STATE-CONTRACT.md",
    "PROJECT-PLAN-TREE.md",
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "private upstream identifier": re.compile(r"\bstartskills\b", re.IGNORECASE),
    "internal AI protocol": re.compile(r"dual-ai-collaboration-v", re.IGNORECASE),
    "local decision ID": re.compile(r"DEC-\d{8}-\d+"),
    "local decision log reference": re.compile(r"PROJECT-DECISION-LOG\.md", re.IGNORECASE),
    "internal authority label": re.compile(r"\bprimary_ai_(?:auto|observed|proposed)\w*", re.IGNORECASE),
    "absolute Windows path": re.compile(r"\b[A-Z]:[\\/]", re.IGNORECASE),
}
FORBIDDEN_UNCONFIRMED_PRD_PATTERNS = {
    "fixed interface-count candidate": re.compile(r"\b5\+1\b", re.IGNORECASE),
    "fixed project-state path": re.compile(r"\.cotend[\\/]", re.IGNORECASE),
    "fixed invocation namespace": re.compile(r"\$cotend:|(?<![\w/])\/cot\b", re.IGNORECASE),
    "fixed plugin and skill bundle": re.compile(
        r"\bPlugin\b.{0,80}\b(?:6|six)\b.{0,40}\bSkills?\b|"
        r"\b(?:6|six)\b.{0,40}\bSkills?\b.{0,80}\bPlugin\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "fixed plugin namespace field": re.compile(r"\bplugin_namespace\b", re.IGNORECASE),
}
# checker-self-scan-allowlist-end


def git_candidates() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return {
        value.decode("utf-8").replace("\\", "/")
        for value in result.stdout.split(b"\0")
        if value
    }


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def table_capabilities(relative_path: str) -> set[str]:
    return set(re.findall(r"^\| (C\d{2}) \|", read(relative_path), re.MULTILINE))


def public_inputs(spec_text: str) -> list[str]:
    match = re.search(
        r"^  public_inputs:\s*$\n(?P<body>(?:^    - .+$\n?)+)",
        spec_text,
        re.MULTILINE,
    )
    if not match:
        return []
    return [line.removeprefix("    - ").strip() for line in match.group("body").splitlines()]


def metadata_values(text: str, key: str) -> set[str]:
    return set(re.findall(rf"^\s*{re.escape(key)}:\s*([^\s#]+)", text, re.MULTILINE))


def metadata_list(text: str, key: str) -> list[str] | None:
    match = re.search(
        rf"^{re.escape(key)}:\s*(?P<inline>\[[^\n]*\])?\s*$",
        text,
        re.MULTILINE,
    )
    if not match:
        return None
    inline = match.group("inline")
    if inline is not None:
        content = inline[1:-1].strip()
        return [] if not content else [value.strip() for value in content.split(",")]

    values: list[str] = []
    for line in text[match.end() :].splitlines():
        if not line.strip():
            continue
        item = re.match(r"^  -\s+(.+?)\s*$", line)
        if not item:
            break
        values.append(item.group(1))
    return values


def index_dependencies(index_text: str) -> dict[str, list[str]]:
    dependencies: dict[str, list[str]] = {}
    for line in index_text.splitlines():
        if not re.match(r"^\| C\d{2} \|", line):
            continue
        cells = [value.strip() for value in line.strip("|").split("|")]
        dependencies[cells[0]] = (
            [] if cells[3] == "none" else [value.strip() for value in cells[3].split(",")]
        )
    return dependencies


def marked_section(text: str, start: str, end: str) -> str | None:
    pattern = re.compile(
        rf"<!-- {re.escape(start)} -->(?P<body>.*?)<!-- {re.escape(end)} -->",
        re.DOTALL,
    )
    match = pattern.search(text)
    return None if match is None else match.group("body")


def novice_journey_errors(journey_text: str) -> list[str]:
    errors: list[str] = []

    journey_statuses = metadata_values(journey_text, "status")
    if len(journey_statuses) != 1 or not journey_statuses <= EXPECTED_NOVICE_STATUSES:
        errors.append("novice journey status is not an allowed lifecycle state")
    try:
        journey_text.encode("ascii")
    except UnicodeEncodeError:
        errors.append("novice journey public text must remain ASCII English")

    for marker in (
        "novice-guide-start",
        "novice-guide-end",
        "fixture-prompts-start",
        "fixture-prompts-end",
    ):
        if journey_text.count(f"<!-- {marker} -->") != 1:
            errors.append(f"novice journey marker must appear exactly once: {marker}")

    interface_design_statuses = metadata_values(journey_text, "interface_design_status")
    if (
        len(interface_design_statuses) != 1
        or interface_design_statuses - EXPECTED_INTERFACE_DESIGN_STATUSES
    ):
        errors.append("novice journeys interface_design_status is not allowed")

    for key in (
        "architecture_design_status",
        "project_state_layout_status",
        "distribution_design_status",
    ):
        if metadata_values(journey_text, key) != {"unconfirmed"}:
            errors.append(f"novice journeys {key} must remain unconfirmed")

    if metadata_values(journey_text, "product_baseline_version") != {"0.1.0"}:
        errors.append("novice journey product baseline must be 0.1.0")
    if metadata_values(journey_text, "phase") != {"P2_design_novice_product_surface"}:
        errors.append("novice journey phase must remain P2 design")
    if metadata_values(journey_text, "public_language") != {"en"}:
        errors.append("novice journey public language must be en")
    if metadata_values(journey_text, "fixture_corpus_version") != {"3"}:
        errors.append("novice journey fixture corpus version must be 3")
    if metadata_values(journey_text, "fixture_count") != {"24"}:
        errors.append("novice journey fixture count must be 24")
    if metadata_values(journey_text, "fixture_prompt_sha256") != {
        EXPECTED_NOVICE_PROMPT_SHA256
    }:
        errors.append("novice journey prompt hash metadata does not match corpus version 3")

    guide_section = marked_section(journey_text, "novice-guide-start", "novice-guide-end")
    if guide_section is None:
        errors.append("novice guide packet markers are missing or out of order")
        guide_section = ""
    journey_ids = re.findall(r"^## (J\d+)\b", guide_section, re.MULTILINE)
    if journey_ids != EXPECTED_JOURNEYS:
        errors.append(f"evaluator-visible novice journey IDs must be J1-J6 in order: {journey_ids}")
    all_journey_ids = re.findall(r"^## (J\d+)\b", journey_text, re.MULTILINE)
    if all_journey_ids != EXPECTED_JOURNEYS:
        errors.append(f"novice journey IDs outside the evaluator packet are not allowed: {all_journey_ids}")

    journey_matches = list(re.finditer(r"^## (J\d+)\b", guide_section, re.MULTILINE))
    for index, match in enumerate(journey_matches):
        end = journey_matches[index + 1].start() if index + 1 < len(journey_matches) else len(guide_section)
        body = guide_section[match.start() : end]
        results = re.findall(
            r"^\| `(success|blocked|failure|deferred|interrupted|recovery_required)` \|",
            body,
            re.MULTILINE,
        )
        if results != EXPECTED_JOURNEY_RESULTS:
            errors.append(f"{match.group(1)} result map is incomplete or out of order: {results}")

    capability_rows = re.findall(r"^\| (C\d{2}) \|", journey_text, re.MULTILINE)
    expected_capability_rows = [f"C{number:02d}" for number in range(1, 20)]
    if capability_rows != expected_capability_rows:
        errors.append(
            "novice journey capability matrix must contain C01-C19 exactly once and in order"
        )

    prompt_section = marked_section(journey_text, "fixture-prompts-start", "fixture-prompts-end")
    if prompt_section is None:
        errors.append("novice journey fixture prompt markers are missing")
    else:
        prompt_hash = hashlib.sha256(prompt_section.encode("utf-8")).hexdigest()
        if prompt_hash != EXPECTED_NOVICE_PROMPT_SHA256:
            errors.append(f"novice journey prompt corpus hash mismatch: {prompt_hash}")
        prompt_ids = re.findall(r"^\| (F\d{2}) \|", prompt_section, re.MULTILINE)
        if prompt_ids != list(EXPECTED_NOVICE_FIXTURES):
            errors.append(f"novice journey prompts must be frozen F01-F24: {prompt_ids}")

    answer_match = re.search(
        r"^### Frozen Answer Key\s*$\n(?P<body>.*?)(?=^### Pass Criteria\s*$)",
        journey_text,
        re.MULTILINE | re.DOTALL,
    )
    if answer_match is None:
        errors.append("novice journey answer key is missing")
    else:
        answer_rows = re.findall(
            r"^\| (F\d{2}) \| `([a-z_]+)` \| `([a-z_]+)` \| `(yes|no)` \| `(framework|downstream_project|unclear)` \|$",
            answer_match.group("body"),
            re.MULTILINE,
        )
        answer_ids = [fixture_id for fixture_id, _, _, _, _ in answer_rows]
        if answer_ids != list(EXPECTED_NOVICE_FIXTURES):
            errors.append(f"novice journey answers must be frozen F01-F24: {answer_ids}")
        actual_answers = {
            fixture_id: (entry_class, next_outcome, decision, cotend_role)
            for fixture_id, entry_class, next_outcome, decision, cotend_role in answer_rows
        }
        if actual_answers != EXPECTED_NOVICE_FIXTURES:
            errors.append("novice journey frozen answer key does not match corpus version 3")

    if "CoTend is the product." not in journey_text:
        errors.append("novice journeys must preserve the framework product boundary")
    if "The downstream software used in this proof is a fixture." not in journey_text:
        errors.append("novice journeys must preserve the downstream fixture boundary")

    return errors


def interface_evidence_errors(
    evidence_text: str,
    interface_text: str,
    journey_text: str,
    expected_mapping: dict[str, tuple[str, str]],
    catalog_skill_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    try:
        evidence_text.encode("ascii")
    except UnicodeEncodeError:
        errors.append("interface evidence must remain ASCII English")

    exact_metadata = {
        "status": {"executed_public_safe"},
        "source_document": {"docs/INTERFACE-CANDIDATE-EVALUATION.md"},
        "journey_prompt_sha256": {EXPECTED_NOVICE_PROMPT_SHA256},
        "repository_access": {"none"},
        "tool_use": {"none"},
        "expected_rows": {"24"},
        "exact_rows": {"24"},
        "correct_decision_flags": {"24"},
        "required_user_stops": {"16_of_16"},
        "verdict": {"pass"},
    }
    for key, expected in exact_metadata.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"interface evidence metadata mismatch: {key}")

    interface_versions = metadata_values(interface_text, "interface_mapping_version")
    if metadata_values(evidence_text, "evaluation_version") != interface_versions:
        errors.append("interface evidence version does not match the candidate packet")
    catalog_hashes = metadata_values(interface_text, "interface_catalog_sha256")
    if metadata_values(evidence_text, "catalog_sha256") != catalog_hashes:
        errors.append("interface evidence catalog hash does not match the candidate packet")
    if len(metadata_values(evidence_text, "evaluator_surface")) != 1:
        errors.append("interface evidence must record one evaluator surface")
    if len(metadata_values(evidence_text, "evaluator_model")) != 1:
        errors.append("interface evidence must record one evaluator model label")
    evaluator_cli = metadata_values(evidence_text, "evaluator_cli")
    if len(evaluator_cli) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", next(iter(evaluator_cli), "")):
        errors.append("interface evidence must record one semantic CLI version")

    for marker in (
        "evaluator-rules-start",
        "evaluator-rules-end",
        "evaluator-output-start",
        "evaluator-output-end",
    ):
        if evidence_text.count(f"<!-- {marker} -->") != 1:
            errors.append(f"interface evidence marker must appear exactly once: {marker}")

    rules = marked_section(evidence_text, "evaluator-rules-start", "evaluator-rules-end") or ""
    catalog = marked_section(interface_text, "interface-catalog-start", "interface-catalog-end") or ""
    prompts = marked_section(journey_text, "fixture-prompts-start", "fixture-prompts-end") or ""
    packet_hash = hashlib.sha256((rules + catalog + prompts).encode("utf-8")).hexdigest()
    if metadata_values(evidence_text, "packet_sha256") != {packet_hash}:
        errors.append("interface evidence packet hash mismatch")

    output = marked_section(evidence_text, "evaluator-output-start", "evaluator-output-end") or ""
    output_hash = hashlib.sha256(output.encode("utf-8")).hexdigest()
    if metadata_values(evidence_text, "raw_output_sha256") != {output_hash}:
        errors.append("interface evidence raw-output hash mismatch")
    output_block = re.fullmatch(r"\s*```text\n(?P<rows>.*?)\n```\s*", output, re.DOTALL)
    if output_block is None:
        errors.append("interface evidence output must contain exactly one text block")
        output_rows: list[tuple[str, str, str]] = []
    else:
        rows_text = output_block.group("rows")
        output_rows = re.findall(
            r"^(F\d{2}) \| (\$cotend-[a-z0-9-]+) \| (yes|no)$",
            rows_text,
            re.MULTILINE,
        )
        if len(output_rows) != len(rows_text.splitlines()):
            errors.append("interface evidence output contains an unexpected line")

    output_ids = [fixture_id for fixture_id, _, _ in output_rows]
    if output_ids != list(expected_mapping):
        errors.append(f"interface evidence output must contain F01-F24 in order: {output_ids}")
    actual_output = {
        fixture_id: (skill_id, decision)
        for fixture_id, skill_id, decision in output_rows
    }
    if actual_output != expected_mapping:
        errors.append("interface evidence output does not score 24 of 24")
    if {skill_id for _, skill_id, _ in output_rows} != catalog_skill_ids:
        errors.append("interface evidence does not exercise every catalog entry")

    return errors


def interface_candidate_errors(
    interface_text: str,
    journey_text: str,
    evidence_text: str | None = None,
) -> list[str]:
    errors: list[str] = []

    statuses = metadata_values(interface_text, "status")
    if len(statuses) != 1 or statuses - EXPECTED_NOVICE_STATUSES:
        errors.append("interface evaluation must declare one allowed lifecycle status")
    try:
        interface_text.encode("ascii")
    except UnicodeEncodeError:
        errors.append("interface evaluation public text must remain ASCII English")

    exact_metadata = {
        "product_baseline_version": {"0.1.0"},
        "phase": {"P2_design_novice_product_surface"},
        "public_language": {"en"},
        "launch_platform": {"Codex"},
        "architecture_design_status": {"unconfirmed"},
        "project_state_layout_status": {"unconfirmed"},
        "distribution_design_status": {"unconfirmed"},
        "fixture_source": {"docs/NOVICE-JOURNEYS.md"},
        "fixture_source_version": {"3"},
        "fixture_source_prompt_sha256": {EXPECTED_NOVICE_PROMPT_SHA256},
        "interface_mapping_count": {"24"},
        "blind_exact_rows": {"24_of_24"},
        "blind_user_stops": {"16_of_16"},
        "blind_result": {"pass"},
    }
    for key, expected in exact_metadata.items():
        if metadata_values(interface_text, key) != expected:
            errors.append(f"interface evaluation metadata mismatch: {key}")

    lifecycle = next(iter(statuses), "") if len(statuses) == 1 else ""
    expected_authority_state = {
        "draft_for_review": ("pending_user_confirmation", "unconfirmed"),
        "reviewed_pending_user_confirmation": (
            "pending_user_confirmation",
            "unconfirmed",
        ),
        "active_user_confirmed": (
            "active_user_confirmed",
            "baseline_user_confirmed",
        ),
    }.get(lifecycle)
    if expected_authority_state is not None:
        recommendation_status, interface_design_status = expected_authority_state
        if metadata_values(interface_text, "recommendation_status") != {
            recommendation_status
        }:
            errors.append("interface recommendation authority does not match lifecycle")
        if metadata_values(interface_text, "interface_design_status") != {
            interface_design_status
        }:
            errors.append("interface design authority does not match lifecycle")

    if lifecycle == "active_user_confirmed":
        if metadata_values(interface_text, "recommendation_candidate") != {"I6"}:
            errors.append("active interface baseline must preserve confirmed candidate I6")
        if metadata_values(interface_text, "recommendation_strategy") != {
            "layered_common_prefix"
        }:
            errors.append(
                "active interface baseline must preserve the confirmed strategy"
            )
        if metadata_values(interface_text, "interface_catalog_sha256") != {
            EXPECTED_CONFIRMED_INTERFACE_CATALOG_SHA256
        }:
            errors.append("active interface baseline catalog differs from user confirmation")
        for required_text in (
            "The user has confirmed this recommendation as the P2 interface baseline.",
            "## Confirmed Interface Baseline",
            "Recommend, user confirmed.",
        ):
            if required_text not in interface_text:
                errors.append(
                    f"active interface baseline is missing confirmation text: {required_text}"
                )
        for stale_text in (
            "candidate awaiting user confirmation",
            "Recommend, pending user confirmation.",
            "subject to user confirmation",
            "The user is being asked to confirm",
            "does not activate the recommendation",
        ):
            if stale_text in interface_text:
                errors.append(
                    f"active interface baseline retains pending text: {stale_text}"
                )

    recommendation_candidates = metadata_values(interface_text, "recommendation_candidate")
    recommendation_strategies = metadata_values(interface_text, "recommendation_strategy")
    if len(recommendation_candidates) != 1:
        errors.append("interface evaluation must name one recommendation candidate")
    if len(recommendation_strategies) != 1 or not re.fullmatch(
        r"[a-z][a-z0-9_]+", next(iter(recommendation_strategies), "")
    ):
        errors.append("interface evaluation must name one recommendation strategy")
    mapping_versions = metadata_values(interface_text, "interface_mapping_version")
    if len(mapping_versions) != 1 or not next(iter(mapping_versions), "").isdigit():
        errors.append("interface mapping version must be a positive integer")

    for marker in (
        "platform-evidence-start",
        "platform-evidence-end",
        "interface-catalog-start",
        "interface-catalog-end",
    ):
        if interface_text.count(f"<!-- {marker} -->") != 1:
            errors.append(f"interface marker must appear exactly once: {marker}")

    gate_ids = re.findall(r"^\| (H\d+) \|", interface_text, re.MULTILINE)
    if gate_ids != EXPECTED_INTERFACE_GATES:
        errors.append(f"interface hard gates must be H1-H8 in order: {gate_ids}")

    candidate_rows = re.findall(
        r"^\| (I\d+) \| (?P<candidate>[^|]+) \| (?P<strength>[^|]+) \| "
        r"(?P<weakness>[^|]+) \| (?P<disposition>[^|]+) \|$",
        interface_text,
        re.MULTILINE,
    )
    candidate_ids = [row[0] for row in candidate_rows]
    if candidate_ids != EXPECTED_INTERFACE_CANDIDATES:
        errors.append(f"interface candidates must be I1-I6 in order: {candidate_ids}")
    recommendation_candidate = next(iter(recommendation_candidates), "")
    dispositions = {row[0]: row[4].strip() for row in candidate_rows}
    if recommendation_candidate not in dispositions or not dispositions.get(
        recommendation_candidate, ""
    ).startswith("Recommend"):
        errors.append("the metadata recommendation must match the recommended candidate row")

    platform_evidence = marked_section(
        interface_text, "platform-evidence-start", "platform-evidence-end"
    ) or ""
    platform_hash = hashlib.sha256(platform_evidence.encode("utf-8")).hexdigest()
    if metadata_values(interface_text, "platform_evidence_sha256") != {platform_hash}:
        errors.append("platform evidence table hash mismatch")
    platform_rows = re.findall(
        r"^\| (P\d{2}) \| ([^|]+) \| \[[^\]]+\]"
        r"\((https://learn\.chatgpt\.com/[^)]+)\) \| (\d{4}-\d{2}-\d{2}) \| ([^|]+) \|$",
        platform_evidence,
        re.MULTILINE,
    )
    platform_ids = [claim_id for claim_id, _, _, _, _ in platform_rows]
    if platform_ids != EXPECTED_PLATFORM_CLAIMS:
        errors.append(f"platform evidence claims must be P01-P09 in order: {platform_ids}")
    evidence_dates = metadata_values(interface_text, "platform_evidence_date")
    if len(evidence_dates) != 1 or any(row[3] not in evidence_dates for row in platform_rows):
        errors.append("platform evidence rows must use the recorded access date")
    for claim_id, claim, _, _, boundary in platform_rows:
        if len(claim.strip()) < 24 or len(boundary.strip()) < 24:
            errors.append(f"platform evidence claim is not bounded enough: {claim_id}")
    p04_boundary = next((row[4].casefold() for row in platform_rows if row[0] == "P04"), "")
    if "vary" not in p04_boundary or "verify" not in p04_boundary:
        errors.append("slash-list evidence must disclose environment variation and re-verification")

    catalog = marked_section(interface_text, "interface-catalog-start", "interface-catalog-end") or ""
    catalog_hash = hashlib.sha256(catalog.encode("utf-8")).hexdigest()
    if metadata_values(interface_text, "interface_catalog_sha256") != {catalog_hash}:
        errors.append("interface catalog metadata hash mismatch")
    catalog_rows = re.findall(
        r"^\| `([^`]+)` \| `([^`]+)` \| (core|contextual) \| `([^`]+)` \| ([^|]+) \|$",
        catalog,
        re.MULTILINE,
    )
    if len(catalog_rows) != len(EXPECTED_INTERFACE_DESTINATIONS):
        errors.append("interface catalog must contain ten unique semantic destinations")
    actual_entries = {
        skill_id: (display_name, layer, destination, description.strip())
        for skill_id, display_name, layer, destination, description in catalog_rows
    }
    if len(actual_entries) != len(catalog_rows):
        errors.append("interface catalog Skill IDs must be unique")
    if len({row[1] for row in catalog_rows}) != len(catalog_rows):
        errors.append("interface catalog display names must be unique")
    destination_to_skill = {destination: skill_id for skill_id, _, _, destination, _ in catalog_rows}
    if set(destination_to_skill) != set(EXPECTED_INTERFACE_DESTINATIONS):
        errors.append("interface catalog semantic destinations are incomplete or duplicated")
    for skill_id, (display_name, layer, destination, description) in actual_entries.items():
        if not skill_id.startswith("$cotend-"):
            errors.append(f"interface Skill ID lacks the cotend- prefix: {skill_id}")
        if not display_name.startswith("CoTend "):
            errors.append(f"interface display name lacks the CoTend prefix: {display_name}")
        expected_layer, required_terms = EXPECTED_INTERFACE_DESTINATIONS.get(
            destination, (None, ())
        )
        if layer != expected_layer:
            errors.append(f"interface destination has the wrong surface layer: {destination}")
        description_text = description.casefold()
        missing_terms = [term for term in required_terms if term not in description_text]
        if missing_terms:
            errors.append(f"interface description is incomplete for {destination}: {missing_terms}")
    if "$cotend-advanced" in actual_entries or any(
        display_name == "CoTend Advanced"
        for display_name, _, _, _ in actual_entries.values()
    ):
        errors.append("a generic advanced entry is not allowed")

    expected_mapping = {
        fixture_id: (
            destination_to_skill.get(destination, ""),
            EXPECTED_NOVICE_FIXTURES[fixture_id][2],
        )
        for fixture_id, destination in EXPECTED_INTERFACE_FIXTURE_DESTINATIONS.items()
    }
    mapping_match = re.search(
        r"^### Frozen Interface Mapping\s*$\n(?P<body>.*?)(?=^### Pass Criteria\s*$)",
        interface_text,
        re.MULTILINE | re.DOTALL,
    )
    if mapping_match is None:
        errors.append("frozen interface mapping is missing")
    else:
        mapping_rows = re.findall(
            r"^\| (F\d{2}) \| `([^`]+)` \| `(yes|no)` \|$",
            mapping_match.group("body"),
            re.MULTILINE,
        )
        mapping_ids = [fixture_id for fixture_id, _, _ in mapping_rows]
        if mapping_ids != list(expected_mapping):
            errors.append(f"interface mapping must contain F01-F24 in order: {mapping_ids}")
        actual_mapping = {
            fixture_id: (skill_id, decision)
            for fixture_id, skill_id, decision in mapping_rows
        }
        if actual_mapping != expected_mapping:
            errors.append("interface frozen mapping does not match its semantic catalog")

    evidence_paths = metadata_values(interface_text, "blind_evidence")
    if len(evidence_paths) != 1 or not next(iter(evidence_paths), "").startswith("docs/evidence/"):
        errors.append("interface evaluation must name one public-safe blind evidence file")
    elif evidence_text is None:
        errors.append("interface blind evidence file is missing")
    else:
        errors.extend(
            interface_evidence_errors(
                evidence_text,
                interface_text,
                journey_text,
                expected_mapping,
                set(actual_entries),
            )
        )

    if "docs/COMMAND-CONTRACTS.md" in interface_text:
        errors.append("interface evaluation must not use ignored design history as a public source")
    if "CoTend is the product:" not in interface_text:
        errors.append("interface evaluation must preserve the framework product boundary")
    if "There is no generic `CoTend Advanced` entry" not in interface_text:
        errors.append("interface evaluation must reject a generic advanced placeholder")
    if metadata_values(journey_text, "fixture_prompt_sha256") != {
        EXPECTED_NOVICE_PROMPT_SHA256
    }:
        errors.append("interface evaluation fixture source no longer matches the journey corpus")

    return errors


def interface_authority_errors(
    interface_text: str,
    journey_text: str,
    prd_text: str,
    interface_path: str,
) -> list[str]:
    errors: list[str] = []
    interface_design_status = metadata_values(interface_text, "interface_design_status")
    for source_path, source_text in (
        ("docs/NOVICE-JOURNEYS.md", journey_text),
        ("docs/PRODUCT-PRD.md", prd_text),
    ):
        if metadata_values(source_text, "interface_design_status") != (
            interface_design_status
        ):
            errors.append(f"interface design authority drift: {source_path}")

    if interface_design_status == {"baseline_user_confirmed"}:
        if metadata_values(prd_text, "interface_baseline") != {interface_path}:
            errors.append("PRD must link the active interface baseline")
        if metadata_values(prd_text, "stage") != {"novice_product_surface_design"}:
            errors.append("PRD stage must match the active P2 interface baseline")
        if re.search(
            r"公开入口.{0,20}架构.{0,20}状态布局.{0,20}安装渠道.{0,40}另行决定",
            prd_text,
        ):
            errors.append("PRD retains stale unconfirmed-interface prose")

    return errors


def checker_self_scan_errors(checker_text: str) -> list[str]:
    errors: list[str] = []
    starts = list(
        re.finditer(r"^# checker-self-scan-allowlist-start$", checker_text, re.MULTILINE)
    )
    ends = list(
        re.finditer(r"^# checker-self-scan-allowlist-end$", checker_text, re.MULTILINE)
    )
    if len(starts) != 1 or len(ends) != 1 or starts[0].start() >= ends[0].end():
        return ["checker self-scan allowlist markers are invalid"]
    reduced = checker_text[: starts[0].start()] + checker_text[ends[0].end() :]
    for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
        if pattern.search(reduced):
            errors.append(f"scripts/check_repository.py: {label} outside the policy allowlist")
    return errors


def contract_relationship_errors(index_text: str, specs: dict[str, str]) -> list[str]:
    errors: list[str] = []
    dependencies = index_dependencies(index_text)
    if set(dependencies) != EXPECTED_CAPABILITIES:
        errors.append("behavior dependency index must contain C01-C19")

    for capability, required in dependencies.items():
        unknown = set(required) - set(dependencies)
        if unknown:
            errors.append(f"{capability}: unknown dependencies {sorted(unknown)}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(capability: str) -> None:
        if capability in visiting:
            errors.append(f"behavior dependency cycle includes {capability}")
            return
        if capability in visited:
            return
        visiting.add(capability)
        for dependency in dependencies.get(capability, []):
            visit(dependency)
        visiting.remove(capability)
        visited.add(capability)

    for capability in dependencies:
        visit(capability)

    owner_to_spec: dict[str, str] = {}
    for spec_path, spec_text in specs.items():
        spec_ids = metadata_values(spec_text, "spec_id")
        if len(spec_ids) != 1:
            errors.append(f"{spec_path}: expected one spec_id")
            continue
        spec_id = next(iter(spec_ids))
        declared_dependencies = metadata_list(spec_text, "depends_on")
        declared_consumers = metadata_list(spec_text, "required_by")
        owners = metadata_list(spec_text, "shared_rule_owners")
        if declared_dependencies is None or declared_consumers is None or owners is None:
            errors.append(f"{spec_path}: missing relationship metadata")
            continue
        if declared_dependencies != dependencies.get(spec_id):
            errors.append(f"{spec_id}: depends_on does not match behavior index")
        expected_consumers = sorted(
            capability for capability, required in dependencies.items() if spec_id in required
        )
        if sorted(declared_consumers) != expected_consumers:
            errors.append(f"{spec_id}: required_by is not the inverse dependency index")
        for owner in owners:
            previous = owner_to_spec.get(owner)
            if previous is not None:
                errors.append(f"shared rule owner {owner} is duplicated by {previous} and {spec_id}")
            owner_to_spec[owner] = spec_id

    return errors


def main() -> int:
    errors: list[str] = []
    candidates = git_candidates()

    for local_path in LOCAL_ONLY_PATHS:
        if local_path in candidates or any(path.startswith(f"{local_path}/") for path in candidates):
            errors.append(f"local-only path is publishable: {local_path}")

    text_candidates = {
        path
        for path in candidates
        if (ROOT / path).is_file() and (ROOT / path).suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".py"}
    }
    for relative_path in sorted(text_candidates - {".gitignore", "scripts/check_repository.py"}):
        text = read(relative_path)
        for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative_path}: {label}")
    errors.extend(checker_self_scan_errors(read("scripts/check_repository.py")))

    coverage_ids = table_capabilities("docs/CAPABILITY-COVERAGE.md")
    index_ids = table_capabilities("docs/BEHAVIOR-SPEC-INDEX.md")
    if coverage_ids != EXPECTED_CAPABILITIES:
        errors.append(f"capability coverage mismatch: {sorted(coverage_ids)}")
    if index_ids != EXPECTED_CAPABILITIES:
        errors.append(f"behavior index mismatch: {sorted(index_ids)}")

    index_text = read("docs/BEHAVIOR-SPEC-INDEX.md")
    if metadata_values(index_text, "capability_count") != {"19"}:
        errors.append("behavior index capability_count must be 19")

    prd_text = read("docs/PRODUCT-PRD.md")
    for key in (
        "architecture_design_status",
        "project_state_layout_status",
        "distribution_design_status",
    ):
        if metadata_values(prd_text, key) != {"unconfirmed"}:
            errors.append(f"PRD {key} must remain unconfirmed")
    for label, pattern in FORBIDDEN_UNCONFIRMED_PRD_PATTERNS.items():
        if pattern.search(prd_text):
            errors.append(f"docs/PRODUCT-PRD.md: {label}")

    spec_paths = sorted(
        path
        for path in candidates
        if path.startswith("docs/behavior-specs/") and path.endswith(".md")
    )
    spec_texts = {spec_path: read(spec_path) for spec_path in spec_paths}
    for spec_path in spec_paths:
        spec_text = spec_texts[spec_path]
        inputs = public_inputs(spec_text)
        if not inputs:
            errors.append(f"{spec_path}: missing public_inputs")
        for input_path in inputs:
            if input_path not in candidates:
                errors.append(f"{spec_path}: public input is missing or ignored: {input_path}")
        if metadata_values(spec_text, "product_baseline_version") != {"0.1.0"}:
            errors.append(f"{spec_path}: product baseline mismatch")
    errors.extend(contract_relationship_errors(index_text, spec_texts))

    journey_path = "docs/NOVICE-JOURNEYS.md"
    journey_text = ""
    if journey_path not in candidates:
        errors.append("novice journey specification is missing or ignored")
    else:
        journey_text = read(journey_path)
        errors.extend(novice_journey_errors(journey_text))

    interface_path = "docs/INTERFACE-CANDIDATE-EVALUATION.md"
    interface_text = ""
    if interface_path not in candidates:
        errors.append("interface candidate evaluation is missing or ignored")
    else:
        interface_text = read(interface_path)
        evidence_paths = metadata_values(interface_text, "blind_evidence")
        evidence_path = next(iter(evidence_paths), "") if len(evidence_paths) == 1 else ""
        evidence_text = read(evidence_path) if evidence_path in candidates else None
        errors.extend(interface_candidate_errors(interface_text, journey_text, evidence_text))

    if interface_text:
        errors.extend(
            interface_authority_errors(
                interface_text,
                journey_text,
                prd_text,
                interface_path,
            )
        )

    status_path = ROOT / "STATUS.md"
    plan_path = ROOT / "PROJECT-PLAN-TREE.md"
    if status_path.exists() and plan_path.exists():
        status_leaves = metadata_values(read("STATUS.md"), "current_next_leaf")
        plan_leaves = metadata_values(read("PROJECT-PLAN-TREE.md"), "current_next_leaf")
        if len(status_leaves) != 1 or status_leaves != plan_leaves:
            errors.append(f"local active leaf drift: STATUS={sorted(status_leaves)} PLAN={sorted(plan_leaves)}")

    understanding_index = ROOT / "PROJECT-UNDERSTANDING" / "README.md"
    if understanding_index.exists() and "active_route:" in understanding_index.read_text(encoding="utf-8"):
        errors.append("understanding index must not duplicate the active route")

    root_understanding = ROOT / "PROJECT-UNDERSTANDING" / "G0-full-project-understanding.md"
    if root_understanding.exists():
        root_text = root_understanding.read_text(encoding="utf-8")
        if re.search(r"\b16\s*个能力", root_text) or "C01-C19" not in root_text:
            errors.append("root understanding capability baseline drift")

    if errors:
        print("REPOSITORY_CHECK_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "REPOSITORY_CHECK_OK "
        f"public_candidates={len(candidates)} capabilities={len(EXPECTED_CAPABILITIES)} "
        f"behavior_specs={len(spec_paths)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
