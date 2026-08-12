from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import verify_cotend_project_init as project_init_contract


ROOT = Path(__file__).resolve().parents[1]
IDEA_CONTRACT_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "idea-to-consensus.md"
)
SEMANTIC_SKILL_PATH = ROOT / "skills" / "cotend-semantic-alignment" / "SKILL.md"
INIT_SKILL_PATH = ROOT / "skills" / "cotend-project-init" / "SKILL.md"
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-REQUIREMENTS-CLARIFICATION.md"
GRILL_ME_PATH = ROOT / "skills" / "grill-me" / "SKILL.md"
EXPECTED_GRILL_ME_SHA256 = (
    "8cfed91b3d4f8407d868648bb83bd48ddfd25ac1f1a5e909f4c80d54e2b0fe98"
)

RequestState = Literal["clear", "fuzzy", "pending_answer"]
EntryPoint = Literal["ordinary", "init"]
Reply = Literal["none", "continue", "recommended_1", "explicit_answer"]
QuestionKind = Literal["none", "decision_worthy", "factual"]
ExternalState = Literal["none", "aligned", "stale", "conflict"]

REQUIRED_IDEA_MARKERS = (
    "## CoTend Native Requirements Clarification",
    "CoTend owns the clarification route.",
    "`grill-me` supplies interaction discipline, not route or truth authority.",
    "Ask exactly one high-value question at a time.",
    "A bare `continue`",
    "Persist a decision-worthy answer",
    "`external_brainstorm`",
    "Init never executes this contract.",
)
REQUIRED_SEMANTIC_MARKERS = (
    "For a fuzzy idea or intake artifact entering `new_baseline`",
    "Use the active CoTend-governed brainstorm/PRD",
    "never create a parallel requirements source",
)
REQUIRED_INIT_MARKERS = (
    "complete Init only",
    "independently invoked `$cotend-semantic-alignment new_baseline`",
    "must not read or summarize the artifact to infer the product goal",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生需求澄清",
    "## 第一方责任链",
    "## 八类验证场景",
    "cotend-codex-r000004",
    "external_brainstorm",
    "0.1.0-rc.2",
)
FORBIDDEN_ACTIVE_PATTERNS = {
    "external_brainstorm_dispatch": re.compile(
        r"(?:return|route|dispatch|update).{0,80}trellis[-_ ]brainstorm",
        re.IGNORECASE,
    ),
    "legacy_brainstorm_command": re.compile(
        r"trellis[-_]brainstorm",
        re.IGNORECASE,
    ),
}


class NativeClarificationError(ValueError):
    pass


@dataclass(frozen=True)
class ClarificationResult:
    route: str
    route_owner: str
    question_count: int
    answer_selected: bool
    decision_log_required: bool
    persist_before_route_effect: bool
    external_classification: str
    external_route_owner: bool = False
    protected_truth_confirmed: bool = False
    create_parallel_truth: bool = False


def _classify_external(external_state: ExternalState) -> str:
    return {
        "none": "none",
        "aligned": "reference_only",
        "stale": "historical",
        "conflict": "conflict",
    }[external_state]


