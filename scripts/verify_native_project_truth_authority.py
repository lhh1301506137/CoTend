from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = (
    ROOT
    / "skills"
    / "cotend-collaboration"
    / "references"
    / "authority-and-triggers.md"
)
DOCUMENT_PATH = ROOT / "docs" / "PROJECT-TRUTH-AUTHORITY.md"
SKILL_ROOT = ROOT / "skills"

ExternalState = Literal["absent", "aligned", "stale", "conflict", "unknown"]
SemanticLevel = Literal["none", "L0_L2", "L3_L4"]

REQUIRED_AUTHORITY_MARKERS = (
    "## Scoped Authority Domains",
    "stop_affected_and_align",
    "single canonical owner of execution authorization",
    "must not create another permission system",
    "Plan Tree/current project truth owns the active route and task/spec links.",
    "External framework\n  artifacts remain `reference_only | historical | conflict`.",
    "Current task/specification records remain linked evidence",
    "create a second task/state tree",
)
REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 原生项目真相权限",
    "## 唯一权威链",
    "## 外部开发框架分类",
    "## 冲突和恢复",
    "## L62 边界",
    "不创建第二棵真相树",
    "cotend-codex-r000003",
    "0.1.0-rc.2",
)
FORBIDDEN_AUTHORITY_PATTERNS = {
    "active_trellis_owns": re.compile(
        r"active\s+Trellis\s+owns", re.IGNORECASE
    ),
    "binding_trellis_truth": re.compile(
        r"binding\s+Trellis\s+(?:task|PRD|spec|truth)", re.IGNORECASE
    ),
    "trellis_binding_substrate": re.compile(
        r"Trellis\s+(?:task/PRD/spec\s+)?remains\s+the\s+binding", re.IGNORECASE
    ),
    "trellis_durable_substrate": re.compile(
        r"Trellis\s+is\s+the\s+durable\s+project\s+substrate", re.IGNORECASE
    ),
    "trellis_state_first": re.compile(
        r"resolve\s+through.+Trellis\s+state\s+first", re.IGNORECASE
    ),
    "trellis_truth_precedence": re.compile(
        r"then\s+active\s+Trellis\s+truth", re.IGNORECASE
    ),
}


class NativeAuthorityError(ValueError):
    pass


@dataclass(frozen=True)
class AuthorityResult:
    classification: str
    action: str
    route_owner: str
    blocked_scope: str
    user_decision_required: bool
    external_is_authority: bool = False
    create_parallel_truth: bool = False


def evaluate_external_artifact(
    external_state: ExternalState,
    semantic_level: SemanticLevel = "none",
    *,
    has_plan_tree: bool = True,
    has_project_equivalent_route: bool = False,
) -> AuthorityResult:
    if has_plan_tree and has_project_equivalent_route:
        raise NativeAuthorityError("exactly one CoTend route owner may be active")
    route_owner = (
        "cotend_plan_tree"
        if has_plan_tree
        else "project_equivalent_route"
        if has_project_equivalent_route
        else "create_minimum_cotend_route"
    )
    if external_state == "absent":
        if semantic_level != "none":
            raise NativeAuthorityError("absent external state cannot carry a conflict level")
        return AuthorityResult(
            "none",
            "use_cotend_authority_chain",
            route_owner,
            "none",
            False,
        )
    if external_state == "aligned":
        if semantic_level != "none":
            raise NativeAuthorityError("aligned external state cannot carry a conflict level")
        return AuthorityResult(
            "reference_only",
            "link_without_delegation",
            route_owner,
            "none",
            False,
        )
    if external_state == "stale":
        if semantic_level != "none":
            raise NativeAuthorityError("stale external state cannot carry a conflict level")
        return AuthorityResult(
            "historical",
            "preserve_without_routing",
            route_owner,
            "none",
            False,
        )
    if external_state == "unknown":
        if semantic_level != "none":
            raise NativeAuthorityError("unknown state is not yet semantically classified")
        return AuthorityResult(
            "conflict",
            "block_affected_until_classified",
            route_owner,
            "affected_dependencies",
            False,
        )
    if external_state != "conflict":
        raise NativeAuthorityError(f"unsupported external state: {external_state}")
    if semantic_level == "L0_L2":
        return AuthorityResult(
            "conflict",
            "stop_affected_and_route_semantic_alignment",
            route_owner,
            "affected_semantic_scope",
            True,
        )
    if semantic_level == "L3_L4":
        return AuthorityResult(
            "conflict",
            "rebase_cotend_route_from_reliable_boundary",
            route_owner,
            "until_route_rebased",
            False,
        )
    raise NativeAuthorityError("conflict state requires L0_L2 or L3_L4")


