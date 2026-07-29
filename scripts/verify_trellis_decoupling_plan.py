from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import verify_native_project_truth_authority as native_authority
import verify_native_requirements_clarification as native_clarification
import verify_native_spec_change_route_rebase as native_route_rebase
import verify_native_workflow_state_runtime_profiles as native_workflow_state
import verify_native_init_resume_before_development as native_project_entry
import verify_native_implementation_pass as native_implementation
import verify_native_verification_pass as native_verification
import verify_native_closeout_pass as native_closeout
import verify_native_cumulative_main_journey as native_cumulative_journey
import verify_native_negative_recovery_ownership as native_negative_recovery


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
DOCUMENT_PATH = ROOT / "docs" / "TRELLIS-DECOUPLING-PARITY-PLAN.md"
G06_EVIDENCE_PATH = (
    ROOT / "docs" / "evidence" / "NATIVE-REAL-PROJECT-ACCEPTANCE-G06.md"
)
EXPECTED_CAPABILITY_IDS = [
    "TD01-workflow-state-and-mode",
    "TD02-init-resume-and-before-development",
    "TD03-requirements-clarification",
    "TD04-implementation-pass",
    "TD05-verification-pass",
    "TD06-spec-change-and-route-rebase",
    "TD07-closeout-archive-and-recovery",
    "TD08-project-truth-authority",
]
EXPECTED_REPLACEMENT_ORDER = [
    "TD08-project-truth-authority",
    "TD03-requirements-clarification",
    "TD06-spec-change-and-route-rebase",
    "TD01-workflow-state-and-mode",
    "TD02-init-resume-and-before-development",
    "TD04-implementation-pass",
    "TD05-verification-pass",
    "TD07-closeout-archive-and-recovery",
]
EXPECTED_GATE_IDS = [
    "G01-baseline-freeze",
    "G02-per-capability-native-parity",
    "G03-cumulative-main-journey",
    "G04-negative-recovery-and-ownership",
    "G05-zero-runtime-dependency",
    "G06-real-project-and-rollback",
]
EXPECTED_DOCUMENT_MARKERS = [
    "# CoTend 原生工作流与 Trellis 解耦等价计划",
    "不是已经复制 Trellis 源码",
    "## 八类能力等价矩阵",
    "## 为什么先替换权限，再替换命令",
    "### G01 基线冻结",
    "### L62 / TD08 已完成",
    "### L63 / TD03 已完成",
    "### L64 / TD06 已完成",
    "### L65 / TD01 已完成",
    "### L66 / TD02 已完成",
    "### L67 / TD04 已完成",
    "### L68 / TD05 已完成",
    "### L69 / TD07 已完成",
    "### L70 / G03 已完成",
    "### L71 / G04 已完成",
    "### L72 / G05 已完成",
    "### L73 / G06 已完成",
    "G04 不修改 Skill 字节",
    "G05 不构建 rc.3",
    "G06 不构建 rc.3",
]
EXPECTED_G06_EVIDENCE_MARKERS = [
    "# CoTend G06 Real-Project Acceptance Evidence",
    "gate: G06-real-project-and-rollback",
    "status: complete",
    "framework_protocol: cotend-collaboration-v1.67",
    "development_target_artifact: cotend-codex-r000013",
    "development_target_manifest: 39e1455b11f482d80d33dff421e0db5c08182f597c175f0391bd679750f903fd",
    "predecessor_target_artifact: cotend-codex-r000012",
    "predecessor_target_manifest: 44419b00c17ab0036477c6c3b9843f239a6a567ee714ccf7828b40a4af195276",
    "retained_project_journey: passed",
    "real_writable_product: passed",
    "independent_checker: passed",
    "formal_product_review: passed",
    "ai_uat: pass_with_control_plane_notes",
    "rollback_restore: passed_r13_to_r12_to_r13",
    "pre_acceptance_fresh_session: passed_with_control_plane_note",
    "user_acceptance: maintainer_explicitly_accepted",
    "post_acceptance_fresh_session: passed",
    "development_reopened_after_acceptance: false",
    "runtime_skill_change_in_g06: false",
    "rc3_built: false",
    "public_action: false",
]
EXPECTED_BASELINE_INVENTORY_SHA256 = (
    "a1c9893a7462d7abd925b1ae468a3dd97366fae850e2881a23546e5471e93aeb"
)
EXPECTED_CURRENT_INVENTORY_SHA256 = (
    "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
)
AUTHORIZED_TD08_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/SKILL.md",
    "skills/cotend-collaboration/references/code-context-harness.md",
    "skills/cotend-collaboration/references/framework-change-evaluation.md",
    "skills/cotend-collaboration/references/idea-to-consensus.md",
    "skills/cotend-collaboration/references/native-agent-orchestration.md",
    "skills/cotend-collaboration/references/plan-tree.md",
    "skills/cotend-project-init/SKILL.md",
    "skills/cotend-semantic-alignment/SKILL.md",
}
AUTHORIZED_TD03_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/references/authority-and-triggers.md",
    "skills/cotend-collaboration/references/decision-log.md",
    "skills/cotend-collaboration/references/plan-tree.md",
    "skills/cotend-project-init/SKILL.md",
}
AUTHORIZED_TD06_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/references/decision-log.md",
    "skills/cotend-collaboration/references/semantic-implementation-closure.md",
    "skills/cotend-collaboration/references/templates.md",
    "skills/cotend-project-init/SKILL.md",
}
AUTHORIZED_TD01_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/SKILL.md",
    "skills/cotend-collaboration/agents/openai.yaml",
    "skills/cotend-collaboration/references/acceptance-test-harness.md",
    "skills/cotend-collaboration/references/code-context-harness.md",
    "skills/cotend-collaboration/references/continuous-and-unattended.md",
    "skills/cotend-collaboration/references/framework-change-evaluation.md",
    "skills/cotend-collaboration/references/native-agent-orchestration.md",
    "skills/cotend-collaboration/references/plan-tree.md",
    "skills/cotend-collaboration/references/quality-sentinel.md",
    "skills/cotend-collaboration/references/runtime-profiles.md",
    "skills/cotend-collaboration/references/semantic-implementation-closure.md",
    "skills/cotend-collaboration/references/upstream-dependency-review.md",
    "skills/cotend-init/SKILL.md",
    "skills/cotend-model-upgrade/SKILL.md",
    "skills/cotend-project-init/SKILL.md",
}
AUTHORIZED_TD02_INVENTORY_REDUCTIONS = {
    "skills/cotend-project-init/SKILL.md",
}
AUTHORIZED_TD04_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/SKILL.md",
    "skills/cotend-collaboration/references/native-agent-orchestration.md",
    "skills/cotend-collaboration/references/runtime-profiles.md",
    "skills/cotend-model-upgrade/SKILL.md",
    "skills/cotend-model-upgrade/references/packet-templates.md",
    "skills/cotend-project-init/SKILL.md",
}
AUTHORIZED_TD05_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/SKILL.md",
    "skills/cotend-collaboration/references/acceptance-test-harness.md",
    "skills/cotend-collaboration/references/native-agent-orchestration.md",
    "skills/cotend-collaboration/references/runtime-profiles.md",
    "skills/cotend-model-upgrade/SKILL.md",
    "skills/cotend-project-init/SKILL.md",
}
AUTHORIZED_TD07_INVENTORY_REDUCTIONS = {
    "skills/cotend-collaboration/references/continuous-and-unattended.md",
    "skills/cotend-collaboration/references/plan-tree.md",
    "skills/cotend-collaboration/references/risk-and-approval.md",
    "skills/cotend-collaboration/references/templates.md",
    "skills/cotend-project-init/SKILL.md",
}


