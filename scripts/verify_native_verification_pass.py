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
VERIFICATION_PASS_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "verification-pass.md"
)
IMPLEMENTATION_PASS_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "implementation-pass.md"
)
COLLABORATION_PATH = ROOT / "skills" / "cotend-collaboration" / "SKILL.md"
ACCEPTANCE_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "acceptance-test-harness.md"
)
REVIEW_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "review-and-self-review.md"
)
RUNTIME_PROFILES_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "runtime-profiles.md"
)
ORCHESTRATION_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "native-agent-orchestration.md"
)
PROJECT_INIT_PATH = ROOT / "skills" / "cotend-project-init" / "SKILL.md"
MODEL_UPGRADE_PATH = ROOT / "skills" / "cotend-model-upgrade" / "SKILL.md"
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-VERIFICATION-PASS.md"
EVIDENCE_PATH = (
    ROOT / "docs" / "evidence" / "NATIVE-VERIFICATION-PASS-TARGET-R9.md"
)
DECOUPLING_PLAN_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
SOURCE_LOCK_PATH = ROOT / "upstream" / "framework.lock.json"
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"

Profile = Literal["full", "adaptive"]
CheckState = Literal[
    "pass",
    "fail_fixable",
    "fail_unfixable",
    "missing",
    "tool_unavailable",
]
FindingState = Literal["none", "fixable", "unfixable", "critical"]
ResumeState = Literal[
    "fresh",
    "interrupted_current",
    "drifted",
    "ambiguous_side_effect",
    "passed_current",
]

REMOVED_TD05_COMMAND = "trellis-check"
REQUIRED_REMAINING_COMMANDS: tuple[str, ...] = ()
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
EXPECTED_R8_MANIFEST = (
    "84c4c02a2d56502b7ed9457fad23e0077ff8a9cf567c544ea7fdaf54c6a94bc3"
)

REQUIRED_VERIFICATION_MARKERS = (
    "# Native Verification Pass",
    "## Entry Contract",
    "verification_pass_input:",
    "execution_shape: independent_checker | primary_inline_checker",
    "## Direct Scope Derivation",
    "## Findings And Authorized Fixes",
    "post-fix implementation identity",
    "status: passed | passed_after_fix | failed | blocked",
    "## Full And Adaptive Execution",
    "## Interruption, Drift, And Idempotency",
    "formal_self_review: required | not_ready",
    "user_acceptance: false",
    "route_or_release: false",
    "## Authority Boundary",
)
REQUIRED_COLLABORATION_MARKERS = (
    "fixed Native\n  Implementation/Verification pair",
    "Adaptive performs the same contracts\n  inline",
    "Native Closeout alone owns exact staging",
)
REQUIRED_ACCEPTANCE_MARKERS = (
    "This module owns verification-surface selection and direct observations.",
    "The canonical evidence and result values remain owned",
)
REQUIRED_REVIEW_MARKERS = (
    "Ordinary implementation self-check is not formal review.",
    "`ai_generated` and not independent external review or user acceptance",
)
REQUIRED_RUNTIME_MARKERS = (
    "Native Implementation Pass -> Native Verification Pass",
    "performs the Native Verification Pass inline",
    "Local commit/Native Closeout remains opt-in",
    "Local closeout never implies push/release/publication",
)
REQUIRED_ORCHESTRATION_MARKERS = (
    "Full profile's fixed `Native Implementation Pass -> Native Verification Pass` pair",
    "single integration owner",
)
REQUIRED_PROJECT_INIT_MARKERS = (
    "apply_coherence_sized_execution_on_active_route",
    "apply_outcome_triggered_governance_on_active_route",
    "one plan/implement/verify/triggered-review/primary-owner-state/commit",
)
REQUIRED_MODEL_MARKERS = (
    "`takeover_ready` requires current full-scope Project",
    "Full and Adaptive produce the same identity",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生检查阶段",
    "status: native_parity_verified",
    "cotend-codex-r000009",
    "Full 独立 Checker",
    "Adaptive 内联 Checker",
    "7 处、6 个文件",
    "正式自审",
    "TD07",
)


class NativeVerificationPassError(ValueError):
    pass


