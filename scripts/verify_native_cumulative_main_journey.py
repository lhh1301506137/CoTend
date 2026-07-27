from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

import verify_native_closeout_pass as native_closeout
import verify_native_implementation_pass as native_implementation
import verify_native_init_resume_before_development as native_project_entry
import verify_native_project_truth_authority as native_authority
import verify_native_requirements_clarification as native_clarification
import verify_native_spec_change_route_rebase as native_route_rebase
import verify_native_verification_pass as native_verification
import verify_native_workflow_state_runtime_profiles as native_workflow_state


ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-CUMULATIVE-MAIN-JOURNEY.md"
EVIDENCE_PATH = (
    ROOT / "docs" / "evidence" / "NATIVE-CUMULATIVE-MAIN-JOURNEY-G03.md"
)
CONTRACT_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"

Profile = Literal["full", "adaptive"]
AcceptanceEvent = Literal["continue", "synthetic_accept", "implicit_ai_accept"]

EXPECTED_G03_EVIDENCE = [
    "init_to_implementation_to_check_to_acceptance",
    "interruption_and_route_rebase",
    "handoff_and_new_session_recovery",
]
EXPECTED_NATIVE_EVALUATORS = (
    "project_truth_authority",
    "workflow_state_runtime_profile",
    "project_init",
    "requirements_clarification",
    "plan_and_route",
    "predevelopment_readiness",
    "implementation_pass",
    "verification_pass",
    "closeout_pass",
)
EXPECTED_STAGE_EVALUATORS = EXPECTED_NATIVE_EVALUATORS + (
    "init_handback_gate",
    "formal_review_gate",
    "goal_completion_gate",
    "synthetic_acceptance_gate",
    "handoff_new_session_recovery",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生累计主旅程",
    "## 单一旅程状态",
    "## Full 与 Adaptive",
    "## 中断与 Route Rebase",
    "## HANDOFF 与新会话恢复",
    "## 合成验收边界",
    "accepted_synthetic",
    "不是用户真实验收",
    "cotend-codex-r000010",
    "G04、G05、G06",
)
REQUIRED_EVIDENCE_MARKERS = (
    "gate: G03-cumulative-main-journey",
    "status: complete",
    "journey_scenarios: 3",
    "evidence_groups: 3",
    "direct_evaluator_composition: passed",
    "full_adaptive_equivalence: passed",
    "bare_continue_acceptance_block: passed",
    "handoff_digest_and_new_object_recovery: passed",
    "real_user_acceptance_claimed: false",
    "development_target_artifact: cotend-codex-r000010",
    "skill_behavior_changed: false",
)


class NativeCumulativeJourneyError(ValueError):
    pass


@dataclass(frozen=True)
class StageRecord:
    stage: str
    owner: str
    status: str
    input_identity: str
    output_identity: str
    evaluator: str


@dataclass(frozen=True)
class AcceptanceResult:
    status: str
    event: str
    explicit_event_required: bool
    state_changed: bool
    real_user_acceptance_claimed: bool = False
    product_done_claimed: bool = False
    release_authorized: bool = False


@dataclass(frozen=True)
class RecoveryResult:
    status: str
    session_id: str
    journey_id: str
    goal_id: str
    profile: str
    execution_mode: str
    active_leaf: str
    route_revision: int
    decisions: tuple[str, ...]
    verification_identity: str
    acceptance_status: str
    next_mode: str
    automatic_product_work_started: bool
    external_framework_owner: bool
    real_user_acceptance_claimed: bool


@dataclass(frozen=True)
class JourneyResult:
    status: str
    journey_id: str
    goal_id: str
    profile: str
    execution_mode: str
    active_leaf: str
    route_revision: int
    decisions: tuple[str, ...]
    implementation_identity: str
    verification_identity: str
    evidence_identity: str
    acceptance_status: str
    continue_status: str
    handoff_digest: str
    handoff_document: str
    recovery: RecoveryResult
    reliable_resume_boundary: str
    invalidated_identity_count: int
    stage_records: tuple[StageRecord, ...]
    external_framework_owner: bool
    parallel_truth_created: bool
    real_user_acceptance_claimed: bool
    release_authorized: bool