class TrellisDecouplingPlanError(ValueError):
    pass


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TrellisDecouplingPlanError(
            "Trellis decoupling contract is not readable JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise TrellisDecouplingPlanError(
            "Trellis decoupling contract must be a JSON object"
        )
    return payload


def runtime_inventory(root: Path = ROOT) -> dict[str, int]:
    inventory: dict[str, int] = {}
    skill_root = root / "skills"
    for path in sorted(item for item in skill_root.rglob("*") if item.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise TrellisDecouplingPlanError(
                f"runtime Skill file is not UTF-8 text: {path}"
            ) from exc
        count = len(re.findall("trellis", text, re.IGNORECASE))
        if count:
            inventory[path.relative_to(root).as_posix()] = count
    return inventory


def tracked_paths(root: Path = ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        value.decode("utf-8")
        for value in result.stdout.split(b"\0")
        if value
    ]


def _require_non_empty_strings(value: Any, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise TrellisDecouplingPlanError(
            f"{label} must be a non-empty list of non-empty strings"
        )
    return value


def validate_contract(
    contract: dict[str, Any],
    document_text: str,
    g06_evidence_text: str,
    actual_inventory: dict[str, int],
    actual_tracked_paths: list[str],
) -> dict[str, Any]:
    if contract.get("schema") != "cotend.trellis-decoupling-plan":
        raise TrellisDecouplingPlanError("Trellis decoupling schema drifted")
    if contract.get("schema_version") != 2:
        raise TrellisDecouplingPlanError("Trellis decoupling schema version drifted")
    if contract.get("status") != "native_runtime_decoupled_real_project_verified":
        raise TrellisDecouplingPlanError(
            "native replacement state drifted"
        )
    if contract.get("authority") != "product_owner_confirmed_through_2026-07-29":
        raise TrellisDecouplingPlanError("product-owner authority drifted")
    if (
        contract.get("decision")
        != "preserve_governance_capabilities_replace_trellis_identity_authority_and_runtime_dependency"
    ):
        raise TrellisDecouplingPlanError("confirmed decoupling decision drifted")
    if contract.get("current_candidate") != "cotend@0.1.0-rc.2_local_unpublished":
        raise TrellisDecouplingPlanError("current candidate identity drifted")
    if contract.get("target_candidate") != "cotend@0.1.0-rc.3_after_parity":
        raise TrellisDecouplingPlanError("target candidate identity drifted")
    if contract.get("development_target_artifact") != "cotend-codex-r000013":
        raise TrellisDecouplingPlanError("development target artifact drifted")

    source = contract.get("source_boundary")
    if not isinstance(source, dict):
        raise TrellisDecouplingPlanError("source boundary is missing")
    if source.get("trellis_source_adoption") != "none":
        raise TrellisDecouplingPlanError("Trellis source adoption must remain none")
    if source.get("trellis_package_dependency") is not False:
        raise TrellisDecouplingPlanError(
            "Trellis may not become a package dependency"
        )
    if source.get("trellis_runtime_tracked_paths") != []:
        raise TrellisDecouplingPlanError(
            "Trellis runtime tracked path inventory must remain empty"
        )

    baseline = contract.get("baseline")
    if not isinstance(baseline, dict):
        raise TrellisDecouplingPlanError("baseline inventory is missing")
    expected_inventory = baseline.get("file_mentions")
    if not isinstance(expected_inventory, dict) or any(
        not isinstance(path, str)
        or not isinstance(count, int)
        or count <= 0
        for path, count in expected_inventory.items()
    ):
        raise TrellisDecouplingPlanError("baseline file inventory is invalid")
    baseline_digest = hashlib.sha256(
        json.dumps(
            expected_inventory,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    if baseline_digest != EXPECTED_BASELINE_INVENTORY_SHA256:
        raise TrellisDecouplingPlanError(
            "immutable 241/22 runtime Trellis baseline changed"
        )
    if baseline.get("mention_count") != sum(expected_inventory.values()):
        raise TrellisDecouplingPlanError("baseline mention total drifted")
    if baseline.get("file_count") != len(expected_inventory):
        raise TrellisDecouplingPlanError("baseline file count drifted")
    if baseline.get("scope") != "skills/":
        raise TrellisDecouplingPlanError("runtime inventory scope drifted")
    if baseline.get("mention_count") != 241 or baseline.get("file_count") != 22:
        raise TrellisDecouplingPlanError("immutable baseline cardinality drifted")

    current = contract.get("current_runtime")
    if not isinstance(current, dict):
        raise TrellisDecouplingPlanError("current runtime inventory is missing")
    current_inventory = current.get("file_mentions")
    if current_inventory != actual_inventory:
        raise TrellisDecouplingPlanError(
            "current runtime Trellis inventory differs from repository Skills"
        )
    if current.get("mention_count") != sum(actual_inventory.values()):
        raise TrellisDecouplingPlanError("current runtime mention total drifted")
    if current.get("file_count") != len(actual_inventory):
        raise TrellisDecouplingPlanError("current runtime file count drifted")
    if current.get("scope") != "skills/":
        raise TrellisDecouplingPlanError("current runtime scope drifted")
    current_digest = hashlib.sha256(
        json.dumps(
            actual_inventory,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    if current_digest != EXPECTED_CURRENT_INVENTORY_SHA256:
        raise TrellisDecouplingPlanError(
            "exact L72 zero runtime inventory changed"
        )
    if actual_inventory:
        raise TrellisDecouplingPlanError(
            "G05 requires zero runtime Trellis inventory"
        )
    changed_inventory_paths = {
        path
        for path in set(expected_inventory) | set(actual_inventory)
        if expected_inventory.get(path, 0) != actual_inventory.get(path, 0)
    }
    authorized_reductions = (
        AUTHORIZED_TD08_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD03_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD06_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD01_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD02_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD04_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD05_INVENTORY_REDUCTIONS
        | AUTHORIZED_TD07_INVENTORY_REDUCTIONS
    )
    if changed_inventory_paths != authorized_reductions:
        raise TrellisDecouplingPlanError(
            "runtime inventory changed outside the exact TD08, TD03, TD06, TD01, TD02, TD04, TD05, and TD07 surfaces"
        )
    if any(
        actual_inventory.get(path, 0) >= expected_inventory.get(path, 0)
        for path in changed_inventory_paths
    ):
        raise TrellisDecouplingPlanError(
            "native migrations must reduce, not add, Trellis runtime references"
        )

    runtime_path_prefixes = (
        "skills/",
        "src/",
        "delivery/",
        "packaging/",
        ".codex-plugin/",
    )
    tracked_trellis_runtime_paths = [
        path
        for path in actual_tracked_paths
        if (
            path == ".trellis"
            or path.startswith(".trellis/")
            or path.startswith(runtime_path_prefixes)
        )
        and any(
            part.lower() == ".trellis" or "trellis" in part.lower()
            for part in Path(path).parts
        )
    ]
    if tracked_trellis_runtime_paths:
        raise TrellisDecouplingPlanError(
            "runtime Trellis-named paths are forbidden: "
            + ", ".join(sorted(tracked_trellis_runtime_paths))
        )

    target = contract.get("target")
    if not isinstance(target, dict):
        raise TrellisDecouplingPlanError("target boundary is missing")
    expected_target = {
        "packaged_runtime_trellis_mentions": 0,
        "trellis_commands": 0,
        "trellis_state_paths": 0,
        "trellis_task_spec_authority": False,
        "capability_regression_allowed": False,
        "mechanical_rename_allowed": False,
        "research_and_provenance_mentions": "retained_with_attribution",
        "external_framework_policy": (
            "generic_conflict_detection_no_core_activation_or_delegation"
        ),
    }
    if target != expected_target:
        raise TrellisDecouplingPlanError("final runtime boundary drifted")

    capabilities = contract.get("capabilities")
    if not isinstance(capabilities, list):
        raise TrellisDecouplingPlanError("capability parity matrix is missing")
    if [item.get("id") for item in capabilities if isinstance(item, dict)] != (
        EXPECTED_CAPABILITY_IDS
    ):
        raise TrellisDecouplingPlanError("eight capability IDs or order drifted")
    for item in capabilities:
        if not isinstance(item, dict):
            raise TrellisDecouplingPlanError("capability entry must be an object")
        capability_id = item["id"]
        _require_non_empty_strings(
            item.get("trellis_surfaces"), f"{capability_id}.trellis_surfaces"
        )
        _require_non_empty_strings(
            item.get("required_outcomes"), f"{capability_id}.required_outcomes"
        )
        _require_non_empty_strings(
            item.get("cotend_owners"), f"{capability_id}.cotend_owners"
        )
        if item.get("status") != "native_parity_verified":
            raise TrellisDecouplingPlanError(
                f"{capability_id} replacement status drifted"
            )
        if item.get("removal_gate") != "native_parity_verified":
            raise TrellisDecouplingPlanError(
                f"{capability_id} removal gate drifted"
            )
        if not isinstance(item.get("known_gap"), str) or not item["known_gap"]:
            raise TrellisDecouplingPlanError(
                f"{capability_id} must retain an explicit gap"
            )
        if capability_id == "TD01-workflow-state-and-mode":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD01 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-WORKFLOW-STATE-AND-RUNTIME-PROFILES.md",
                "skills/cotend-collaboration/references/runtime-profiles.md",
                "scripts/verify_native_workflow_state_runtime_profiles.py",
                "tests/test_native_workflow_state_runtime_profiles.py",
            ]:
                raise TrellisDecouplingPlanError("TD01 evidence inventory drifted")
        if capability_id == "TD02-init-resume-and-before-development":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD02 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-INIT-RESUME-BEFORE-DEVELOPMENT.md",
                "skills/cotend-project-init/SKILL.md",
                "skills/cotend-collaboration/references/code-context-harness.md",
                "scripts/verify_native_init_resume_before_development.py",
                "tests/test_native_init_resume_before_development.py",
            ]:
                raise TrellisDecouplingPlanError("TD02 evidence inventory drifted")
        if capability_id == "TD04-implementation-pass":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD04 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-IMPLEMENTATION-PASS.md",
                "skills/cotend-collaboration/references/implementation-pass.md",
                "scripts/verify_native_implementation_pass.py",
                "tests/test_native_implementation_pass.py",
            ]:
                raise TrellisDecouplingPlanError("TD04 evidence inventory drifted")
        if capability_id == "TD05-verification-pass":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD05 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-VERIFICATION-PASS.md",
                "skills/cotend-collaboration/references/verification-pass.md",
                "scripts/verify_native_verification_pass.py",
                "tests/test_native_verification_pass.py",
            ]:
                raise TrellisDecouplingPlanError("TD05 evidence inventory drifted")
        if capability_id == "TD08-project-truth-authority":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD08 native coverage drifted")
            if item.get("evidence") != [
                "docs/PROJECT-TRUTH-AUTHORITY.md",
                "skills/cotend-collaboration/references/authority-and-triggers.md",
                "scripts/verify_native_project_truth_authority.py",
                "tests/test_native_project_truth_authority.py",
            ]:
                raise TrellisDecouplingPlanError("TD08 evidence inventory drifted")
        if capability_id == "TD03-requirements-clarification":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD03 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-REQUIREMENTS-CLARIFICATION.md",
                "skills/cotend-collaboration/references/idea-to-consensus.md",
                "scripts/verify_native_requirements_clarification.py",
                "tests/test_native_requirements_clarification.py",
            ]:
                raise TrellisDecouplingPlanError("TD03 evidence inventory drifted")
        if capability_id == "TD06-spec-change-and-route-rebase":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD06 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-SPEC-CHANGE-AND-ROUTE-REBASE.md",
                "skills/cotend-collaboration/references/plan-tree.md",
                "scripts/verify_native_spec_change_route_rebase.py",
                "tests/test_native_spec_change_route_rebase.py",
            ]:
                raise TrellisDecouplingPlanError("TD06 evidence inventory drifted")
        if capability_id == "TD07-closeout-archive-and-recovery":
            if item.get("native_coverage") != "verified_native_contract":
                raise TrellisDecouplingPlanError("TD07 native coverage drifted")
            if item.get("evidence") != [
                "docs/NATIVE-CLOSEOUT-ARCHIVE-AND-RECOVERY.md",
                "skills/cotend-collaboration/references/closeout-pass.md",
                "scripts/verify_native_closeout_pass.py",
                "tests/test_native_closeout_pass.py",
            ]:
                raise TrellisDecouplingPlanError("TD07 evidence inventory drifted")

    if contract.get("replacement_order") != EXPECTED_REPLACEMENT_ORDER:
        raise TrellisDecouplingPlanError("dependency-driven replacement order drifted")
    if set(contract["replacement_order"]) != set(EXPECTED_CAPABILITY_IDS):
        raise TrellisDecouplingPlanError(
            "replacement order must cover every capability exactly once"
        )

    gates = contract.get("gates")
    if not isinstance(gates, list) or [
        item.get("id") for item in gates if isinstance(item, dict)
    ] != EXPECTED_GATE_IDS:
        raise TrellisDecouplingPlanError("parity gate inventory drifted")
    for gate in gates:
        if not isinstance(gate, dict):
            raise TrellisDecouplingPlanError("parity gate must be an object")
        _require_non_empty_strings(gate.get("evidence"), f"{gate['id']}.evidence")
        if (
            gate.get("id") == "G03-cumulative-main-journey"
            and gate.get("evidence")
            != [
                "init_to_implementation_to_check_to_acceptance",
                "interruption_and_route_rebase",
                "handoff_and_new_session_recovery",
            ]
        ):
            raise TrellisDecouplingPlanError("G03 evidence contract drifted")
        if (
            gate.get("id") == "G04-negative-recovery-and-ownership"
            and gate.get("evidence")
            != [
                "foreign_framework_conflict",
                "unknown_or_drifted_state",
                "failed_check_and_recovery",
                "unrelated_files_and_truth_preserved",
            ]
        ):
            raise TrellisDecouplingPlanError("G04 evidence contract drifted")
        if (
            gate.get("id") == "G06-real-project-and-rollback"
            and gate.get("evidence")
            != [
                "real_writable_project_journey",
                "user_acceptance",
                "rollback_to_last_verified_candidate",
                "pre_and_post_acceptance_fresh_session_recovery",
                "docs/evidence/NATIVE-REAL-PROJECT-ACCEPTANCE-G06.md",
            ]
        ):
            raise TrellisDecouplingPlanError("G06 evidence contract drifted")
        expected_status = "complete"
        if gate.get("status") != expected_status:
            raise TrellisDecouplingPlanError(
                f"{gate['id']} completion status regressed"
            )

    if contract.get("this_slice") != {
        "skill_behavior_changed": False,
        "trellis_route_removed": False,
        "removed_capability_ids": [],
        "target_artifact_changed": False,
        "package_identity_changed": False,
        "push_release_submission_or_publish": False,
        "validation_gate_completed": "G06-real-project-and-rollback",
    }:
        raise TrellisDecouplingPlanError(
            "L73 G06 real-project acceptance slice boundary drifted"
        )

    for marker in EXPECTED_DOCUMENT_MARKERS:
        if marker not in document_text:
            raise TrellisDecouplingPlanError(
                f"decoupling document is missing marker: {marker}"
            )
    for marker in EXPECTED_G06_EVIDENCE_MARKERS:
        if marker not in g06_evidence_text:
            raise TrellisDecouplingPlanError(
                f"G06 public evidence is missing marker: {marker}"
            )
    native_result = native_authority.verify_repository(ROOT)
    if native_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError("TD08 native authority verifier did not pass")
    clarification_result = native_clarification.verify_repository(ROOT)
    if clarification_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD03 native clarification verifier did not pass"
        )
    route_rebase_result = native_route_rebase.verify_repository(ROOT)
    if route_rebase_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD06 native spec-change verifier did not pass"
        )
    workflow_state_result = native_workflow_state.verify_repository(ROOT)
    if workflow_state_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD01 native workflow-state verifier did not pass"
        )
    project_entry_result = native_project_entry.verify_repository(ROOT)
    if project_entry_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD02 native init/resume/pre-development verifier did not pass"
        )
    implementation_result = native_implementation.verify_repository(ROOT)
    if implementation_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD04 native implementation verifier did not pass"
        )
    verification_result = native_verification.verify_repository(ROOT)
    if verification_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD05 native verification verifier did not pass"
        )
    closeout_result = native_closeout.verify_repository(ROOT)
    if closeout_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError(
            "TD07 native closeout verifier did not pass"
        )
    cumulative_result = native_cumulative_journey.verify_repository(ROOT)
    if (
        cumulative_result.get("status")
        != "native_cumulative_main_journey_verified"
    ):
        raise TrellisDecouplingPlanError(
            "G03 native cumulative main-journey verifier did not pass"
        )
    negative_recovery_result = native_negative_recovery.verify_repository(ROOT)
    if (
        negative_recovery_result.get("status")
        != "native_negative_recovery_ownership_verified"
    ):
        raise TrellisDecouplingPlanError(
            "G04 native negative-recovery verifier did not pass"
        )

    return {
        "status": contract["status"],
        "capabilities": len(capabilities),
        "gates": len(gates),
        "runtime_mentions": sum(actual_inventory.values()),
        "runtime_files": len(actual_inventory),
        "trellis_runtime_paths": 0,
        "skill_behavior_changed": True,
        "native_capabilities_verified": 8,
        "cumulative_gates_verified": 4,
    }


