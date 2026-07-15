from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import verify_plugin_submission_materials as submission  # noqa: E402


FIXTURE_CONTRACT_PATH = (
    ROOT
    / "packaging"
    / "codex-plugin"
    / "submission-materials"
    / "reviewer-fixtures.json"
)
DEFAULT_OUTPUT = ROOT / "dist" / "reviewer-fixtures"
ALLOWED_OUTPUT_ROOTS = {"dist", ".private-provenance"}
OWNER_FILE = ".cotend-reviewer-fixtures.json"
EXPECTED_CASE_IDS = submission.EXPECTED_POSITIVE_IDS + submission.EXPECTED_NEGATIVE_IDS
EXPECTED_COMMAND = ["{python}", "-m", "unittest", "discover", "-s", "tests"]
FORBIDDEN_TEXT = re.compile(
    r"\b[A-Za-z]:[\\/]|/home/|/Users/|PROJECT-DECISION-LOG|\.private-provenance",
    re.IGNORECASE,
)


class ReviewerFixtureError(RuntimeError):
    pass


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewerFixtureError(f"invalid {label}: {path}") from exc
    if not isinstance(value, dict):
        raise ReviewerFixtureError(f"{label} must contain a JSON object")
    return value


def contract_sha256() -> str:
    return hashlib.sha256(FIXTURE_CONTRACT_PATH.read_bytes()).hexdigest()


def _exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise ReviewerFixtureError(f"{label} fields drifted")
    return value


def _safe_relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or ".git" in path.parts
        or str(path) != value
    ):
        raise ReviewerFixtureError(f"unsafe fixture path: {value}")
    return path


