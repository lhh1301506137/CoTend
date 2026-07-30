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
IMPLEMENTATION_PASS_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "implementation-pass.md"
)
COLLABORATION_PATH = ROOT / "skills" / "cotend-collaboration" / "SKILL.md"
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
MODEL_PACKET_PATH = (
    ROOT
    / "skills"
    / "cotend-model-upgrade"
    / "references"
    / "packet-templates.md"
)
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-IMPLEMENTATION-PASS.md"
EVIDENCE_PATH = (
    ROOT / "docs" / "evidence" / "NATIVE-IMPLEMENTATION-PASS-TARGET-R8.md"
)
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"

Profile = Literal["full", "adaptive"]
TestState = Literal["pass", "fail_fixable", "fail_unfixable"]
ResumeState = Literal[
    "fresh",
    "safe_checkpoint",
    "drifted",
    "ambiguous_side_effect",
    "closed_current",
]

REMOVED_TD04_COMMAND = "trellis-implement"
REQUIRED_REMAINING_COMMANDS: tuple[str, ...] = ()
EXPECTED_TRELLIS_MENTIONS = 0
EXPECTED_TRELLIS_FILES = 0
EXPECTED_SKILL_FILES = 61
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
EXPECTED_R7_MANIFEST = (
    "246b16c990a85a2e183e0033c0b3a15a087e793ce0ace1f18e3d736f5a8fd045"
)

REQUIRED_IMPLEMENTATION_MARKERS = (
    "# Native Implementation Pass",
    "execute only one current authorized leaf or explicitly bounded slice",
    "## Entry Contract",
    "implementation_pass:",
    "execution_shape: delegated_implementer | primary_inline",
    "status: dependency_waiting | integration_waiting | blocked | closed",
    "## Authority Boundary",
    "## Full And Adaptive Execution",
    "## Interruption And Resume",
    "formal_checker: false",
    "user_acceptance: false",
    "route_or_release: false",
)
REQUIRED_COLLABORATION_MARKERS = (
    "read `references/implementation-pass.md`",
    "Full delegates its native Implementer role and Adaptive executes the same contract inline",
    "Full dispatches an independent Checker role and Adaptive enters the same Checker contract inline",
)
REQUIRED_RUNTIME_MARKERS = (
    "The Implementer executes `implementation-pass.md` through a bounded role packet",
    "The Primary executes the native `implementation-pass.md` contract",
    "Both profiles finish verified checkpoints through `closeout-pass.md`",
    "neither delegates closeout to an external framework",
)
REQUIRED_ORCHESTRATION_MARKERS = (
    "The Implementer always uses the native `implementation-pass.md` contract",
    "dispatch the Implementer through `implementation-pass.md`",
)
REQUIRED_PROJECT_INIT_MARKERS = (
    "Both profiles implement through `cotend-collaboration/references/implementation-pass.md` and check through `cotend-collaboration/references/verification-pass.md`.",
    "dispatch a bounded native Implementer",
    "Local closeout always uses `cotend-collaboration/references/closeout-pass.md`",
)
REQUIRED_MODEL_MARKERS = (
    "The Implementer always uses CoTend's native Implementation Pass",
    "the Checker always uses its native Verification Pass",
)
REQUIRED_MODEL_PACKET_MARKERS = (
    "framework_fixed_behavior: native_implementation_pass -> checker_contract",
    "- inline Checker contract",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生实现阶段",
    "status: native_parity_verified",
    "cotend-codex-r000008",
    "Full 与 Adaptive",
    "15 类行为场景",
    "7 处、6 个文件",
    "Verification Pass",
    "TD07",
)


class NativeImplementationPassError(ValueError):
    pass


@dataclass(frozen=True)
class ImplementationResult:
    profile: str
    execution_shape: str
    status: str
    blocking_reason: str
    implementation_started: bool
    writes_performed: bool
    test_action: str
    resume_action: str
    checker_handoff: str
    idempotent_noop: bool
    changed_paths_within_ownership: bool
    unrelated_files_preserved: bool
    external_framework_owner: bool
    scope_expanded: bool
    route_changed: bool
    formal_checker_claimed: bool
    formal_review_claimed: bool
    user_acceptance_claimed: bool
    release_authorized: bool
    evidence_fields: tuple[str, ...]