def evaluate_clarification(
    request_state: RequestState,
    *,
    entry_point: EntryPoint = "ordinary",
    reply: Reply = "none",
    question_kind: QuestionKind = "none",
    external_state: ExternalState = "none",
) -> ClarificationResult:
    external_classification = _classify_external(external_state)
    if entry_point == "init":
        if reply != "none" or question_kind != "none":
            raise NativeClarificationError(
                "Init cannot consume a product-clarification answer"
            )
        return ClarificationResult(
            route=(
                "report_existing_route"
                if request_state == "clear"
                else "handback_to_cotend_semantic_alignment"
            ),
            route_owner="cotend_project_init_handback",
            question_count=0,
            answer_selected=False,
            decision_log_required=False,
            persist_before_route_effect=False,
            external_classification=external_classification,
        )

    if request_state == "clear":
        if reply != "none" or question_kind != "none":
            raise NativeClarificationError(
                "clear requirements cannot consume a pending clarification answer"
            )
        return ClarificationResult(
            route="continue_existing_cotend_route",
            route_owner="existing_cotend_route",
            question_count=0,
            answer_selected=False,
            decision_log_required=False,
            persist_before_route_effect=False,
            external_classification=external_classification,
        )

    if request_state == "fuzzy":
        if reply != "none" or question_kind not in ("none", "decision_worthy"):
            raise NativeClarificationError(
                "a new fuzzy request must ask before consuming an answer"
            )
        return ClarificationResult(
            route=(
                "ask_one_conflict_question"
                if external_state == "conflict"
                else "ask_one_high_value_question"
            ),
            route_owner="cotend_semantic_alignment",
            question_count=1,
            answer_selected=False,
            decision_log_required=False,
            persist_before_route_effect=False,
            external_classification=external_classification,
        )

    if request_state != "pending_answer":
        raise NativeClarificationError(f"unsupported request state: {request_state}")
    if question_kind == "none":
        raise NativeClarificationError(
            "a pending answer must identify whether the question is decision-worthy"
        )
    if reply in ("none", "continue"):
        return ClarificationResult(
            route=(
                "await_pending_question"
                if reply == "none"
                else "represent_pending_question"
            ),
            route_owner="cotend_semantic_alignment",
            question_count=1,
            answer_selected=False,
            decision_log_required=False,
            persist_before_route_effect=False,
            external_classification=external_classification,
        )
    decision_worthy = question_kind == "decision_worthy"
    return ClarificationResult(
        route=(
            "record_decision_then_continue_clarification"
            if decision_worthy
            else "continue_clarification_without_decision_log"
        ),
        route_owner="cotend_semantic_alignment",
        question_count=0,
        answer_selected=True,
        decision_log_required=decision_worthy,
        persist_before_route_effect=decision_worthy,
        external_classification=external_classification,
    )


EXPECTED_SCENARIOS = {
    "clear_request": {
        "kwargs": {"request_state": "clear"},
        "route": "continue_existing_cotend_route",
        "question_count": 0,
    },
    "fuzzy_request": {
        "kwargs": {"request_state": "fuzzy"},
        "route": "ask_one_high_value_question",
        "question_count": 1,
    },
    "init_fuzzy_handback": {
        "kwargs": {"request_state": "fuzzy", "entry_point": "init"},
        "route": "handback_to_cotend_semantic_alignment",
        "question_count": 0,
    },
    "bare_continue_pending": {
        "kwargs": {
            "request_state": "pending_answer",
            "reply": "continue",
            "question_kind": "decision_worthy",
        },
        "route": "represent_pending_question",
        "question_count": 1,
    },
    "recommended_one_decision": {
        "kwargs": {
            "request_state": "pending_answer",
            "reply": "recommended_1",
            "question_kind": "decision_worthy",
        },
        "route": "record_decision_then_continue_clarification",
        "question_count": 0,
    },
    "factual_answer": {
        "kwargs": {
            "request_state": "pending_answer",
            "reply": "explicit_answer",
            "question_kind": "factual",
        },
        "route": "continue_clarification_without_decision_log",
        "question_count": 0,
    },
    "aligned_external_evidence": {
        "kwargs": {"request_state": "fuzzy", "external_state": "aligned"},
        "route": "ask_one_high_value_question",
        "question_count": 1,
    },
    "conflicting_external_evidence": {
        "kwargs": {"request_state": "fuzzy", "external_state": "conflict"},
        "route": "ask_one_conflict_question",
        "question_count": 1,
    },
}


def scan_forbidden_active_routes(root: Path = ROOT) -> list[str]:
    findings: list[str] = []
    for path in sorted((root / "skills").rglob("*")):
        if (
            not path.is_file()
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_ACTIVE_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}:{path.relative_to(root).as_posix()}")
    return findings


