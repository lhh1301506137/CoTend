from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import verify_cotend_project_init as project_init_contract


ROOT = Path(__file__).resolve().parents[1]
PLAN_TREE_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "plan-tree.md"
)
TEMPLATES_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "templates.md"
)
DECISION_LOG_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "decision-log.md"
)
CLOSURE_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "semantic-implementation-closure.md"
)
SEMANTIC_SKILL_PATH = ROOT / "skills" / "cotend-semantic-alignment" / "SKILL.md"
INIT_SKILL_PATH = ROOT / "skills" / "cotend-project-init" / "SKILL.md"
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-SPEC-CHANGE-AND-ROUTE-REBASE.md"

ChangeKind = Literal["ordinary_leaf", "material_l3_l4", "material_l0_l2"]
Decision = Literal["none", "continue", "accept", "reject"]
ExternalState = Literal["none", "aligned", "stale", "conflict"]
InterruptedAt = Literal["none", "applying", "revalidating"]

REQUIRED_PLAN_MARKERS = (
    "### CoTend Native Specification Ownership",
    "Semantic Alignment is the only writable owner",
    "Plan Tree is the only route owner.",
    "External project or framework specifications are classified evidence only.",
    "Rejected, deferred, and superseded candidates remain recoverable history.",
    "Do not open a packet for an ordinary next-leaf choice",
    "A bare `继续`",
    "Set `reliable_resume_boundary`",
    "Link classified external task/PRD evidence without making it the packet owner.",
)
REQUIRED_TEMPLATE_MARKERS = (
    "status: evaluating | pending_user_confirmation | applying | revalidating | blocked | closed",
    "durable_carrier: existing_plan_tree_node | cotend_owned_project_spec | status | decision_log | knowledge_changelog",
    "disposition: unaffected | reusable | rework_required | revalidation_required | invalidated | superseded",
)
REQUIRED_SEMANTIC_MARKERS = (
    "## Protected Route Rebase And Impact Propagation",
    "A bare `继续`",
    "An old `done` node",
    "Set the canonical reliable resume boundary",
    "If the user rejects the candidate",
)
REQUIRED_INTEGRATION_MARKERS = {
    DECISION_LOG_PATH: (
        "a CoTend-owned project PRD, spec, or brief for current detailed requirements.",
        "docs/<active-spec>.md",
    ),
    CLOSURE_PATH: (
        "existing CoTend-owned Plan Tree node, project PRD/spec evidence section",
    ),
    INIT_SKILL_PATH: (
        "existing CoTend-owned Plan Tree/project-spec/STATUS/decision/knowledge carrier",
        "closeout, task, PRD, spec, state, profile",
    ),
}
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生规格变化与 Route Rebase",
    "## 第一方责任链",
    "## 十类确定性场景",
    "cotend-codex-r000005",
    "158 处、21 文件",
    "0.1.0-rc.2",
    "G06",
)
FORBIDDEN_ACTIVE_PATTERNS = {
    "external_update_spec_command": re.compile(
        r"trellis[-_]update[-_]spec", re.IGNORECASE
    ),
    "external_active_carrier": re.compile(
        r"active_trellis_or_prd", re.IGNORECASE
    ),
    "external_active_requirement_owner": re.compile(
        r"Trellis\s+`prd\.md`\s+for\s+active\s+task\s+requirements",
        re.IGNORECASE,
    ),
    "external_writable_closure_carrier": re.compile(
        r"Trellis\s+task/PRD\s+evidence\s+section", re.IGNORECASE
    ),
    "external_rebase_carrier_chain": re.compile(
        r"Plan\s+Tree/Trellis/PRD/STATUS/decision/knowledge\s+carrier",
        re.IGNORECASE,
    ),
    "external_update_compatibility": re.compile(
        r"implementation/check/update/finish\s+procedure", re.IGNORECASE
    ),
}


class NativeRouteRebaseError(ValueError):
    pass


