from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import build_release_archive as release  # noqa: E402
import prepare_reviewer_fixtures as fixtures  # noqa: E402
import verify_plugin_submission_materials as submission  # noqa: E402


CI_PATH = ROOT / ".github" / "workflows" / "ci.yml"
CI_REQUIREMENTS_PATH = ROOT / "requirements-ci.txt"
RELEASE_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "release.yml"
SETTINGS_PATH = ROOT / "docs" / "GITHUB-REPOSITORY-SETTINGS.md"
EXPECTED_FILES = {
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "PRIVACY.md",
    "requirements-ci.txt",
    "SECURITY.md",
    "SUPPORT.md",
    "TERMS.md",
    "docs/COMPATIBILITY.md",
    "docs/EXAMPLE-WORKFLOW.md",
    "docs/GITHUB-REPOSITORY-SETTINGS.md",
    "docs/MAINTAINER-RELEASE.md",
    "docs/TROUBLESHOOTING.md",
    "docs/UPGRADING.md",
    "docs/evidence/GITHUB-REPOSITORY-MATURITY.md",
    "docs/releases/v0.1.0-rc.1.md",
    "packaging/codex-plugin/submission-materials/reviewer-fixtures.json",
    "scripts/build_release_archive.py",
    "scripts/prepare_reviewer_fixtures.py",
    "scripts/verify_repository_maturity.py",
    "tests/test_release_archive.py",
    "tests/test_repository_maturity.py",
    "tests/test_reviewer_fixtures.py",
}
EXPECTED_PUBLIC_URLS = {
    "website": "https://github.com/lhh1301506137/CoTend",
    "support": "https://github.com/lhh1301506137/CoTend/blob/main/SUPPORT.md",
    "privacy": "https://github.com/lhh1301506137/CoTend/blob/main/PRIVACY.md",
    "terms": "https://github.com/lhh1301506137/CoTend/blob/main/TERMS.md",
}


class RepositoryMaturityError(RuntimeError):
    pass


def git_candidates() -> set[str]:
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return {
        item.decode("utf-8").replace("\\", "/")
        for item in completed.stdout.split(b"\0")
        if item
    }


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise RepositoryMaturityError(f"{label} is missing markers: {missing}")


def validate_ci_workflow(
    text: str | None = None,
    requirements_text: str | None = None,
) -> dict[str, Any]:
    if text is None:
        text = CI_PATH.read_text(encoding="utf-8")
    if requirements_text is None:
        requirements_text = CI_REQUIREMENTS_PATH.read_text(encoding="utf-8")
    _require_markers(
        text,
        (
            "pull_request:",
            "push:",
            "workflow_dispatch:",
            "permissions:\n  contents: read",
            "ubuntu-latest",
            "windows-latest",
            'python: "3.10"',
            'python: "3.13"',
            "python -m pip install --disable-pip-version-check --requirement requirements-ci.txt",
            "python -m unittest discover -s tests",
            "python scripts/check_repository.py",
            "python scripts/verify_codex_plugin_package.py --repository-only",
            "python scripts/verify_plugin_submission_materials.py",
            "python scripts/prepare_reviewer_fixtures.py",
            "python scripts/build_release_archive.py --check-tag v0.1.0-rc.1",
            "python scripts/verify_repository_maturity.py --no-build",
            "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4",
            "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4",
        ),
        "CI workflow",
    )
    if "contents: write" in text or "pull-requests: write" in text:
        raise RepositoryMaturityError("CI workflow must remain read-only")
    if re.search(r"uses:\s+[^\s]+@v\d+\s*$", text, re.MULTILINE):
        raise RepositoryMaturityError("CI actions must be pinned to full commits")
    requirements = [
        line.strip()
        for line in requirements_text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if requirements != ["PyYAML==6.0.3"]:
        raise RepositoryMaturityError(
            "CI dependencies must contain only the exact PyYAML==6.0.3 pin"
        )
    return {
        "operating_systems": 2,
        "python_versions": 2,
        "matrix_jobs": 3,
        "pinned_ci_dependencies": 1,
    }


def validate_release_workflow(text: str | None = None) -> dict[str, Any]:
    if text is None:
        text = RELEASE_WORKFLOW_PATH.read_text(encoding="utf-8")
    _require_markers(
        text,
        (
            "workflow_dispatch:",
            "permissions:\n  contents: write",
            "create-draft-release",
            "ref: ${{ inputs.tag }}",
            "python -m pip install --disable-pip-version-check --requirement requirements-ci.txt",
            "git ls-remote --exit-code --tags origin",
            "git cat-file -t",
            "git rev-parse HEAD",
            "--verify-tag",
            "--draft",
            "--prerelease",
            "--latest=false",
            "Refuse to replace an existing release",
        ),
        "release workflow",
    )
    workflow_trigger = text.split("permissions:", 1)[0]
    if re.search(r"^\s{2}(?:push|pull_request|schedule):", workflow_trigger, re.MULTILINE):
        raise RepositoryMaturityError("release workflow must remain manual-only")
    for forbidden in ("git push", "git tag ", "--draft=false", "gh release edit"):
        if forbidden in text:
            raise RepositoryMaturityError(
                f"release workflow contains forbidden publication behavior: {forbidden}"
            )
    if re.search(r"uses:\s+[^\s]+@v\d+\s*$", text, re.MULTILINE):
        raise RepositoryMaturityError("release actions must be pinned to full commits")
    return {
        "manual_only": True,
        "existing_tag_required": True,
        "annotated_tag_required": True,
        "tag_checkout": True,
        "pinned_release_dependencies_installed": True,
        "draft_only": True,
        "publish_supported": False,
    }


def validate_public_entry_points() -> dict[str, Any]:
    candidates = git_candidates()
    missing = sorted(EXPECTED_FILES - candidates)
    if missing:
        raise RepositoryMaturityError(f"required public files are missing: {missing}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for relative in (
        "CONTRIBUTING.md",
        "SUPPORT.md",
        "SECURITY.md",
        "PRIVACY.md",
        "TERMS.md",
        "CODE_OF_CONDUCT.md",
        "docs/COMPATIBILITY.md",
        "docs/UPGRADING.md",
        "docs/TROUBLESHOOTING.md",
        "docs/EXAMPLE-WORKFLOW.md",
        "docs/MAINTAINER-RELEASE.md",
        "CHANGELOG.md",
    ):
        if f"]({relative})" not in readme:
            raise RepositoryMaturityError(f"README does not link {relative}")

    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")
    terms = (ROOT / "TERMS.md").read_text(encoding="utf-8")
    support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
    _require_markers(
        security,
        ("Report a vulnerability", "Do not open a public issue", "no stable support window"),
        "security policy",
    )
    _require_markers(
        privacy,
        ("does not provide a hosted account", "does not control that processing", "SECURITY.md"),
        "privacy policy",
    )
    _require_markers(
        terms,
        ("Apache License 2.0", 'provided on an "AS IS"', "Your responsibility"),
        "terms",
    )
    _require_markers(
        support,
        ("best-effort basis", "no paid plan", "Do not attach"),
        "support policy",
    )
    return {
        "required_files": len(EXPECTED_FILES),
        "community_policies": 6,
        "issue_forms": 2,
    }


def validate_relative_markdown_links() -> dict[str, int]:
    candidates = git_candidates()
    markdown_paths = sorted(
        path for path in candidates if path.lower().endswith(".md")
    )
    checked = 0
    for relative in markdown_paths:
        source = ROOT / relative
        text = source.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().strip("<>")
            if (
                not target
                or target.startswith("#")
                or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE)
            ):
                continue
            target_path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            resolved = (source.parent / target_path).resolve(strict=False)
            if not resolved.is_relative_to(ROOT.resolve()):
                raise RepositoryMaturityError(
                    f"Markdown link escapes the repository: {relative} -> {target}"
                )
            if not resolved.exists():
                raise RepositoryMaturityError(
                    f"Markdown link target is missing: {relative} -> {target}"
                )
            checked += 1
    return {"markdown_files": len(markdown_paths), "relative_links": checked}


