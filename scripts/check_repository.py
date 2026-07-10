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
LOCAL_ONLY_PATHS = {
    "STATUS.md",
    "REVIEW-LOG.md",
    "QUALITY-SIGNALS.md",
    "PROJECT-DECISION-LOG.md",
    "PROJECT-KNOWLEDGE-CHANGELOG.md",
    "PROJECT-PLAN-TREE.md",
    "PROJECT-PLAN-NODES",
    "PROJECT-UNDERSTANDING",
    "docs/COMMAND-CONTRACTS.md",
    "docs/V1-ARCHITECTURE.md",
    "docs/PROJECT-STATE-CONTRACT.md",
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

    for key in (
        "interface_design_status",
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
        "interface_design_status",
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
    if journey_path not in candidates:
        errors.append("novice journey specification is missing or ignored")
    else:
        errors.extend(novice_journey_errors(read(journey_path)))

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
