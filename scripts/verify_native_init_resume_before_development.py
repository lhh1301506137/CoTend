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
PROJECT_INIT_PATH = ROOT / "skills" / "cotend-project-init" / "SKILL.md"
INIT_PATH = ROOT / "skills" / "cotend-init" / "SKILL.md"
COLLABORATION_PATH = ROOT / "skills" / "cotend-collaboration" / "SKILL.md"
CODE_CONTEXT_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "code-context-harness.md"
)
RUNTIME_PROFILES_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "runtime-profiles.md"
)
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-INIT-RESUME-BEFORE-DEVELOPMENT.md"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "evidence"
    / "NATIVE-INIT-RESUME-BEFORE-DEVELOPMENT-TARGET-R7.md"
)
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"

NativeState = Literal["absent", "current", "dormant", "conflict"]
CompositeRequest = Literal["none", "writable_semantic", "read_only_semantic"]
ProviderState = Literal[
    "codegraph_fresh",
    "codegraph_unindexed",
    "codegraph_stale",
    "codegraph_missing",
    "codegraph_unavailable",
    "none",
]

LOAD_ORDER = (
    "current_truth",
    "active_leaf_and_route",
    "requirements_acceptance_and_risk",
    "code_context_provider_and_impact",
    "actual_file_verification",
)
REMOVED_TD02_COMMANDS = ("trellis-start", "trellis-before-dev")
REQUIRED_REMAINING_COMMANDS: tuple[str, ...] = ()
EXPECTED_TRELLIS_MENTIONS = 0
EXPECTED_TRELLIS_FILES = 0
EXPECTED_PROJECT_INIT_TRELLIS_MENTIONS = 0

REQUIRED_PROJECT_INIT_MARKERS = (
    "## Native Initialization And Resume Boundary",
    "classify exactly one Auto Mode;",
    "report readiness and return control exactly once.",
    "a second run with unchanged inputs",
    "must produce no diff.",
    "Do not start product implementation in the same response",
    "The native pre-development readiness gate",
    "current CoTend truth -> active leaf and route -> requirements/acceptance/risk -> code-context provider and impact set -> direct file verification",
)
REQUIRED_CODE_CONTEXT_MARKERS = (
    "## Native Pre-Development Readiness Gate",
    "Initialization may prepare the provider or index, but it cannot satisfy the explicit Init handback",
    "read current CoTend truth first",
    "A generic `continue` never clears a specialized decision.",
    "current_truth_loaded_before_code_context: true | false",
    "external_framework_owner: false",
    "project_truth_modified: false",
)
REQUIRED_INIT_MARKERS = (
    "After this Skill has returned control",
    "does not authorize same-response implementation",
)
REQUIRED_COLLABORATION_MARKERS = (
    "After an explicit Init handback is satisfied",
    "pass native pre-development readiness before broad edits",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生初始化、续接与开发前门",
    "cotend-codex-r000007",
    "入口侧共 13 类场景",
    "开发前侧共 9 类场景",
    "7 处、6 个文件",
    "TD07 已由 Native Closeout Pass 承接",
)
REQUIRED_EVIDENCE_MARKERS = (
    "current_target_artifact_id: cotend-codex-r000007",
    "current_target_revision: 7",
    "predecessor_target_artifact_id: cotend-codex-r000006",
    "predecessor_target_revision: 6",
    "predecessor_target_manifest_sha256: 58410dbbf9ab0945af62cea0583938c5f5bc733634a72035c5b06e6c71073271",
    "runtime_trellis_inventory: 38_mentions_16_files",
)


class NativeProjectEntryError(ValueError):
    pass


@dataclass(frozen=True)
class EntryResult:
    auto_mode: str
    workflow_state: str
    write_actions: tuple[str, ...]
    write_performed: bool
    readiness: str
    handback: str
    same_response_product_work_started: bool
    bare_continue_allowed: bool
    specialized_decision_preserved: bool
    external_framework_owner: bool = False
    user_truth_preserved: bool = True
    unrelated_files_preserved: bool = True


@dataclass(frozen=True)
class PreDevelopmentResult:
    status: str
    blocking_reason: str
    load_order: tuple[str, ...]
    provider: str
    provider_action: str
    generated_index_write: bool
    broad_edits_allowed: bool
    truth_loaded_before_code_context: bool
    scope_signature: str
    project_truth_modified: bool = False
    external_framework_owner: bool = False
    scope_expanded: bool = False


