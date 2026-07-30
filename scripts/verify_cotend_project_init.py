from __future__ import annotations

import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_INIT_RELATIVE = Path("skills") / "cotend-project-init"
EXPECTED_REFERENCES = (
    "auto-mode-and-onboarding.md",
    "external-reviewer-sync.md",
    "governance-language-pre-handback.md",
    "initialization-core-workflow.md",
    "language-and-runtime.md",
    "maintenance-and-coordination.md",
    "plan-tree-and-semantic-safety.md",
    "reporting-and-handback.md",
    "routing-and-planning.md",
    "verification-and-closeout-workflow.md",
)
EXPECTED_SCRIPTS = (
    "check_cotend_governance_language.py",
    "maintain_project_agents_router.py",
    "validate_governance_language.py",
)
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    *(f"references/{name}" for name in EXPECTED_REFERENCES),
    *(f"scripts/{name}" for name in EXPECTED_SCRIPTS),
}
DIRECT_REFERENCE_RE = re.compile(r"(?<!/)references/([a-z0-9-]+\.md)")
FORBIDDEN_RUNTIME_RE = re.compile(r"trellis", re.IGNORECASE)


class ProjectInitContractError(ValueError):
    pass


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ProjectInitContractError(f"Project Init file is unreadable: {path}") from exc


def load_project_init_contract(root: Path = ROOT) -> dict[str, Any]:
    skill_root = root / PROJECT_INIT_RELATIVE
    actual_files = {
        path.relative_to(skill_root).as_posix()
        for path in skill_root.rglob("*")
        if path.is_file()
    }
    if actual_files != EXPECTED_FILES:
        missing = sorted(EXPECTED_FILES - actual_files)
        unexpected = sorted(actual_files - EXPECTED_FILES)
        raise ProjectInitContractError(
            f"Project Init topology drifted: missing={missing}, unexpected={unexpected}"
        )

    core = _read(skill_root / "SKILL.md")
    direct_references = set(DIRECT_REFERENCE_RE.findall(core))
    if direct_references != set(EXPECTED_REFERENCES):
        raise ProjectInitContractError(
            "Project Init direct-reference routing does not cover the exact ten modules"
        )
    core_lines = len(core.splitlines())
    if core_lines > 260:
        raise ProjectInitContractError(
            f"Project Init core is no longer concise: {core_lines} lines"
        )

    references: dict[str, str] = {}
    for name in EXPECTED_REFERENCES:
        text = _read(skill_root / "references" / name)
        if DIRECT_REFERENCE_RE.search(text):
            raise ProjectInitContractError(
                f"Project Init reference gained a nested Project Init dependency: {name}"
            )
        references[name] = text

    checker = _read(
        skill_root / "scripts" / "check_cotend_governance_language.py"
    )
    router = _read(skill_root / "scripts" / "maintain_project_agents_router.py")
    validator = _read(skill_root / "scripts" / "validate_governance_language.py")
    required_checker_markers = (
        'CHECKER_ID = "cotend-governance-language.v2"',
        'SUPPORTED_TAGS = {"en", "zh-CN", "zh-TW"}',
        '"actual_bytes_checked": True',
        'payload["sha256"] = hashlib.sha256(data).hexdigest()',
        'payload["whole_file_sha256_checked"] = True',
        '"evaluation_scope": "git_added_lines"',
    )
    if any(marker not in checker for marker in required_checker_markers):
        raise ProjectInitContractError("CoTend governance checker contract drifted")
    if re.search(
        r"private[-_ ]dual(?:-governance-language|_(?:chinese|english))",
        checker,
        re.IGNORECASE,
    ):
        raise ProjectInitContractError(
            "CoTend governance checker contains private-Dual identity or reason codes"
        )
    required_router_markers = (
        'CONTRACT = "cotend.project-router.v1"',
        'START_MARKER = "<!-- COTEND:PROJECT-ROUTER:START -->"',
        'END_MARKER = "<!-- COTEND:PROJECT-ROUTER:END -->"',
        "$cotend-collaboration",
        "$cotend-session-handoff",
        'path = root / "AGENTS.md"',
        'mode.add_argument("--apply", action="store_true")',
        'mode.add_argument("--check", action="store_true")',
        'raise RouterError("managed_marker_pair_incomplete")',
        'raise RouterError("managed_marker_pair_duplicate")',
        "os.replace(temporary, path)",
    )
    if any(marker not in router for marker in required_router_markers):
        raise ProjectInitContractError("CoTend project router contract drifted")
    required_validator_markers = (
        'CONTRACT = "cotend.governance-language-pre-handback.v1"',
        'RESOLUTION_CONTRACT = "cotend.user-facing-language-resolution.v1"',
        "expected_sha256=digest",
        "changed_file_changed_during_validation",
        '"max_same_turn_repairs": 1',
        '"max_same_turn_rechecks": 1',
    )
    if any(marker not in validator for marker in required_validator_markers):
        raise ProjectInitContractError("CoTend governance validator contract drifted")

    combined = "\n".join([core, *(references[name] for name in EXPECTED_REFERENCES)])
    required_router_documentation = (
        "maintain_project_agents_router.py --apply",
        "--check",
        "COTEND:PROJECT-ROUTER",
        "AGENTS.md",
    )
    if any(marker not in combined for marker in required_router_documentation):
        raise ProjectInitContractError(
            "Project Init does not document the native project router lifecycle"
        )
    if FORBIDDEN_RUNTIME_RE.search(
        "\n".join(
            [
                combined,
                checker,
                router,
                validator,
                _read(skill_root / "agents" / "openai.yaml"),
            ]
        )
    ):
        raise ProjectInitContractError(
            "Project Init contains a forbidden external runtime identity"
        )

    return {
        "status": "cotend_project_init_topology_verified",
        "core": core,
        "references": references,
        "router": router,
        "combined": combined,
        "file_count": len(actual_files),
        "reference_count": len(references),
        "script_count": len(EXPECTED_SCRIPTS),
        "core_lines": core_lines,
    }


def main() -> int:
    try:
        result = load_project_init_contract()
    except ProjectInitContractError as exc:
        print("COTEND_PROJECT_INIT_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "COTEND_PROJECT_INIT_OK "
        f"files={result['file_count']} references={result['reference_count']} "
        f"scripts={result['script_count']} core_lines={result['core_lines']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