@dataclass(frozen=True)
class RouteRebaseResult:
    packet_required: bool
    status: str
    route_owner: str
    protected_semantic_owner: str
    user_decision_required: bool
    answer_selected: bool
    candidate_active: bool
    affected_route_blocked: bool
    unaffected_route_can_continue: bool
    next_leaf_advance_allowed: bool
    resulting_path: str
    reliable_resume_boundary: str
    completion_evidence: str
    decision_persisted_before_route_effect: bool
    history_disposition: str
    external_classification: str
    old_decisions_preserved: bool = True
    external_route_owner: bool = False
    parallel_spec_tree_created: bool = False


def _classify_external(external_state: ExternalState) -> str:
    return {
        "none": "none",
        "aligned": "reference_only",
        "stale": "historical",
        "conflict": "conflict",
    }[external_state]


def evaluate_route_change(
    change_kind: ChangeKind,
    *,
    decision: Decision = "none",
    external_state: ExternalState = "none",
    dependency_isolated: bool = False,
    evidence_basis_changed: bool = False,
    interrupted_at: InterruptedAt = "none",
) -> RouteRebaseResult:
    external_classification = _classify_external(external_state)
    common = {
        "route_owner": "cotend_plan_tree",
        "protected_semantic_owner": "cotend_semantic_alignment",
        "old_decisions_preserved": True,
        "external_route_owner": False,
        "parallel_spec_tree_created": False,
        "external_classification": external_classification,
    }

    if change_kind == "ordinary_leaf":
        if (
            decision != "none"
            or external_state == "conflict"
            or dependency_isolated
            or evidence_basis_changed
            or interrupted_at != "none"
        ):
            raise NativeRouteRebaseError(
                "ordinary leaf selection cannot carry material rebase state"
            )
        return RouteRebaseResult(
            packet_required=False,
            status="not_triggered",
            user_decision_required=False,
            answer_selected=False,
            candidate_active=False,
            affected_route_blocked=False,
            unaffected_route_can_continue=False,
            next_leaf_advance_allowed=True,
            resulting_path="existing_route_next_leaf",
            reliable_resume_boundary="not_required",
            completion_evidence="unchanged",
            decision_persisted_before_route_effect=False,
            history_disposition="unchanged",
            **common,
        )

    if external_state == "conflict":
        if decision != "none" or interrupted_at != "none":
            raise NativeRouteRebaseError(
                "external conflict must be classified before decision or resume"
            )
        return RouteRebaseResult(
            packet_required=True,
            status="blocked",
            user_decision_required=change_kind == "material_l0_l2",
            answer_selected=False,
            candidate_active=False,
            affected_route_blocked=True,
            unaffected_route_can_continue=dependency_isolated,
            next_leaf_advance_allowed=False,
            resulting_path="previous_path_retained_pending_cotend_resolution",
            reliable_resume_boundary="earliest_jointly_trustworthy_boundary",
            completion_evidence="unknown_until_conflict_resolved",
            decision_persisted_before_route_effect=False,
            history_disposition="external_conflict_recorded_as_evidence",
            **common,
        )

    if change_kind == "material_l3_l4":
        if decision != "none":
            raise NativeRouteRebaseError(
                "L3/L4 execution changes do not consume a product decision"
            )
        status = interrupted_at if interrupted_at != "none" else "revalidating"
        return RouteRebaseResult(
            packet_required=True,
            status=status,
            user_decision_required=False,
            answer_selected=False,
            candidate_active=True,
            affected_route_blocked=False,
            unaffected_route_can_continue=dependency_isolated,
            next_leaf_advance_allowed=False,
            resulting_path="candidate_path_pending_revalidation",
            reliable_resume_boundary="earliest_jointly_trustworthy_boundary",
            completion_evidence=(
                "revalidation_required"
                if evidence_basis_changed or interrupted_at != "none"
                else "must_close_under_resulting_path"
            ),
            decision_persisted_before_route_effect=False,
            history_disposition="previous_and_resulting_paths_preserved",
            **common,
        )

    if change_kind != "material_l0_l2":
        raise NativeRouteRebaseError(f"unsupported change kind: {change_kind}")
    if interrupted_at != "none":
        raise NativeRouteRebaseError(
            "protected change must first resolve its explicit user decision"
        )
    if decision in ("none", "continue"):
        return RouteRebaseResult(
            packet_required=True,
            status="pending_user_confirmation",
            user_decision_required=True,
            answer_selected=False,
            candidate_active=False,
            affected_route_blocked=True,
            unaffected_route_can_continue=dependency_isolated,
            next_leaf_advance_allowed=False,
            resulting_path="previous_path_retained_while_candidate_pending",
            reliable_resume_boundary="affected_route_confirmation_boundary",
            completion_evidence="previous_result_not_transferable_to_candidate",
            decision_persisted_before_route_effect=False,
            history_disposition=(
                "pending_question_represented"
                if decision == "continue"
                else "candidate_recorded_not_active"
            ),
            **common,
        )
    if decision == "accept":
        return RouteRebaseResult(
            packet_required=True,
            status="revalidating",
            user_decision_required=False,
            answer_selected=True,
            candidate_active=True,
            affected_route_blocked=False,
            unaffected_route_can_continue=dependency_isolated,
            next_leaf_advance_allowed=False,
            resulting_path="confirmed_candidate_path_pending_revalidation",
            reliable_resume_boundary="earliest_jointly_trustworthy_boundary",
            completion_evidence="revalidation_required",
            decision_persisted_before_route_effect=True,
            history_disposition="previous_semantics_superseded_and_preserved",
            **common,
        )
    if decision == "reject":
        return RouteRebaseResult(
            packet_required=True,
            status="closed",
            user_decision_required=False,
            answer_selected=True,
            candidate_active=False,
            affected_route_blocked=False,
            unaffected_route_can_continue=True,
            next_leaf_advance_allowed=True,
            resulting_path="previous_path_restored_or_retained",
            reliable_resume_boundary="previous_path_current_boundary",
            completion_evidence="previous_basis_retained_subject_to_dispositions",
            decision_persisted_before_route_effect=True,
            history_disposition="candidate_rejected_and_preserved",
            **common,
        )
    raise NativeRouteRebaseError(f"unsupported decision: {decision}")