def evaluate_entry(
    native_state: NativeState,
    *,
    legacy_protocol: bool = False,
    repair_needed: bool = False,
    explicit_resume: bool = False,
    pending_specialized_decision: bool = False,
    external_route_conflict: bool = False,
    composite_request: CompositeRequest = "none",
    fresh_intake: bool = False,
    baseline_requires_alignment: bool = False,
) -> EntryResult:
    if explicit_resume and native_state != "dormant":
        raise NativeProjectEntryError("only a dormant native record can be resumed")
    if legacy_protocol and native_state == "absent":
        raise NativeProjectEntryError(
            "legacy update requires a durable legacy/native project carrier"
        )

    blocked_reason = ""
    if pending_specialized_decision:
        blocked_reason = "specialized_decision_required"
    elif native_state == "conflict":
        blocked_reason = "native_record_conflict"
    elif external_route_conflict:
        blocked_reason = "external_route_conflict"
    elif native_state == "dormant" and not explicit_resume:
        blocked_reason = "explicit_resume_required"

    if blocked_reason:
        return EntryResult(
            auto_mode="blocked_human_decision",
            workflow_state=native_state,
            write_actions=(),
            write_performed=False,
            readiness="human_needed",
            handback=blocked_reason,
            same_response_product_work_started=False,
            bare_continue_allowed=False,
            specialized_decision_preserved=True,
        )

    if native_state == "absent":
        auto_mode = "fresh_init"
        write_actions = (
            "materialize_native_record",
            "materialize_runtime_profile",
            "create_minimal_governance",
        )
    elif legacy_protocol:
        auto_mode = "legacy_update"
        write_actions = (
            "preserve_and_migrate_active_truth",
            "update_protocol_modules",
        )
    elif repair_needed:
        auto_mode = "partial_repair"
        write_actions = ("repair_safe_control_plane_drift",)
    else:
        auto_mode = "current_resume"
        write_actions = (
            ("resume_native_record",) if explicit_resume else ()
        )

    if composite_request == "writable_semantic":
        readiness = "human_needed"
        handback = "direct_cotend_semantic_alignment"
        bare_continue_allowed = False
    elif composite_request == "read_only_semantic":
        readiness = "human_needed"
        handback = "direct_cotend_diagnose_only"
        bare_continue_allowed = False
    elif (
        auto_mode == "fresh_init"
        and fresh_intake
        and baseline_requires_alignment
    ):
        readiness = "human_needed"
        handback = "semantic_onboarding_choice"
        bare_continue_allowed = False
    else:
        readiness = "continue_ready"
        handback = "resume_same_confirmed_route"
        bare_continue_allowed = True

    return EntryResult(
        auto_mode=auto_mode,
        workflow_state="current",
        write_actions=write_actions,
        write_performed=bool(write_actions),
        readiness=readiness,
        handback=handback,
        same_response_product_work_started=False,
        bare_continue_allowed=bare_continue_allowed,
        specialized_decision_preserved=not bare_continue_allowed,
    )


