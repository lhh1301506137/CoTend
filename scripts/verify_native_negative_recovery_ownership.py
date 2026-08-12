from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

import verify_native_closeout_pass as native_closeout
import verify_native_cumulative_main_journey as native_cumulative
import verify_native_implementation_pass as native_implementation
import verify_native_init_resume_before_development as native_project_entry
import verify_native_project_truth_authority as native_authority
import verify_native_requirements_clarification as native_clarification
import verify_native_spec_change_route_rebase as native_route_rebase
import verify_native_verification_pass as native_verification
import verify_native_workflow_state_runtime_profiles as native_workflow_state


ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-NEGATIVE-RECOVERY-AND-OWNERSHIP.md"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "evidence"
    / "NATIVE-NEGATIVE-RECOVERY-OWNERSHIP-G04.md"
)
CONTRACT_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
FRAMEWORK_LOCK_PATH = ROOT / "upstream" / "framework.lock.json"
CAPABILITY_MAP_PATH = ROOT / "upstream" / "CAPABILITY-IMPLEMENTATION-MAP.json"
ROLE_MAP_PATH = ROOT / "upstream" / "CODEX-SKILL-ROLE-MAP.json"
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"

Profile = Literal["full", "adaptive"]
SemanticLevel = Literal["L0_L2", "L3_L4"]
StateIncident = Literal["unknown_external", "duplicate_native_record"]

EXPECTED_G04_EVIDENCE = [
    "foreign_framework_conflict",
    "unknown_or_drifted_state",
    "failed_check_and_recovery",
    "unrelated_files_and_truth_preserved",
]
EXPECTED_CAPABILITY_IDS = {f"C{number:02d}" for number in range(1, 20)}
EXPECTED_TARGET_SKILLS = {
    "cotend-init",
    "cotend-project-init",
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-semantic-alignment",
    "cotend-model-upgrade",
    "cotend-session-handoff",
    "cotend-tooling",
    "grill-me",
    "karpathy-guidelines",
}
EXPECTED_STAGE_EVALUATORS = {
    "project_truth_authority",
    "workflow_state_runtime_profile",
    "project_init",
    "requirements_clarification",
    "plan_and_route",
    "predevelopment_readiness",
    "implementation_pass",
    "verification_pass",
    "formal_review_gate",
    "closeout_pass",
}
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生负向恢复与所有权",
    "## 不降级基线",
    "## 外部框架冲突",
    "## 未知或漂移状态",
    "## 检查失败与恢复",
    "## 用户文件与项目真相保护",
    "disposable fixture",
    "不是 G06",
    "cotend-codex-r000010",
    "G05、G06",
)
REQUIRED_EVIDENCE_MARKERS = (
    "gate: G04-negative-recovery-and-ownership",
    "status: complete",
    "evidence_groups: 4",
    "direct_evaluator_composition: passed",
    "full_adaptive_equivalence: passed",
    "failed_check_recovery: passed",
    "recovery_failure_checkpoint_retention: passed",
    "protected_file_hash_fixture: passed_disposable",
    "dual_capability_baseline: 19",
    "real_project_claimed: false",
    "real_user_acceptance_claimed: false",
    "development_target_artifact: cotend-codex-r000010",
    "skill_behavior_changed: false",
)


class NativeNegativeRecoveryError(ValueError):
    pass


@dataclass(frozen=True)
class IncidentStage:
    stage: str
    owner: str
    status: str
    input_identity: str
    output_identity: str
    evaluator: str


@dataclass(frozen=True)
class IncidentResult:
    group: str
    scenario: str
    status: str
    incident_id: str
    goal_id: str
    profile: str
    execution_mode: str
    route_revision: int
    checkpoint_identity: str
    implementation_identity: str
    failed_verification_identity: str
    recovered_implementation_identity: str
    recovered_verification_identity: str
    closeout_status: str
    blocking_reason: str
    reliable_resume_boundary: str
    stage_records: tuple[IncidentStage, ...]
    user_decision_required: bool = False
    unaffected_route_preserved: bool = True
    checkpoint_preserved: bool = True
    project_truth_preserved: bool = True
    user_files_preserved: bool = True
    unrelated_files_preserved: bool = True
    stale_evidence_reused: bool = False
    silent_state_reset: bool = False
    closeout_before_recovery: bool = False
    external_framework_owner: bool = False
    parallel_truth_created: bool = False
    real_project_claimed: bool = False
    real_user_acceptance_claimed: bool = False
    release_authorized: bool = False


@dataclass(frozen=True)
class FileProtectionResult:
    status: str
    protected_file_count: int
    owned_record_count: int
    owned_rollback: str
    concurrent_drift_disposition: str
    project_truth_preserved: bool
    user_files_preserved: bool
    unrelated_files_preserved: bool
    staged_external_preserved: bool
    checkpoint_preserved: bool
    real_project_claimed: bool = False
    real_user_acceptance_claimed: bool = False


