from __future__ import annotations

import hashlib
import json
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
EXPECTED_REFERENCE_SOURCES = {
    "RF01": (
        "https://github.com/obra/superpowers",
        "d884ae04edebef577e82ff7c4e143debd0bbec99",
        "MIT",
    ),
    "RF02": (
        "https://github.com/mindfold-ai/trellis",
        "bde902cad75813c73f1413bf8da581168a835b37",
        "AGPL-3.0",
    ),
    "RF03": (
        "https://github.com/github/spec-kit",
        "1be42992e64b08ff0dce3d7a914eaabf04284ffb",
        "MIT",
    ),
    "RF04": (
        "https://github.com/Fission-AI/OpenSpec",
        "0a99f410457271aa773d8b106f03f637f7c6b3c0",
        "MIT",
    ),
    "RF05": (
        "https://github.com/open-gsd/gsd-core",
        "e3a8c063b8f6059aa4c0214302aec51615a4f831",
        "MIT",
    ),
    "RF06": (
        "https://github.com/bmad-code-org/BMAD-METHOD",
        "49069b8b5276afd21402bc3b978b69ad78a7d2ef",
        "MIT",
    ),
}
EXPECTED_CODEX_CARRIER_FIXTURE_FILES = {
    "AGENTS.md",
    "README.md",
    "live-scenarios.json",
    "scenarios/diagnose/calculator.py",
    "scenarios/fresh/README.md",
    "scenarios/pending-decision/STATUS.md",
    "schemas/diagnose-only.schema.json",
    "schemas/init-delegation.schema.json",
    "schemas/pending-decision.schema.json",
}

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
FRAMEWORK_SOURCE_ALLOWED_PATTERN_LABELS = {
    "local decision log reference",
    "internal authority label",
}
FORBIDDEN_SKILL_MAINTAINER_PATTERNS = {
    "personal maintainer profile": re.compile(r"\bthis user's\b", re.IGNORECASE),
    "machine-specific instruction": re.compile(
        r"\bon this machine\b|codegraph-mcp\.ps1", re.IGNORECASE
    ),
    "private short decision ID": re.compile(r"\bDEC-\d{3}\b"),
    "private legacy sync version": re.compile(r"\bv1\.50\b", re.IGNORECASE),
    "private adapter sync layout": re.compile(
        r"skills-backup|SKILLS-INDEX|command-backups", re.IGNORECASE
    ),
    "forced maintainer language": re.compile(
        r"report in Chinese|written in Chinese|must be Chinese|^\s*language:\s*zh-CN\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
}
FORBIDDEN_UNCONFIRMED_PRD_PATTERNS = {
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


def reference_study_errors(study_text: str, registry_text: str) -> list[str]:
    errors: list[str] = []

    exact_study_metadata = {
        "status": {"research_evidence"},
        "authority": {"design_input_only"},
        "sample": {"four_core_plus_two_selective"},
        "source_registry": {"../UPSTREAM-SOURCES.md"},
        "architecture_design_status": {"unconfirmed"},
        "project_state_layout_status": {"unconfirmed"},
        "distribution_design_status": {"unconfirmed"},
        "execution_evidence": {"none"},
        "source_copying": {"none"},
    }
    for key, expected in exact_study_metadata.items():
        if metadata_values(study_text, key) != expected:
            errors.append(f"reference study metadata mismatch: {key}")

    if metadata_values(registry_text, "implementation_dependency") != {
        "pinned_dual_ai_release_2026_07_11_3"
    }:
        errors.append("upstream registry must pin the adopted primary productization source")
    if metadata_values(registry_text, "source_copying") != {
        "scoped_5_adapted_plus_2_byte_identical_skills"
    }:
        errors.append("upstream registry must record the scoped primary-source adoption")

    blocks = list(
        re.finditer(
            r"^## (RF\d{2}) [^\n]+\n(?P<body>.*?)(?=^## RF\d{2} |^## 审查控制|\Z)",
            registry_text,
            re.MULTILINE | re.DOTALL,
        )
    )
    source_ids = [match.group(1) for match in blocks]
    if source_ids != list(EXPECTED_REFERENCE_SOURCES):
        errors.append(f"upstream source IDs must be RF01-RF06 in order: {source_ids}")

    for match in blocks:
        source_id = match.group(1)
        expected = EXPECTED_REFERENCE_SOURCES.get(source_id)
        if expected is None:
            continue
        body = match.group("body")
        expected_source, expected_commit, expected_license = expected
        exact_values = {
            "source": expected_source,
            "reviewed_commit": expected_commit,
            "declared_license": expected_license,
            "adoption_status": "no_source_adoption",
        }
        for key, value in exact_values.items():
            if metadata_values(body, key) != {value}:
                errors.append(f"{source_id}: upstream registry mismatch for {key}")

    required_findings = (
        "语义入口不等于实体 Skill",
        "项目真相必须独立于适配器",
        "生成文件所有权需要确定性证据",
        "Hook 是可选增强，不是 MVP 前提",
        "安装本身就是小白产品的一部分",
        "本研究不批准任何架构",
    )
    for finding in required_findings:
        if finding not in study_text:
            errors.append(f"reference study is missing a required boundary: {finding}")

    return errors


def owner_document_language_errors(
    prd_text: str,
    analysis_documents: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    exact_language_metadata = {
        "launch_language": {"en"},
        "launch_localization_mode": {"english_only"},
        "canonical_interface_language": {"en"},
        "analysis_document_language": {"zh-CN"},
        "analysis_document_language_authority": {"product_owner_confirmed"},
    }
    for key, expected in exact_language_metadata.items():
        if metadata_values(prd_text, key) != expected:
            errors.append(f"PRD language policy mismatch: {key}")

    for required_boundary in (
        "面向产品 owner 的分析、研究、比较、评估和审查说明正文默认使用简体中文",
        "首发产品表面、安装说明和面向最终用户的产品文档继续使用英文",
    ):
        if required_boundary not in prd_text:
            errors.append(f"PRD language boundary is missing: {required_boundary}")

    expected_analysis_paths = (
        "docs/MARKET-LANDSCAPE.md",
        "docs/REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md",
        "UPSTREAM-SOURCES.md",
        "upstream/FRAMEWORK-ADOPTION-PROPOSAL.md",
        "upstream/FRAMEWORK-ADOPTION-PLAN.md",
        "FRAMEWORK-CHANGE-EVAL.md",
    )
    for path in expected_analysis_paths:
        text = analysis_documents.get(path)
        if text is None:
            errors.append(f"owner-facing analysis is missing or ignored: {path}")
            continue
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`\n]+`", "", prose)
        prose = re.sub(r"\]\([^)]+\)", "]", prose)
        cjk_count = len(re.findall(r"[\u4e00-\u9fff]", prose))
        latin_count = len(re.findall(r"[A-Za-z]", prose))
        if cjk_count == 0 or cjk_count < latin_count:
            errors.append(
                f"{path}: owner-facing prose must be predominantly Chinese "
                f"(cjk={cjk_count}, latin={latin_count})"
            )

    return errors


def productization_truth_errors(
    prd_text: str,
    clean_room_text: str,
    coverage_text: str,
    roadmap_text: str,
    behavior_standard_text: str,
    registry_text: str,
    capability_map_text: str,
    specs: dict[str, str],
    journey_text: str,
    interface_text: str,
    interface_evidence_text: str | None,
) -> list[str]:
    errors: list[str] = []

    exact_prd_metadata = {
        "productization_source": {"dual-ai"},
        "productization_default": {"rename_first_preserve_first"},
        "upstream_adoption_status": {"adopted_verified_repository_source"},
        "interface_design_status": {"unconfirmed"},
        "interface_revalidation_reason": {
            "desktop_selector_and_implicit_discovery_not_validated"
        },
        "stage": {"codex_project_carrier_validated_live_delivery_pending"},
    }
    for key, expected in exact_prd_metadata.items():
        if metadata_values(prd_text, key) != expected:
            errors.append(f"PRD productization truth mismatch: {key}")

    for required_text in (
        "默认产品化方法是 `rename-first`、`preserve-first`",
        "仓库 Codex Skill 的 7 目录分层",
        "项目级 `$skill-name` 显式调用已有真实 Codex 证据",
        "用户原创且由已验证 release 以 Apache-2.0 发布的 dual-ai 内容，可以",
        "ready_for_repository_source_implementation: yes",
        "ready_for_live_delivery: no",
    ):
        if required_text not in prd_text:
            errors.append(f"PRD is missing rename-first boundary: {required_text}")
    for stale_text in (
        "clean-room 独立实现的公开产品",
        "P2 界面基线已由用户确认",
        "I6 的规范入口显示名",
        "当前没有第三方归属声明",
    ):
        if stale_text in prd_text:
            errors.append(f"PRD retains superseded productization text: {stale_text}")

    exact_clean_metadata = {
        "productization_default": {"rename_first_preserve_first"},
        "clean_room_scope": {"restricted_unknown_or_private_material"},
    }
    for key, expected in exact_clean_metadata.items():
        if metadata_values(clean_room_text, key) != expected:
            errors.append(f"source-aware policy metadata mismatch: {key}")
    for required_text in (
        "user_owned_upstream_release",
        "adopted",
        "adapted",
        "未列入 adoption 记录",
        "framework lock",
    ):
        if required_text not in clean_room_text:
            errors.append(f"source-aware policy is missing: {required_text}")
    for stale_text in (
        "私有上游只提供抽象理念",
        "公开版的实现、命名、文案、模板和测试必须从本产品需求重新设计并独立编写",
        "禁止边看上游文件边逐段改名",
    ):
        if stale_text in clean_room_text:
            errors.append(f"source-aware policy retains superseded rule: {stale_text}")

    if metadata_values(coverage_text, "source_method") != {
        "user_owned_upstream_release_trace_plus_user_scenarios"
    }:
        errors.append("capability coverage source method is not upstream-trace based")
    if metadata_values(coverage_text, "productization_default") != {
        "preserve_existing_behavior_before_redesign"
    }:
        errors.append("capability coverage does not preserve upstream behavior by default")
    if "Rename-first productization disposition" not in coverage_text:
        errors.append("capability coverage lacks rename-first dispositions")

    exact_roadmap_metadata = {
        "route_type": {"source_aware_rename_first_productization"},
        "current_phase": {"P4-isolated-codex-carrier-validation"},
    }
    for key, expected in exact_roadmap_metadata.items():
        if metadata_values(roadmap_text, key) != expected:
            errors.append(f"productization roadmap mismatch: {key}")
    if "直接改名和最小适配是默认起点" not in roadmap_text:
        errors.append("productization roadmap lacks the confirmed rename-first default")

    expected_mode_line = (
        "implementation_mode: direct_adoption | rename_only | platform_adaptation | "
        "external_dependency | independent | mixed | pending"
    )
    expected_handoff_line = (
        "Direct adoption, rename-only adaptation, and platform adaptation may read "
        "only files named by the adoption record."
    )
    for required_text in (expected_mode_line, expected_handoff_line):
        if required_text not in behavior_standard_text:
            errors.append(
                f"behavior standard lacks a rename-first implementation mode: {required_text}"
            )
    stale_mode_line = "implementation_mode: direct_adaptation | independent | mixed | pending"
    if stale_mode_line in behavior_standard_text:
        errors.append("behavior standard retains the coarse direct-adaptation mode set")

    if (
        "relationship: primary_user_owned_productization_source_plus_secondary_public_references"
        not in registry_text
    ):
        errors.append("upstream registry does not separate primary and secondary sources")
    for required_text in (
        "## UP01 dual-ai 分享包",
        "role: primary_productization_source",
        "reviewed_release: 2026.07.11.3",
        "adoption_status: repository_source_adopted_verified",
        "candidate_record: upstream/FRAMEWORK-CANDIDATE.json",
        "codex_role_map: upstream/CODEX-SKILL-ROLE-MAP.json",
        "adoption_proposal: upstream/FRAMEWORK-ADOPTION-PROPOSAL.md",
        "adoption_plan: upstream/FRAMEWORK-ADOPTION-PLAN.md",
        "capability_map: upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        "adoption_record: upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption",
        "final_framework_lock: upstream/framework.lock.json",
    ):
        if required_text not in registry_text:
            errors.append(f"upstream registry is missing primary source evidence: {required_text}")

    try:
        capability_map = json.loads(capability_map_text)
    except json.JSONDecodeError as exc:
        capability_map = {}
        errors.append(f"capability implementation map JSON is invalid: {exc}")
    capability_entries = capability_map.get("capabilities")
    modes_by_id: dict[str, str] = {}
    if capability_map.get("status") != "adopted_verified":
        errors.append("capability implementation map is not finalized")
    if not isinstance(capability_entries, list):
        errors.append("capability implementation map entries are invalid")
    else:
        for entry in capability_entries:
            if not isinstance(entry, dict):
                continue
            capability_id = entry.get("capability_id")
            mode = entry.get("implementation_mode")
            if isinstance(capability_id, str) and isinstance(mode, str):
                modes_by_id[capability_id] = mode
        if set(modes_by_id) != EXPECTED_CAPABILITIES:
            errors.append("capability implementation map must contain C01-C19")

    if len(specs) != len(EXPECTED_CAPABILITIES):
        errors.append("productization trace check requires all 19 behavior specs")
    for spec_path, spec_text in specs.items():
        spec_ids = metadata_values(spec_text, "spec_id")
        spec_id = next(iter(spec_ids), "") if len(spec_ids) == 1 else ""
        if metadata_values(spec_text, "upstream_productization_trace") != {"mapped"}:
            errors.append(f"{spec_path}: upstream productization trace must be mapped")
        expected_mode = modes_by_id.get(spec_id)
        if expected_mode is None or metadata_values(spec_text, "implementation_mode") != {
            expected_mode
        }:
            errors.append(f"{spec_path}: implementation mode does not match capability map")
        for required_text in (
            "user_owned_upstream_release",
            "files named by an explicitly adopted and integrity-verified upstream release record",
            "unreleased or private upstream working files",
        ):
            if required_text not in spec_text:
                errors.append(f"{spec_path}: source-aware implementation boundary is missing")
                break

    exact_journey_metadata = {
        "status": {"reviewed_pending_user_confirmation"},
        "interface_design_status": {"unconfirmed"},
        "revalidation_reason": {"rename_first_upstream_surface_not_mapped"},
    }
    for key, expected in exact_journey_metadata.items():
        if metadata_values(journey_text, key) != expected:
            errors.append(f"novice journey revalidation metadata mismatch: {key}")

    exact_interface_metadata = {
        "status": {"reviewed_pending_user_confirmation"},
        "recommendation_status": {"pending_user_confirmation"},
        "interface_design_status": {"unconfirmed"},
        "revalidation_reason": {"existing_dual_ai_surface_was_not_mapped_first"},
    }
    for key, expected in exact_interface_metadata.items():
        if metadata_values(interface_text, key) != expected:
            errors.append(f"interface reopening metadata mismatch: {key}")
    for required_text in (
        "historical candidate evidence",
        "current default is to map and rename the existing surface first",
    ):
        if required_text not in interface_text:
            errors.append(f"interface reopening explanation is missing: {required_text}")
    if interface_evidence_text is None:
        errors.append("historical interface evidence is missing")
    else:
        if metadata_values(interface_evidence_text, "authority") != {
            "historical_candidate_evidence_only"
        }:
            errors.append("interface evidence still appears to grant current authority")
        if metadata_values(interface_evidence_text, "current_interface_authority") != {"none"}:
            errors.append("interface evidence current authority must be none")

    return errors


def upstream_adoption_errors(
    candidate_text: str,
    role_map_text: str,
    proposal_text: str,
    adoption_plan_text: str,
    capability_map_text: str,
    adoption_log_text: str,
    lock_text: str,
    public_candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    try:
        candidate = json.loads(candidate_text)
    except (TypeError, json.JSONDecodeError) as exc:
        return [f"upstream framework candidate JSON is invalid: {exc}"]
    try:
        role_map = json.loads(role_map_text)
    except (TypeError, json.JSONDecodeError) as exc:
        return [f"upstream Codex role-map JSON is invalid: {exc}"]
    try:
        capability_map = json.loads(capability_map_text)
        framework_lock = json.loads(lock_text)
    except (TypeError, json.JSONDecodeError) as exc:
        return [f"upstream adoption JSON is invalid: {exc}"]

    def value(data: dict[str, object], *keys: str) -> object:
        current: object = data
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current

    expected_candidate_values = {
        ("schema",): "cotend.framework-candidate",
        ("schema_version",): 1,
        ("status",): "adopted_verified",
        ("candidate_only",): False,
        ("release_id",): "2026.07.11.3",
        ("framework_protocol_version",): "1.52",
        ("dual_model_upgrade_version",): "1.7",
        ("package_schema_version",): 2,
        ("source_framework_commit",): "5496073e19e239ef19eb055f2b470185fab25d3a",
        ("release_anchor", "type"): "annotated_git_tag",
        ("release_anchor", "tag"): "dual-ai-share-2026.07.11.3",
        ("release_anchor", "tag_object"): "cef8add414a6d9704d3f58785a128bc56f44b263",
        ("release_anchor", "release_commit"): "71e45d9ebeff4d9d61c180711c25267b9fe31549",
        ("release_anchor", "package_tree"): "a70231e0445d9795a00212e8e6c53c149bfbc431",
        ("release_anchor", "publisher_identity_authenticated"): False,
        ("integrity", "manifest_sha256"): (
            "919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006"
        ),
        ("integrity", "manifest_entries"): 65,
        ("integrity", "provenance_covered_files"): 66,
        ("integrity", "verification"): "passed",
        ("carriers", "codex", "skill_count"): 7,
        ("carriers", "claude", "skill_count"): 3,
        ("adoption", "state"): "adopted",
        ("adoption", "source_carrier"): "codex-skills/",
        ("adoption", "capability_map"): "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        ("adoption", "adoption_record"): (
            "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
        ),
        ("adoption", "final_framework_lock_exists"): True,
    }
    for keys, expected in expected_candidate_values.items():
        if value(candidate, *keys) != expected:
            errors.append(f"upstream candidate mismatch: {'.'.join(keys)}")
    expected_skill_trees = {
        "diagnose-only": "88dc2e47dba438720a336c38103308aeae3d635e",
        "dual-ai-collaboration": "b75114a7e0fd2027943ed98217a0f9d581cbdae9",
        "dual-ai-init": "cb233ade310c37e0cd038ff5752eeced92a303f0",
        "dual-ai-project-init": "1f2fdd44e90f31fec310eaf78b02e48de4fed53c",
        "dual-model-upgrade": "dfb25bd4464e0266b665af138a5f3902b44ce281",
        "grill-me": "70df660726ef12349a40dc0353a681c82414fe95",
        "karpathy-guidelines": "e119339197d600aa39a24fd7a95c946800c9c949",
    }
    if value(candidate, "carriers", "codex", "skill_trees") != expected_skill_trees:
        errors.append("upstream candidate Codex Skill tree inventory drift")

    expected_skill_ids = {
        "cotend-init",
        "cotend-project-init",
        "cotend-collaboration",
        "cotend-diagnose-only",
        "cotend-model-upgrade",
        "grill-me",
        "karpathy-guidelines",
    }
    skill_files = {
        path for path in public_candidates if path.startswith("codex-skills/")
    }
    actual_skill_ids = {
        path.split("/", 2)[1] for path in skill_files if path.count("/") >= 2
    }
    if actual_skill_ids != expected_skill_ids:
        errors.append("adopted Codex Skill directory set must contain exactly seven Skills")
    if len(skill_files) != 30:
        errors.append(f"adopted Codex Skill source set must contain 30 files: {len(skill_files)}")
    adopted_files = value(candidate, "adoption", "imported_files")
    adapted_files = value(candidate, "adoption", "adapted_files")
    if not isinstance(adopted_files, list) or not isinstance(adapted_files, list):
        errors.append("framework candidate file-level adoption inventory is invalid")
    else:
        adopted_set = set(adopted_files)
        adapted_set = set(adapted_files)
        expected_direct_adoption = {
            "codex-skills/grill-me/SKILL.md",
            "codex-skills/karpathy-guidelines/SKILL.md",
        }
        if adopted_set != expected_direct_adoption:
            errors.append("directly adopted Skill file inventory drift")
        if adopted_set & adapted_set or adopted_set | adapted_set != skill_files:
            errors.append("candidate adopted/adapted inventory does not equal the 30 Skill files")
    if value(candidate, "adoption", "required_before_lock") != []:
        errors.append("framework candidate retains unresolved pre-lock requirements")

    if role_map.get("schema") != "cotend.codex-skill-role-map":
        errors.append("Codex role map schema mismatch")
    if role_map.get("status") != "adopted_verified":
        errors.append("Codex role map is not finalized as adopted")
    if role_map.get("candidate_release") != "2026.07.11.3":
        errors.append("Codex role map release mismatch")
    if role_map.get("public_interface_authority") != (
        "codex_skill_source_set_adopted_live_delivery_pending"
    ):
        errors.append("Codex role map role-layer/name authority boundary drift")
    if role_map.get("role_layer_decision") != "product_owner_confirmed":
        errors.append("Codex role map role-layer decision mismatch")
    if role_map.get("user_owned_naming_decision") != "product_owner_confirmed":
        errors.append("Codex role map user-owned naming decision mismatch")
    if role_map.get("third_party_bundling_decision") != "product_owner_confirmed":
        errors.append("Codex role map third-party bundling decision mismatch")
    if role_map.get("skill_count") != 7:
        errors.append("Codex role map skill_count must be 7")

    role_entries = role_map.get("skills")
    if not isinstance(role_entries, list):
        errors.append("Codex role map skills must be a list")
        role_entries = []
    roles_by_id: dict[str, dict[str, object]] = {}
    for entry in role_entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("source_skill_id"), str):
            errors.append("Codex role map contains an invalid Skill entry")
            continue
        skill_id = entry["source_skill_id"]
        if skill_id in roles_by_id:
            errors.append(f"Codex role map duplicates Skill: {skill_id}")
            continue
        roles_by_id[skill_id] = entry
    if set(roles_by_id) != set(expected_skill_trees):
        errors.append("Codex role map must contain exactly the seven candidate Skills")

    expected_roles = {
        "dual-ai-init": (
            "user_owned_original",
            "unified_visible_entry",
            "adapted",
            "rename_only",
            "cotend-init",
        ),
        "dual-ai-project-init": (
            "user_owned_original",
            "internal_auto_mode_engine",
            "adapted",
            "platform_adaptation",
            "cotend-project-init",
        ),
        "dual-ai-collaboration": (
            "user_owned_original",
            "shared_governance_core",
            "adapted",
            "platform_adaptation",
            "cotend-collaboration",
        ),
        "diagnose-only": (
            "user_owned_original",
            "contextual_read_only_diagnosis",
            "adapted",
            "platform_adaptation",
            "cotend-diagnose-only",
        ),
        "dual-model-upgrade": (
            "user_owned_original",
            "advanced_model_role_lifecycle",
            "adapted",
            "platform_adaptation",
            "cotend-model-upgrade",
        ),
        "grill-me": (
            "adapted_third_party",
            "internal_clarification_companion",
            "adopted",
            "direct_adoption",
            "grill-me",
        ),
        "karpathy-guidelines": (
            "bundled_third_party",
            "internal_ai_implementation_discipline",
            "adopted",
            "direct_adoption",
            "karpathy-guidelines",
        ),
    }
    for skill_id, expected in expected_roles.items():
        entry = roles_by_id.get(skill_id)
        if entry is None:
            continue
        actual = (
            entry.get("source_relationship"),
            entry.get("current_role"),
            entry.get("adoption_status"),
            entry.get("implementation_mode"),
            entry.get("target_skill_id"),
        )
        if actual != expected:
            errors.append(f"Codex role mapping drift: {skill_id}")
        if entry.get("source_tree") != expected_skill_trees[skill_id]:
            errors.append(f"Codex role map tree mismatch: {skill_id}")

    expected_naming_status = {
        "dual-ai-init": "user_confirmed",
        "dual-ai-project-init": "user_confirmed",
        "dual-ai-collaboration": "user_confirmed",
        "diagnose-only": "user_confirmed",
        "dual-model-upgrade": "user_confirmed",
        "grill-me": "preserve_third_party_identity_if_bundled",
        "karpathy-guidelines": "preserve_third_party_identity_if_bundled",
    }
    for skill_id, expected in expected_naming_status.items():
        if roles_by_id.get(skill_id, {}).get("naming_status") != expected:
            errors.append(f"Codex role-map naming status drift: {skill_id}")

    init_entry = roles_by_id.get("dual-ai-init", {})
    if init_entry.get("delegates_to") != ["dual-ai-project-init"]:
        errors.append("dual-ai-init must remain the thin entry delegating to project init")
    for third_party_id in ("grill-me", "karpathy-guidelines"):
        if roles_by_id.get(third_party_id, {}).get("bundling_status") != "user_confirmed":
            errors.append(f"{third_party_id} bundling decision drift")

    adoption = role_map.get("adoption")
    if not isinstance(adoption, dict):
        errors.append("Codex role map adoption boundary is missing")
    else:
        expected_adoption_boundary = {
            "state": "adopted",
            "role_layers_confirmed": True,
            "user_owned_skill_names_confirmed": True,
            "final_names_confirmed": True,
            "final_names_scope": (
                "five_user_owned_ids_plus_preserved_third_party_identity"
            ),
            "physical_skill_count_confirmed": True,
            "physical_skill_count_scope": "repository_codex_skill_source_set",
            "confirmed_codex_skill_count": 7,
            "third_party_bundling_confirmed": True,
            "codex_skill_set_decisions_complete": True,
            "actual_adoption_authorized": True,
            "repository_source_carrier": "codex-skills/",
            "repository_source_implemented": True,
            "capability_map": "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
            "adoption_record": (
                "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
            ),
            "live_install_authorized": False,
            "live_install_performed": False,
            "plugin_or_marketplace_carrier": "deferred",
            "final_framework_lock_exists": True,
        }
        for key, expected in expected_adoption_boundary.items():
            if adoption.get(key) != expected:
                errors.append(f"Codex role-map adoption boundary mismatch: {key}")

    if metadata_values(proposal_text, "status") != {"adopted_verified"}:
        errors.append("framework adoption proposal is not finalized as adopted")
    exact_proposal_metadata = {
        "candidate_release": {"2026.07.11.3"},
        "role_layer_status": {"user_confirmed"},
        "role_layer_decision": {"product_owner_confirmed"},
        "user_owned_skill_name_status": {"user_confirmed"},
        "MIT_companion_bundling_status": {"user_confirmed"},
        "codex_skill_set_decisions_status": {"complete"},
        "adoption_state": {"adopted"},
        "final_framework_lock_exists": {"true"},
        "analysis_language": {"zh-CN"},
    }
    for key, expected in exact_proposal_metadata.items():
        if metadata_values(proposal_text, key) != expected:
            errors.append(f"framework adoption proposal metadata mismatch: {key}")
    for required_text in (
        "7 个 Codex Skill 直接理解成 7 个同级公开命令",
        "dual-ai-init` 是普通用户的统一入口",
        "dual-ai-project-init` 是入口内部的 Auto Mode 引擎",
        "用户已确认保留这套分层",
        "五个用户原创 Skill 分别命名为",
        "确认 Codex 首发源树直接内置 `grill-me` 与 `karpathy-guidelines`",
        "仓库内 Codex 技能源集合已采用为 7 个目录、30 个文件",
        "`upstream/framework.lock.json` 已在以下条件同时满足后创建",
        "adoption_state: adopted",
    ):
        if required_text not in proposal_text:
            errors.append(f"framework adoption proposal is missing: {required_text}")

    if metadata_values(adoption_plan_text, "status") != {"implemented_verified"}:
        errors.append("framework adoption plan is not finalized as implemented")
    exact_plan_metadata = {
        "candidate_release": {"2026.07.11.3"},
        "target_platform": {"Codex"},
        "target_source_carrier": {"codex-skills/"},
        "live_install_target": {"not_authorized"},
        "plugin_or_marketplace_carrier": {"deferred"},
        "implementation_authority": {"product_owner_confirmed"},
        "adoption_state": {"adopted"},
        "final_framework_lock_exists": {"true"},
        "analysis_language": {"zh-CN"},
    }
    for key, expected in exact_plan_metadata.items():
        if metadata_values(adoption_plan_text, key) != expected:
            errors.append(f"framework adoption plan metadata mismatch: {key}")
    for required_text in (
        "7 个技能目录，共 30 个文件",
        "codex-skills/cotend-init/",
        "codex-skills/cotend-project-init/",
        "codex-skills/cotend-collaboration/",
        "codex-skills/cotend-diagnose-only/",
        "codex-skills/cotend-model-upgrade/",
        "codex-skills/grill-me/",
        "codex-skills/karpathy-guidelines/",
        "cotend-collaboration-v1.52",
        "cotend-model-upgrade-v1.7",
        "mechanism_budget: three_repository_integrity_mechanisms_no_new_user_workflow",
        "不新增命令层、路由层、状态目录或重复内核",
        '"type": "containing_commit"',
        "锁文件只能在采用或升级提交中修改",
        "不安装到用户全局 Codex 目录",
        "仓库实现叶已经完成",
    ):
        if required_text not in adoption_plan_text:
            errors.append(f"framework adoption plan is missing: {required_text}")

    required_artifacts = {
        ".gitattributes",
        "NOTICE",
        "THIRD-PARTY-NOTICES.md",
        "THIRD-PARTY-SOURCES.json",
        "THIRD-PARTY-LICENSES/grill-me-MIT.txt",
        "THIRD-PARTY-LICENSES/karpathy-guidelines-MIT.txt",
        "scripts/verify_adopted_skill_set.py",
        "FRAMEWORK-CHANGE-EVAL.md",
        "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        "upstream/FRAMEWORK-ADOPTION-LOG.md",
        "upstream/framework.lock.json",
    }
    missing_artifacts = required_artifacts - public_candidates
    if missing_artifacts:
        errors.append(f"adoption artifacts are missing or ignored: {sorted(missing_artifacts)}")

    if capability_map.get("schema") != "cotend.capability-implementation-map":
        errors.append("capability implementation map schema mismatch")
    if capability_map.get("status") != "adopted_verified":
        errors.append("capability implementation map status mismatch")
    if capability_map.get("capability_count") != 19:
        errors.append("capability implementation map count mismatch")

    expected_lock_values = {
        ("schema",): "cotend.framework-lock",
        ("schema_version",): 1,
        ("status",): "adopted_verified",
        ("release_id",): "2026.07.11.3",
        ("framework_protocol",): "cotend-collaboration-v1.52",
        ("model_upgrade_packet_family",): "cotend-model-upgrade-v1.7",
        ("source_release", "tag"): "dual-ai-share-2026.07.11.3",
        ("source_release", "tag_object"): "cef8add414a6d9704d3f58785a128bc56f44b263",
        ("source_release", "release_commit"): "71e45d9ebeff4d9d61c180711c25267b9fe31549",
        ("source_release", "package_tree"): "a70231e0445d9795a00212e8e6c53c149bfbc431",
        ("source_release", "manifest_sha256"): (
            "919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006"
        ),
        ("target_platform",): "Codex",
        ("source_carrier",): "codex-skills/",
        ("skill_count",): 7,
        ("skill_file_count",): 30,
        ("capability_map",): "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        ("adoption_record",): (
            "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
        ),
        ("delivery_boundaries", "repository_source_adopted"): True,
        ("delivery_boundaries", "live_install_performed"): False,
        ("delivery_boundaries", "plugin_or_marketplace_carrier"): "deferred",
        ("delivery_boundaries", "claude_carrier"): "deferred",
        ("delivery_boundaries", "push_release_or_publish"): "not_performed",
    }
    for keys, expected in expected_lock_values.items():
        if value(framework_lock, *keys) != expected:
            errors.append(f"framework lock mismatch: {'.'.join(keys)}")
    if framework_lock.get("source_skill_trees") != expected_skill_trees:
        errors.append("framework lock source Skill tree inventory drift")
    if framework_lock.get("adoption_anchor") != {
        "type": "containing_commit",
        "path": "upstream/framework.lock.json",
    }:
        errors.append("framework lock containing-commit anchor mismatch")
    for forbidden_key in ("adoption_commit", "resulting_commit", "containing_commit_hash"):
        if forbidden_key in framework_lock:
            errors.append(f"framework lock must not embed its own commit hash: {forbidden_key}")

    lock_mappings = framework_lock.get("skill_mapping")
    if not isinstance(lock_mappings, list):
        errors.append("framework lock Skill mapping is invalid")
    else:
        lock_by_source = {
            item.get("source"): item for item in lock_mappings if isinstance(item, dict)
        }
        for source_id, expected in expected_roles.items():
            item = lock_by_source.get(source_id)
            if item is None:
                errors.append(f"framework lock Skill mapping is missing: {source_id}")
                continue
            expected_disposition = expected[2]
            expected_mode = expected[3]
            expected_target = expected[4]
            if (
                item.get("target"),
                item.get("disposition"),
                item.get("implementation_mode"),
            ) != (expected_target, expected_disposition, expected_mode):
                errors.append(f"framework lock Skill mapping drift: {source_id}")
        if (
            len(lock_mappings) != 7
            or len(lock_by_source) != 7
            or set(lock_by_source) != set(expected_roles)
        ):
            errors.append("framework lock must map exactly seven source Skills")

    for marker in (
        "## release-2026-07-11-3-initial-adoption",
        "status: adopted_verified",
        "resulting_CoTend_commit: containing_commit",
        "live_install_performed: false",
        "7 个 Skill、30 个文件",
    ):
        if marker not in adoption_log_text:
            errors.append(f"framework adoption log is missing: {marker}")

    return errors


def local_recovery_truth_errors(status_text: str, plan_text: str) -> list[str]:
    errors: list[str] = []

    exact_status = {
        "productization_default": {"rename_first_preserve_first"},
        "framework_release_candidate": {"dual_ai_share_2026_07_11_3"},
        "framework_release_adoption": {"adopted_verified_repository_source"},
        "interface_authority": {
            "codex_project_carrier_validated_live_delivery_pending"
        },
    }
    for key, expected in exact_status.items():
        if metadata_values(status_text, key) != expected:
            errors.append(f"local STATUS productization truth mismatch: {key}")

    exact_plan = {
        "productization_default": {"rename_first_preserve_first"},
    }
    for key, expected in exact_plan.items():
        if metadata_values(plan_text, key) != expected:
            errors.append(f"local plan productization truth mismatch: {key}")

    status_leaves = metadata_values(status_text, "current_next_leaf")
    plan_leaves = metadata_values(plan_text, "current_next_leaf")
    active_nodes = metadata_values(plan_text, "active_node")
    if len(status_leaves) != 1 or status_leaves != plan_leaves:
        errors.append(
            f"local active leaf drift: STATUS={sorted(status_leaves)} "
            f"PLAN={sorted(plan_leaves)}"
        )
        return errors
    if active_nodes != plan_leaves:
        errors.append(
            f"local active node drift: NODE={sorted(active_nodes)} "
            f"LEAF={sorted(plan_leaves)}"
        )
        return errors

    current_leaf = next(iter(plan_leaves))
    active_leaf_path = ROOT / "PROJECT-PLAN-NODES" / f"{current_leaf}.md"
    if not active_leaf_path.exists():
        errors.append(f"local active leaf document is missing: {current_leaf}")
        return errors
    active_leaf_text = active_leaf_path.read_text(encoding="utf-8")
    if metadata_values(active_leaf_text, "route_state") != {"active"}:
        errors.append(f"local active leaf route state is not active: {current_leaf}")

    governing_decisions = metadata_values(plan_text, "governing_decision")
    activation_decisions = metadata_values(active_leaf_text, "activation_decision")
    if len(governing_decisions) != 1 or governing_decisions != activation_decisions:
        errors.append("local plan governing decision does not match active leaf activation")

    current_stages = metadata_values(plan_text, "current_stage")
    if len(current_stages) != 1:
        errors.append(f"local plan must identify one current stage: {sorted(current_stages)}")
        return errors
    current_stage = next(iter(current_stages))
    stage_path = ROOT / "PROJECT-PLAN-NODES" / f"{current_stage}.md"
    if not stage_path.exists():
        errors.append(f"local current stage document is missing: {current_stage}")
        return errors
    stage_text = stage_path.read_text(encoding="utf-8")
    if metadata_values(stage_text, "active_leaf") != plan_leaves:
        errors.append("local current stage does not point to the plan's active leaf")

    understanding_match = re.search(
        r"^\s*expanded:\s*(\S+)\s*$", stage_text, re.MULTILINE
    )
    if understanding_match is None:
        errors.append("local current stage lacks an expanded understanding link")
        return errors
    understanding_path = ROOT / understanding_match.group(1)
    if not understanding_path.exists():
        errors.append("local current-stage understanding document is missing")
        return errors
    understanding_text = understanding_path.read_text(encoding="utf-8")
    understanding_leaves = metadata_values(understanding_text, "current_leaf")
    if understanding_leaves and understanding_leaves != plan_leaves:
        errors.append("local current-stage understanding points to a different active leaf")

    return errors


def isolated_codex_carrier_errors(
    evidence_text: str,
    adoption_log_text: str,
    framework_eval_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    fixture_root = "tests/fixtures/codex-carrier"
    expected_paths = {
        f"{fixture_root}/{path}" for path in EXPECTED_CODEX_CARRIER_FIXTURE_FILES
    }
    if "scripts/verify_isolated_codex_carrier.py" not in candidates:
        errors.append("isolated Codex carrier verifier is missing or ignored")
    missing_paths = expected_paths - candidates
    if missing_paths:
        errors.append(
            f"isolated Codex carrier fixture files are missing: {sorted(missing_paths)}"
        )
    actual_paths = {
        path for path in candidates if path.startswith(f"{fixture_root}/")
    }
    if actual_paths != expected_paths:
        errors.append("isolated Codex carrier fixture inventory drift")

    combined_evidence = evidence_text + adoption_log_text
    for marker in (
        "status: passed_with_scope_limitations",
        "codex_cli: 0.142.0",
        "project_skill_carrier: .agents/skills",
        "fixture_skill_count: 7",
        "fixture_skill_file_count: 30",
        "live_scenario_count: 3",
        "negative_mutation_count: 4",
        "cli_boundary_negative_count: 3",
        "desktop_skill_selector_verified: false",
        "implicit_natural_language_trigger_verified: false",
        "passed_3_of_3",
        "passed_4_of_4",
        "passed_7_of_7_with_PYTHONUTF8",
        "1024",
    ):
        if marker not in combined_evidence:
            errors.append(f"isolated Codex carrier evidence is missing: {marker}")

    scenario_path = ROOT / fixture_root / "live-scenarios.json"
    if scenario_path.is_file():
        try:
            scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"isolated Codex live scenarios are invalid JSON: {exc}")
            scenarios = []
        scenario_ids = {
            item.get("id") for item in scenarios if isinstance(item, dict)
        }
        if scenario_ids != {"init-delegation", "pending-decision", "diagnose-only"}:
            errors.append("isolated Codex live scenario set drift")
        if len(scenarios) != 3:
            errors.append("isolated Codex carrier must define exactly three live scenarios")

    for skill in (
        "cotend-init",
        "cotend-project-init",
        "cotend-collaboration",
        "cotend-diagnose-only",
        "cotend-model-upgrade",
    ):
        agent_path = ROOT / "codex-skills" / skill / "agents" / "openai.yaml"
        if not agent_path.is_file():
            errors.append(f"Codex agent metadata is missing: {skill}")
            continue
        prompt = re.search(
            r'^\s*default_prompt:\s*"(.+)"\s*$',
            agent_path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if prompt is None or len(prompt.group(1)) > 1024:
            errors.append(f"Codex default prompt limit mismatch: {skill}")

    if (
        "skills_list_7_of_7_and_three_read_only_explicit_scenarios_passed"
        not in framework_eval_text
    ):
        errors.append("framework evaluation lacks isolated Codex carrier result")
    if "framework_lock_changed: false" not in adoption_log_text:
        errors.append("adoption log lacks carrier lock boundary")
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
            if (
                relative_path.startswith("codex-skills/")
                and label in FRAMEWORK_SOURCE_ALLOWED_PATTERN_LABELS
            ):
                continue
            if pattern.search(text):
                errors.append(f"{relative_path}: {label}")
        if relative_path.startswith("codex-skills/"):
            for label, pattern in FORBIDDEN_SKILL_MAINTAINER_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"{relative_path}: {label}")
    errors.extend(checker_self_scan_errors(read("scripts/check_repository.py")))

    reference_study_path = "docs/REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md"
    upstream_registry_path = "UPSTREAM-SOURCES.md"
    framework_candidate_path = "upstream/FRAMEWORK-CANDIDATE.json"
    codex_role_map_path = "upstream/CODEX-SKILL-ROLE-MAP.json"
    adoption_proposal_path = "upstream/FRAMEWORK-ADOPTION-PROPOSAL.md"
    adoption_plan_path = "upstream/FRAMEWORK-ADOPTION-PLAN.md"
    capability_map_path = "upstream/CAPABILITY-IMPLEMENTATION-MAP.json"
    adoption_log_path = "upstream/FRAMEWORK-ADOPTION-LOG.md"
    framework_lock_path = "upstream/framework.lock.json"
    if reference_study_path not in candidates:
        errors.append("reference framework implementation study is missing or ignored")
    if upstream_registry_path not in candidates:
        errors.append("upstream source registry is missing or ignored")
    for path in (
        framework_candidate_path,
        codex_role_map_path,
        adoption_proposal_path,
        adoption_plan_path,
        capability_map_path,
        adoption_log_path,
        framework_lock_path,
    ):
        if path not in candidates:
            errors.append(f"upstream adoption artifact is missing or ignored: {path}")
    if reference_study_path in candidates and upstream_registry_path in candidates:
        errors.extend(
            reference_study_errors(
                read(reference_study_path),
                read(upstream_registry_path),
            )
        )

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
    analysis_paths = (
        "docs/MARKET-LANDSCAPE.md",
        reference_study_path,
        upstream_registry_path,
        adoption_proposal_path,
        adoption_plan_path,
        "FRAMEWORK-CHANGE-EVAL.md",
    )
    errors.extend(
        owner_document_language_errors(
            prd_text,
            {path: read(path) for path in analysis_paths if path in candidates},
        )
    )

    framework_eval_text = read("FRAMEWORK-CHANGE-EVAL.md")
    for key, expected in {
        "change_type": {"workflow_behavior"},
        "decision": {"watch"},
    }.items():
        if metadata_values(framework_eval_text, key) != expected:
            errors.append(f"framework change evaluation mismatch: {key}")
    for required_text in (
        "11_of_11_negative_mutations_rejected",
        "maintainer_residue_mutation_rejected",
        "later_head_passed_and_lock_only_update_rejected",
        "four_protected_blobs_match_and_text_eol_lf_enforced",
        "first_live_codex_validation",
    ):
        if required_text not in framework_eval_text:
            errors.append(f"framework change evaluation is missing: {required_text}")

    carrier_evidence_path = "docs/evidence/ISOLATED-CODEX-CARRIER-VALIDATION.md"
    if carrier_evidence_path not in candidates:
        errors.append("isolated Codex carrier evidence is missing or ignored")
    else:
        errors.extend(
            isolated_codex_carrier_errors(
                read(carrier_evidence_path),
                read(adoption_log_path),
                framework_eval_text,
                candidates,
            )
        )

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
    evidence_text: str | None = None
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

    errors.extend(
        productization_truth_errors(
            prd_text,
            read("docs/CLEAN-ROOM-POLICY.md"),
            read("docs/CAPABILITY-COVERAGE.md"),
            read("docs/PRODUCTIZATION-ROADMAP.md"),
            read("docs/BEHAVIOR-SPECIFICATION-STANDARD.md"),
            read(upstream_registry_path),
            read(capability_map_path),
            spec_texts,
            journey_text,
            interface_text,
            evidence_text,
        )
    )

    upstream_adoption_paths = {
        framework_candidate_path,
        codex_role_map_path,
        adoption_proposal_path,
        adoption_plan_path,
        capability_map_path,
        adoption_log_path,
        framework_lock_path,
    }
    if upstream_adoption_paths <= candidates:
        errors.extend(
            upstream_adoption_errors(
                read(framework_candidate_path),
                read(codex_role_map_path),
                read(adoption_proposal_path),
                read(adoption_plan_path),
                read(capability_map_path),
                read(adoption_log_path),
                read(framework_lock_path),
                candidates,
            )
        )

    status_path = ROOT / "STATUS.md"
    plan_path = ROOT / "PROJECT-PLAN-TREE.md"
    if status_path.exists() and plan_path.exists():
        errors.extend(
            local_recovery_truth_errors(read("STATUS.md"), read("PROJECT-PLAN-TREE.md"))
        )
    elif status_path.exists() or plan_path.exists():
        errors.append("local recovery truth requires both STATUS and PROJECT-PLAN-TREE")

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
