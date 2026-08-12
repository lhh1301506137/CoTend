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
CLOSEOUT_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "closeout-pass.md"
)
COLLABORATION_PATH = ROOT / "skills" / "cotend-collaboration" / "SKILL.md"
CONTINUOUS_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "continuous-and-unattended.md"
)
RISK_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "risk-and-approval.md"
)
GOAL_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "goal-completion.md"
)
PLAN_TREE_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "plan-tree.md"
)
RUNTIME_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "runtime-profiles.md"
)
TEMPLATES_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "collaboration-packet-templates.md"
)
PROJECT_INIT_PATH = ROOT / "skills" / "cotend-project-init" / "SKILL.md"
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-CLOSEOUT-ARCHIVE-AND-RECOVERY.md"
EVIDENCE_PATH = (
    ROOT / "docs" / "evidence" / "NATIVE-CLOSEOUT-PASS-TARGET-R10.md"
)
DECOUPLING_PLAN_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
SOURCE_LOCK_PATH = ROOT / "upstream" / "framework.lock.json"
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"

Profile = Literal["full", "adaptive"]
CommitIntent = Literal["create", "reuse_current", "not_applicable"]
RecordWriteState = Literal["pass", "fail_owned_current", "fail_concurrent_drift"]
CommitState = Literal["pass", "fail"]
PostcommitState = Literal["pass", "fail"]
ResumePhase = Literal[
    "fresh",
    "preflight_complete",
    "records_written",
    "commit_created",
    "postcommit_verified",
    "completed_current",
    "drifted",
    "ambiguous_side_effect",
]

EXPECTED_TRELLIS_MENTIONS = 0
EXPECTED_TRELLIS_FILES = 0
EXPECTED_SKILL_FILES = 104
EXPECTED_R16_MANIFEST = (
    "a7f7ece2522a5901030e19cd5944359f80c027482f66f822a2053fc5080dcfb5"
)
EXPECTED_R15_MANIFEST = (
    "acc17586cf713acc85fef9e6be02013de6bc012b7864ade22bed495ee68a9e7b"
)
EXPECTED_R14_MANIFEST = (
    "07ac592c82ed87f1759b38f04ed1f453c44e21d454fd12b4ce9eca459e4f3ed4"
)
EXPECTED_R13_MANIFEST = (
    "39e1455b11f482d80d33dff421e0db5c08182f597c175f0391bd679750f903fd"
)
EXPECTED_R9_MANIFEST = (
    "32049aa36e25d0a46eacf92ce2cf06c42b688947e93fc3c6d6b1ae478a019072"
)
EXPECTED_R10_MANIFEST = (
    "0715c20f517f906996d4882e47c664449a23cf6f7747b6a2d42835f35591b8a9"
)
EXPECTED_R11_MANIFEST = (
    "eac48844295f9ba12d64df469aa25fab9e76a8c9ceb9817857350b5029767627"
)
REMOVED_TD07_TERMS = (
    "trellis-finish",
    "trellis_finish_archive_done",
    "trellis_finish_archive_allowed",
    "auto_local_commit_and_trellis_finish",
    "trellis_links",
    "capability: closeout",
)

REQUIRED_CLOSEOUT_MARKERS = (
    "# Native Closeout Pass",
    "## Entry Contract",
    "verification_result: passed | passed_after_fix",
    "formal_review_verdict: APPROVE",
    "## Canonical Phases",
    "commit_created_or_not_needed",
    "## Durable Record Ownership",
    "HANDOFF.md",
    "## Local Commit Boundary",
    "## Failure And Rollback",
    "## Interruption And Resume",
    "history_rewrite_performed: false",
    "## Full And Adaptive",
    "## Authority Boundary",
)
REQUIRED_COLLABORATION_MARKERS = (
    "Native Closeout alone owns exact staging",
    "STATUS.md#cotend_workflow",
)
REQUIRED_CONTINUOUS_MARKERS = (
    "local_closeout_authorization.status: active",
    "Native Closeout commit gate prompt",
    "Native Closeout Pass still owns exact staging",
    "native_closeout_done: yes | no | not_applicable",
)
REQUIRED_RISK_MARKERS = (
    "auto_local_commit_and_native_closeout",
    "Native Closeout Pass may proceed",
    "After local closeout, report commit hash",
)
REQUIRED_RUNTIME_MARKERS = (
    "Local commit/Native Closeout remains opt-in",
    "Local closeout never implies push/release/publication",
)
REQUIRED_PROJECT_INIT_MARKERS = (
    "one plan/implement/verify/triggered-review/primary-owner-state/commit",
    "local-closeout authorization",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生收尾、归档与恢复",
    "status: native_parity_verified",
    "cotend-codex-r000010",
    "Full 与 Adaptive",
    "提交前失败",
    "提交后失败",
    "7 处、6 个文件",
    "G03-G06",
)