@dataclass(frozen=True)
class VerificationResult:
    profile: str
    execution_shape: str
    status: str
    blocking_reason: str
    inspection_started: bool
    writes_performed: bool
    finding_action: str
    check_action: str
    resume_action: str
    input_implementation_identity: str
    checked_implementation_identity: str
    direct_diff_inspected: bool
    specs_and_acceptance_read: bool
    required_checks_executed: bool
    unresolved_findings: int
    evidence_fields: tuple[str, ...]
    formal_review_handoff: str
    ai_uat_handoff: str
    idempotent_noop: bool
    independent_scope_derived: bool
    implementer_report_only: bool
    unrelated_files_preserved: bool
    external_framework_owner: bool
    formal_review_claimed: bool
    ai_uat_claimed: bool
    user_acceptance_claimed: bool
    route_changed: bool
    release_authorized: bool


EVIDENCE_FIELDS = (
    "diff_and_paths_inspected",
    "requirements_specs_and_constraints_read",
    "commands_and_results",
    "findings_and_dispositions",
    "fixes_and_post_fix_identity",
    "skipped_checks_and_reasons",
    "residual_risks_or_questions",
)


def _result(
    *,
    profile: Profile,
    status: str,
    blocking_reason: str,
    implementation_identity: str,
    inspection_started: bool = False,
    writes_performed: bool = False,
    finding_action: str = "not_started",
    check_action: str = "not_run",
    resume_action: str = "not_needed",
    checked_implementation_identity: str = "not_bound",
    direct_diff_inspected: bool = False,
    specs_and_acceptance_read: bool = False,
    required_checks_executed: bool = False,
    unresolved_findings: int = 0,
    formal_review_handoff: str = "not_ready",
    ai_uat_handoff: str = "not_ready",
    idempotent_noop: bool = False,
) -> VerificationResult:
    return VerificationResult(
        profile=profile,
        execution_shape=(
            "independent_checker" if profile == "full" else "primary_inline_checker"
        ),
        status=status,
        blocking_reason=blocking_reason,
        inspection_started=inspection_started,
        writes_performed=writes_performed,
        finding_action=finding_action,
        check_action=check_action,
        resume_action=resume_action,
        input_implementation_identity=implementation_identity,
        checked_implementation_identity=checked_implementation_identity,
        direct_diff_inspected=direct_diff_inspected,
        specs_and_acceptance_read=specs_and_acceptance_read,
        required_checks_executed=required_checks_executed,
        unresolved_findings=unresolved_findings,
        evidence_fields=EVIDENCE_FIELDS,
        formal_review_handoff=formal_review_handoff,
        ai_uat_handoff=ai_uat_handoff,
        idempotent_noop=idempotent_noop,
        independent_scope_derived=direct_diff_inspected,
        implementer_report_only=False,
        unrelated_files_preserved=True,
        external_framework_owner=False,
        formal_review_claimed=False,
        ai_uat_claimed=False,
        user_acceptance_claimed=False,
        route_changed=False,
        release_authorized=False,
    )