def validate_repository_settings() -> dict[str, Any]:
    text = SETTINGS_PATH.read_text(encoding="utf-8")
    _require_markers(
        text,
        (
            "AI development governance for people who build software with AI.",
            "agent-skills",
            "ai-coding",
            "ai-development",
            "codex",
            "developer-tools",
            "project-governance",
            "vibe-coding",
            "Private vulnerability reporting: enable",
            "requires separate authorization",
        )
        + tuple(EXPECTED_PUBLIC_URLS.values()),
        "GitHub repository settings",
    )
    return {
        "topics": 7,
        "public_url_candidates": len(EXPECTED_PUBLIC_URLS),
        "external_application_required": True,
    }


def validate_repository_maturity(*, build_artifacts: bool = False) -> dict[str, Any]:
    entries = validate_public_entry_points()
    ci = validate_ci_workflow()
    release_workflow = validate_release_workflow()
    settings = validate_repository_settings()
    links = validate_relative_markdown_links()
    package.validate_contract()
    submission_result = submission.validate_submission_materials()
    fixture_result = fixtures.validate_fixture_contract()
    release_result = release.validate_release_metadata(release.expected_tag())
    build_result: dict[str, Any] | None = None
    fixture_build: dict[str, Any] | None = None
    if build_artifacts:
        fixture_build = fixtures.prepare_fixtures()
        build_result = release.build_release_archive(tag=release.expected_tag())
    return {
        "status": "repository_internal_maturity_ready_external_state_not_checked",
        "candidate": f"{package.PLUGIN_NAME}@{package.PLUGIN_VERSION}",
        "tag": release_result["tag"],
        "entry_points": entries,
        "ci": ci,
        "release_workflow": release_workflow,
        "settings": settings,
        "markdown_links": links,
        "submission": submission_result,
        "reviewer_fixtures": {
            "cases": fixture_result["case_count"],
            "preflight": fixture_result["preflight_count"],
            "model_execution_performed": False,
        },
        "artifacts_built": build_artifacts,
        "archive_sha256": None if build_result is None else build_result["archive_sha256"],
        "fixtures_materialized": fixture_build is not None,
        "external_state_checked": False,
        "external_state_source": "GitHub",
        "public_push_performed": None,
        "github_settings_applied": None,
        "tag_created": None,
        "release_created": None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify CoTend's repository-internal GitHub maturity contracts."
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Validate contracts without rebuilding ignored release and reviewer artifacts.",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = validate_repository_maturity(build_artifacts=not args.no_build)
    except (
        RepositoryMaturityError,
        package.PluginPackageError,
        release.ReleaseArchiveError,
        fixtures.ReviewerFixtureError,
        submission.SubmissionMaterialError,
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"GITHUB_REPOSITORY_MATURITY_FAILED reason={exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    else:
        print(
            "GITHUB_REPOSITORY_MATURITY_OK "
            f"status={result['status']} candidate={result['candidate']} "
            f"workflows=2 community={result['entry_points']['community_policies']} "
            f"reviewer_cases={result['reviewer_fixtures']['cases']} "
            f"tag={result['tag']} external_state=not_checked"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