def _identity(label: str, payload: Any) -> str:
    encoded = json.dumps(
        {"label": label, "payload": payload},
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _execution_mode(profile: Profile) -> str:
    return "delegated_pair" if profile == "full" else "inline"


def _record_stage(
    records: list[IncidentStage],
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
        IncidentStage(
            stage=stage,
            owner=owner,
            status=status,
            input_identity=input_identity,
            output_identity=output_identity,
            evaluator=evaluator,
        )
    )
    return output_identity


def _validate_profile(profile: str) -> Profile:
    if profile not in {"full", "adaptive"}:
        raise NativeNegativeRecoveryError("invalid runtime profile")
    return profile  # type: ignore[return-value]


def _assert_no_authority_crossing(*results: object) -> None:
    forbidden_flags = (
        "external_is_authority",
        "external_route_owner",
        "external_framework_owner",
        "create_parallel_truth",
        "parallel_spec_tree_created",
        "parallel_state_tree_created",
        "user_acceptance_claimed",
        "release_authorized",
        "push_release_publish_authorized",
    )
    for result in results:
        for flag in forbidden_flags:
            if bool(getattr(result, flag, False)):
                raise NativeNegativeRecoveryError(
                    f"authority boundary crossed: {type(result).__name__}.{flag}"
                )


def run_foreign_framework_conflict(
    profile: Profile,
    semantic_level: SemanticLevel,
) -> IncidentResult:
    profile = _validate_profile(profile)
    incident_id = f"G04-foreign-{semantic_level}-{profile}"
    goal_id = "G04-protected-cotend-goal"
    records: list[IncidentStage] = []
    cursor = _identity("incident", {"incident_id": incident_id, "goal_id": goal_id})
    checkpoint_identity = cursor

    authority = native_authority.evaluate_external_artifact(
        "conflict", semantic_level
    )
    cursor = _record_stage(
        records,
        stage="project_truth_authority",
        owner=authority.route_owner,
        status=authority.classification,
        input_identity=cursor,
        semantic_output=asdict(authority),
        evaluator="project_truth_authority",
    )
    workflow = native_workflow_state.evaluate_workflow(
        "current",
        native_profiles=(profile,),
        external_state="conflict",
        external_affects_route=True,
    )
    cursor = _record_stage(
        records,
        stage="workflow_state_runtime_profile",
        owner=workflow.native_record_owner,
        status=workflow.state,
        input_identity=cursor,
        semantic_output=asdict(workflow),
        evaluator="workflow_state_runtime_profile",
    )
    entry = native_project_entry.evaluate_entry(
        "current", external_route_conflict=True
    )
    cursor = _record_stage(
        records,
        stage="project_init",
        owner="cotend_project_init",
        status=entry.readiness,
        input_identity=cursor,
        semantic_output=asdict(entry),
        evaluator="project_init",
    )
    clarification = native_clarification.evaluate_clarification(
        "fuzzy", external_state="conflict"
    )
    cursor = _record_stage(
        records,
        stage="requirements_clarification",
        owner=clarification.route_owner,
        status=clarification.route,
        input_identity=cursor,
        semantic_output=asdict(clarification),
        evaluator="requirements_clarification",
    )
    change_kind = (
        "material_l0_l2" if semantic_level == "L0_L2" else "material_l3_l4"
    )
    route = native_route_rebase.evaluate_route_change(
        change_kind,
        external_state="conflict",
        dependency_isolated=True,
    )
    cursor = _record_stage(
        records,
        stage="plan_and_route",
        owner=route.route_owner,
        status=route.status,
        input_identity=cursor,
        semantic_output=asdict(route),
        evaluator="plan_and_route",
    )
    predevelopment = native_project_entry.evaluate_predevelopment(
        workflow_state="conflict"
    )
    _record_stage(
        records,
        stage="predevelopment_readiness",
        owner="cotend_code_context_harness",
        status=predevelopment.status,
        input_identity=cursor,
        semantic_output=asdict(predevelopment),
        evaluator="predevelopment_readiness",
    )

    _assert_no_authority_crossing(
        authority,
        workflow,
        entry,
        clarification,
        route,
        predevelopment,
    )
    if (
        authority.action
        not in {
            "stop_affected_and_route_semantic_alignment",
            "rebase_cotend_route_from_reliable_boundary",
        }
        or workflow.can_continue
        or entry.write_performed
        or entry.bare_continue_allowed
        or route.status != "blocked"
        or not route.affected_route_blocked
        or not route.unaffected_route_can_continue
        or predevelopment.status != "blocked"
        or predevelopment.broad_edits_allowed
    ):
        raise NativeNegativeRecoveryError(
            "foreign framework conflict did not fail closed"
        )

    return IncidentResult(
        group="foreign_framework_conflict",
        scenario=f"foreign_{semantic_level.lower()}_conflict",
        status="blocked_safe",
        incident_id=incident_id,
        goal_id=goal_id,
        profile=profile,
        execution_mode=_execution_mode(profile),
        route_revision=1,
        checkpoint_identity=checkpoint_identity,
        implementation_identity="none",
        failed_verification_identity="none",
        recovered_implementation_identity="none",
        recovered_verification_identity="none",
        closeout_status="not_started",
        blocking_reason=authority.action,
        reliable_resume_boundary=route.reliable_resume_boundary,
        stage_records=tuple(records),
        user_decision_required=authority.user_decision_required,
        unaffected_route_preserved=route.unaffected_route_can_continue,
    )


def run_unknown_or_drifted_state(
    profile: Profile,
    state_incident: StateIncident,
) -> IncidentResult:
    profile = _validate_profile(profile)
    incident_id = f"G04-state-{state_incident}-{profile}"
    goal_id = "G04-state-integrity-goal"
    records: list[IncidentStage] = []
    cursor = _identity("incident", {"incident_id": incident_id, "goal_id": goal_id})
    checkpoint_identity = cursor

    if state_incident == "unknown_external":
        authority = native_authority.evaluate_external_artifact("unknown")
        workflow = native_workflow_state.evaluate_workflow(
            "current",
            native_profiles=(profile,),
            external_state="conflict",
            external_affects_route=True,
        )
        route = native_route_rebase.evaluate_route_change(
            "material_l3_l4",
            external_state="conflict",
            dependency_isolated=True,
        )
        entry = native_project_entry.evaluate_entry(
            "current", external_route_conflict=True
        )
        blocking_reason = authority.action
    elif state_incident == "duplicate_native_record":
        authority = native_authority.evaluate_external_artifact("absent")
        workflow = native_workflow_state.evaluate_workflow(
            "current", native_profiles=("full", "adaptive")
        )
        route = native_route_rebase.evaluate_route_change(
            "material_l3_l4",
            dependency_isolated=True,
            evidence_basis_changed=True,
            interrupted_at="applying",
        )
        entry = native_project_entry.evaluate_entry("conflict")
        blocking_reason = workflow.migration_result
    else:
        raise NativeNegativeRecoveryError(
            f"unsupported state incident: {state_incident}"
        )

    cursor = _record_stage(
        records,
        stage="project_truth_authority",
        owner=authority.route_owner,
        status=authority.classification,
        input_identity=cursor,
        semantic_output=asdict(authority),
        evaluator="project_truth_authority",
    )
    cursor = _record_stage(
        records,
        stage="workflow_state_runtime_profile",
        owner=workflow.native_record_owner,
        status=workflow.state,
        input_identity=cursor,
        semantic_output=asdict(workflow),
        evaluator="workflow_state_runtime_profile",
    )
    cursor = _record_stage(
        records,
        stage="project_init",
        owner="cotend_project_init",
        status=entry.readiness,
        input_identity=cursor,
        semantic_output=asdict(entry),
        evaluator="project_init",
    )
    cursor = _record_stage(
        records,
        stage="plan_and_route",
        owner=route.route_owner,
        status=route.status,
        input_identity=cursor,
        semantic_output=asdict(route),
        evaluator="plan_and_route",
    )
    predevelopment = native_project_entry.evaluate_predevelopment(
        workflow_state="conflict"
    )
    _record_stage(
        records,
        stage="predevelopment_readiness",
        owner="cotend_code_context_harness",
        status=predevelopment.status,
        input_identity=cursor,
        semantic_output=asdict(predevelopment),
        evaluator="predevelopment_readiness",
    )

    _assert_no_authority_crossing(
        authority, workflow, entry, route, predevelopment
    )
    if (
        workflow.state != "conflict"
        or workflow.can_continue
        or workflow.write_native_record
        or entry.write_performed
        or entry.bare_continue_allowed
        or predevelopment.status != "blocked"
        or predevelopment.broad_edits_allowed
    ):
        raise NativeNegativeRecoveryError(
            "unknown or drifted state was silently accepted"
        )

    return IncidentResult(
        group="unknown_or_drifted_state",
        scenario=state_incident,
        status="blocked_safe",
        incident_id=incident_id,
        goal_id=goal_id,
        profile=profile,
        execution_mode=_execution_mode(profile),
        route_revision=1,
        checkpoint_identity=checkpoint_identity,
        implementation_identity="none",
        failed_verification_identity="none",
        recovered_implementation_identity="none",
        recovered_verification_identity="none",
        closeout_status="not_started",
        blocking_reason=blocking_reason,
        reliable_resume_boundary=route.reliable_resume_boundary,
        stage_records=tuple(records),
        user_decision_required=workflow.user_decision_required,
        unaffected_route_preserved=route.unaffected_route_can_continue,
    )


def run_failed_check_recovery(
    profile: Profile,
    *,
    recovery_failure: bool = False,
) -> IncidentResult:
    profile = _validate_profile(profile)
    scenario = "recovery_failure" if recovery_failure else "successful_recovery"
    incident_id = f"G04-check-{scenario}-{profile}"
    goal_id = "G04-check-recovery-goal"
    active_leaf = "L71-validate-native-negative-recovery-and-ownership"
    records: list[IncidentStage] = []
    cursor = _identity("incident", {"incident_id": incident_id, "goal_id": goal_id})

    authority = native_authority.evaluate_external_artifact("absent")
    cursor = _record_stage(
        records,
        stage="project_truth_authority",
        owner=authority.route_owner,
        status=authority.classification,
        input_identity=cursor,
        semantic_output=asdict(authority),
        evaluator="project_truth_authority",
    )
    workflow = native_workflow_state.evaluate_workflow(
        "current", native_profiles=(profile,)
    )
    cursor = _record_stage(
        records,
        stage="workflow_state_runtime_profile",
        owner=workflow.native_record_owner,
        status=workflow.state,
        input_identity=cursor,
        semantic_output=asdict(workflow),
        evaluator="workflow_state_runtime_profile",
    )
    entry = native_project_entry.evaluate_entry("current")
    cursor = _record_stage(
        records,
        stage="project_init",
        owner="cotend_project_init",
        status=entry.readiness,
        input_identity=cursor,
        semantic_output=asdict(entry),
        evaluator="project_init",
    )
    clarification = native_clarification.evaluate_clarification("clear")
    cursor = _record_stage(
        records,
        stage="requirements_clarification",
        owner=clarification.route_owner,
        status=clarification.route,
        input_identity=cursor,
        semantic_output=asdict(clarification),
        evaluator="requirements_clarification",
    )
    route = native_route_rebase.evaluate_route_change("ordinary_leaf")
    cursor = _record_stage(
        records,
        stage="plan_and_route",
        owner=route.route_owner,
        status=route.status,
        input_identity=cursor,
        semantic_output=asdict(route),
        evaluator="plan_and_route",
    )
    predevelopment = native_project_entry.evaluate_predevelopment()
    cursor = _record_stage(
        records,
        stage="predevelopment_readiness",
        owner="cotend_code_context_harness",
        status=predevelopment.status,
        input_identity=cursor,
        semantic_output=asdict(predevelopment),
        evaluator="predevelopment_readiness",
    )
    checkpoint_identity = cursor

    implementation = native_implementation.evaluate_implementation(
        profile=profile,
        active_leaf=active_leaf,
        allowed_paths=("src/feature.py", "tests/test_feature.py"),
        acceptance=("G04 fixture behavior passes",),
    )
    implementation_identity = _record_stage(
        records,
        stage="implementation_pass",
        owner=implementation.execution_shape,
        status=implementation.status,
        input_identity=cursor,
        semantic_output=asdict(implementation),
        evaluator="implementation_pass",
    )
    failed_verification = native_verification.evaluate_verification(
        profile=profile,
        active_leaf=active_leaf,
        implementation_identity=implementation_identity,
        changed_paths=("src/feature.py", "tests/test_feature.py"),
        allowed_fix_paths=("src/feature.py", "tests/test_feature.py"),
        requirements=("G04-REQ",),
        acceptance=("G04-AC",),
        required_checks=("unit", "integration"),
        check_state="fail_unfixable",
    )
    failed_verification_identity = _record_stage(
        records,
        stage="verification_failed",
        owner=failed_verification.execution_shape,
        status=failed_verification.status,
        input_identity=implementation_identity,
        semantic_output=asdict(failed_verification),
        evaluator="verification_pass",
    )
    if (
        failed_verification.status != "failed"
        or failed_verification.formal_review_handoff != "not_ready"
        or failed_verification.user_acceptance_claimed
        or failed_verification.release_authorized
    ):
        raise NativeNegativeRecoveryError(
            "failed verification crossed a completion boundary"
        )

    recovered_implementation = native_implementation.evaluate_implementation(
        profile=profile,
        active_leaf=active_leaf,
        allowed_paths=("src/feature.py", "tests/test_feature.py"),
        acceptance=("G04 fixture behavior passes",),
        resume_state="drifted",
    )
    recovered_implementation_identity = _record_stage(
        records,
        stage="implementation_recovered",
        owner=recovered_implementation.execution_shape,
        status=recovered_implementation.status,
        input_identity=failed_verification_identity,
        semantic_output=asdict(recovered_implementation),
        evaluator="implementation_pass",
    )
    recovered_verification = native_verification.evaluate_verification(
        profile=profile,
        active_leaf=active_leaf,
        implementation_identity=recovered_implementation_identity,
        changed_paths=("src/feature.py", "tests/test_feature.py"),
        allowed_fix_paths=("src/feature.py", "tests/test_feature.py"),
        requirements=("G04-REQ",),
        acceptance=("G04-AC",),
        required_checks=("unit", "integration"),
    )
    recovered_verification_identity = _record_stage(
        records,
        stage="verification_recovered",
        owner=recovered_verification.execution_shape,
        status=recovered_verification.status,
        input_identity=recovered_implementation_identity,
        semantic_output=asdict(recovered_verification),
        evaluator="verification_pass",
    )
    formal_review_identity = _record_stage(
        records,
        stage="formal_self_review_fixture",
        owner="codex_self_fixture",
        status="APPROVE",
        input_identity=recovered_verification_identity,
        semantic_output={
            "reviewed_verification_identity": recovered_verification_identity,
            "unresolved_P0_P1_P2": 0,
            "independence": "same_session_self_fixture",
            "real_external_review_claimed": False,
        },
        evaluator="formal_review_gate",
    )
    closeout = native_closeout.evaluate_closeout(
        profile=profile,
        closeout_id=incident_id,
        active_leaf=active_leaf,
        implementation_identity=recovered_implementation_identity,
        verification_result=recovered_verification.status,
        verification_identity=recovered_verification_identity,
        formal_review_verdict="APPROVE",
        unresolved_review_findings=0,
        workspace_identity=_identity("workspace", incident_id),
        authorized_paths=(
            "src/feature.py",
            "tests/test_feature.py",
            "STATUS.md",
            "REVIEW-LOG.md",
        ),
        observed_changed_paths=("src/feature.py", "tests/test_feature.py"),
        required_records=("STATUS.md", "REVIEW-LOG.md"),
        commit_intent="not_applicable",
        git_repository=False,
        record_write_state=("fail_concurrent_drift" if recovery_failure else "pass"),
    )
    _record_stage(
        records,
        stage="closeout_after_recovery",
        owner="cotend_native_closeout",
        status=closeout.status,
        input_identity=formal_review_identity,
        semantic_output={
            **asdict(closeout),
            "formal_review_identity": formal_review_identity,
        },
        evaluator="closeout_pass",
    )

    _assert_no_authority_crossing(
        authority,
        workflow,
        entry,
        clarification,
        route,
        predevelopment,
        implementation,
        failed_verification,
        recovered_implementation,
        recovered_verification,
        closeout,
    )
    if (
        implementation_identity == recovered_implementation_identity
        or failed_verification_identity == recovered_verification_identity
        or recovered_verification.input_implementation_identity
        != recovered_implementation_identity
        or recovered_verification.status != "passed"
    ):
        raise NativeNegativeRecoveryError(
            "recovery reused stale implementation or verification evidence"
        )
    if recovery_failure:
        if (
            closeout.status != "blocked"
            or closeout.rollback_action != "preserved_concurrent_drift"
            or closeout.history_rewrite_performed
            or closeout.done_claimed
        ):
            raise NativeNegativeRecoveryError(
                "recovery failure did not preserve checkpoint evidence"
            )
        status = "recovery_failed_safe"
    else:
        if (
            closeout.status != "completed"
            or not closeout.postcommit_verified
            or closeout.done_claimed
        ):
            raise NativeNegativeRecoveryError(
                "successful recovery did not complete closeout safely"
            )
        status = "recovered"

    return IncidentResult(
        group="failed_check_and_recovery",
        scenario=scenario,
        status=status,
        incident_id=incident_id,
        goal_id=goal_id,
        profile=profile,
        execution_mode=_execution_mode(profile),
        route_revision=1,
        checkpoint_identity=checkpoint_identity,
        implementation_identity=implementation_identity,
        failed_verification_identity=failed_verification_identity,
        recovered_implementation_identity=recovered_implementation_identity,
        recovered_verification_identity=recovered_verification_identity,
        closeout_status=closeout.status,
        blocking_reason=closeout.blocking_reason,
        reliable_resume_boundary="predevelopment_verified_checkpoint",
        stage_records=tuple(records),
        checkpoint_preserved=True,
        stale_evidence_reused=False,
        closeout_before_recovery=False,
    )


def _snapshot_files(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def run_protected_file_fixture(
    *,
    tamper_protected: bool = False,
) -> FileProtectionResult:
    with tempfile.TemporaryDirectory(prefix="cotend-g04-") as temporary:
        root = Path(temporary)
        payloads = {
            "records/REVIEW-LOG.md": b"owned review record\n",
            "truth/PROJECT-BRIEF.md": b"confirmed project meaning\n",
            "user/notes.txt": b"user-authored notes\n",
            "src/unrelated.py": b"UNRELATED = True\n",
            "staged/external.txt": b"external staged change\n",
        }
        for relative, content in payloads.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        before = _snapshot_files(root)
        owned_path = root / "records" / "REVIEW-LOG.md"
        protected = {
            key
            for key in before
            if key != "records/REVIEW-LOG.md"
        }

        owned_path.write_bytes(b"partial closeout write\n")
        owned_failure = native_closeout.evaluate_closeout(
            closeout_id="G04-owned-rollback",
            active_leaf="L71-validate-native-negative-recovery-and-ownership",
            authorized_paths=("records/REVIEW-LOG.md",),
            observed_changed_paths=("records/REVIEW-LOG.md",),
            required_records=("records/REVIEW-LOG.md",),
            commit_intent="not_applicable",
            git_repository=False,
            record_write_state="fail_owned_current",
        )
        if owned_failure.rollback_action != "restored_owned_precommit_writes":
            raise NativeNegativeRecoveryError(
                "owned record failure did not request bounded rollback"
            )
        owned_path.write_bytes(payloads["records/REVIEW-LOG.md"])
        after_owned_rollback = _snapshot_files(root)
        if after_owned_rollback != before:
            raise NativeNegativeRecoveryError(
                "owned record rollback changed protected fixture bytes"
            )

        owned_path.write_bytes(b"concurrent external record edit\n")
        concurrent = native_closeout.evaluate_closeout(
            closeout_id="G04-concurrent-drift",
            active_leaf="L71-validate-native-negative-recovery-and-ownership",
            authorized_paths=("records/REVIEW-LOG.md",),
            observed_changed_paths=("records/REVIEW-LOG.md",),
            required_records=("records/REVIEW-LOG.md",),
            commit_intent="not_applicable",
            git_repository=False,
            record_write_state="fail_concurrent_drift",
        )
        if (
            concurrent.rollback_action != "preserved_concurrent_drift"
            or concurrent.history_rewrite_performed
        ):
            raise NativeNegativeRecoveryError(
                "concurrent drift was overwritten during recovery"
            )
        if tamper_protected:
            (root / "user" / "notes.txt").write_bytes(b"tampered\n")
        after_concurrent = _snapshot_files(root)
        changed_protected = {
            key
            for key in protected
            if after_concurrent.get(key) != before.get(key)
        }
        if changed_protected:
            raise NativeNegativeRecoveryError(
                "protected fixture bytes changed: "
                + ", ".join(sorted(changed_protected))
            )

        return FileProtectionResult(
            status="protected",
            protected_file_count=len(protected),
            owned_record_count=1,
            owned_rollback=owned_failure.rollback_action,
            concurrent_drift_disposition=concurrent.rollback_action,
            project_truth_preserved=(
                after_concurrent["truth/PROJECT-BRIEF.md"]
                == before["truth/PROJECT-BRIEF.md"]
            ),
            user_files_preserved=(
                after_concurrent["user/notes.txt"] == before["user/notes.txt"]
            ),
            unrelated_files_preserved=(
                after_concurrent["src/unrelated.py"]
                == before["src/unrelated.py"]
            ),
            staged_external_preserved=(
                after_concurrent["staged/external.txt"]
                == before["staged/external.txt"]
            ),
            checkpoint_preserved=True,
        )


def reject_damaged_handoff() -> bool:
    baseline = native_cumulative.run_main_journey(
        "full", journey_id="G04-damaged-handoff-baseline"
    )
    envelope = json.loads(baseline.handoff_document)
    envelope["payload"]["route_revision"] = 999
    try:
        native_cumulative.recover_handoff(
            json.dumps(envelope), session_id="G04-independent-recovery"
        )
    except native_cumulative.NativeCumulativeJourneyError:
        return True
    raise NativeNegativeRecoveryError("damaged handoff was accepted")


def equivalence_projection(result: IncidentResult) -> dict[str, Any]:
    return {
        "group": result.group,
        "scenario": result.scenario,
        "status": result.status,
        "route_revision": result.route_revision,
        "closeout_status": result.closeout_status,
        "blocking_reason": result.blocking_reason,
        "reliable_resume_boundary": result.reliable_resume_boundary,
        "user_decision_required": result.user_decision_required,
        "unaffected_route_preserved": result.unaffected_route_preserved,
        "checkpoint_preserved": result.checkpoint_preserved,
        "project_truth_preserved": result.project_truth_preserved,
        "user_files_preserved": result.user_files_preserved,
        "unrelated_files_preserved": result.unrelated_files_preserved,
        "stale_evidence_reused": result.stale_evidence_reused,
        "silent_state_reset": result.silent_state_reset,
        "closeout_before_recovery": result.closeout_before_recovery,
        "external_framework_owner": result.external_framework_owner,
        "parallel_truth_created": result.parallel_truth_created,
        "real_project_claimed": result.real_project_claimed,
        "real_user_acceptance_claimed": result.real_user_acceptance_claimed,
        "release_authorized": result.release_authorized,
        "stage_shape": tuple(
            (record.stage, record.status, record.evaluator)
            for record in result.stage_records
        ),
    }


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise NativeNegativeRecoveryError(
            f"{label} is missing required markers: {', '.join(missing)}"
        )


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NativeNegativeRecoveryError(f"{label} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise NativeNegativeRecoveryError(f"{label} must be a JSON object")
    return payload


def _validate_no_regression_baseline(root: Path) -> dict[str, Any]:
    framework_lock = _load_json(
        root / FRAMEWORK_LOCK_PATH.relative_to(ROOT), "framework lock"
    )
    capability_map = _load_json(
        root / CAPABILITY_MAP_PATH.relative_to(ROOT), "capability map"
    )
    role_map = _load_json(root / ROLE_MAP_PATH.relative_to(ROOT), "role map")
    target_lock = _load_json(
        root / TARGET_LOCK_PATH.relative_to(ROOT), "target artifact lock"
    )

    capabilities = capability_map.get("capabilities")
    capability_ids = {
        item.get("capability_id")
        for item in capabilities
        if isinstance(item, dict)
    } if isinstance(capabilities, list) else set()
    skills = role_map.get("skills")
    target_skills = {
        item.get("target_skill_id")
        for item in skills
        if isinstance(item, dict)
    } if isinstance(skills, list) else set()
    source_release = framework_lock.get("source_anchor")
    target = target_lock.get("target")
    skill_files, skill_digest = native_closeout.skill_manifest(root)
    if (
        framework_lock.get("release_id")
        != "exact-source:fe21e970bc2bdc69de5e2ce1710aef2dd156a54d"
        or framework_lock.get("framework_protocol")
        != "cotend-collaboration-v2.01"
        or not isinstance(source_release, dict)
        or source_release.get("type") != "exact_source_commit"
        or source_release.get("commit")
        != "fe21e970bc2bdc69de5e2ce1710aef2dd156a54d"
        or source_release.get("publication_state") != "not_public_release"
        or framework_lock.get("skill_count") != 10
        or framework_lock.get("skill_file_count") != 94
        or capability_map.get("capability_count") != 19
        or capability_ids != EXPECTED_CAPABILITY_IDS
        or role_map.get("skill_count") != 10
        or target_skills != EXPECTED_TARGET_SKILLS
        or not isinstance(target, dict)
        or target.get("artifact_id") != "cotend-codex-r000017"
        or target.get("revision") != 17
        or target.get("manifest_sha256") != skill_digest
        or target_lock.get("skill_count") != 10
        or target_lock.get("skill_file_count") != len(skill_files)
    ):
        raise NativeNegativeRecoveryError(
            "locked dual-ai to CoTend no-regression baseline drifted"
        )

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
    capability_results = {
        capability_id: verifier(root)
        for capability_id, verifier in capability_checks
    }
    if any(
        result.get("status") != "native_parity_verified"
        for result in capability_results.values()
    ):
        raise NativeNegativeRecoveryError("a G02 native capability regressed")
    cumulative = native_cumulative.verify_repository(root)
    if cumulative.get("status") != "native_cumulative_main_journey_verified":
        raise NativeNegativeRecoveryError("G03 cumulative journey regressed")

    return {
        "dual_capabilities": len(capability_ids),
        "mapped_skill_roles": len(target_skills),
        "native_capabilities": len(capability_results),
        "source_release": framework_lock["release_id"],
        "target_artifact": target["artifact_id"],
        "target_manifest_sha256": skill_digest,
    }


def verify_repository(root: Path = ROOT) -> dict[str, Any]:
    document_path = root / DOCUMENT_PATH.relative_to(ROOT)
    evidence_path = root / EVIDENCE_PATH.relative_to(ROOT)
    contract_path = root / CONTRACT_PATH.relative_to(ROOT)
    _require_markers(
        document_path.read_text(encoding="utf-8"),
        REQUIRED_DOCUMENT_MARKERS,
        "native negative recovery document",
    )
    _require_markers(
        evidence_path.read_text(encoding="utf-8"),
        REQUIRED_EVIDENCE_MARKERS,
        "native negative recovery evidence",
    )
    contract = _load_json(contract_path, "Trellis decoupling contract")
    gates = contract.get("gates")
    if not isinstance(gates, list):
        raise NativeNegativeRecoveryError("decoupling gates are missing")
    g04 = next(
        (
            gate
            for gate in gates
            if isinstance(gate, dict)
            and gate.get("id") == "G04-negative-recovery-and-ownership"
        ),
        None,
    )
    if (
        not isinstance(g04, dict)
        or g04.get("status") != "complete"
        or g04.get("evidence") != EXPECTED_G04_EVIDENCE
    ):
        raise NativeNegativeRecoveryError("G04 machine contract drifted")
    baseline = _validate_no_regression_baseline(root)
    conflicts = {
        f"{semantic_level}-{profile}": run_foreign_framework_conflict(
            profile, semantic_level
        )
        for semantic_level in ("L0_L2", "L3_L4")
        for profile in ("full", "adaptive")
    }
    state_incidents = {
        f"{state_incident}-{profile}": run_unknown_or_drifted_state(
            profile, state_incident
        )
        for state_incident in ("unknown_external", "duplicate_native_record")
        for profile in ("full", "adaptive")
    }
    recoveries = {
        f"{scenario}-{profile}": run_failed_check_recovery(
            profile, recovery_failure=scenario == "recovery_failure"
        )
        for scenario in ("successful_recovery", "recovery_failure")
        for profile in ("full", "adaptive")
    }
    for semantic_level in ("L0_L2", "L3_L4"):
        if equivalence_projection(conflicts[f"{semantic_level}-full"]) != (
            equivalence_projection(conflicts[f"{semantic_level}-adaptive"])
        ):
            raise NativeNegativeRecoveryError(
                f"Full and Adaptive conflict outcomes drifted: {semantic_level}"
            )
    for state_incident in ("unknown_external", "duplicate_native_record"):
        if equivalence_projection(state_incidents[f"{state_incident}-full"]) != (
            equivalence_projection(state_incidents[f"{state_incident}-adaptive"])
        ):
            raise NativeNegativeRecoveryError(
                f"Full and Adaptive state outcomes drifted: {state_incident}"
            )
    for scenario in ("successful_recovery", "recovery_failure"):
        if equivalence_projection(recoveries[f"{scenario}-full"]) != (
            equivalence_projection(recoveries[f"{scenario}-adaptive"])
        ):
            raise NativeNegativeRecoveryError(
                f"Full and Adaptive recovery outcomes drifted: {scenario}"
            )

    fixture = run_protected_file_fixture()
    if (
        fixture.status != "protected"
        or not fixture.project_truth_preserved
        or not fixture.user_files_preserved
        or not fixture.unrelated_files_preserved
        or not fixture.staged_external_preserved
        or not fixture.checkpoint_preserved
        or fixture.real_project_claimed
        or fixture.real_user_acceptance_claimed
    ):
        raise NativeNegativeRecoveryError("protected file fixture drifted")
    if not reject_damaged_handoff():
        raise NativeNegativeRecoveryError("damaged handoff was not rejected")

    all_incidents = [*conflicts.values(), *state_incidents.values(), *recoveries.values()]
    evaluators = {
        record.evaluator
        for result in all_incidents
        for record in result.stage_records
    }
    if evaluators != EXPECTED_STAGE_EVALUATORS:
        missing = sorted(EXPECTED_STAGE_EVALUATORS - evaluators)
        extra = sorted(evaluators - EXPECTED_STAGE_EVALUATORS)
        raise NativeNegativeRecoveryError(
            f"G04 evaluator composition drifted: missing={missing} extra={extra}"
        )
    for result in all_incidents:
        for previous, current in zip(
            result.stage_records, result.stage_records[1:]
        ):
            if current.input_identity != previous.output_identity:
                raise NativeNegativeRecoveryError(
                    f"G04 stage identity chain broke: {result.incident_id}"
                )
        if (
            result.external_framework_owner
            or result.parallel_truth_created
            or result.real_project_claimed
            or result.real_user_acceptance_claimed
            or result.release_authorized
            or result.stale_evidence_reused
            or result.silent_state_reset
            or result.closeout_before_recovery
            or not result.project_truth_preserved
            or not result.user_files_preserved
            or not result.unrelated_files_preserved
        ):
            raise NativeNegativeRecoveryError(
                f"G04 incident crossed a boundary: {result.incident_id}"
            )

    return {
        "status": "native_negative_recovery_ownership_verified",
        "gate": "G04-negative-recovery-and-ownership",
        "evidence_group_count": 4,
        "incident_scenario_count": len(all_incidents) + 1,
        "native_capabilities_composed": baseline["native_capabilities"],
        "dual_capability_baseline": baseline["dual_capabilities"],
        "mapped_skill_roles": baseline["mapped_skill_roles"],
        "full_adaptive_equivalent": True,
        "damaged_handoff_rejected": True,
        "protected_file_fixture": asdict(fixture),
        "real_project_claimed": False,
        "real_user_acceptance_claimed": False,
        "skill_behavior_changed": False,
        "target_artifact": baseline["target_artifact"],
        "target_manifest_sha256": baseline["target_manifest_sha256"],
        "results": {
            "foreign_framework_conflict": {
                key: asdict(value) for key, value in conflicts.items()
            },
            "unknown_or_drifted_state": {
                key: asdict(value) for key, value in state_incidents.items()
            },
            "failed_check_and_recovery": {
                key: asdict(value) for key, value in recoveries.items()
            },
        },
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, NativeNegativeRecoveryError) as exc:
        print("NATIVE_NEGATIVE_RECOVERY_OWNERSHIP_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_NEGATIVE_RECOVERY_OWNERSHIP_OK "
        f"gate={result['gate']} "
        f"incidents={result['incident_scenario_count']} "
        f"groups={result['evidence_group_count']} "
        f"capabilities={result['native_capabilities_composed']} "
        f"behavior_changed=false target={result['target_artifact']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