class NativeCloseoutPassError(ValueError):
    pass


@dataclass(frozen=True)
class CloseoutResult:
    profile: str
    status: str
    blocking_reason: str
    closeout_id: str
    active_leaf: str
    phase_reached: str
    resume_action: str
    preflight_completed: bool
    record_write_attempted: bool
    record_writes_performed: bool
    synchronized_records: tuple[str, ...]
    handoff_result: str
    commit_result: str
    commit_identity: str
    postcommit_verified: bool
    rollback_action: str
    history_rewrite_performed: bool
    unrelated_files_preserved: bool
    sensitive_paths_staged: bool
    external_framework_owner: bool
    idempotent_noop: bool
    writes_performed: bool
    verification_replaced: bool
    formal_review_replaced: bool
    done_claimed: bool
    user_acceptance_claimed: bool
    route_changed: bool
    push_release_publish_authorized: bool
    goal_completion_handoff: str


def _result(
    *,
    profile: Profile,
    status: str,
    blocking_reason: str,
    closeout_id: str,
    active_leaf: str,
    phase_reached: str = "preflight",
    resume_action: str = "not_started",
    preflight_completed: bool = False,
    record_write_attempted: bool = False,
    record_writes_performed: bool = False,
    synchronized_records: tuple[str, ...] = (),
    handoff_result: str = "not_started",
    commit_result: str = "not_started",
    commit_identity: str = "none",
    postcommit_verified: bool = False,
    rollback_action: str = "not_needed",
    idempotent_noop: bool = False,
    writes_performed: bool = False,
    goal_completion_handoff: str = "blocked",
) -> CloseoutResult:
    return CloseoutResult(
        profile=profile,
        status=status,
        blocking_reason=blocking_reason,
        closeout_id=closeout_id,
        active_leaf=active_leaf,
        phase_reached=phase_reached,
        resume_action=resume_action,
        preflight_completed=preflight_completed,
        record_write_attempted=record_write_attempted,
        record_writes_performed=record_writes_performed,
        synchronized_records=synchronized_records,
        handoff_result=handoff_result,
        commit_result=commit_result,
        commit_identity=commit_identity,
        postcommit_verified=postcommit_verified,
        rollback_action=rollback_action,
        history_rewrite_performed=False,
        unrelated_files_preserved=True,
        sensitive_paths_staged=False,
        external_framework_owner=False,
        idempotent_noop=idempotent_noop,
        writes_performed=writes_performed,
        verification_replaced=False,
        formal_review_replaced=False,
        done_claimed=False,
        user_acceptance_claimed=False,
        route_changed=False,
        push_release_publish_authorized=False,
        goal_completion_handoff=goal_completion_handoff,
    )


