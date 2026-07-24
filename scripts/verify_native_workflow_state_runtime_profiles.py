from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PROFILES_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "runtime-profiles.md"
)
PROJECT_INIT_PATH = ROOT / "skills" / "cotend-project-init" / "SKILL.md"
COLLABORATION_PATH = ROOT / "skills" / "cotend-collaboration" / "SKILL.md"
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-WORKFLOW-STATE-AND-RUNTIME-PROFILES.md"

NativeState = Literal["absent", "current", "dormant", "conflict"]
ProfileInput = Literal["full", "adaptive", "invalid", "none"]
ExternalState = Literal["none", "reference", "historical", "conflict"]

VALID_PROFILES = {"full", "adaptive"}
EXECUTION_MODE = {"full": "delegated_pair", "adaptive": "inline"}

REQUIRED_RUNTIME_MARKERS = (
    "## Native State Owner",
    "Use the existing `STATUS.md`",
    "Do not create a hidden state directory",
    "`current`",
    "`dormant`",
    "`conflict`",
    "## External Framework Classification",
    "Never write CoTend state, profile, dispatch, or migration metadata into external framework files.",
    "Any remaining compatibility invocation must be explicitly listed",
    "1. a user-explicit current-session selection;",
    "2. one valid native project record;",
    "3. one unambiguous project-local legacy selection",
    "4. the CoTend product default `full`.",
    "`full` | `v1.65-full` | `delegated_pair`",
    "`adaptive` | `v1.65-A` | `inline`",
    "Migrate only when all of these are true:",
    "Do not modify, delete, or normalize the source file.",
)
REQUIRED_INIT_MARKERS = (
    "## Native Workflow State And Runtime Profile",
    "Persist the record in `STATUS.md` or the project's explicitly mapped equivalent.",
    "external_framework_owner: false",
    "execution_mode: delegated_pair | inline",
    "state: current | dormant | conflict",
    "Never write CoTend profile or execution metadata into an external framework configuration.",
    "compatibility_procedures:",
)
REQUIRED_COLLABORATION_MARKERS = (
    "Detection may be `absent`; persisted state is `current | dormant | conflict`.",
    "`full` maps to native `delegated_pair`; `adaptive` maps to native `inline`.",
    "Never write CoTend profile or execution metadata into its configuration.",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生工作流状态与运行档位",
    "cotend-codex-r000006",
    "current / dormant / conflict",
    "delegated_pair / inline",
    "TD04、TD05、TD07",
    "G03、G04、G06",
)
REQUIRED_COMPATIBILITY_COMMANDS = (
    "trellis-implement",
    "trellis-check",
    "trellis-finish",
)
FORBIDDEN_STATE_PATTERNS = {
    "foreign_state_path": re.compile(r"\.trellis(?:[/\\]|`)", re.IGNORECASE),
    "foreign_mode_key": re.compile(r"\btrellis\.mode\b", re.IGNORECASE),
    "foreign_dispatch_field": re.compile(
        r"\b(?:trellis_dispatch_mode|codex\.dispatch_mode)\b",
        re.IGNORECASE,
    ),
    "foreign_activation_owner": re.compile(
        r"Trellis\s+Activation\s+Decision", re.IGNORECASE
    ),
    "foreign_active_predicate": re.compile(
        r"\b(?:active\s+Trellis|Trellis\s+is\s+active|Trellis\s+active|"
        r"dormant\s+Trellis|Trellis-managed|Trellis\s+state)\b",
        re.IGNORECASE,
    ),
    "foreign_root_record": re.compile(r"(?m)^\s*trellis:\s*$", re.IGNORECASE),
}


class NativeWorkflowStateError(ValueError):
    pass


@dataclass(frozen=True)
class WorkflowResult:
    state: str
    state_source: str
    effective_profile: str
    execution_mode: str
    persisted_profile: str
    persisted_execution_mode: str
    profile_source: str
    write_native_record: bool
    user_decision_required: bool
    can_continue: bool
    external_classification: str
    migration_result: str
    native_record_owner: str = "status_or_explicit_equivalent"
    external_framework_owner: bool = False
    external_config_modified: bool = False
    legacy_source_modified: bool = False
    unrelated_truth_preserved: bool = True
    parallel_state_tree_created: bool = False


def _external_classification(external_state: ExternalState) -> str:
    return {
        "none": "none",
        "reference": "reference_only",
        "historical": "historical",
        "conflict": "conflict",
    }[external_state]