def _identity(label: str, payload: Any) -> str:
    encoded = json.dumps(
        {"label": label, "payload": payload},
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _record_stage(
    records: list[StageRecord],
    *,
    stage: str,
    owner: str,
    status: str,
    input_identity: str,
    semantic_output: Any,
    evaluator: str,
) -> str:
    output_identity = _identity(
        stage,
        {"input_identity": input_identity, "semantic_output": semantic_output},
    )
    records.append(
        StageRecord(
            stage=stage,
            owner=owner,
            status=status,
            input_identity=input_identity,
            output_identity=output_identity,
            evaluator=evaluator,
        )
    )
    return output_identity


def evaluate_acceptance(
    status: str,
    event: AcceptanceEvent,
    *,
    synthetic_fixture: bool = True,
) -> AcceptanceResult:
    if status not in {"awaiting_explicit_acceptance", "accepted_synthetic"}:
        raise NativeCumulativeJourneyError("invalid acceptance state")
    if status == "accepted_synthetic":
        if event != "synthetic_accept" or not synthetic_fixture:
            raise NativeCumulativeJourneyError(
                "an accepted synthetic fixture cannot consume another event"
            )
        return AcceptanceResult(
            status=status,
            event=event,
            explicit_event_required=False,
            state_changed=False,
        )
    if event in {"continue", "implicit_ai_accept"}:
        return AcceptanceResult(
            status="awaiting_explicit_acceptance",
            event=event,
            explicit_event_required=True,
            state_changed=False,
        )
    if event == "synthetic_accept" and synthetic_fixture:
        return AcceptanceResult(
            status="accepted_synthetic",
            event=event,
            explicit_event_required=False,
            state_changed=True,
        )
    raise NativeCumulativeJourneyError(
        "synthetic acceptance requires an explicitly labelled disposable fixture"
    )


HANDOFF_KEYS = {
    "schema",
    "synthetic_fixture",
    "journey_id",
    "goal_id",
    "profile",
    "execution_mode",
    "active_leaf",
    "route_revision",
    "decisions",
    "implementation_identity",
    "verification_identity",
    "evidence_identity",
    "acceptance_status",
    "real_user_acceptance_claimed",
    "next_mode",
}


def build_handoff(payload: dict[str, Any]) -> tuple[str, str]:
    if set(payload) != HANDOFF_KEYS:
        raise NativeCumulativeJourneyError("handoff payload fields drifted")
    encoded_payload = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    digest = hashlib.sha256(encoded_payload.encode("utf-8")).hexdigest()
    document = json.dumps(
        {"digest": f"sha256:{digest}", "payload": payload},
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return document, f"sha256:{digest}"


def recover_handoff(document: str, *, session_id: str) -> RecoveryResult:
    try:
        envelope = json.loads(document)
    except json.JSONDecodeError as exc:
        raise NativeCumulativeJourneyError("handoff is not valid JSON") from exc
    if not isinstance(envelope, dict) or set(envelope) != {"digest", "payload"}:
        raise NativeCumulativeJourneyError("handoff envelope fields drifted")
    payload = envelope["payload"]
    if not isinstance(payload, dict) or set(payload) != HANDOFF_KEYS:
        raise NativeCumulativeJourneyError("handoff payload fields drifted")
    encoded_payload = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    expected_digest = "sha256:" + hashlib.sha256(
        encoded_payload.encode("utf-8")
    ).hexdigest()
    if envelope["digest"] != expected_digest:
        raise NativeCumulativeJourneyError("handoff digest mismatch")
    if payload["schema"] != "cotend.synthetic-handoff.v1":
        raise NativeCumulativeJourneyError("handoff schema drifted")
    if payload["synthetic_fixture"] is not True:
        raise NativeCumulativeJourneyError("handoff must remain a synthetic fixture")
    if payload["profile"] not in {"full", "adaptive"}:
        raise NativeCumulativeJourneyError("handoff profile is invalid")
    if payload["acceptance_status"] != "accepted_synthetic":
        raise NativeCumulativeJourneyError("handoff acceptance state is not current")
    if payload["real_user_acceptance_claimed"] is not False:
        raise NativeCumulativeJourneyError("synthetic handoff claimed user acceptance")
    if payload["next_mode"] != "new_goal_needed":
        raise NativeCumulativeJourneyError("accepted handoff must stop for a new goal")
    if not isinstance(payload["route_revision"], int) or payload["route_revision"] < 1:
        raise NativeCumulativeJourneyError("handoff route revision is invalid")
    if not isinstance(payload["decisions"], list) or not payload["decisions"]:
        raise NativeCumulativeJourneyError("handoff decisions are missing")
    if not session_id.strip():
        raise NativeCumulativeJourneyError("recovery session id is required")

    profile = payload["profile"]
    workflow = native_workflow_state.evaluate_workflow(
        "current", native_profiles=(profile,)
    )
    entry = native_project_entry.evaluate_entry("current")
    if (
        not workflow.can_continue
        or workflow.effective_profile != profile
        or entry.auto_mode != "current_resume"
        or entry.same_response_product_work_started
    ):
        raise NativeCumulativeJourneyError("new session did not resume current truth")

    return RecoveryResult(
        status="recovered_accepted_synthetic",
        session_id=session_id,
        journey_id=payload["journey_id"],
        goal_id=payload["goal_id"],
        profile=profile,
        execution_mode=workflow.execution_mode,
        active_leaf=payload["active_leaf"],
        route_revision=payload["route_revision"],
        decisions=tuple(payload["decisions"]),
        verification_identity=payload["verification_identity"],
        acceptance_status=payload["acceptance_status"],
        next_mode=payload["next_mode"],
        automatic_product_work_started=False,
        external_framework_owner=workflow.external_framework_owner,
        real_user_acceptance_claimed=False,
    )


def run_main_journey(
    profile: Profile,
    *,
    journey_id: str = "G03-main-journey",
    route_rebase_interruption: bool = False,
) -> JourneyResult:
    if profile not in {"full", "adaptive"}:
        raise NativeCumulativeJourneyError("unsupported runtime profile")
    if not journey_id.strip():
        raise NativeCumulativeJourneyError("journey id is required")

    goal_id = "GOAL-G03-SYNTHETIC-LOCAL-CLI"
    active_leaf = "L4-implement-synthetic-local-cli"
    decisions = ("DEC-G03-SYNTHETIC-REQUIREMENTS",)
    acceptance_contract = (
        "authorized local implementation completes",
        "required checks pass",
        "explicit acceptance event is required",
    )
    allowed_paths = ("src/synthetic_cli.py", "tests/test_synthetic_cli.py")
    records: list[StageRecord] = []
    cursor = _identity(
        "journey_start",
        {"journey_id": journey_id, "goal_id": goal_id, "baseline": "confirmed"},
    )

    authority = native_authority.evaluate_external_artifact("absent")
    if authority.route_owner != "cotend_plan_tree" or authority.external_is_authority:
        raise NativeCumulativeJourneyError("project truth authority escaped CoTend")
    cursor = _record_stage(
        records,
        stage="project_truth_authority",
        owner=authority.route_owner,
        status=authority.action,
        input_identity=cursor,
        semantic_output=asdict(authority),
        evaluator="project_truth_authority",
    )

    workflow = native_workflow_state.evaluate_workflow(
        "absent", session_profile=profile, persist_session=True
    )
    if not workflow.can_continue or workflow.effective_profile != profile:
        raise NativeCumulativeJourneyError("workflow profile did not materialize")
    cursor = _record_stage(
        records,
        stage="workflow_state_runtime_profile",
        owner=workflow.native_record_owner,
        status=workflow.state,
        input_identity=cursor,
        semantic_output={
            "state": workflow.state,
            "profile_is_valid_and_persisted": (
                workflow.persisted_profile == profile
            ),
            "external_framework_owner": workflow.external_framework_owner,
        },
        evaluator="workflow_state_runtime_profile",
    )

    entry = native_project_entry.evaluate_entry("absent")
    if (
        entry.auto_mode != "fresh_init"
        or entry.handback != "resume_same_confirmed_route"
        or entry.same_response_product_work_started
    ):
        raise NativeCumulativeJourneyError("Init handback contract failed")
    cursor = _record_stage(
        records,
        stage="project_init",
        owner="cotend_project_init",
        status=entry.auto_mode,
        input_identity=cursor,
        semantic_output={
            "handback": entry.handback,
            "same_response_product_work_started": (
                entry.same_response_product_work_started
            ),
        },
        evaluator="project_init",
    )
    cursor = _record_stage(
        records,
        stage="init_handback_resume_event",
        owner="synthetic_user_fixture_event",
        status="explicit_resume_same_confirmed_route",
        input_identity=cursor,
        semantic_output={
            "separate_event_after_init_report": True,
            "specialized_decision_answered": False,
            "scope_expanded": False,
        },
        evaluator="init_handback_gate",
    )

    question = native_clarification.evaluate_clarification("fuzzy")
    answer = native_clarification.evaluate_clarification(
        "pending_answer",
        reply="recommended_1",
        question_kind="decision_worthy",
    )
    if (
        question.question_count != 1
        or answer.question_count != 0
        or not answer.answer_selected
        or not answer.persist_before_route_effect
    ):
        raise NativeCumulativeJourneyError("requirements decision did not close")
    cursor = _record_stage(
        records,
        stage="requirements_clarification",
        owner=answer.route_owner,
        status=answer.route,
        input_identity=cursor,
        semantic_output={
            "decision": decisions[0],
            "decision_log_required": answer.decision_log_required,
            "persist_before_route_effect": answer.persist_before_route_effect,
        },
        evaluator="requirements_clarification",
    )

    route_revision = 1
    reliable_resume_boundary = "not_required"
    invalidated_identity_count = 0
    if route_rebase_interruption:
        route_change = native_route_rebase.evaluate_route_change(
            "material_l3_l4",
            evidence_basis_changed=True,
            interrupted_at="applying",
        )
        if (
            route_change.status != "applying"
            or route_change.route_owner != "cotend_plan_tree"
            or route_change.next_leaf_advance_allowed
        ):
            raise NativeCumulativeJourneyError("interrupted Route Rebase did not stop")
        reliable_resume_boundary = route_change.reliable_resume_boundary
        cursor = _record_stage(
            records,
            stage="route_rebase_interrupted",
            owner=route_change.route_owner,
            status=route_change.status,
            input_identity=cursor,
            semantic_output={
                "resume_boundary": reliable_resume_boundary,
                "completion_evidence": route_change.completion_evidence,
            },
            evaluator="plan_and_route",
        )
        checkpoint = json.loads(
            json.dumps(
                {
                    "cursor": cursor,
                    "route_revision": route_revision,
                    "resume_boundary": reliable_resume_boundary,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        resumed = native_route_rebase.evaluate_route_change(
            "material_l3_l4", evidence_basis_changed=True
        )
        if (
            resumed.status != "revalidating"
            or checkpoint["resume_boundary"]
            != resumed.reliable_resume_boundary
            or resumed.next_leaf_advance_allowed
        ):
            raise NativeCumulativeJourneyError("Route Rebase recovery boundary drifted")
        route_revision += 1
        invalidated_identity_count = 2
        cursor = _record_stage(
            records,
            stage="route_rebase_resumed",
            owner=resumed.route_owner,
            status="revalidated",
            input_identity=checkpoint["cursor"],
            semantic_output={
                "route_revision": route_revision,
                "old_implementation_identity": "invalidated",
                "old_verification_identity": "invalidated",
            },
            evaluator="plan_and_route",
        )
    else:
        route = native_route_rebase.evaluate_route_change("ordinary_leaf")
        if not route.next_leaf_advance_allowed or route.packet_required:
            raise NativeCumulativeJourneyError("ordinary plan route did not advance")
        cursor = _record_stage(
            records,
            stage="plan_route",
            owner=route.route_owner,
            status=route.status,
            input_identity=cursor,
            semantic_output={
                "active_leaf": active_leaf,
                "route_revision": route_revision,
            },
            evaluator="plan_and_route",
        )

    predevelopment = native_project_entry.evaluate_predevelopment(
        init_handback_satisfied=True,
        workflow_state="current",
        specialized_decision_pending=False,
        route_authorized=True,
        current_truth_available=True,
        active_leaf_available=True,
        requirements_available=True,
        acceptance_available=True,
        risk_authorized=True,
        canonical_root_clear=True,
        provider_state="codegraph_fresh",
    )
    if (
        predevelopment.status != "ready"
        or not predevelopment.truth_loaded_before_code_context
        or not predevelopment.broad_edits_allowed
    ):
        raise NativeCumulativeJourneyError("pre-development readiness failed")
    cursor = _record_stage(
        records,
        stage="predevelopment_readiness",
        owner="cotend_code_context_harness",
        status=predevelopment.status,
        input_identity=cursor,
        semantic_output={
            "load_order": predevelopment.load_order,
            "scope_signature": predevelopment.scope_signature,
        },
        evaluator="predevelopment_readiness",
    )

    implementation = native_implementation.evaluate_implementation(
        profile=profile,
        active_leaf=active_leaf,
        allowed_paths=allowed_paths,
        acceptance=acceptance_contract,
        resume_state=("safe_checkpoint" if route_rebase_interruption else "fresh"),
    )
    if (
        implementation.status != "integration_waiting"
        or implementation.checker_handoff != "required"
        or implementation.external_framework_owner
        or implementation.user_acceptance_claimed
    ):
        raise NativeCumulativeJourneyError("implementation did not reach Checker")
    implementation_identity = _record_stage(
        records,
        stage="implementation_pass",
        owner=implementation.execution_shape,
        status=implementation.status,
        input_identity=cursor,
        semantic_output={
            "goal_id": goal_id,
            "active_leaf": active_leaf,
            "route_revision": route_revision,
            "allowed_paths": allowed_paths,
            "test_action": implementation.test_action,
        },
        evaluator="implementation_pass",
    )

    verification = native_verification.evaluate_verification(
        profile=profile,
        active_leaf=active_leaf,
        checker_handoff=implementation.checker_handoff,
        implementation_status=implementation.status,
        implementation_identity=implementation_identity,
        changed_paths=allowed_paths,
        allowed_fix_paths=allowed_paths,
        requirements=("REQ-G03-SYNTHETIC",),
        acceptance=acceptance_contract,
        required_checks=("unit", "acceptance"),
        resume_state=(
            "interrupted_current" if route_rebase_interruption else "fresh"
        ),
    )
    if (
        verification.status != "passed"
        or verification.checked_implementation_identity != implementation_identity
        or verification.formal_review_handoff != "required"
        or verification.external_framework_owner
        or verification.user_acceptance_claimed
    ):
        raise NativeCumulativeJourneyError("verification identity did not close")
    verification_identity = _record_stage(
        records,
        stage="verification_pass",
        owner=verification.execution_shape,
        status=verification.status,
        input_identity=implementation_identity,
        semantic_output={
            "checked_implementation_identity": (
                verification.checked_implementation_identity
            ),
            "required_checks_executed": verification.required_checks_executed,
            "unresolved_findings": verification.unresolved_findings,
        },
        evaluator="verification_pass",
    )

    formal_review_identity = _record_stage(
        records,
        stage="formal_self_review_fixture",
        owner="codex_self_fixture",
        status="APPROVE",
        input_identity=verification_identity,
        semantic_output={
            "reviewed_verification_identity": verification_identity,
            "unresolved_P0_P1_P2": 0,
            "independence": "same_session_self_fixture",
            "real_external_review_claimed": False,
        },
        evaluator="formal_review_gate",
    )

    authorized_paths = allowed_paths + ("STATUS.md", "REVIEW-LOG.md")
    closeout = native_closeout.evaluate_closeout(
        profile=profile,
        closeout_id=f"closeout:{journey_id}:r{route_revision}",
        active_leaf=active_leaf,
        implementation_identity=implementation_identity,
        verification_identity=verification_identity,
        workspace_identity=_identity("workspace", allowed_paths),
        authorized_paths=authorized_paths,
        observed_changed_paths=allowed_paths,
        required_records=("STATUS.md", "REVIEW-LOG.md"),
        handoff_required=False,
        commit_intent="not_applicable",
        git_repository=False,
    )
    if (
        closeout.status != "completed"
        or closeout.handoff_result != "not_required"
        or closeout.user_acceptance_claimed
        or closeout.done_claimed
        or closeout.external_framework_owner
    ):
        raise NativeCumulativeJourneyError("closeout overreached or failed")
    evidence_identity = _record_stage(
        records,
        stage="closeout_pass",
        owner="cotend_native_closeout",
        status=closeout.status,
        input_identity=formal_review_identity,
        semantic_output={
            "implementation_identity": implementation_identity,
            "verification_identity": verification_identity,
            "formal_review_identity": formal_review_identity,
            "synchronized_records": closeout.synchronized_records,
            "postcommit_verified": closeout.postcommit_verified,
        },
        evaluator="closeout_pass",
    )

    goal_completion_identity = _record_stage(
        records,
        stage="goal_completion_gate",
        owner="cotend_goal_completion",
        status="awaiting_explicit_acceptance",
        input_identity=evidence_identity,
        semantic_output={
            "goal_id": goal_id,
            "verification_identity": verification_identity,
            "evidence_identity": evidence_identity,
            "ai_uat_is_not_user_acceptance": True,
        },
        evaluator="goal_completion_gate",
    )

    continued = evaluate_acceptance(
        "awaiting_explicit_acceptance", "continue"
    )
    if continued.status != "awaiting_explicit_acceptance" or continued.state_changed:
        raise NativeCumulativeJourneyError("bare continue crossed acceptance gate")
    acceptance = evaluate_acceptance(continued.status, "synthetic_accept")
    if acceptance.status != "accepted_synthetic" or not acceptance.state_changed:
        raise NativeCumulativeJourneyError("explicit synthetic acceptance failed")
    final_identity = _record_stage(
        records,
        stage="synthetic_acceptance_gate",
        owner="product_owner_fixture_event",
        status=acceptance.status,
        input_identity=goal_completion_identity,
        semantic_output={
            "continue_status": continued.status,
            "acceptance_status": acceptance.status,
            "real_user_acceptance_claimed": False,
        },
        evaluator="synthetic_acceptance_gate",
    )

    handoff_payload = {
        "schema": "cotend.synthetic-handoff.v1",
        "synthetic_fixture": True,
        "journey_id": journey_id,
        "goal_id": goal_id,
        "profile": profile,
        "execution_mode": workflow.execution_mode,
        "active_leaf": active_leaf,
        "route_revision": route_revision,
        "decisions": list(decisions),
        "implementation_identity": implementation_identity,
        "verification_identity": verification_identity,
        "evidence_identity": final_identity,
        "acceptance_status": acceptance.status,
        "real_user_acceptance_claimed": False,
        "next_mode": "new_goal_needed",
    }
    handoff_document, handoff_digest = build_handoff(handoff_payload)
    handoff_identity = _record_stage(
        records,
        stage="handoff_serialization",
        owner="cotend_handoff",
        status="serialized_and_digest_bound",
        input_identity=final_identity,
        semantic_output={
            "handoff_digest": handoff_digest,
            "acceptance_status": acceptance.status,
        },
        evaluator="handoff_new_session_recovery",
    )
    recovery = recover_handoff(
        handoff_document, session_id=f"new-session:{journey_id}:{profile}"
    )
    if (
        recovery.goal_id != goal_id
        or recovery.route_revision != route_revision
        or recovery.decisions != decisions
        or recovery.verification_identity != verification_identity
        or recovery.acceptance_status != acceptance.status
        or recovery.automatic_product_work_started
    ):
        raise NativeCumulativeJourneyError("new-session recovery drifted")
    _record_stage(
        records,
        stage="new_session_recovery",
        owner="cotend_project_init",
        status=recovery.status,
        input_identity=handoff_identity,
        semantic_output={
            "goal_id": recovery.goal_id,
            "route_revision": recovery.route_revision,
            "acceptance_status": recovery.acceptance_status,
            "next_mode": recovery.next_mode,
        },
        evaluator="handoff_new_session_recovery",
    )

    evaluators = {record.evaluator for record in records}
    if set(EXPECTED_STAGE_EVALUATORS) - evaluators:
        missing = sorted(set(EXPECTED_STAGE_EVALUATORS) - evaluators)
        raise NativeCumulativeJourneyError(
            "cumulative journey skipped evaluators: " + ", ".join(missing)
        )
    for previous, current in zip(records, records[1:]):
        if current.input_identity != previous.output_identity:
            raise NativeCumulativeJourneyError("stage identity chain is broken")

    return JourneyResult(
        status="accepted_synthetic_and_recovered",
        journey_id=journey_id,
        goal_id=goal_id,
        profile=profile,
        execution_mode=workflow.execution_mode,
        active_leaf=active_leaf,
        route_revision=route_revision,
        decisions=decisions,
        implementation_identity=implementation_identity,
        verification_identity=verification_identity,
        evidence_identity=final_identity,
        acceptance_status=acceptance.status,
        continue_status=continued.status,
        handoff_digest=handoff_digest,
        handoff_document=handoff_document,
        recovery=recovery,
        reliable_resume_boundary=reliable_resume_boundary,
        invalidated_identity_count=invalidated_identity_count,
        stage_records=tuple(records),
        external_framework_owner=False,
        parallel_truth_created=False,
        real_user_acceptance_claimed=False,
        release_authorized=False,
    )


def equivalence_projection(result: JourneyResult) -> dict[str, Any]:
    return {
        "status": result.status,
        "journey_id": result.journey_id,
        "goal_id": result.goal_id,
        "active_leaf": result.active_leaf,
        "route_revision": result.route_revision,
        "decisions": result.decisions,
        "implementation_identity": result.implementation_identity,
        "verification_identity": result.verification_identity,
        "evidence_identity": result.evidence_identity,
        "acceptance_status": result.acceptance_status,
        "continue_status": result.continue_status,
        "recovered_acceptance_status": result.recovery.acceptance_status,
        "recovered_next_mode": result.recovery.next_mode,
        "stage_statuses": tuple(
            (record.stage, record.status) for record in result.stage_records
        ),
        "external_framework_owner": result.external_framework_owner,
        "parallel_truth_created": result.parallel_truth_created,
        "real_user_acceptance_claimed": result.real_user_acceptance_claimed,
        "release_authorized": result.release_authorized,
    }


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise NativeCumulativeJourneyError(
            f"{label} is missing required markers: {', '.join(missing)}"
        )


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NativeCumulativeJourneyError(f"{label} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise NativeCumulativeJourneyError(f"{label} must be a JSON object")
    return payload


def verify_repository(root: Path = ROOT) -> dict[str, Any]:
    document_path = root / DOCUMENT_PATH.relative_to(ROOT)
    evidence_path = root / EVIDENCE_PATH.relative_to(ROOT)
    contract_path = root / CONTRACT_PATH.relative_to(ROOT)
    target_lock_path = root / TARGET_LOCK_PATH.relative_to(ROOT)
    _require_markers(
        document_path.read_text(encoding="utf-8"),
        REQUIRED_DOCUMENT_MARKERS,
        "native cumulative journey document",
    )
    _require_markers(
        evidence_path.read_text(encoding="utf-8"),
        REQUIRED_EVIDENCE_MARKERS,
        "native cumulative journey evidence",
    )
    contract = _load_json(contract_path, "Trellis decoupling contract")
    target_lock = _load_json(target_lock_path, "target artifact lock")
    gates = contract.get("gates")
    if not isinstance(gates, list):
        raise NativeCumulativeJourneyError("decoupling gates are missing")
    g03 = next(
        (gate for gate in gates if gate.get("id") == "G03-cumulative-main-journey"),
        None,
    )
    if not isinstance(g03, dict):
        raise NativeCumulativeJourneyError("G03 gate is missing")
    if g03.get("status") != "complete" or g03.get("evidence") != EXPECTED_G03_EVIDENCE:
        raise NativeCumulativeJourneyError("G03 machine contract drifted")
    target = target_lock.get("target")
    if (
        not isinstance(target, dict)
        or target.get("artifact_id") != "cotend-codex-r000012"
    ):
        raise NativeCumulativeJourneyError("G03 changed the target artifact")

    capability_checks = (
        ("TD08", native_authority.verify_repository),
        ("TD03", native_clarification.verify_repository),
        ("TD06", native_route_rebase.verify_repository),
        ("TD01", native_workflow_state.verify_repository),
        ("TD02", native_project_entry.verify_repository),
        ("TD04", native_implementation.verify_repository),
        ("TD05", native_verification.verify_repository),
        ("TD07", native_closeout.verify_repository),
    )
    capability_results: dict[str, dict[str, Any]] = {}
    for capability_id, verifier in capability_checks:
        try:
            capability_results[capability_id] = verifier(root)
        except (OSError, ValueError) as exc:
            raise NativeCumulativeJourneyError(
                f"{capability_id} prerequisite verification failed: {exc}"
            ) from exc
    if any(
        result.get("status") != "native_parity_verified"
        for result in capability_results.values()
    ):
        raise NativeCumulativeJourneyError("a G02 prerequisite regressed")

    full = run_main_journey("full")
    adaptive = run_main_journey("adaptive")
    if equivalence_projection(full) != equivalence_projection(adaptive):
        raise NativeCumulativeJourneyError("Full and Adaptive outcomes drifted")
    rebased = run_main_journey(
        "full",
        journey_id="G03-interrupted-route-rebase",
        route_rebase_interruption=True,
    )
    if (
        rebased.route_revision != 2
        or rebased.invalidated_identity_count != 2
        or rebased.reliable_resume_boundary
        != "earliest_jointly_trustworthy_boundary"
    ):
        raise NativeCumulativeJourneyError("interrupted Route Rebase did not recover")
    for result in (full, adaptive, rebased):
        if (
            result.external_framework_owner
            or result.parallel_truth_created
            or result.real_user_acceptance_claimed
            or result.release_authorized
            or result.recovery.automatic_product_work_started
        ):
            raise NativeCumulativeJourneyError("journey crossed an authority boundary")

    return {
        "status": "native_cumulative_main_journey_verified",
        "gate": "G03-cumulative-main-journey",
        "evidence_group_count": 3,
        "journey_scenario_count": 3,
        "native_capabilities_composed": len(capability_results),
        "full_adaptive_equivalent": True,
        "route_rebase_recovered": True,
        "handoff_new_session_recovered": True,
        "bare_continue_blocked_at_acceptance": True,
        "real_user_acceptance_claimed": False,
        "skill_behavior_changed": False,
        "target_artifact": target["artifact_id"],
        "results": {
            "full": asdict(full),
            "adaptive": asdict(adaptive),
            "interrupted_route_rebase": asdict(rebased),
        },
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, NativeCumulativeJourneyError) as exc:
        print("NATIVE_CUMULATIVE_MAIN_JOURNEY_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_CUMULATIVE_MAIN_JOURNEY_OK "
        f"gate={result['gate']} "
        f"journeys={result['journey_scenario_count']} "
        f"groups={result['evidence_group_count']} "
        f"capabilities={result['native_capabilities_composed']} "
        f"behavior_changed=false target={result['target_artifact']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