def evaluate_closeout(
    *,
    profile: Profile = "full",
    closeout_id: str = "closeout-001",
    active_leaf: str = "authorized-leaf",
    implementation_identity: str = "sha256:implementation-v1",
    verification_result: str = "passed",
    verification_identity: str = "sha256:verification-v1",
    formal_review_verdict: str = "APPROVE",
    unresolved_review_findings: int = 0,
    workspace_identity: str = "sha256:workspace-v1",
    authorized_paths: tuple[str, ...] = (
        "src/example.py",
        "tests/test_example.py",
        "STATUS.md",
        "REVIEW-LOG.md",
    ),
    observed_changed_paths: tuple[str, ...] = (
        "src/example.py",
        "tests/test_example.py",
    ),
    required_records: tuple[str, ...] = ("STATUS.md", "REVIEW-LOG.md"),
    handoff_required: bool = False,
    handoff_record: str = "HANDOFF.md",
    handoff_surface_available: bool = True,
    local_closeout_authorization: bool = True,
    commit_intent: CommitIntent = "create",
    git_repository: bool = True,
    active_leaf_current: bool = True,
    verification_current: bool = True,
    review_current: bool = True,
    workspace_inventory_complete: bool = True,
    record_ownership_clear: bool = True,
    record_hashes_current: bool = True,
    staged_paths_clean: bool = True,
    pending_human_decision: bool = False,
    critical_boundary: bool = False,
    sensitive_or_private_path: bool = False,
    unrelated_or_unknown_path: bool = False,
    record_write_state: RecordWriteState = "pass",
    commit_state: CommitState = "pass",
    current_commit_matches: bool = True,
    postcommit_state: PostcommitState = "pass",
    resume_phase: ResumePhase = "fresh",
) -> CloseoutResult:
    if profile not in {"full", "adaptive"}:
        raise NativeCloseoutPassError("invalid runtime profile")
    if verification_result not in {"passed", "passed_after_fix"}:
        raise NativeCloseoutPassError("invalid verification result")
    if commit_intent not in {"create", "reuse_current", "not_applicable"}:
        raise NativeCloseoutPassError("invalid commit intent")
    if record_write_state not in {
        "pass",
        "fail_owned_current",
        "fail_concurrent_drift",
    }:
        raise NativeCloseoutPassError("invalid record write state")
    if commit_state not in {"pass", "fail"}:
        raise NativeCloseoutPassError("invalid commit state")
    if postcommit_state not in {"pass", "fail"}:
        raise NativeCloseoutPassError("invalid postcommit state")
    if resume_phase not in {
        "fresh",
        "preflight_complete",
        "records_written",
        "commit_created",
        "postcommit_verified",
        "completed_current",
        "drifted",
        "ambiguous_side_effect",
    }:
        raise NativeCloseoutPassError("invalid resume phase")
    for name, value in {
        "closeout_id": closeout_id,
        "active_leaf": active_leaf,
        "implementation_identity": implementation_identity,
        "verification_identity": verification_identity,
        "workspace_identity": workspace_identity,
        "handoff_record": handoff_record,
    }.items():
        if not value.strip():
            raise NativeCloseoutPassError(f"missing required field: {name}")
    for name, value in {
        "authorized_paths": authorized_paths,
        "observed_changed_paths": observed_changed_paths,
        "required_records": required_records,
    }.items():
        if not value or any(not item.strip() for item in value):
            raise NativeCloseoutPassError(f"missing required field: {name}")
    if unresolved_review_findings < 0:
        raise NativeCloseoutPassError("invalid unresolved review finding count")

    if resume_phase == "ambiguous_side_effect":
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="ambiguous_side_effect",
            closeout_id=closeout_id,
            active_leaf=active_leaf,
            resume_action="reconcile_actual_state_before_retry",
        )

    observed_set = set(observed_changed_paths)
    authorized_set = set(authorized_paths)
    preconditions = (
        (active_leaf_current, "active_leaf_drift"),
        (verification_current, "stale_verification_identity"),
        (review_current, "stale_formal_review"),
        (formal_review_verdict == "APPROVE", "formal_review_not_approved"),
        (unresolved_review_findings == 0, "unresolved_review_findings"),
        (workspace_inventory_complete, "workspace_inventory_incomplete"),
        (record_ownership_clear, "record_owner_ambiguous"),
        (record_hashes_current, "record_hash_drift"),
        (local_closeout_authorization, "local_closeout_not_authorized"),
        (not pending_human_decision, "pending_human_decision"),
        (not critical_boundary, "critical_boundary"),
        (not sensitive_or_private_path, "sensitive_or_private_path"),
        (not unrelated_or_unknown_path, "unrelated_or_unknown_path"),
        (observed_set <= authorized_set, "observed_path_outside_authorization"),
        (set(required_records) <= authorized_set, "record_outside_authorization"),
        (staged_paths_clean, "unrelated_staged_content"),
        (
            not handoff_required or handoff_surface_available,
            "required_handoff_surface_missing",
        ),
        (
            not handoff_required or handoff_record in required_records,
            "required_handoff_record_missing",
        ),
        (commit_intent == "not_applicable" or git_repository, "git_repository_missing"),
        (
            (
                commit_intent == "not_applicable"
                or (
                    commit_intent != "reuse_current"
                    and resume_phase
                    not in {
                        "commit_created",
                        "postcommit_verified",
                        "completed_current",
                    }
                )
                or current_commit_matches
            ),
            "current_commit_does_not_match_checkpoint",
        ),
    )
    for condition, reason in preconditions:
        if not condition:
            return _result(
                profile=profile,
                status="blocked",
                blocking_reason=reason,
                closeout_id=closeout_id,
                active_leaf=active_leaf,
                resume_action="return_to_preflight_after_resolution",
            )

    resume_action = {
        "fresh": "start_preflight",
        "preflight_complete": "rerun_preflight_from_current_bytes",
        "records_written": "verify_record_post_hashes_then_continue",
        "commit_created": "inspect_existing_commit_then_verify",
        "postcommit_verified": "rebind_verified_evidence_then_finalize",
        "completed_current": "return_existing_current_result",
        "drifted": "restart_from_earliest_reliable_boundary",
    }[resume_phase]

    if resume_phase == "completed_current":
        if postcommit_state == "fail":
            return _result(
                profile=profile,
                status="failed",
                blocking_reason="postcommit_verification_failed",
                closeout_id=closeout_id,
                active_leaf=active_leaf,
                phase_reached="commit_created_or_not_needed",
                resume_action="preserve_evidence_and_request_separate_repair",
                preflight_completed=True,
                synchronized_records=required_records,
                handoff_result="updated" if handoff_required else "not_required",
                commit_result=(
                    "not_applicable"
                    if commit_intent == "not_applicable"
                    else "existing_current"
                ),
                commit_identity=(
                    "none"
                    if commit_intent == "not_applicable"
                    else "git:checkpoint-current"
                ),
                rollback_action="postcommit_evidence_preserved",
                writes_performed=False,
            )
        return _result(
            profile=profile,
            status="completed",
            blocking_reason="none",
            closeout_id=closeout_id,
            active_leaf=active_leaf,
            phase_reached="completed",
            resume_action=resume_action,
            preflight_completed=True,
            synchronized_records=required_records,
            handoff_result="updated" if handoff_required else "not_required",
            commit_result=(
                "not_applicable"
                if commit_intent == "not_applicable"
                else "existing_current"
            ),
            commit_identity=(
                "none"
                if commit_intent == "not_applicable"
                else "git:checkpoint-current"
            ),
            postcommit_verified=True,
            idempotent_noop=True,
            writes_performed=False,
            goal_completion_handoff="not_triggered",
        )

    records_already_current = resume_phase in {
        "records_written",
        "commit_created",
        "postcommit_verified",
    }
    commit_already_current = resume_phase in {
        "commit_created",
        "postcommit_verified",
    }

    if not records_already_current:
        if record_write_state == "fail_owned_current":
            return _result(
                profile=profile,
                status="failed",
                blocking_reason="record_write_failed",
                closeout_id=closeout_id,
                active_leaf=active_leaf,
                phase_reached="preflight",
                resume_action="repair_record_write_then_restart_preflight",
                preflight_completed=True,
                record_write_attempted=True,
                record_writes_performed=True,
                rollback_action="restored_owned_precommit_writes",
                writes_performed=True,
            )
        if record_write_state == "fail_concurrent_drift":
            return _result(
                profile=profile,
                status="blocked",
                blocking_reason="concurrent_record_drift_during_rollback",
                closeout_id=closeout_id,
                active_leaf=active_leaf,
                phase_reached="preflight",
                resume_action="reconcile_concurrent_drift_before_retry",
                preflight_completed=True,
                record_write_attempted=True,
                record_writes_performed=True,
                rollback_action="preserved_concurrent_drift",
                writes_performed=True,
            )

    record_writes_performed = not records_already_current
    handoff_result = "updated" if handoff_required else "not_required"

    if commit_already_current:
        commit_result = "existing_current"
        commit_identity = "git:checkpoint-current"
        commit_was_written = False
    elif commit_intent == "not_applicable":
        commit_result = "not_applicable"
        commit_identity = "none"
        commit_was_written = False
    elif commit_intent == "reuse_current":
        commit_result = "existing_current"
        commit_identity = "git:checkpoint-current"
        commit_was_written = False
    elif commit_state == "fail":
        return _result(
            profile=profile,
            status="failed",
            blocking_reason="local_commit_failed",
            closeout_id=closeout_id,
            active_leaf=active_leaf,
            phase_reached="records_written",
            resume_action="repair_commit_failure_then_restart_preflight",
            preflight_completed=True,
            record_write_attempted=not records_already_current,
            record_writes_performed=record_writes_performed,
            synchronized_records=(),
            handoff_result="blocked_missing" if handoff_required else "not_required",
            commit_result="failed",
            rollback_action="restored_owned_precommit_writes",
            writes_performed=record_writes_performed,
        )
    else:
        commit_result = "created"
        commit_identity = "git:checkpoint-new"
        commit_was_written = True

    if postcommit_state == "fail":
        return _result(
            profile=profile,
            status="failed",
            blocking_reason="postcommit_verification_failed",
            closeout_id=closeout_id,
            active_leaf=active_leaf,
            phase_reached="commit_created_or_not_needed",
            resume_action="preserve_evidence_and_request_separate_repair",
            preflight_completed=True,
            record_write_attempted=not records_already_current,
            record_writes_performed=record_writes_performed,
            synchronized_records=required_records,
            handoff_result=handoff_result,
            commit_result=commit_result,
            commit_identity=commit_identity,
            rollback_action="postcommit_evidence_preserved",
            writes_performed=record_writes_performed or commit_was_written,
        )

    return _result(
        profile=profile,
        status="completed",
        blocking_reason="none",
        closeout_id=closeout_id,
        active_leaf=active_leaf,
        phase_reached="completed",
        resume_action=resume_action,
        preflight_completed=True,
        record_write_attempted=not records_already_current,
        record_writes_performed=record_writes_performed,
        synchronized_records=required_records,
        handoff_result=handoff_result,
        commit_result=commit_result,
        commit_identity=commit_identity,
        postcommit_verified=True,
        writes_performed=record_writes_performed or commit_was_written,
        goal_completion_handoff="not_triggered",
    )