def validate_fixture_contract(
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if contract is None:
        contract = load_json_object(FIXTURE_CONTRACT_PATH, "reviewer fixture contract")
    _exact_keys(
        contract,
        {
            "schema",
            "schema_version",
            "status",
            "package",
            "reviewer_contract",
            "output_policy",
            "cases",
        },
        "reviewer fixture contract",
    )
    if (
        contract["schema"] != "cotend.codex-plugin-reviewer-fixtures"
        or contract["schema_version"] != 1
        or contract["status"]
        != "repository_fixture_kit_ready_model_execution_not_run"
    ):
        raise ReviewerFixtureError("reviewer fixture contract identity drifted")

    package_contract = package.validate_contract()
    expected_package = {
        "plugin_id": package.PLUGIN_NAME,
        "version": package.PLUGIN_VERSION,
        "path_hash_manifest_sha256": package.path_hash_manifest_sha256(
            package_contract["expected_package_manifest"]
        ),
    }
    if contract["package"] != expected_package:
        raise ReviewerFixtureError("reviewer fixtures are not bound to the package")
    if contract["reviewer_contract"] != submission.REVIEWER_TESTS_PATH.relative_to(
        ROOT
    ).as_posix():
        raise ReviewerFixtureError("reviewer fixture contract path drifted")
    if contract["output_policy"] != {
        "default_root": "dist/reviewer-fixtures",
        "disposable_git_repositories": True,
        "network_required": False,
        "private_context_required": False,
        "model_execution_performed": False,
    }:
        raise ReviewerFixtureError("reviewer fixture output policy drifted")

    reviewer_tests = submission.load_json_object(
        submission.REVIEWER_TESTS_PATH, "reviewer test contract"
    )
    submission.validate_submission_materials(reviewer_tests=reviewer_tests)
    reviewer_cases = reviewer_tests["positive_cases"] + reviewer_tests["negative_cases"]
    expected_names = {case["id"]: case["fixture"]["name"] for case in reviewer_cases}

    cases = contract["cases"]
    if not isinstance(cases, list) or [case.get("id") for case in cases] != EXPECTED_CASE_IDS:
        raise ReviewerFixtureError("reviewer fixture case inventory drifted")
    preflight_count = 0
    for case in cases:
        case = _exact_keys(case, {"id", "name", "files", "preflight"}, "fixture case")
        if case["name"] != expected_names[case["id"]]:
            raise ReviewerFixtureError(f"reviewer fixture name drifted: {case['id']}")
        files = case["files"]
        if not isinstance(files, dict) or (case["id"] != "P01" and not files):
            raise ReviewerFixtureError(f"reviewer fixture files are invalid: {case['id']}")
        if case["id"] == "P01" and files:
            raise ReviewerFixtureError("P01 must remain an empty project")
        for relative, content in files.items():
            if not isinstance(relative, str) or not isinstance(content, str):
                raise ReviewerFixtureError("reviewer fixture files must be text")
            _safe_relative_path(relative)
            if not content or FORBIDDEN_TEXT.search(content):
                raise ReviewerFixtureError(
                    f"reviewer fixture contains private or invalid text: {case['id']}"
                )
        checks = case["preflight"]
        if not isinstance(checks, list):
            raise ReviewerFixtureError("reviewer fixture preflight must be a list")
        for check in checks:
            check = _exact_keys(
                check, {"command", "expected_exit_code"}, "fixture preflight"
            )
            if check["command"] != EXPECTED_COMMAND or check["expected_exit_code"] not in {
                0,
                1,
            }:
                raise ReviewerFixtureError("reviewer fixture preflight drifted")
            preflight_count += 1
    if preflight_count != 5:
        raise ReviewerFixtureError("reviewer fixture preflight count drifted")
    return {
        "contract": contract,
        "case_count": len(cases),
        "positive_count": len(submission.EXPECTED_POSITIVE_IDS),
        "negative_count": len(submission.EXPECTED_NEGATIVE_IDS),
        "preflight_count": preflight_count,
        "contract_sha256": contract_sha256(),
    }


def guarded_output(path: Path) -> Path:
    raw = path.expanduser()
    if not raw.is_absolute():
        raw = ROOT / raw
    repository_root = ROOT.resolve()
    lexical = Path(os.path.abspath(raw))
    try:
        relative = lexical.relative_to(repository_root)
    except ValueError as exc:
        raise ReviewerFixtureError("reviewer fixture output escaped the repository") from exc
    if len(relative.parts) < 2 or relative.parts[0] not in ALLOWED_OUTPUT_ROOTS:
        raise ReviewerFixtureError(
            "reviewer fixture output must be below dist/ or .private-provenance/"
        )
    cursor = repository_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and package._is_linklike(cursor):
            raise ReviewerFixtureError("reviewer fixture output contains a link or junction")
    resolved = lexical.resolve(strict=False)
    try:
        resolved_relative = resolved.relative_to(repository_root)
    except ValueError as exc:
        raise ReviewerFixtureError(
            "reviewer fixture output resolved outside the repository"
        ) from exc
    if (
        len(resolved_relative.parts) < 2
        or resolved_relative.parts[0] not in ALLOWED_OUTPUT_ROOTS
    ):
        raise ReviewerFixtureError(
            "reviewer fixture output resolved outside an allowed root"
        )
    return resolved


def _working_files(case_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in case_root.rglob("*"):
        if not path.is_file() or ".git" in path.relative_to(case_root).parts:
            continue
        relative = path.relative_to(case_root).as_posix()
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(result.items()))


def _expected_working_files(case: dict[str, Any]) -> dict[str, str]:
    return {
        relative: hashlib.sha256(content.encode("utf-8")).hexdigest()
        for relative, content in sorted(case["files"].items())
    }


def _verify_existing_owned_output(output: Path, contract: dict[str, Any]) -> None:
    owner_path = output / OWNER_FILE
    owner = load_json_object(owner_path, "reviewer fixture ownership marker")
    if owner != {
        "schema": "cotend.generated-reviewer-fixtures",
        "schema_version": 1,
        "source_sha256": contract_sha256(),
    }:
        raise ReviewerFixtureError("existing reviewer fixture output is not owned")
    expected_case_names = {case["id"] for case in contract["cases"]}
    actual_children = {path.name for path in output.iterdir()}
    if actual_children != expected_case_names | {OWNER_FILE}:
        raise ReviewerFixtureError("existing reviewer fixture output has unexpected content")
    for case in contract["cases"]:
        case_root = output / case["id"]
        if not (case_root / ".git").is_dir():
            raise ReviewerFixtureError("existing reviewer fixture Git state is missing")
        if _working_files(case_root) != _expected_working_files(case):
            raise ReviewerFixtureError("existing reviewer fixture files were modified")


def remove_generated_tree(path: Path) -> None:
    if not path.exists():
        return
    package.reject_link_tree(path, label="generated reviewer fixtures")
    for current, directories, filenames in os.walk(path, topdown=False):
        current_path = Path(current)
        for name in filenames:
            os.chmod(current_path / name, stat.S_IREAD | stat.S_IWRITE)
        for name in directories:
            os.chmod(
                current_path / name,
                stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC,
            )
    os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
    shutil.rmtree(path)


def _run_git(case_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
        }
    )
    completed = subprocess.run(
        [
            "git",
            "-c",
            f"core.hooksPath={os.devnull}",
            "-c",
            "commit.gpgSign=false",
            *args,
        ],
        cwd=case_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        timeout=30,
    )
    if completed.returncode != 0:
        raise ReviewerFixtureError(
            f"Git fixture command failed: {' '.join(args)}: "
            + (completed.stdout + completed.stderr)[-400:]
        )
    return completed