EXPECTED_SCENARIOS = {
    "ordinary_local_leaf": {
        "kwargs": {"change_kind": "ordinary_leaf"},
        "expected": {
            "packet_required": False,
            "status": "not_triggered",
            "next_leaf_advance_allowed": True,
        },
    },
    "material_l3_l4": {
        "kwargs": {"change_kind": "material_l3_l4"},
        "expected": {
            "status": "revalidating",
            "user_decision_required": False,
            "candidate_active": True,
        },
    },
    "material_l0_l2_pending": {
        "kwargs": {"change_kind": "material_l0_l2"},
        "expected": {
            "status": "pending_user_confirmation",
            "user_decision_required": True,
            "candidate_active": False,
        },
    },
    "bare_continue_pending": {
        "kwargs": {
            "change_kind": "material_l0_l2",
            "decision": "continue",
        },
        "expected": {
            "status": "pending_user_confirmation",
            "answer_selected": False,
            "candidate_active": False,
        },
    },
    "accepted_protected_change": {
        "kwargs": {
            "change_kind": "material_l0_l2",
            "decision": "accept",
        },
        "expected": {
            "status": "revalidating",
            "answer_selected": True,
            "decision_persisted_before_route_effect": True,
        },
    },
    "rejected_protected_change": {
        "kwargs": {
            "change_kind": "material_l0_l2",
            "decision": "reject",
        },
        "expected": {
            "status": "closed",
            "candidate_active": False,
            "resulting_path": "previous_path_restored_or_retained",
        },
    },
    "unrelated_isolated_route": {
        "kwargs": {
            "change_kind": "material_l0_l2",
            "dependency_isolated": True,
        },
        "expected": {
            "affected_route_blocked": True,
            "unaffected_route_can_continue": True,
        },
    },
    "evidence_basis_invalidated": {
        "kwargs": {
            "change_kind": "material_l3_l4",
            "evidence_basis_changed": True,
        },
        "expected": {
            "completion_evidence": "revalidation_required",
            "next_leaf_advance_allowed": False,
        },
    },
    "interrupted_apply": {
        "kwargs": {
            "change_kind": "material_l3_l4",
            "interrupted_at": "applying",
        },
        "expected": {
            "status": "applying",
            "reliable_resume_boundary": "earliest_jointly_trustworthy_boundary",
            "next_leaf_advance_allowed": False,
        },
    },
    "external_spec_conflict": {
        "kwargs": {
            "change_kind": "material_l3_l4",
            "external_state": "conflict",
        },
        "expected": {
            "status": "blocked",
            "external_classification": "conflict",
            "affected_route_blocked": True,
        },
    },
}


