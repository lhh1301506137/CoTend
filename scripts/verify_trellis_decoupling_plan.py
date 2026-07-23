from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import verify_native_project_truth_authority as native_authority


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
DOCUMENT_PATH = ROOT / "docs" / "TRELLIS-DECOUPLING-PARITY-PLAN.md"
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
    "### G05 运行时零依赖",
    "只移除 TD08",
]
EXPECTED_BASELINE_INVENTORY_SHA256 = (
    "a1c9893a7462d7abd925b1ae468a3dd97366fae850e2881a23546e5471e93aeb"
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
    actual_inventory: dict[str, int],
    actual_tracked_paths: list[str],
) -> dict[str, Any]:
    if contract.get("schema") != "cotend.trellis-decoupling-plan":
        raise TrellisDecouplingPlanError("Trellis decoupling schema drifted")
    if contract.get("schema_version") != 2:
        raise TrellisDecouplingPlanError("Trellis decoupling schema version drifted")
    if contract.get("status") != "native_replacement_in_progress":
        raise TrellisDecouplingPlanError(
            "native replacement state drifted"
        )
    if (
        contract.get("decision")
        != "preserve_governance_capabilities_replace_trellis_identity_authority_and_runtime_dependency"
    ):
        raise TrellisDecouplingPlanError("confirmed decoupling decision drifted")
    if contract.get("current_candidate") != "cotend@0.1.0-rc.2_local_unpublished":
        raise TrellisDecouplingPlanError("current candidate identity drifted")
    if contract.get("target_candidate") != "cotend@0.1.0-rc.3_after_parity":
        raise TrellisDecouplingPlanError("target candidate identity drifted")
    if contract.get("development_target_artifact") != "cotend-codex-r000003":
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
    changed_inventory_paths = {
        path
        for path in set(expected_inventory) | set(actual_inventory)
        if expected_inventory.get(path, 0) != actual_inventory.get(path, 0)
    }
    if changed_inventory_paths != AUTHORIZED_TD08_INVENTORY_REDUCTIONS:
        raise TrellisDecouplingPlanError(
            "runtime inventory changed outside the exact TD08 authority surfaces"
        )
    if any(
        actual_inventory.get(path, 0) >= expected_inventory.get(path, 0)
        for path in changed_inventory_paths
    ):
        raise TrellisDecouplingPlanError(
            "TD08 migration must reduce, not add, Trellis runtime references"
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
        expected_status = (
            "native_parity_verified"
            if capability_id == "TD08-project-truth-authority"
            else "baseline_frozen"
        )
        if item.get("status") != expected_status:
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
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            raise TrellisDecouplingPlanError("parity gate must be an object")
        _require_non_empty_strings(gate.get("evidence"), f"{gate['id']}.evidence")
        expected_status = (
            "complete"
            if index == 0
            else "in_progress_1_of_8"
            if index == 1
            else "not_started"
        )
        if gate.get("status") != expected_status:
            raise TrellisDecouplingPlanError(
                f"{gate['id']} status advanced without executed evidence"
            )

    if contract.get("this_slice") != {
        "skill_behavior_changed": True,
        "trellis_route_removed": True,
        "removed_capability_ids": ["TD08-project-truth-authority"],
        "target_artifact_changed": True,
        "package_identity_changed": False,
        "push_release_submission_or_publish": False,
    }:
        raise TrellisDecouplingPlanError(
            "L62 slice boundary drifted"
        )

    for marker in EXPECTED_DOCUMENT_MARKERS:
        if marker not in document_text:
            raise TrellisDecouplingPlanError(
                f"decoupling document is missing marker: {marker}"
            )
    native_result = native_authority.verify_repository(ROOT)
    if native_result.get("status") != "native_parity_verified":
        raise TrellisDecouplingPlanError("TD08 native authority verifier did not pass")

    return {
        "status": contract["status"],
        "capabilities": len(capabilities),
        "gates": len(gates),
        "runtime_mentions": sum(actual_inventory.values()),
        "runtime_files": len(actual_inventory),
        "trellis_runtime_paths": 0,
        "skill_behavior_changed": True,
        "native_capabilities_verified": 1,
    }


def verify_repository(root: Path = ROOT) -> dict[str, Any]:
    contract = load_contract(root / "upstream" / "TRELLIS-DECOUPLING-PLAN.json")
    document_text = (
        root / "docs" / "TRELLIS-DECOUPLING-PARITY-PLAN.md"
    ).read_text(encoding="utf-8")
    return validate_contract(
        contract,
        document_text,
        runtime_inventory(root),
        tracked_paths(root),
    )


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, subprocess.CalledProcessError, TrellisDecouplingPlanError) as exc:
        print("TRELLIS_DECOUPLING_PLAN_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "TRELLIS_DECOUPLING_PLAN_OK "
        f"capabilities={result['capabilities']} gates={result['gates']} "
        f"runtime_mentions={result['runtime_mentions']} "
        f"runtime_files={result['runtime_files']} behavior_changed=true "
        f"native_verified={result['native_capabilities_verified']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