def _result(
    *,
    profile: Profile,
    status: str,
    blocking_reason: str,
    implementation_started: bool = False,
    writes_performed: bool = False,
    test_action: str = "not_run",
    resume_action: str = "not_needed",
    checker_handoff: str = "not_ready",
    idempotent_noop: bool = False,
) -> ImplementationResult:
    return ImplementationResult(
        profile=profile,
        execution_shape=(
            "delegated_implementer" if profile == "full" else "primary_inline"
        ),
        status=status,
        blocking_reason=blocking_reason,
        implementation_started=implementation_started,
        writes_performed=writes_performed,
        test_action=test_action,
        resume_action=resume_action,
        checker_handoff=checker_handoff,
        idempotent_noop=idempotent_noop,
        changed_paths_within_ownership=True,
        unrelated_files_preserved=True,
        external_framework_owner=False,
        scope_expanded=False,
        route_changed=False,
        formal_checker_claimed=False,
        formal_review_claimed=False,
        user_acceptance_claimed=False,
        release_authorized=False,
        evidence_fields=(
            "changed_or_inspected_paths",
            "commands_and_results",
            "evidence_pointers",
            "residual_risks_or_questions",
        ),
    )


def evaluate_implementation(
    *,
    profile: Profile = "full",
    active_leaf: str = "authorized-leaf",
    authorized: bool = True,
    protected_semantics_current: bool = True,
    pending_human_decision: bool = False,
    dependencies_ready: bool = True,
    ownership_clear: bool = True,
    scope_within_leaf: bool = True,
    risk_allowed: bool = True,
    allowed_paths: tuple[str, ...] = ("src/feature.py",),
    acceptance: tuple[str, ...] = ("declared behavior passes",),
    integration_owner: str = "root_primary",
    test_state: TestState = "pass",
    resume_state: ResumeState = "fresh",
) -> ImplementationResult:
    if profile not in {"full", "adaptive"}:
        raise NativeImplementationPassError("unsupported runtime profile")
    if test_state not in {"pass", "fail_fixable", "fail_unfixable"}:
        raise NativeImplementationPassError("unsupported test state")
    if resume_state not in {
        "fresh",
        "safe_checkpoint",
        "drifted",
        "ambiguous_side_effect",
        "closed_current",
    }:
        raise NativeImplementationPassError("unsupported resume state")
    if not active_leaf.strip():
        raise NativeImplementationPassError("active leaf is required")
    if not allowed_paths or any(not item.strip() for item in allowed_paths):
        raise NativeImplementationPassError("write ownership is required")
    if not acceptance or any(not item.strip() for item in acceptance):
        raise NativeImplementationPassError("acceptance is required")
    if not integration_owner.strip():
        raise NativeImplementationPassError("integration owner is required")

    if resume_state == "closed_current":
        return _result(
            profile=profile,
            status="closed",
            blocking_reason="none",
            checker_handoff="required",
            idempotent_noop=True,
            resume_action="return_existing_current_result",
        )
    if resume_state == "ambiguous_side_effect":
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="ambiguous_side_effect_requires_reconciliation",
            resume_action="stop_before_retry",
        )
    if not authorized:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="active_leaf_not_authorized",
        )
    if pending_human_decision:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="pending_human_decision",
        )
    if not protected_semantics_current:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="protected_semantics_not_current",
        )
    if not dependencies_ready:
        return _result(
            profile=profile,
            status="dependency_waiting",
            blocking_reason="implementation_dependency_unresolved",
        )
    if not ownership_clear:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="write_ownership_overlap",
        )
    if not scope_within_leaf:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="scope_expansion_requires_root_disposition",
        )
    if not risk_allowed:
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="critical_risk_requires_user",
        )

    resume_action = {
        "fresh": "start_from_bound_leaf",
        "safe_checkpoint": "continue_from_verified_checkpoint",
        "drifted": "revalidate_then_implement",
    }[resume_state]
    if test_state == "fail_unfixable":
        return _result(
            profile=profile,
            status="blocked",
            blocking_reason="test_failure_outside_current_fix_boundary",
            implementation_started=True,
            writes_performed=True,
            test_action="record_failure_and_stop",
            resume_action=resume_action,
        )
    if test_state == "fail_fixable":
        test_action = "fix_in_scope_retest_and_record"
    else:
        test_action = "run_and_record_pass"
    return _result(
        profile=profile,
        status="integration_waiting",
        blocking_reason="none",
        implementation_started=True,
        writes_performed=True,
        test_action=test_action,
        resume_action=resume_action,
        checker_handoff="required",
    )