def _scope_signature(provider: str) -> str:
    payload = {
        "load_order": LOAD_ORDER,
        "provider": provider,
        "external_framework_owner": False,
    }
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def evaluate_predevelopment(
    *,
    init_handback_satisfied: bool = True,
    workflow_state: Literal["current", "dormant", "conflict"] = "current",
    specialized_decision_pending: bool = False,
    route_authorized: bool = True,
    current_truth_available: bool = True,
    active_leaf_available: bool = True,
    requirements_available: bool = True,
    acceptance_available: bool = True,
    risk_authorized: bool = True,
    canonical_root_clear: bool = True,
    provider_state: ProviderState = "codegraph_fresh",
    safe_index_write_allowed: bool = True,
    fallback_allowed: bool = True,
    broad_work_required: bool = True,
) -> PreDevelopmentResult:
    if not broad_work_required:
        return PreDevelopmentResult(
            status="not_required",
            blocking_reason="none",
            load_order=(),
            provider="none",
            provider_action="none",
            generated_index_write=False,
            broad_edits_allowed=True,
            truth_loaded_before_code_context=False,
            scope_signature=_scope_signature("none"),
        )

    blockers = (
        (not init_handback_satisfied, "init_handback_unsatisfied"),
        (workflow_state == "dormant", "workflow_dormant"),
        (workflow_state == "conflict", "workflow_conflict"),
        (specialized_decision_pending, "specialized_decision_required"),
        (not route_authorized, "route_not_authorized"),
        (not current_truth_available, "current_truth_missing"),
        (not active_leaf_available, "active_leaf_missing"),
        (not requirements_available, "requirements_missing"),
        (not acceptance_available, "acceptance_missing"),
        (not risk_authorized, "risk_not_authorized"),
        (not canonical_root_clear, "canonical_root_ambiguous"),
    )
    for blocked, reason in blockers:
        if blocked:
            return PreDevelopmentResult(
                status="blocked",
                blocking_reason=reason,
                load_order=LOAD_ORDER[:3],
                provider="none",
                provider_action="none",
                generated_index_write=False,
                broad_edits_allowed=False,
                truth_loaded_before_code_context=True,
                scope_signature=_scope_signature("blocked"),
            )

    provider = "codegraph"
    action = "inspect"
    generated_write = False
    if provider_state == "codegraph_unindexed":
        if safe_index_write_allowed:
            action = "initialize_index"
            generated_write = True
        elif fallback_allowed:
            provider = "rg_fallback"
            action = "record_fallback"
        else:
            provider = "none"
    elif provider_state == "codegraph_stale":
        if safe_index_write_allowed:
            action = "refresh_index"
            generated_write = True
        elif fallback_allowed:
            provider = "rg_fallback"
            action = "record_fallback"
        else:
            provider = "none"
    elif provider_state in {"codegraph_missing", "codegraph_unavailable", "none"}:
        if fallback_allowed:
            provider = "rg_fallback"
            action = "record_fallback"
        else:
            provider = "none"
            action = "none"

    if provider == "none":
        return PreDevelopmentResult(
            status="blocked",
            blocking_reason="code_context_unavailable",
            load_order=LOAD_ORDER[:3],
            provider="none",
            provider_action="none",
            generated_index_write=False,
            broad_edits_allowed=False,
            truth_loaded_before_code_context=True,
            scope_signature=_scope_signature("blocked"),
        )

    return PreDevelopmentResult(
        status="ready",
        blocking_reason="none",
        load_order=LOAD_ORDER,
        provider=provider,
        provider_action=action,
        generated_index_write=generated_write,
        broad_edits_allowed=True,
        truth_loaded_before_code_context=True,
        scope_signature=_scope_signature(provider),
    )


ENTRY_SCENARIOS = {
    "fresh_init": {
        "kwargs": {"native_state": "absent"},
        "expected": {"auto_mode": "fresh_init", "write_performed": True},
    },
    "legacy_update": {
        "kwargs": {"native_state": "current", "legacy_protocol": True},
        "expected": {"auto_mode": "legacy_update", "write_performed": True},
    },
    "partial_repair": {
        "kwargs": {"native_state": "current", "repair_needed": True},
        "expected": {"auto_mode": "partial_repair", "write_performed": True},
    },
    "current_resume": {
        "kwargs": {"native_state": "current"},
        "expected": {"auto_mode": "current_resume", "write_performed": False},
    },
    "dormant_stops": {
        "kwargs": {"native_state": "dormant"},
        "expected": {
            "auto_mode": "blocked_human_decision",
            "bare_continue_allowed": False,
        },
    },
    "dormant_explicit_resume": {
        "kwargs": {"native_state": "dormant", "explicit_resume": True},
        "expected": {
            "auto_mode": "current_resume",
            "workflow_state": "current",
            "write_performed": True,
        },
    },
    "native_conflict_stops": {
        "kwargs": {"native_state": "conflict"},
        "expected": {"handback": "native_record_conflict"},
    },
    "external_route_conflict_stops": {
        "kwargs": {
            "native_state": "current",
            "external_route_conflict": True,
        },
        "expected": {"handback": "external_route_conflict"},
    },
    "specialized_decision_stops": {
        "kwargs": {
            "native_state": "current",
            "pending_specialized_decision": True,
        },
        "expected": {
            "handback": "specialized_decision_required",
            "bare_continue_allowed": False,
        },
    },
    "composite_writable_handoff": {
        "kwargs": {
            "native_state": "current",
            "composite_request": "writable_semantic",
        },
        "expected": {"handback": "direct_cotend_semantic_alignment"},
    },
    "composite_read_only_handoff": {
        "kwargs": {
            "native_state": "current",
            "composite_request": "read_only_semantic",
        },
        "expected": {"handback": "direct_cotend_diagnose_only"},
    },
    "fresh_intake_handoff": {
        "kwargs": {
            "native_state": "absent",
            "fresh_intake": True,
            "baseline_requires_alignment": True,
        },
        "expected": {"handback": "semantic_onboarding_choice"},
    },
    "same_confirmed_route_handback": {
        "kwargs": {"native_state": "current"},
        "expected": {
            "handback": "resume_same_confirmed_route",
            "bare_continue_allowed": True,
            "same_response_product_work_started": False,
        },
    },
}