def scan_forbidden_active_spec_routes(root: Path = ROOT) -> list[str]:
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


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise NativeRouteRebaseError(f"{label} is missing: {marker}")


def verify_repository(root: Path = ROOT) -> dict[str, object]:
    plan_text = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "plan-tree.md"
    ).read_text(encoding="utf-8")
    template_text = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "templates.md"
    ).read_text(encoding="utf-8")
    semantic_text = (
        root / "skills" / "cotend-semantic-alignment" / "SKILL.md"
    ).read_text(encoding="utf-8")
    document_text = (
        root / "docs" / "NATIVE-SPEC-CHANGE-AND-ROUTE-REBASE.md"
    ).read_text(encoding="utf-8")
    _require_markers(plan_text, REQUIRED_PLAN_MARKERS, "Plan Tree contract")
    _require_markers(template_text, REQUIRED_TEMPLATE_MARKERS, "packet schema")
    _require_markers(semantic_text, REQUIRED_SEMANTIC_MARKERS, "semantic integration")
    _require_markers(document_text, REQUIRED_DOCUMENT_MARKERS, "public contract")

    for path, markers in REQUIRED_INTEGRATION_MARKERS.items():
        relative = path.relative_to(ROOT)
        if path == INIT_SKILL_PATH:
            try:
                text = project_init_contract.load_project_init_contract(root)[
                    "combined"
                ]
            except project_init_contract.ProjectInitContractError as exc:
                raise NativeRouteRebaseError(str(exc)) from exc
        else:
            text = (root / relative).read_text(encoding="utf-8")
        _require_markers(text, markers, relative.as_posix())

    findings = scan_forbidden_active_spec_routes(root)
    if findings:
        raise NativeRouteRebaseError(
            "external spec route or writable authority remains: "
            + ", ".join(findings)
        )

    scenario_results: dict[str, dict[str, object]] = {}
    for scenario_id, contract in EXPECTED_SCENARIOS.items():
        result = evaluate_route_change(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeRouteRebaseError(
                    f"scenario result drifted: {scenario_id}.{key}"
                )
        if (
            not result.old_decisions_preserved
            or result.external_route_owner
            or result.parallel_spec_tree_created
        ):
            raise NativeRouteRebaseError(
                f"scenario lost history or delegated/duplicated authority: {scenario_id}"
            )
        scenario_results[scenario_id] = payload

    continued = scenario_results["bare_continue_pending"]
    if continued["answer_selected"] or continued["candidate_active"]:
        raise NativeRouteRebaseError("bare continue selected the protected candidate")
    accepted = scenario_results["accepted_protected_change"]
    if not accepted["decision_persisted_before_route_effect"]:
        raise NativeRouteRebaseError(
            "accepted protected change was applied before persistence"
        )
    rejected = scenario_results["rejected_protected_change"]
    if rejected["history_disposition"] != "candidate_rejected_and_preserved":
        raise NativeRouteRebaseError("rejected candidate history was not preserved")
    external = scenario_results["external_spec_conflict"]
    if external["external_route_owner"]:
        raise NativeRouteRebaseError("external specification became route owner")

    return {
        "status": "native_parity_verified",
        "capability": "TD06-spec-change-and-route-rebase",
        "scenario_count": len(scenario_results),
        "scenarios": scenario_results,
        "forbidden_active_spec_routes": 0,
        "external_route_owner": False,
        "parallel_spec_tree_created": False,
        "old_decisions_preserved": True,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, NativeRouteRebaseError) as exc:
        print("NATIVE_SPEC_CHANGE_ROUTE_REBASE_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_SPEC_CHANGE_ROUTE_REBASE_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        "external_route_owner=false parallel_spec_tree=false "
        "old_decisions_preserved=true"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