SCENARIOS = {
    "full_success": {
        "kwargs": {"profile": "full"},
        "expected": {"status": "integration_waiting", "checker_handoff": "required"},
    },
    "adaptive_success": {
        "kwargs": {"profile": "adaptive"},
        "expected": {"status": "integration_waiting", "checker_handoff": "required"},
    },
    "unauthorized_leaf": {
        "kwargs": {"authorized": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "pending_human_decision": {
        "kwargs": {"pending_human_decision": True},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "semantic_conflict": {
        "kwargs": {"protected_semantics_current": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "dependency_wait": {
        "kwargs": {"dependencies_ready": False},
        "expected": {"status": "dependency_waiting", "writes_performed": False},
    },
    "ownership_overlap": {
        "kwargs": {"ownership_clear": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "scope_violation": {
        "kwargs": {"scope_within_leaf": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "critical_risk": {
        "kwargs": {"risk_allowed": False},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "fixable_test_failure": {
        "kwargs": {"test_state": "fail_fixable"},
        "expected": {
            "status": "integration_waiting",
            "test_action": "fix_in_scope_retest_and_record",
        },
    },
    "unfixable_test_failure": {
        "kwargs": {"test_state": "fail_unfixable"},
        "expected": {"status": "blocked", "checker_handoff": "not_ready"},
    },
    "safe_checkpoint_resume": {
        "kwargs": {"resume_state": "safe_checkpoint"},
        "expected": {"resume_action": "continue_from_verified_checkpoint"},
    },
    "drifted_resume_revalidates": {
        "kwargs": {"resume_state": "drifted"},
        "expected": {"resume_action": "revalidate_then_implement"},
    },
    "ambiguous_side_effect_stops": {
        "kwargs": {"resume_state": "ambiguous_side_effect"},
        "expected": {"status": "blocked", "writes_performed": False},
    },
    "closed_current_idempotent": {
        "kwargs": {"resume_state": "closed_current"},
        "expected": {"status": "closed", "idempotent_noop": True},
    },
}


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise NativeImplementationPassError(f"{label} is missing: {marker}")


def runtime_inventory(root: Path = ROOT) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for path in sorted((root / "skills").rglob("*")):
        if not path.is_file():
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
        raise NativeImplementationPassError(str(exc)) from exc
    texts = {
        "implementation": (root / IMPLEMENTATION_PASS_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "collaboration": (root / COLLABORATION_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "runtime": (root / RUNTIME_PROFILES_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "orchestration": (root / ORCHESTRATION_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "project_init": project_init,
        "model_upgrade": (root / MODEL_UPGRADE_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "model_packet": (root / MODEL_PACKET_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "document": (root / DOCUMENT_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        "evidence": (root / EVIDENCE_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
    }
    _require_markers(texts["implementation"], REQUIRED_IMPLEMENTATION_MARKERS, "implementation contract")
    _require_markers(texts["collaboration"], REQUIRED_COLLABORATION_MARKERS, "collaboration Skill")
    _require_markers(texts["runtime"], REQUIRED_RUNTIME_MARKERS, "runtime profiles")
    _require_markers(texts["orchestration"], REQUIRED_ORCHESTRATION_MARKERS, "native orchestration")
    _require_markers(texts["project_init"], REQUIRED_PROJECT_INIT_MARKERS, "Project Init")
    _require_markers(texts["model_upgrade"], REQUIRED_MODEL_MARKERS, "Model Upgrade")
    _require_markers(texts["model_packet"], REQUIRED_MODEL_PACKET_MARKERS, "Model Upgrade packet")
    _require_markers(texts["document"], REQUIRED_DOCUMENT_MARKERS, "public contract")

    skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
    )
    if REMOVED_TD04_COMMAND in skill_text.lower():
        raise NativeImplementationPassError("TD04 compatibility command remains")
    for command in REQUIRED_REMAINING_COMMANDS:
        if command not in skill_text.lower():
            raise NativeImplementationPassError(f"required later command missing: {command}")
    if (root / "skills" / "cotend-implement").exists():
        raise NativeImplementationPassError("a user-visible cotend-implement Skill was created")
    for pattern in (r"\$cotend-implement\b", r"/cotend-implement\b", r"name:\s*cotend-implement\b"):
        if re.search(pattern, skill_text, re.IGNORECASE):
            raise NativeImplementationPassError("a public cotend-implement invocation was created")

    inventory = runtime_inventory(root)
    if sum(inventory.values()) != EXPECTED_TRELLIS_MENTIONS or len(inventory) != EXPECTED_TRELLIS_FILES:
        raise NativeImplementationPassError("exact TD04 runtime Trellis inventory drifted")

    lock = json.loads((root / "delivery" / "codex-artifact.lock.json").read_text(encoding="utf-8"))
    target = lock.get("target", {})
    predecessors = lock.get("predecessor_targets", [])
    files, digest = skill_manifest(root)
    if (
        target.get("artifact_id") != "cotend-codex-r000015"
        or target.get("revision") != 15
        or target.get("manifest_sha256") != digest
        or lock.get("skill_count") != 9
        or lock.get("skill_file_count") != EXPECTED_SKILL_FILES
    ):
        raise NativeImplementationPassError("current target identity or manifest drifted")
    if not predecessors or predecessors[0] != {
        "platform": "Codex",
        "lineage": "cotend-codex",
        "artifact_id": "cotend-codex-r000014",
        "revision": 14,
        "source_release_id": "exact-source:9e6bbeeb4b91f98406e60dcbced923b3e1dd6826",
        "framework_protocol": "cotend-collaboration-v1.71",
        "manifest_sha256": EXPECTED_R14_MANIFEST,
    }:
        raise NativeImplementationPassError("r14 predecessor identity drifted")
    if len(files) != EXPECTED_SKILL_FILES:
        raise NativeImplementationPassError("current Skill file inventory drifted")
    _require_markers(
        texts["evidence"],
        (
            "current_target_artifact_id: cotend-codex-r000008",
            "current_target_revision: 8",
            f"current_target_manifest_sha256: {EXPECTED_R8_MANIFEST}",
            "predecessor_target_artifact_id: cotend-codex-r000007",
            f"predecessor_target_manifest_sha256: {EXPECTED_R7_MANIFEST}",
            "runtime_trellis_inventory: 28_mentions_15_files",
            "TD04-implementation-pass",
        ),
        "target evidence",
    )

    scenario_results: dict[str, dict[str, object]] = {}
    for scenario_id, contract in SCENARIOS.items():
        result = evaluate_implementation(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeImplementationPassError(
                    f"implementation scenario drifted: {scenario_id}.{key}"
                )
        if (
            not result.changed_paths_within_ownership
            or not result.unrelated_files_preserved
            or result.external_framework_owner
            or result.scope_expanded
            or result.route_changed
            or result.formal_checker_claimed
            or result.formal_review_claimed
            or result.user_acceptance_claimed
            or result.release_authorized
        ):
            raise NativeImplementationPassError(
                f"implementation authority invariant failed: {scenario_id}"
            )
        scenario_results[scenario_id] = payload

    full = evaluate_implementation(profile="full")
    adaptive = evaluate_implementation(profile="adaptive")
    parity_fields = (
        "status",
        "blocking_reason",
        "writes_performed",
        "test_action",
        "checker_handoff",
        "evidence_fields",
    )
    if any(getattr(full, field) != getattr(adaptive, field) for field in parity_fields):
        raise NativeImplementationPassError("Full and Adaptive result contracts diverged")

    return {
        "status": "native_parity_verified",
        "capability": "TD04-implementation-pass",
        "scenario_count": len(scenario_results),
        "scenarios": scenario_results,
        "runtime_mentions": sum(inventory.values()),
        "runtime_files": len(inventory),
        "td04_commands": 0,
        "remaining_commands": len(REQUIRED_REMAINING_COMMANDS),
        "skill_files": len(files),
        "target_artifact": target.get("artifact_id"),
        "target_manifest": digest,
        "full_adaptive_result_parity": True,
        "external_framework_owner": False,
        "formal_checker_claimed": False,
        "unrelated_files_preserved": True,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, json.JSONDecodeError, NativeImplementationPassError) as exc:
        print("NATIVE_IMPLEMENTATION_PASS_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_IMPLEMENTATION_PASS_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        f"runtime_mentions={result['runtime_mentions']} "
        f"runtime_files={result['runtime_files']} td04_commands=0 "
        f"remaining_commands={result['remaining_commands']} "
        f"target={result['target_artifact']}"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