def verify_repository(root: Path = ROOT) -> dict[str, object]:
    idea_text = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "idea-to-consensus.md"
    ).read_text(encoding="utf-8")
    semantic_text = (
        root / "skills" / "cotend-semantic-alignment" / "SKILL.md"
    ).read_text(encoding="utf-8")
    try:
        init_text = project_init_contract.load_project_init_contract(root)[
            "combined"
        ]
    except project_init_contract.ProjectInitContractError as exc:
        raise NativeClarificationError(str(exc)) from exc
    document_text = (
        root / "docs" / "NATIVE-REQUIREMENTS-CLARIFICATION.md"
    ).read_text(encoding="utf-8")
    for marker in REQUIRED_IDEA_MARKERS:
        if marker not in idea_text:
            raise NativeClarificationError(
                f"native clarification contract is missing: {marker}"
            )
    for marker in REQUIRED_SEMANTIC_MARKERS:
        if marker not in semantic_text:
            raise NativeClarificationError(
                f"Semantic Alignment integration is missing: {marker}"
            )
    for marker in REQUIRED_INIT_MARKERS:
        if marker not in init_text:
            raise NativeClarificationError(f"Init handback is missing: {marker}")
    for marker in REQUIRED_DOCUMENT_MARKERS:
        if marker not in document_text:
            raise NativeClarificationError(
                f"native clarification document is missing: {marker}"
            )

    findings = scan_forbidden_active_routes(root)
    if findings:
        raise NativeClarificationError(
            "external brainstorm route remains active: " + ", ".join(findings)
        )

    grill_sha256 = hashlib.sha256(
        (root / "skills" / "grill-me" / "SKILL.md").read_bytes()
    ).hexdigest()
    if grill_sha256 != EXPECTED_GRILL_ME_SHA256:
        raise NativeClarificationError("grill-me adopted bytes changed")

    scenario_results: dict[str, dict[str, object]] = {}
    for scenario_id, expected in EXPECTED_SCENARIOS.items():
        result = evaluate_clarification(**expected["kwargs"])
        payload = asdict(result)
        if result.route != expected["route"]:
            raise NativeClarificationError(f"scenario route drifted: {scenario_id}")
        if result.question_count != expected["question_count"]:
            raise NativeClarificationError(
                f"scenario question count drifted: {scenario_id}"
            )
        if result.question_count > 1:
            raise NativeClarificationError(
                f"scenario asked more than one question: {scenario_id}"
            )
        if (
            result.external_route_owner
            or result.protected_truth_confirmed
            or result.create_parallel_truth
        ):
            raise NativeClarificationError(
                f"scenario delegated authority or duplicated truth: {scenario_id}"
            )
        scenario_results[scenario_id] = payload

    accepted = scenario_results["recommended_one_decision"]
    if not (
        accepted["answer_selected"]
        and accepted["decision_log_required"]
        and accepted["persist_before_route_effect"]
    ):
        raise NativeClarificationError(
            "decision-worthy recommended answer is not persisted before route effect"
        )
    continued = scenario_results["bare_continue_pending"]
    if continued["answer_selected"] or continued["decision_log_required"]:
        raise NativeClarificationError("bare continue selected a pending answer")
    aligned = scenario_results["aligned_external_evidence"]
    if aligned["external_classification"] != "reference_only":
        raise NativeClarificationError("aligned external evidence is not reference_only")
    conflict = scenario_results["conflicting_external_evidence"]
    if conflict["external_classification"] != "conflict":
        raise NativeClarificationError("conflicting external evidence was not isolated")

    return {
        "status": "native_parity_verified",
        "capability": "TD03-requirements-clarification",
        "scenario_count": len(scenario_results),
        "scenarios": scenario_results,
        "max_questions_per_scenario": max(
            value["question_count"] for value in scenario_results.values()
        ),
        "grill_me_sha256": grill_sha256,
        "external_route_owner": False,
        "parallel_truth_created": False,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, NativeClarificationError) as exc:
        print("NATIVE_REQUIREMENTS_CLARIFICATION_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_REQUIREMENTS_CLARIFICATION_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        "max_questions=1 external_route_owner=false parallel_truth=false"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