EXPECTED_SCENARIOS = {
    "no_external_framework": {
        "args": ("absent", "none"),
        "classification": "none",
        "action": "use_cotend_authority_chain",
        "user_decision_required": False,
    },
    "aligned_external_framework": {
        "args": ("aligned", "none"),
        "classification": "reference_only",
        "action": "link_without_delegation",
        "user_decision_required": False,
    },
    "stale_external_framework": {
        "args": ("stale", "none"),
        "classification": "historical",
        "action": "preserve_without_routing",
        "user_decision_required": False,
    },
    "protected_semantic_conflict": {
        "args": ("conflict", "L0_L2"),
        "classification": "conflict",
        "action": "stop_affected_and_route_semantic_alignment",
        "user_decision_required": True,
    },
    "execution_route_conflict": {
        "args": ("conflict", "L3_L4"),
        "classification": "conflict",
        "action": "rebase_cotend_route_from_reliable_boundary",
        "user_decision_required": False,
    },
    "unknown_dependency_impact": {
        "args": ("unknown", "none"),
        "classification": "conflict",
        "action": "block_affected_until_classified",
        "user_decision_required": False,
    },
}


def scan_forbidden_authority(root: Path = ROOT) -> list[str]:
    findings: list[str] = []
    for path in sorted((root / "skills").rglob("*")):
        if (
            not path.is_file()
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_AUTHORITY_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}:{path.relative_to(root).as_posix()}")
    return findings


def verify_repository(root: Path = ROOT) -> dict[str, object]:
    authority_paths = (
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "authority-and-triggers.md",
        root / "skills" / "cotend-collaboration" / "SKILL.md",
        root
        / "skills"
        / "cotend-collaboration"
        / "references"
        / "plan-tree.md",
    )
    authority_text = "\n".join(
        path.read_text(encoding="utf-8") for path in authority_paths
    )
    document_text = (root / "docs" / "PROJECT-TRUTH-AUTHORITY.md").read_text(
        encoding="utf-8"
    )
    for marker in REQUIRED_AUTHORITY_MARKERS:
        if marker not in authority_text:
            raise NativeAuthorityError(f"authority contract is missing: {marker}")
    for marker in REQUIRED_DOCUMENT_MARKERS:
        if marker not in document_text:
            raise NativeAuthorityError(f"authority document is missing: {marker}")
    findings = scan_forbidden_authority(root)
    if findings:
        raise NativeAuthorityError(
            "external framework still owns project truth: " + ", ".join(findings)
        )

    scenario_results: dict[str, dict[str, object]] = {}
    for scenario_id, expected in EXPECTED_SCENARIOS.items():
        result = evaluate_external_artifact(*expected["args"])
        payload = asdict(result)
        for key in ("classification", "action", "user_decision_required"):
            if payload[key] != expected[key]:
                raise NativeAuthorityError(
                    f"scenario result drifted: {scenario_id}.{key}"
                )
        if result.external_is_authority or result.create_parallel_truth:
            raise NativeAuthorityError(
                f"scenario delegated authority or duplicated truth: {scenario_id}"
            )
        scenario_results[scenario_id] = payload

    mapped = evaluate_external_artifact(
        "aligned",
        has_plan_tree=False,
        has_project_equivalent_route=True,
    )
    if mapped.route_owner != "project_equivalent_route":
        raise NativeAuthorityError("project-equivalent route mapping drifted")

    return {
        "status": "native_parity_verified",
        "capability": "TD08-project-truth-authority",
        "scenarios": scenario_results,
        "scenario_count": len(scenario_results),
        "forbidden_authority_findings": 0,
        "external_authority": False,
        "parallel_truth_created": False,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (OSError, UnicodeError, NativeAuthorityError) as exc:
        print("NATIVE_PROJECT_TRUTH_AUTHORITY_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_PROJECT_TRUTH_AUTHORITY_OK "
        f"capability={result['capability']} scenarios={result['scenario_count']} "
        "external_authority=false parallel_truth=false"
    )
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