def evaluate_verification(
    *,
    profile: Profile = "full",
    active_leaf: str = "authorized-leaf",
    checker_handoff: str = "required",
    implementation_status: str = "integration_waiting",
    implementation_identity: str = "sha256:implementation-v1",
    diff_basis: str = "git-diff:base-to-workspace",
    changed_paths: tuple[str, ...] = ("src/example.py", "tests/test_example.py"),
    allowed_fix_paths: tuple[str, ...] = ("src/example.py", "tests/test_example.py"),
    requirements: tuple[str, ...] = ("REQ-1",),
    acceptance: tuple[str, ...] = ("AC-1",),
    required_checks: tuple[str, ...] = ("unit",),
    active_leaf_current: bool = True,
    protected_semantics_current: bool = True,
    acceptance_current: bool = True,
    implementation_identity_current: bool = True,
    diff_observable: bool = True,
    scope_clean: bool = True,
    direct_evidence_available: bool = True,
    risk_allowed: bool = True,
    check_state: CheckState = "pass",
    finding_state: FindingState = "none",
    fix_within_scope: bool = True,
    retest_passes: bool = True,
    resume_state: ResumeState = "fresh",
    ai_uat_required: bool = False,
) -> VerificationResult:
    if profile not in {"full", "adaptive"}:
        raise NativeVerificationPassError("invalid runtime profile")
    if checker_handoff not in {"required", "not_ready"}:
        raise NativeVerificationPassError("invalid checker handoff")
    if implementation_status not in {"integration_waiting", "closed"}:
        raise NativeVerificationPassError("invalid implementation status")
    if check_state not in {
        "pass",
        "fail_fixable",
        "fail_unfixable",
        "missing",
        "tool_unavailable",
    }:
        raise NativeVerificationPassError("invalid check state")
    if finding_state not in {"none", "fixable", "unfixable", "critical"}:
        raise NativeVerificationPassError("invalid finding state")
    if resume_state not in {
        "fresh",
        "interrupted_current",
        "drifted",
        "ambiguous_side_effect",
        "passed_current",
    }:
        raise NativeVerificationPassError("invalid resume state")
    for name, value in {
        "active_leaf": active_leaf,
        "implementation_identity": implementation_identity,
        "diff_basis": diff_basis,
    }.items():
        if not value.strip():
            raise NativeVerificationPassError(f"missing required field: {name}")
    for name, value in {
        "changed_paths": changed_paths,
        "allowed_fix_paths": allowed_fix_paths,
        "requirements": requirements,
        "acceptance": acceptance,
        "required_checks": required_checks,
    }.items():
        if not value or any(not item.strip() for item in value):
            raise NativeVerificationPassError(f"missing required field: {name}")

    preconditions = (
        (checker_handoff == "required", "checker_handoff_not_ready"),
        (active_leaf_current, "active_leaf_drift"),
        (protected_semantics_current, "protected_semantic_conflict"),
        (acceptance_current, "acceptance_contract_conflict"),
        (implementation_identity_current, "stale_implementation_identity"),
        (diff_observable, "diff_basis_not_reconstructable"),
        (risk_allowed, "risk_or_stop_boundary"),
    )
    for condition, reason in preconditions:
        if not condition:
            return _result(
                profile=profile,
                status="blocked",
                blocking_reason=reason,
                implementation_identity=implementation_identity,
            )

    if resume_state == "ambiguous_side_effect":
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="ambiguous_side_effect",
            implementation_identity=implementation_identity,
            resume_action="reconcile_before_retry",
        )

    cached_result_current = (
        scope_clean
        and direct_evidence_available
        and check_state == "pass"
        and finding_state == "none"
    )
    if resume_state == "passed_current" and cached_result_current:
        return _result(
            profile=profile,
            status="passed",
            blocking_reason="none",
            implementation_identity=implementation_identity,
            resume_action="return_existing_current_result",
            checked_implementation_identity=implementation_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
            required_checks_executed=True,
            formal_review_handoff="required",
            ai_uat_handoff="required" if ai_uat_required else "not_needed",
            idempotent_noop=True,
        )

    resume_action = {
        "fresh": "start_direct_check",
        "interrupted_current": "continue_from_verified_checker_checkpoint",
        "drifted": "rederive_scope_and_rerun_required_checks",
        "passed_current": "rederive_scope_and_rerun_required_checks",
    }[resume_state]

    if not scope_clean:
        return _result(
            profile=profile,
            status="failed",
            blocking_reason="unexpected_or_out_of_scope_changed_paths",
            implementation_identity=implementation_identity,
            inspection_started=True,
            finding_action="report_unresolved_scope_finding",
            check_action="not_run_scope_failed_first",
            resume_action=resume_action,
            checked_implementation_identity=implementation_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
            unresolved_findings=1,
        )

    if not direct_evidence_available:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="direct_evidence_missing",
            implementation_identity=implementation_identity,
            inspection_started=True,
            finding_action="reject_implementer_report_only",
            check_action="not_run_evidence_missing",
            resume_action=resume_action,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
        )

    if finding_state == "critical":
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="critical_finding_requires_human_rejoin",
            implementation_identity=implementation_identity,
            inspection_started=True,
            finding_action="record_critical_and_stop",
            check_action="stop_before_fix",
            resume_action=resume_action,
            checked_implementation_identity=implementation_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
            unresolved_findings=1,
        )

    if check_state in {"missing", "tool_unavailable"}:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason=(
                "required_check_missing"
                if check_state == "missing"
                else "required_check_tool_unavailable"
            ),
            implementation_identity=implementation_identity,
            inspection_started=True,
            finding_action="record_blocked_check",
            check_action="required_check_not_run",
            resume_action=resume_action,
            checked_implementation_identity=implementation_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
        )

    if finding_state == "unfixable" or check_state == "fail_unfixable":
        return _result(
            profile=profile,
            status="failed",
            blocking_reason="unresolved_verification_failure",
            implementation_identity=implementation_identity,
            inspection_started=True,
            finding_action="record_unresolved_failure",
            check_action="run_and_record_failure",
            resume_action=resume_action,
            checked_implementation_identity=implementation_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
            required_checks_executed=True,
            unresolved_findings=1,
        )

    fix_needed = finding_state == "fixable" or check_state == "fail_fixable"
    if fix_needed and not fix_within_scope:
        return _result(
            profile=profile,
            status="failed",
            blocking_reason="fix_outside_authorized_scope",
            implementation_identity=implementation_identity,
            inspection_started=True,
            finding_action="return_fix_to_root_primary",
            check_action="run_and_record_failure",
            resume_action=resume_action,
            checked_implementation_identity=implementation_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
            required_checks_executed=True,
            unresolved_findings=1,
        )

    if fix_needed:
        post_fix_identity = f"{implementation_identity}+checker-fix"
        if not retest_passes:
            return _result(
                profile=profile,
                status="failed",
                blocking_reason="post_fix_retest_failed",
                implementation_identity=implementation_identity,
                inspection_started=True,
                writes_performed=True,
                finding_action="fix_in_scope_but_unresolved",
                check_action="fix_rerun_and_record_failure",
                resume_action=resume_action,
                checked_implementation_identity=post_fix_identity,
                direct_diff_inspected=True,
                specs_and_acceptance_read=True,
                required_checks_executed=True,
                unresolved_findings=1,
            )
        return _result(
            profile=profile,
            status="passed_after_fix",
            blocking_reason="none",
            implementation_identity=implementation_identity,
            inspection_started=True,
            writes_performed=True,
            finding_action="fix_in_scope_rebind_identity_and_close",
            check_action="fix_rerun_and_record_pass",
            resume_action=resume_action,
            checked_implementation_identity=post_fix_identity,
            direct_diff_inspected=True,
            specs_and_acceptance_read=True,
            required_checks_executed=True,
            formal_review_handoff="required",
            ai_uat_handoff="required" if ai_uat_required else "not_needed",
        )

    return _result(
        profile=profile,
        status="passed",
        blocking_reason="none",
        implementation_identity=implementation_identity,
        inspection_started=True,
        finding_action="no_material_findings",
        check_action="run_and_record_pass",
        resume_action=resume_action,
        checked_implementation_identity=implementation_identity,
        direct_diff_inspected=True,
        specs_and_acceptance_read=True,
        required_checks_executed=True,
        formal_review_handoff="required",
        ai_uat_handoff="required" if ai_uat_required else "not_needed",
    )