def _materialize_case(case: dict[str, Any], case_root: Path) -> list[dict[str, Any]]:
    case_root.mkdir(parents=True)
    for relative, content in case["files"].items():
        target = case_root.joinpath(*_safe_relative_path(relative).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    _run_git(case_root, "init", "--quiet", "--initial-branch=main")
    _run_git(case_root, "add", "--all")
    _run_git(
        case_root,
        "-c",
        "user.name=CoTend Reviewer Fixture",
        "-c",
        "user.email=fixture@invalid.example",
        "commit",
        "--quiet",
        "--allow-empty",
        "-m",
        f"Fixture baseline {case['id']}",
    )
    results: list[dict[str, Any]] = []
    for check in case["preflight"]:
        command = [
            sys.executable if value == "{python}" else value for value in check["command"]
        ]
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            command,
            cwd=case_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            timeout=30,
        )
        if completed.returncode != check["expected_exit_code"]:
            raise ReviewerFixtureError(
                f"fixture preflight result drifted: {case['id']} "
                f"expected={check['expected_exit_code']} actual={completed.returncode}"
            )
        results.append(
            {
                "case_id": case["id"],
                "expected_exit_code": check["expected_exit_code"],
                "actual_exit_code": completed.returncode,
            }
        )
    if _run_git(case_root, "status", "--porcelain").stdout:
        raise ReviewerFixtureError(f"reviewer fixture is not clean: {case['id']}")
    if _working_files(case_root) != _expected_working_files(case):
        raise ReviewerFixtureError(f"reviewer fixture files drifted: {case['id']}")
    return results


def prepare_fixtures(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    validation = validate_fixture_contract()
    contract = validation["contract"]
    output = guarded_output(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".reviewer-fixtures-", dir=output.parent))
    try:
        preflight_results: list[dict[str, Any]] = []
        for case in contract["cases"]:
            preflight_results.extend(_materialize_case(case, temporary / case["id"]))
        (temporary / OWNER_FILE).write_text(
            json.dumps(
                {
                    "schema": "cotend.generated-reviewer-fixtures",
                    "schema_version": 1,
                    "source_sha256": validation["contract_sha256"],
                },
                indent=2,
                ensure_ascii=True,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        if output.exists():
            _verify_existing_owned_output(output, contract)
            remove_generated_tree(output)
        os.replace(temporary, output)
        return {
            "status": contract["status"],
            "output": str(output),
            "case_count": validation["case_count"],
            "positive_count": validation["positive_count"],
            "negative_count": validation["negative_count"],
            "preflight_count": len(preflight_results),
            "preflight_passed": sum(
                item["actual_exit_code"] == 0 for item in preflight_results
            ),
            "preflight_expected_failures": sum(
                item["actual_exit_code"] != 0 for item in preflight_results
            ),
            "model_execution_performed": False,
            "contract_sha256": validation["contract_sha256"],
        }
    finally:
        if temporary.exists():
            remove_generated_tree(temporary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare deterministic disposable Git projects for the 5+3 reviewer cases."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = prepare_fixtures(args.output)
    except (ReviewerFixtureError, package.PluginPackageError) as exc:
        print(f"REVIEWER_FIXTURES_FAILED reason={exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    else:
        print(
            "REVIEWER_FIXTURES_OK "
            f"cases={result['case_count']} positive={result['positive_count']} "
            f"negative={result['negative_count']} preflight={result['preflight_count']} "
            f"expected_failures={result['preflight_expected_failures']} "
            "model_execution=false"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