PREDEVELOPMENT_SCENARIOS = {
    "fresh_codegraph_ready": {
        "kwargs": {},
        "expected": {"status": "ready", "provider": "codegraph"},
    },
    "unindexed_codegraph_initializes": {
        "kwargs": {"provider_state": "codegraph_unindexed"},
        "expected": {
            "status": "ready",
            "provider_action": "initialize_index",
            "generated_index_write": True,
        },
    },
    "stale_codegraph_refreshes": {
        "kwargs": {"provider_state": "codegraph_stale"},
        "expected": {"provider_action": "refresh_index"},
    },
    "missing_codegraph_records_fallback": {
        "kwargs": {"provider_state": "codegraph_missing"},
        "expected": {
            "status": "ready",
            "provider": "rg_fallback",
            "provider_action": "record_fallback",
        },
    },
    "ambiguous_root_stops": {
        "kwargs": {"canonical_root_clear": False},
        "expected": {
            "status": "blocked",
            "blocking_reason": "canonical_root_ambiguous",
        },
    },
    "unsatisfied_init_handback_stops": {
        "kwargs": {"init_handback_satisfied": False},
        "expected": {
            "status": "blocked",
            "blocking_reason": "init_handback_unsatisfied",
        },
    },
    "specialized_decision_stops": {
        "kwargs": {"specialized_decision_pending": True},
        "expected": {
            "status": "blocked",
            "blocking_reason": "specialized_decision_required",
        },
    },
    "missing_acceptance_stops": {
        "kwargs": {"acceptance_available": False},
        "expected": {
            "status": "blocked",
            "blocking_reason": "acceptance_missing",
        },
    },
    "tiny_bounded_work_skips_broad_gate": {
        "kwargs": {"broad_work_required": False},
        "expected": {"status": "not_required", "provider": "none"},
    },
}


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise NativeProjectEntryError(f"{label} is missing: {marker}")


def trellis_inventory(root: Path = ROOT) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for path in sorted((root / "skills").rglob("*")):
        if not path.is_file():
            continue
        count = len(re.findall("trellis", path.read_text(encoding="utf-8"), re.I))
        if count:
            inventory[path.relative_to(root).as_posix()] = count
    return inventory