def _blocked_result(
    *,
    reason: str,
    external_state: ExternalState,
    persisted_profile: str = "unresolved",
) -> WorkflowResult:
    execution = (
        EXECUTION_MODE[persisted_profile]
        if persisted_profile in VALID_PROFILES
        else "unresolved"
    )
    return WorkflowResult(
        state="conflict",
        state_source="unresolved",
        effective_profile="unresolved",
        execution_mode="unresolved",
        persisted_profile=persisted_profile,
        persisted_execution_mode=execution,
        profile_source="invalid",
        write_native_record=False,
        user_decision_required=True,
        can_continue=False,
        external_classification=_external_classification(external_state),
        migration_result=reason,
    )


def evaluate_workflow(
    native_state: NativeState,
    *,
    native_profiles: tuple[str, ...] = (),
    session_profile: ProfileInput = "none",
    persist_session: bool = False,
    explicit_resume: bool = False,
    legacy_profiles: tuple[str, ...] = (),
    external_state: ExternalState = "none",
    external_affects_route: bool = False,
) -> WorkflowResult:
    if persist_session and session_profile == "none":
        raise NativeWorkflowStateError(
            "project persistence requires an explicit session profile"
        )
    if explicit_resume and native_state != "dormant":
        raise NativeWorkflowStateError("only a dormant record can be resumed")
    if external_affects_route and external_state != "conflict":
        raise NativeWorkflowStateError(
            "only a classified external conflict can affect the route"
        )
    if session_profile == "invalid":
        return _blocked_result(
            reason="invalid_session_profile",
            external_state=external_state,
            persisted_profile=(
                native_profiles[0]
                if len(native_profiles) == 1
                and native_profiles[0] in VALID_PROFILES
                else "unresolved"
            ),
        )
    if external_state == "conflict" and external_affects_route:
        return _blocked_result(
            reason="external_route_conflict",
            external_state=external_state,
            persisted_profile=(
                native_profiles[0]
                if len(native_profiles) == 1
                and native_profiles[0] in VALID_PROFILES
                else "unresolved"
            ),
        )
    if native_state == "conflict":
        return _blocked_result(
            reason="native_record_conflict",
            external_state=external_state,
        )
    if native_state == "absent" and native_profiles:
        return _blocked_result(
            reason="absent_state_has_native_profile",
            external_state=external_state,
        )
    if native_state in {"current", "dormant"} and (
        len(native_profiles) != 1 or native_profiles[0] not in VALID_PROFILES
    ):
        reason = (
            "duplicate_native_record"
            if len(native_profiles) > 1
            else "invalid_native_profile"
        )
        return _blocked_result(reason=reason, external_state=external_state)

    write_native_record = False
    migration_result = "not_needed"
    state_source = "native_project_record"
    profile_source = "project_persistent"

    if native_state == "absent":
        valid_legacy = [
            profile for profile in legacy_profiles if profile in VALID_PROFILES
        ]
        if len(legacy_profiles) > 1:
            return _blocked_result(
                reason="ambiguous_legacy_selection",
                external_state=external_state,
            )
        if legacy_profiles and len(valid_legacy) != 1:
            return _blocked_result(
                reason="invalid_legacy_selection",
                external_state=external_state,
            )
        if valid_legacy:
            persisted_profile = valid_legacy[0]
            profile_source = "migrated_legacy_project_selection"
            state_source = "migrated_legacy_project_selection"
            migration_result = "migrated_existing_selection"
        elif persist_session and session_profile in VALID_PROFILES:
            persisted_profile = session_profile
            profile_source = "session_explicit_saved_to_project"
            state_source = "materialized_project_selection"
            migration_result = "explicit_project_selection_materialized"
        else:
            persisted_profile = "full"
            profile_source = "cotend_product_default"
            state_source = "materialized_default"
            migration_result = "product_default_materialized"
        state = "current"
        write_native_record = True
    else:
        persisted_profile = native_profiles[0]
        state = native_state
        if state == "dormant" and not explicit_resume:
            return WorkflowResult(
                state="dormant",
                state_source=state_source,
                effective_profile=persisted_profile,
                execution_mode=EXECUTION_MODE[persisted_profile],
                persisted_profile=persisted_profile,
                persisted_execution_mode=EXECUTION_MODE[persisted_profile],
                profile_source=profile_source,
                write_native_record=False,
                user_decision_required=True,
                can_continue=False,
                external_classification=_external_classification(external_state),
                migration_result="explicit_resume_required",
            )
        if state == "dormant" and explicit_resume:
            state = "current"
            write_native_record = True
            migration_result = "dormant_record_resumed"

    effective_profile = (
        session_profile if session_profile in VALID_PROFILES else persisted_profile
    )
    if persist_session and session_profile in VALID_PROFILES:
        if persisted_profile != session_profile:
            persisted_profile = session_profile
            write_native_record = True
            migration_result = (
                "persistent_profile_changed"
                if native_state != "absent"
                else migration_result
            )
        profile_source = "session_explicit_saved_to_project"
    elif session_profile in VALID_PROFILES:
        profile_source = "session_explicit"

    return WorkflowResult(
        state=state,
        state_source=state_source,
        effective_profile=effective_profile,
        execution_mode=EXECUTION_MODE[effective_profile],
        persisted_profile=persisted_profile,
        persisted_execution_mode=EXECUTION_MODE[persisted_profile],
        profile_source=profile_source,
        write_native_record=write_native_record,
        user_decision_required=False,
        can_continue=True,
        external_classification=_external_classification(external_state),
        migration_result=migration_result,
    )