SCENARIOS = {
    "full_success": {
        "kwargs": {"profile": "full"},
        "expected": {"status": "completed", "commit_result": "created"},
    },
    "adaptive_success": {
        "kwargs": {"profile": "adaptive"},
        "expected": {"status": "completed", "commit_result": "created"},
    },
    "non_git_no_commit": {
        "kwargs": {"commit_intent": "not_applicable", "git_repository": False},
        "expected": {"status": "completed", "commit_result": "not_applicable"},
    },
    "reuse_current_commit": {
        "kwargs": {"commit_intent": "reuse_current"},
        "expected": {"commit_result": "existing_current"},
    },
    "stale_verification": {
        "kwargs": {"verification_current": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "pending_human_decision": {
        "kwargs": {"pending_human_decision": True},
        "expected": {"blocking_reason": "pending_human_decision"},
    },
    "critical_boundary": {
        "kwargs": {"critical_boundary": True},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "unrelated_path": {
        "kwargs": {"unrelated_or_unknown_path": True},
        "expected": {"blocking_reason": "unrelated_or_unknown_path"},
    },
    "sensitive_path": {
        "kwargs": {"sensitive_or_private_path": True},
        "expected": {"blocking_reason": "sensitive_or_private_path"},
    },
    "record_write_failure": {
        "kwargs": {"record_write_state": "fail_owned_current"},
        "expected": {
            "status": "failed",
            "rollback_action": "restored_owned_precommit_writes",
        },
    },
    "record_rollback_concurrent_drift": {
        "kwargs": {"record_write_state": "fail_concurrent_drift"},
        "expected": {
            "status": "blocked",
            "rollback_action": "preserved_concurrent_drift",
        },
    },
    "commit_failure": {
        "kwargs": {"commit_state": "fail"},
        "expected": {
            "commit_result": "failed",
            "status": "failed",
            "synchronized_records": (),
            "handoff_result": "not_required",
        },
    },
    "postcommit_failure": {
        "kwargs": {"postcommit_state": "fail"},
        "expected": {
            "status": "failed",
            "rollback_action": "postcommit_evidence_preserved",
        },
    },
    "preflight_resume": {
        "kwargs": {"resume_phase": "preflight_complete"},
        "expected": {"resume_action": "rerun_preflight_from_current_bytes"},
    },
    "records_resume": {
        "kwargs": {"resume_phase": "records_written"},
        "expected": {
            "resume_action": "verify_record_post_hashes_then_continue",
            "record_writes_performed": False,
        },
    },
    "commit_resume": {
        "kwargs": {"resume_phase": "commit_created"},
        "expected": {
            "commit_result": "existing_current",
            "record_writes_performed": False,
        },
    },
    "postcommit_resume": {
        "kwargs": {"resume_phase": "postcommit_verified"},
        "expected": {"resume_action": "rebind_verified_evidence_then_finalize"},
    },
    "drifted_resume": {
        "kwargs": {"resume_phase": "drifted"},
        "expected": {"resume_action": "restart_from_earliest_reliable_boundary"},
    },
    "ambiguous_side_effect": {
        "kwargs": {"resume_phase": "ambiguous_side_effect"},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "completed_idempotent": {
        "kwargs": {"resume_phase": "completed_current"},
        "expected": {"idempotent_noop": True, "writes_performed": False},
    },
    "required_handoff_missing": {
        "kwargs": {"handoff_required": True, "handoff_surface_available": False},
        "expected": {"blocking_reason": "required_handoff_surface_missing"},
    },
    "authorization_disabled": {
        "kwargs": {"local_closeout_authorization": False},
        "expected": {"blocking_reason": "local_closeout_not_authorized"},
    },
    "unrelated_staged_content": {
        "kwargs": {"staged_paths_clean": False},
        "expected": {"blocking_reason": "unrelated_staged_content"},
    },
}


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise NativeCloseoutPassError(f"{label} is missing: {marker}")


def runtime_inventory(root: Path = ROOT) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for path in sorted((root / "skills").rglob("*")):
        if (
            not path.is_file()
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        text = path.read_text(encoding="utf-8")
        count = len(re.findall("trellis", text, re.IGNORECASE))
        if count:
            inventory[path.relative_to(root).as_posix()] = count
    return inventory


def skill_manifest(root: Path = ROOT) -> tuple[dict[str, str], str]:
    files = {
        path.relative_to(root / "skills").as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }
    digest = hashlib.sha256(
        json.dumps(
            files,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return files, digest


def verify_repository(root: Path = ROOT) -> dict[str, object]:
    try:
        project_init = project_init_contract.load_project_init_contract(root)[
            "combined"
        ]
    except project_init_contract.ProjectInitContractError as exc:
        raise NativeCloseoutPassError(str(exc)) from exc
    paths = {
        "closeout": CLOSEOUT_PATH,
        "collaboration": COLLABORATION_PATH,
        "continuous": CONTINUOUS_PATH,
        "risk": RISK_PATH,
        "goal": GOAL_PATH,
        "plan_tree": PLAN_TREE_PATH,
        "runtime": RUNTIME_PATH,
        "templates": TEMPLATES_PATH,
        "document": DOCUMENT_PATH,
        "evidence": EVIDENCE_PATH,
    }
    texts = {
        name: (root / path.relative_to(ROOT)).read_text(encoding="utf-8")
        for name, path in paths.items()
    }
    texts["project_init"] = project_init
    _require_markers(texts["closeout"], REQUIRED_CLOSEOUT_MARKERS, "closeout contract")
    _require_markers(
        texts["collaboration"], REQUIRED_COLLABORATION_MARKERS, "Collaboration Skill"
    )
    _require_markers(
        texts["continuous"], REQUIRED_CONTINUOUS_MARKERS, "continuous contract"
    )
    _require_markers(texts["risk"], REQUIRED_RISK_MARKERS, "risk contract")
    _require_markers(
        texts["runtime"], REQUIRED_RUNTIME_MARKERS, "runtime profiles"
    )
    _require_markers(
        texts["project_init"], REQUIRED_PROJECT_INIT_MARKERS, "Project Init"
    )
    _require_markers(texts["document"], REQUIRED_DOCUMENT_MARKERS, "public contract")
    if "this module consumes its exact result and never creates a Done-specific completion packet" not in texts["goal"]:
        raise NativeCloseoutPassError("goal/closeout independence is missing")
    if "At a material checkpoint, after any required actual-artifact gate passes:" not in texts["plan_tree"]:
        raise NativeCloseoutPassError("Plan Tree closeout checkpoint is missing")
    if "native_closeout_allowed: yes | no | not_applicable" not in texts["templates"]:
        raise NativeCloseoutPassError("native closeout template is missing")

    skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    lowered = skill_text.lower()
    for term in REMOVED_TD07_TERMS:
        if term in lowered:
            raise NativeCloseoutPassError(f"TD07 compatibility term remains: {term}")
    for pattern in (
        r"\$cotend-closeout\b",
        r"/cotend-closeout\b",
        r"name:\s*cotend-closeout\b",
    ):
        if re.search(pattern, skill_text, re.IGNORECASE):
            raise NativeCloseoutPassError("a public cotend-closeout invocation was created")
    if (root / "skills" / "cotend-closeout").exists():
        raise NativeCloseoutPassError("a user-visible cotend-closeout Skill was created")

    inventory = runtime_inventory(root)
    if (
        sum(inventory.values()) != EXPECTED_TRELLIS_MENTIONS
        or len(inventory) != EXPECTED_TRELLIS_FILES
    ):
        raise NativeCloseoutPassError("exact TD07 runtime Trellis inventory drifted")

    source_lock = json.loads(
        (root / SOURCE_LOCK_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    )
    if source_lock.get("skill_file_count") != 94:
        raise NativeCloseoutPassError("current upstream source inventory drifted")

    lock = json.loads(
        (root / TARGET_LOCK_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    )
    target = lock.get("target", {})
    predecessors = lock.get("predecessor_targets", [])
    files, digest = skill_manifest(root)
    if (
        target.get("artifact_id") != "cotend-codex-r000017"
        or target.get("revision") != 17
        or target.get("manifest_sha256") != digest
        or lock.get("skill_count") != 10
        or lock.get("skill_file_count") != EXPECTED_SKILL_FILES
        or len(files) != EXPECTED_SKILL_FILES
    ):
        raise NativeCloseoutPassError("r17 target identity or manifest drifted")
    if not predecessors or predecessors[0] != {
        "platform": "Codex",
        "lineage": "cotend-codex",
        "artifact_id": "cotend-codex-r000016",
        "revision": 16,
        "source_release_id": "exact-source:c14d4133bf0438d435048858554c88c89a7870a3",
        "framework_protocol": "cotend-collaboration-v1.79",
        "manifest_sha256": EXPECTED_R16_MANIFEST,
    }:
        raise NativeCloseoutPassError("r16 predecessor identity drifted")

    _require_markers(
        texts["evidence"],
        (
            "current_target_artifact_id: cotend-codex-r000010",
            "current_target_revision: 10",
            f"current_target_manifest_sha256: {EXPECTED_R10_MANIFEST}",
            "predecessor_target_artifact_id: cotend-codex-r000009",
            f"predecessor_target_manifest_sha256: {EXPECTED_R9_MANIFEST}",
            "runtime_trellis_inventory: 7_mentions_6_files",
            "current_skill_files: 40",
            "full_unit_tests: 311_passed",
            "official_skill_quick_validate: passed_8_of_8",
            "repository_check: passed_248_public_candidates_19_capabilities_19_specs",
            "delivery_lifecycle: passed_11_steps_5_identity_8_negative_6_concurrency_8_recovery",
            "writable_lifecycle: passed_4_scenarios_9_negative",
            "production_plugin_lifecycle: passed_17_steps_5_recovery",
            "github_marketplace_carrier: passed_15_steps_5_recovery",
            "TD07-closeout-archive-and-recovery",
        ),
        "target evidence",
    )

    decoupling = json.loads(
        (root / DECOUPLING_PLAN_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    )
    td07 = next(
        (
            item
            for item in decoupling.get("capabilities", [])
            if item.get("id") == "TD07-closeout-archive-and-recovery"
        ),
        None,
    )
    g02 = next(
        (
            item
            for item in decoupling.get("gates", [])
            if item.get("id") == "G02-per-capability-native-parity"
        ),
        None,
    )
    current_runtime = decoupling.get("current_runtime", {})
    if (
        not isinstance(td07, dict)
        or td07.get("status") != "native_parity_verified"
        or not isinstance(g02, dict)
        or g02.get("status") != "complete"
        or current_runtime.get("mention_count") != EXPECTED_TRELLIS_MENTIONS
        or current_runtime.get("file_count") != EXPECTED_TRELLIS_FILES
        or current_runtime.get("file_mentions") != inventory
    ):
        raise NativeCloseoutPassError("TD07 decoupling state or inventory drifted")

    scenario_results: dict[str, dict[str, object]] = {}
    for scenario_id, contract in SCENARIOS.items():
        result = evaluate_closeout(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeCloseoutPassError(
                    f"closeout scenario drifted: {scenario_id}.{key}"
                )
        if (
            result.history_rewrite_performed
            or not result.unrelated_files_preserved
            or result.sensitive_paths_staged
            or result.external_framework_owner
            or result.verification_replaced
            or result.formal_review_replaced
            or result.done_claimed
            or result.user_acceptance_claimed
            or result.route_changed
            or result.push_release_publish_authorized
        ):
            raise NativeCloseoutPassError(
                f"closeout authority invariant failed: {scenario_id}"
            )
        scenario_results[scenario_id] = payload

    full = evaluate_closeout(profile="full")
    adaptive = evaluate_closeout(profile="adaptive")
    parity_fields = tuple(
        field for field in CloseoutResult.__dataclass_fields__ if field != "profile"
    )
    if any(getattr(full, field) != getattr(adaptive, field) for field in parity_fields):
        raise NativeCloseoutPassError("Full and Adaptive closeout contracts diverged")

    return {
        "status": "native_parity_verified",
        "capability": "TD07-closeout-archive-and-recovery",
        "scenario_count": len(scenario_results),
        "scenarios": scenario_results,
        "runtime_mentions": sum(inventory.values()),
        "runtime_files": len(inventory),
        "td07_compatibility_terms": 0,
        "skill_files": len(files),
        "target_artifact": target.get("artifact_id"),
        "target_manifest": digest,
        "full_adaptive_result_parity": True,
        "history_rewrite_performed": False,
        "external_framework_owner": False,
        "user_acceptance_claimed": False,
        "push_release_publish_authorized": False,
        "unrelated_files_preserved": True,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, json.JSONDecodeError, NativeCloseoutPassError) as exc:
        print("NATIVE_CLOSEOUT_PASS_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_CLOSEOUT_PASS_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        f"runtime_mentions={result['runtime_mentions']} "
        f"runtime_files={result['runtime_files']} td07_terms=0 "
        f"target={result['target_artifact']}"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