def verify_repository(root: Path = ROOT) -> dict[str, object]:
    try:
        project_init = project_init_contract.load_project_init_contract(root)[
            "combined"
        ]
    except project_init_contract.ProjectInitContractError as exc:
        raise NativeProjectEntryError(str(exc)) from exc
    init = (root / "skills" / "cotend-init" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    collaboration = (
        root / "skills" / "cotend-collaboration" / "SKILL.md"
    ).read_text(encoding="utf-8")
    code_context = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "code-context-harness.md"
    ).read_text(encoding="utf-8")
    runtime_profiles = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "runtime-profiles.md"
    ).read_text(encoding="utf-8")
    document = (
        root / "docs" / "NATIVE-INIT-RESUME-BEFORE-DEVELOPMENT.md"
    ).read_text(encoding="utf-8")
    evidence = (
        root
        / "docs"
        / "evidence"
        / "NATIVE-INIT-RESUME-BEFORE-DEVELOPMENT-TARGET-R7.md"
    ).read_text(encoding="utf-8")

    _require_markers(
        project_init,
        REQUIRED_PROJECT_INIT_MARKERS,
        "Project Init",
    )
    _require_markers(
        code_context,
        REQUIRED_CODE_CONTEXT_MARKERS,
        "Code Context Harness",
    )
    _require_markers(init, REQUIRED_INIT_MARKERS, "Init")
    _require_markers(
        collaboration,
        REQUIRED_COLLABORATION_MARKERS,
        "Collaboration core",
    )
    _require_markers(document, REQUIRED_DOCUMENT_MARKERS, "public contract")
    _require_markers(evidence, REQUIRED_EVIDENCE_MARKERS, "target evidence")

    combined_skills = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
    )
    for command in REMOVED_TD02_COMMANDS:
        if command in combined_skills:
            raise NativeProjectEntryError(
                f"TD02 compatibility command remains: {command}"
            )
    _require_markers(combined_skills, REQUIRED_REMAINING_COMMANDS, "remaining routes")
    if "capability: startup | pre_development" in runtime_profiles:
        raise NativeProjectEntryError(
            "native record still exposes TD02 compatibility capabilities"
        )
    if "capability: closeout" in runtime_profiles:
        raise NativeProjectEntryError(
            "obsolete closeout compatibility capability remains"
        )

    inventory = trellis_inventory(root)
    if (
        sum(inventory.values()) != EXPECTED_TRELLIS_MENTIONS
        or len(inventory) != EXPECTED_TRELLIS_FILES
        or inventory.get("skills/cotend-project-init/SKILL.md", 0)
        != EXPECTED_PROJECT_INIT_TRELLIS_MENTIONS
    ):
        raise NativeProjectEntryError(
            "current runtime inventory is not the zero-dependency checkpoint"
        )

    entry_results: dict[str, dict[str, object]] = {}
    for scenario_id, contract in ENTRY_SCENARIOS.items():
        result = evaluate_entry(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeProjectEntryError(
                    f"entry scenario drifted: {scenario_id}.{key}"
                )
        if (
            result.same_response_product_work_started
            or result.external_framework_owner
            or not result.user_truth_preserved
            or not result.unrelated_files_preserved
        ):
            raise NativeProjectEntryError(
                f"entry invariant failed: {scenario_id}"
            )
        entry_results[scenario_id] = payload

    first = evaluate_entry("absent")
    second = evaluate_entry("current")
    if not first.write_performed or second.write_performed:
        raise NativeProjectEntryError("repeated initialization is not idempotent")

    predevelopment_results: dict[str, dict[str, object]] = {}
    for scenario_id, contract in PREDEVELOPMENT_SCENARIOS.items():
        result = evaluate_predevelopment(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeProjectEntryError(
                    f"pre-development scenario drifted: {scenario_id}.{key}"
                )
        if (
            result.project_truth_modified
            or result.external_framework_owner
            or result.scope_expanded
        ):
            raise NativeProjectEntryError(
                f"pre-development invariant failed: {scenario_id}"
            )
        if result.status == "ready" and result.load_order != LOAD_ORDER:
            raise NativeProjectEntryError(
                f"pre-development load order drifted: {scenario_id}"
            )
        predevelopment_results[scenario_id] = payload

    first_context = evaluate_predevelopment(
        provider_state="codegraph_unindexed"
    )
    repeated_context = evaluate_predevelopment(provider_state="codegraph_fresh")
    if (
        not first_context.generated_index_write
        or repeated_context.generated_index_write
        or first_context.scope_signature != repeated_context.scope_signature
    ):
        raise NativeProjectEntryError(
            "repeated pre-development readiness is not idempotent"
        )

    target_lock = json.loads(
        (root / "delivery" / "codex-artifact.lock.json").read_text(
            encoding="utf-8"
        )
    )
    target = target_lock.get("target", {})
    predecessors = target_lock.get("predecessor_targets", [])
    lineage = [target, *predecessors]
    r7 = next(
        (
            item
            for item in lineage
            if item.get("artifact_id") == "cotend-codex-r000007"
            and item.get("revision") == 7
        ),
        None,
    )
    if (
        not isinstance(target.get("revision"), int)
        or target.get("revision") < 7
        or r7 is None
        or r7.get("manifest_sha256")
        != "246b16c990a85a2e183e0033c0b3a15a087e793ce0ace1f18e3d736f5a8fd045"
    ):
        raise NativeProjectEntryError("verified r7 target lineage drifted")

    return {
        "status": "native_parity_verified",
        "entry_scenarios": entry_results,
        "predevelopment_scenarios": predevelopment_results,
        "runtime_mentions": sum(inventory.values()),
        "runtime_files": len(inventory),
        "td02_commands": 0,
        "remaining_commands": len(REQUIRED_REMAINING_COMMANDS),
        "target_artifact": target.get("artifact_id"),
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, json.JSONDecodeError, NativeProjectEntryError) as exc:
        print("NATIVE_INIT_RESUME_BEFORE_DEVELOPMENT_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_INIT_RESUME_BEFORE_DEVELOPMENT_OK "
        f"entry_scenarios={len(result['entry_scenarios'])} "
        f"predevelopment_scenarios={len(result['predevelopment_scenarios'])} "
        f"runtime_mentions={result['runtime_mentions']} "
        f"runtime_files={result['runtime_files']} td02_commands=0 "
        f"remaining_commands={result['remaining_commands']} "
        f"target={result['target_artifact']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