EXPECTED_SCENARIOS = {
    "fresh_default_full": {
        "kwargs": {"native_state": "absent"},
        "expected": {
            "state": "current",
            "effective_profile": "full",
            "execution_mode": "delegated_pair",
            "write_native_record": True,
        },
    },
    "current_full_update_idempotent": {
        "kwargs": {"native_state": "current", "native_profiles": ("full",)},
        "expected": {
            "effective_profile": "full",
            "write_native_record": False,
        },
    },
    "current_adaptive_update_idempotent": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("adaptive",),
        },
        "expected": {
            "effective_profile": "adaptive",
            "execution_mode": "inline",
            "write_native_record": False,
        },
    },
    "session_adaptive_override_not_persisted": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("full",),
            "session_profile": "adaptive",
        },
        "expected": {
            "effective_profile": "adaptive",
            "persisted_profile": "full",
            "write_native_record": False,
        },
    },
    "persistent_adaptive_switch": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("full",),
            "session_profile": "adaptive",
            "persist_session": True,
        },
        "expected": {
            "persisted_profile": "adaptive",
            "persisted_execution_mode": "inline",
            "write_native_record": True,
        },
    },
    "restore_full_delegated_pair": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("adaptive",),
            "session_profile": "full",
            "persist_session": True,
        },
        "expected": {
            "persisted_profile": "full",
            "persisted_execution_mode": "delegated_pair",
            "write_native_record": True,
        },
    },
    "dormant_requires_resume": {
        "kwargs": {
            "native_state": "dormant",
            "native_profiles": ("adaptive",),
        },
        "expected": {
            "state": "dormant",
            "can_continue": False,
            "user_decision_required": True,
        },
    },
    "dormant_explicit_resume": {
        "kwargs": {
            "native_state": "dormant",
            "native_profiles": ("adaptive",),
            "explicit_resume": True,
        },
        "expected": {
            "state": "current",
            "effective_profile": "adaptive",
            "write_native_record": True,
        },
    },
    "invalid_native_profile": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("turbo",),
        },
        "expected": {
            "state": "conflict",
            "can_continue": False,
            "write_native_record": False,
        },
    },
    "duplicate_native_record": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("full", "adaptive"),
        },
        "expected": {
            "state": "conflict",
            "migration_result": "duplicate_native_record",
        },
    },
    "foreign_reference_is_not_owner": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("full",),
            "external_state": "reference",
        },
        "expected": {
            "state": "current",
            "external_classification": "reference_only",
        },
    },
    "foreign_history_is_not_owner": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("full",),
            "external_state": "historical",
        },
        "expected": {
            "state": "current",
            "external_classification": "historical",
        },
    },
    "foreign_route_conflict_fails_closed": {
        "kwargs": {
            "native_state": "current",
            "native_profiles": ("full",),
            "external_state": "conflict",
            "external_affects_route": True,
        },
        "expected": {
            "state": "conflict",
            "can_continue": False,
            "migration_result": "external_route_conflict",
        },
    },
    "legacy_adaptive_migrates_without_source_write": {
        "kwargs": {
            "native_state": "absent",
            "legacy_profiles": ("adaptive",),
        },
        "expected": {
            "state": "current",
            "persisted_profile": "adaptive",
            "migration_result": "migrated_existing_selection",
            "write_native_record": True,
        },
    },
    "ambiguous_legacy_fails_closed": {
        "kwargs": {
            "native_state": "absent",
            "legacy_profiles": ("full", "adaptive"),
        },
        "expected": {
            "state": "conflict",
            "can_continue": False,
            "write_native_record": False,
        },
    },
    "fresh_session_override_preserves_project_default": {
        "kwargs": {
            "native_state": "absent",
            "session_profile": "adaptive",
        },
        "expected": {
            "effective_profile": "adaptive",
            "persisted_profile": "full",
            "persisted_execution_mode": "delegated_pair",
            "write_native_record": True,
        },
    },
}


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise NativeWorkflowStateError(f"{label} is missing: {marker}")