SCENARIOS = {
    "full_clean_pass": {
        "kwargs": {"profile": "full"},
        "expected": {"status": "passed", "formal_review_handoff": "required"},
    },
    "adaptive_clean_pass": {
        "kwargs": {"profile": "adaptive"},
        "expected": {"status": "passed", "formal_review_handoff": "required"},
    },
    "checker_handoff_not_ready": {
        "kwargs": {"checker_handoff": "not_ready"},
        "expected": {"status": "blocked", "inspection_started": False},
    },
    "active_leaf_drift": {
        "kwargs": {"active_leaf_current": False},
        "expected": {"blocking_reason": "active_leaf_drift", "writes_performed": False},
    },
    "semantic_conflict": {
        "kwargs": {"protected_semantics_current": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "acceptance_conflict": {
        "kwargs": {"acceptance_current": False},
        "expected": {"blocking_reason": "acceptance_contract_conflict"},
    },
    "stale_implementation_identity": {
        "kwargs": {"implementation_identity_current": False},
        "expected": {"blocking_reason": "stale_implementation_identity"},
    },
    "diff_not_reconstructable": {
        "kwargs": {"diff_observable": False},
        "expected": {"blocking_reason": "diff_basis_not_reconstructable"},
    },
    "unexpected_changed_path": {
        "kwargs": {"scope_clean": False},
        "expected": {"status": "failed", "unresolved_findings": 1},
    },
    "implementer_report_without_direct_evidence": {
        "kwargs": {"direct_evidence_available": False},
        "expected": {"status": "blocked", "implementer_report_only": False},
    },
    "fixable_finding_fixed": {
        "kwargs": {"finding_state": "fixable"},
        "expected": {"status": "passed_after_fix", "writes_performed": True},
    },
    "fixable_check_fixed": {
        "kwargs": {"check_state": "fail_fixable"},
        "expected": {"status": "passed_after_fix", "required_checks_executed": True},
    },
    "fix_outside_scope": {
        "kwargs": {"finding_state": "fixable", "fix_within_scope": False},
        "expected": {"status": "failed", "writes_performed": False},
    },
    "post_fix_retest_failure": {
        "kwargs": {"finding_state": "fixable", "retest_passes": False},
        "expected": {"status": "failed", "writes_performed": True},
    },
    "unfixable_finding": {
        "kwargs": {"finding_state": "unfixable"},
        "expected": {"status": "failed", "formal_review_handoff": "not_ready"},
    },
    "unfixable_check_failure": {
        "kwargs": {"check_state": "fail_unfixable"},
        "expected": {"status": "failed", "required_checks_executed": True},
    },
    "required_check_missing": {
        "kwargs": {"check_state": "missing"},
        "expected": {"status": "blocked", "required_checks_executed": False},
    },
    "required_tool_unavailable": {
        "kwargs": {"check_state": "tool_unavailable"},
        "expected": {"blocking_reason": "required_check_tool_unavailable"},
    },
    "critical_finding_stops": {
        "kwargs": {"finding_state": "critical"},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "interrupted_current_resume": {
        "kwargs": {"resume_state": "interrupted_current"},
        "expected": {"resume_action": "continue_from_verified_checker_checkpoint"},
    },
    "drifted_resume_rechecks": {
        "kwargs": {"resume_state": "drifted"},
        "expected": {"resume_action": "rederive_scope_and_rerun_required_checks"},
    },
    "ambiguous_side_effect_stops": {
        "kwargs": {"resume_state": "ambiguous_side_effect"},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "passed_current_idempotent": {
        "kwargs": {"resume_state": "passed_current"},
        "expected": {"status": "passed", "idempotent_noop": True},
    },
}


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise NativeVerificationPassError(f"{label} is missing: {marker}")


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
        raise NativeVerificationPassError(str(exc)) from exc
    paths = {
        "verification": VERIFICATION_PASS_PATH,
        "implementation": IMPLEMENTATION_PASS_PATH,
        "collaboration": COLLABORATION_PATH,
        "acceptance": ACCEPTANCE_PATH,
        "review": REVIEW_PATH,
        "runtime": RUNTIME_PROFILES_PATH,
        "orchestration": ORCHESTRATION_PATH,
        "model_upgrade": MODEL_UPGRADE_PATH,
        "document": DOCUMENT_PATH,
        "evidence": EVIDENCE_PATH,
    }
    texts = {
        name: (root / path.relative_to(ROOT)).read_text(encoding="utf-8")
        for name, path in paths.items()
    }
    texts["project_init"] = project_init
    _require_markers(texts["verification"], REQUIRED_VERIFICATION_MARKERS, "verification contract")
    _require_markers(texts["collaboration"], REQUIRED_COLLABORATION_MARKERS, "collaboration Skill")
    _require_markers(texts["acceptance"], REQUIRED_ACCEPTANCE_MARKERS, "acceptance harness")
    _require_markers(texts["review"], REQUIRED_REVIEW_MARKERS, "formal review contract")
    _require_markers(texts["runtime"], REQUIRED_RUNTIME_MARKERS, "runtime profiles")
    _require_markers(texts["orchestration"], REQUIRED_ORCHESTRATION_MARKERS, "native orchestration")
    _require_markers(texts["project_init"], REQUIRED_PROJECT_INIT_MARKERS, "Project Init")
    _require_markers(texts["model_upgrade"], REQUIRED_MODEL_MARKERS, "Model Upgrade")
    _require_markers(texts["document"], REQUIRED_DOCUMENT_MARKERS, "public contract")

    skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    if REMOVED_TD05_COMMAND in skill_text.lower():
        raise NativeVerificationPassError("TD05 compatibility command remains")
    for command in REQUIRED_REMAINING_COMMANDS:
        if command not in skill_text.lower():
            raise NativeVerificationPassError(f"required later command missing: {command}")
    if re.search(r"capability:\s*verification(?:\s*\||\s*$)", skill_text, re.IGNORECASE | re.MULTILINE):
        raise NativeVerificationPassError("obsolete verification compatibility mapping remains")
    if (root / "skills" / "cotend-check").exists():
        raise NativeVerificationPassError("a user-visible cotend-check Skill was created")
    for pattern in (r"\$cotend-check\b", r"/cotend-check\b", r"name:\s*cotend-check\b"):
        if re.search(pattern, skill_text, re.IGNORECASE):
            raise NativeVerificationPassError("a public cotend-check invocation was created")

    inventory = runtime_inventory(root)
    if sum(inventory.values()) != EXPECTED_TRELLIS_MENTIONS or len(inventory) != EXPECTED_TRELLIS_FILES:
        raise NativeVerificationPassError("exact TD05 runtime Trellis inventory drifted")

    source_lock = json.loads((root / SOURCE_LOCK_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))
    if source_lock.get("skill_file_count") != 94:
        raise NativeVerificationPassError("current upstream source inventory drifted")

    lock = json.loads((root / TARGET_LOCK_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))
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
        raise NativeVerificationPassError("r17 target identity or manifest drifted")
    if not predecessors or predecessors[0] != {
        "platform": "Codex",
        "lineage": "cotend-codex",
        "artifact_id": "cotend-codex-r000016",
        "revision": 16,
        "source_release_id": "exact-source:c14d4133bf0438d435048858554c88c89a7870a3",
        "framework_protocol": "cotend-collaboration-v1.79",
        "manifest_sha256": EXPECTED_R16_MANIFEST,
    }:
        raise NativeVerificationPassError("r16 predecessor identity drifted")

    _require_markers(
        texts["evidence"],
        (
            "current_target_artifact_id: cotend-codex-r000009",
            "current_target_revision: 9",
            f"current_target_manifest_sha256: {EXPECTED_R9_MANIFEST}",
            "predecessor_target_artifact_id: cotend-codex-r000008",
            f"predecessor_target_manifest_sha256: {EXPECTED_R8_MANIFEST}",
            "runtime_trellis_inventory: 20_mentions_10_files",
            "TD05-verification-pass",
        ),
        "target evidence",
    )

    decoupling = json.loads((root / DECOUPLING_PLAN_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))
    td05 = next(
        (item for item in decoupling.get("capabilities", []) if item.get("id") == "TD05-verification-pass"),
        None,
    )
    g02 = next(
        (item for item in decoupling.get("gates", []) if item.get("id") == "G02-per-capability-native-parity"),
        None,
    )
    current_runtime = decoupling.get("current_runtime", {})
    if (
        not isinstance(td05, dict)
        or td05.get("status") != "native_parity_verified"
        or not isinstance(g02, dict)
        or g02.get("status") != "complete"
        or current_runtime.get("mention_count") != EXPECTED_TRELLIS_MENTIONS
        or current_runtime.get("file_count") != EXPECTED_TRELLIS_FILES
        or current_runtime.get("file_mentions") != inventory
    ):
        raise NativeVerificationPassError("TD05 decoupling state or exact inventory drifted")

    scenario_results: dict[str, dict[str, object]] = {}
    for scenario_id, contract in SCENARIOS.items():
        result = evaluate_verification(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeVerificationPassError(
                    f"verification scenario drifted: {scenario_id}.{key}"
                )
        if (
            result.implementer_report_only
            or not result.unrelated_files_preserved
            or result.external_framework_owner
            or result.formal_review_claimed
            or result.ai_uat_claimed
            or result.user_acceptance_claimed
            or result.route_changed
            or result.release_authorized
        ):
            raise NativeVerificationPassError(
                f"verification authority invariant failed: {scenario_id}"
            )
        scenario_results[scenario_id] = payload

    full = evaluate_verification(profile="full")
    adaptive = evaluate_verification(profile="adaptive")
    parity_fields = tuple(
        field
        for field in VerificationResult.__dataclass_fields__
        if field not in {"profile", "execution_shape"}
    )
    if any(getattr(full, field) != getattr(adaptive, field) for field in parity_fields):
        raise NativeVerificationPassError("Full and Adaptive Checker contracts diverged")

    return {
        "status": "native_parity_verified",
        "capability": "TD05-verification-pass",
        "scenario_count": len(scenario_results),
        "scenarios": scenario_results,
        "runtime_mentions": sum(inventory.values()),
        "runtime_files": len(inventory),
        "td05_commands": 0,
        "remaining_commands": len(REQUIRED_REMAINING_COMMANDS),
        "skill_files": len(files),
        "target_artifact": target.get("artifact_id"),
        "target_manifest": digest,
        "full_adaptive_result_parity": True,
        "external_framework_owner": False,
        "formal_review_claimed": False,
        "user_acceptance_claimed": False,
        "unrelated_files_preserved": True,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, json.JSONDecodeError, NativeVerificationPassError) as exc:
        print("NATIVE_VERIFICATION_PASS_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_VERIFICATION_PASS_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        f"runtime_mentions={result['runtime_mentions']} "
        f"runtime_files={result['runtime_files']} td05_commands=0 "
        f"remaining_commands={result['remaining_commands']} "
        f"target={result['target_artifact']}"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