def verify_repository(root: Path = ROOT) -> dict[str, Any]:
    contract = load_contract(root / "upstream" / "TRELLIS-DECOUPLING-PLAN.json")
    document_text = (
        root / "docs" / "TRELLIS-DECOUPLING-PARITY-PLAN.md"
    ).read_text(encoding="utf-8")
    g06_evidence_text = (
        root / "docs" / "evidence" / "NATIVE-REAL-PROJECT-ACCEPTANCE-G06.md"
    ).read_text(encoding="utf-8")
    return validate_contract(
        contract,
        document_text,
        g06_evidence_text,
        runtime_inventory(root),
        tracked_paths(root),
    )


def main() -> int:
    try:
        result = verify_repository()
    except (
        OSError,
        subprocess.CalledProcessError,
        TrellisDecouplingPlanError,
        native_cumulative_journey.NativeCumulativeJourneyError,
        native_negative_recovery.NativeNegativeRecoveryError,
    ) as exc:
        print("TRELLIS_DECOUPLING_PLAN_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "TRELLIS_DECOUPLING_PLAN_OK "
        f"capabilities={result['capabilities']} gates={result['gates']} "
        f"runtime_mentions={result['runtime_mentions']} "
        f"runtime_files={result['runtime_files']} behavior_changed=true "
        f"native_verified={result['native_capabilities_verified']} "
        f"cumulative_gates={result['cumulative_gates_verified']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