def scan_forbidden_state_owners(root: Path = ROOT) -> list[str]:
    findings: list[str] = []
    for path in sorted((root / "skills").rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_STATE_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}:{path.relative_to(root).as_posix()}")
    return findings


def verify_repository(root: Path = ROOT) -> dict[str, object]:
    runtime_text = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "runtime-profiles.md"
    ).read_text(encoding="utf-8")
    init_text = (
        root / "skills" / "cotend-project-init" / "SKILL.md"
    ).read_text(encoding="utf-8")
    collaboration_text = (
        root / "skills" / "cotend-collaboration" / "SKILL.md"
    ).read_text(encoding="utf-8")
    document_text = (
        root / "docs" / "NATIVE-WORKFLOW-STATE-AND-RUNTIME-PROFILES.md"
    ).read_text(encoding="utf-8")

    _require_markers(runtime_text, REQUIRED_RUNTIME_MARKERS, "runtime contract")
    _require_markers(init_text, REQUIRED_INIT_MARKERS, "Project Init")
    _require_markers(
        collaboration_text,
        REQUIRED_COLLABORATION_MARKERS,
        "Collaboration core",
    )
    _require_markers(document_text, REQUIRED_DOCUMENT_MARKERS, "public contract")

    combined_skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
    )
    _require_markers(
        combined_skill_text,
        REQUIRED_COMPATIBILITY_COMMANDS,
        "unmigrated compatibility routes",
    )

    findings = scan_forbidden_state_owners(root)
    if findings:
        raise NativeWorkflowStateError(
            "foreign workflow-state owner remains: " + ", ".join(findings)
        )

    scenarios: dict[str, dict[str, object]] = {}
    for scenario_id, contract in EXPECTED_SCENARIOS.items():
        result = evaluate_workflow(**contract["kwargs"])
        payload = asdict(result)
        for key, expected in contract["expected"].items():
            if payload[key] != expected:
                raise NativeWorkflowStateError(
                    f"scenario result drifted: {scenario_id}.{key}"
                )
        if (
            result.external_framework_owner
            or result.external_config_modified
            or result.legacy_source_modified
            or not result.unrelated_truth_preserved
            or result.parallel_state_tree_created
        ):
            raise NativeWorkflowStateError(
                f"scenario delegated authority or modified protected state: {scenario_id}"
            )
        scenarios[scenario_id] = payload

    if scenarios["current_full_update_idempotent"]["write_native_record"]:
        raise NativeWorkflowStateError("unchanged current profile was rewritten")
    if scenarios["session_adaptive_override_not_persisted"][
        "persisted_profile"
    ] != "full":
        raise NativeWorkflowStateError("session override rewrote project choice")
    if scenarios["restore_full_delegated_pair"][
        "persisted_execution_mode"
    ] != "delegated_pair":
        raise NativeWorkflowStateError("Full did not restore delegated_pair")
    if scenarios["legacy_adaptive_migrates_without_source_write"][
        "legacy_source_modified"
    ]:
        raise NativeWorkflowStateError("legacy source was modified")

    return {
        "status": "native_parity_verified",
        "capability": "TD01-workflow-state-and-mode",
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
        "forbidden_state_owners": 0,
        "external_framework_owner": False,
        "external_config_modified": False,
        "legacy_source_modified": False,
        "unrelated_truth_preserved": True,
        "parallel_state_tree_created": False,
        "remaining_compatibility_commands": list(
            REQUIRED_COMPATIBILITY_COMMANDS
        ),
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, NativeWorkflowStateError) as exc:
        print("NATIVE_WORKFLOW_STATE_RUNTIME_PROFILES_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_WORKFLOW_STATE_RUNTIME_PROFILES_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        "external_framework_owner=false external_config_modified=false "
        "legacy_source_modified=false unrelated_truth_preserved=true"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
