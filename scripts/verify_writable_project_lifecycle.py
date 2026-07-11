from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import verify_isolated_codex_carrier as carrier


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "tests" / "fixtures" / "codex-writable-lifecycle"
PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_FIXTURE = PRIVATE_ROOT / "L22-writable-project-lifecycle"
PROJECTS_DIR = "projects"
FRESH_PROJECT = "fresh-init"
EXPECTED_SCENARIOS = {
    "fresh-init",
    "current-resume",
    "pending-decision",
    "partial-repair",
}
EXPECTED_TEMPLATE_FILES = {
    "AGENTS.md",
    "README.md",
    "lifecycle-result.schema.json",
    "live-scenarios.json",
    "project-template/README.md",
    "project-template/USER-NOTES.md",
    "project-template/src/calculator.py",
}
FRESH_ALLOWED_CHANGES = {"STATUS.md", "REVIEW-LOG.md"}
CONTROL_PLANE_ALLOWED_CHANGES = {"STATUS.md", "REVIEW-LOG.md"}
PENDING_QUESTION_ID = "L22-Q1"
BUILT_IN_PERMISSION_PROFILE = ":workspace"
LIVE_MODEL = "gpt-5.4"
LIVE_REASONING_EFFORT = "high"
LIVE_EXECUTION_DEFERRED = True


class LifecycleError(RuntimeError):
    pass


def require_live_execution_enabled() -> None:
    if LIVE_EXECUTION_DEFERRED:
        raise LifecycleError(
            "live lifecycle execution is deferred; run deterministic checks only"
        )


def guarded_fixture(path: Path) -> Path:
    private_root = PRIVATE_ROOT.resolve()
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(private_root)
    except ValueError as exc:
        raise LifecycleError("fixture must stay under .private-provenance") from exc
    if not relative.parts:
        raise LifecycleError("fixture cannot be the .private-provenance root")
    return resolved


def remove_fixture_tree(path: Path) -> None:
    path = guarded_fixture(path)

    def make_writable_and_retry(
        function: Any,
        failed_path: str,
        _error: Any,
    ) -> None:
        os.chmod(failed_path, stat.S_IWRITE)
        function(failed_path)

    shutil.rmtree(path, onerror=make_writable_and_retry)


def archive_previous_run_artifacts(fixture: Path) -> None:
    artifact_names = [
        name for name in ("runs", "evidence") if (fixture / name).exists()
    ]
    if not artifact_names:
        return
    history = fixture / "history"
    history.mkdir(parents=True, exist_ok=True)
    run_number = 1
    while (history / f"run-{run_number:03d}").exists():
        run_number += 1
    archive = history / f"run-{run_number:03d}"
    archive.mkdir()
    for name in artifact_names:
        shutil.move(str(fixture / name), str(archive / name))


def project_manifest(project: Path) -> dict[str, str]:
    return carrier.file_manifest(project, exclude={".git"})


def repository_outside_fixture_manifest() -> dict[str, str]:
    return carrier.file_manifest(
        ROOT,
        exclude={".git", ".codegraph", ".private-provenance", "__pycache__"},
    )


def git(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=project,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git_head(project: Path) -> str:
    return git(project, "rev-parse", "HEAD").stdout.strip()


def commit_fixture_state(project: Path, message: str) -> str:
    git(project, "add", "--all")
    git(
        project,
        "-c",
        "user.name=CoTend Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "--quiet",
        "-m",
        message,
    )
    return git_head(project)


def install_skills(project: Path) -> None:
    target = project / ".agents" / "skills"
    target.mkdir(parents=True)
    for skill in sorted(carrier.EXPECTED_SKILLS):
        shutil.copytree(carrier.SOURCE_ROOT / skill, target / skill)


def initialize_nested_repo(project: Path) -> None:
    subprocess.run(
        ["git", "init", "--quiet", "--initial-branch=main", str(project)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    commit_fixture_state(project, "fixture: initial project")


def prepare_fixture(fixture: Path) -> Path:
    fixture = guarded_fixture(fixture)
    if fixture.exists():
        archive_previous_run_artifacts(fixture)
        for name in ("support", PROJECTS_DIR):
            path = fixture / name
            if path.exists():
                remove_fixture_tree(path)
    support = fixture / "support"
    shutil.copytree(TEMPLATE_ROOT, support)
    project = fixture / PROJECTS_DIR / FRESH_PROJECT
    shutil.copytree(support / "project-template", project)
    shutil.copy2(support / "AGENTS.md", project / "AGENTS.md")
    install_skills(project)
    initialize_nested_repo(project)
    return project


def changed_paths(before: dict[str, str], after: dict[str, str]) -> set[str]:
    return {
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    }


def assert_allowed_changes(
    before: dict[str, str],
    after: dict[str, str],
    allowed: set[str],
    *,
    exact: bool = False,
) -> set[str]:
    changed = changed_paths(before, after)
    if exact and changed != allowed:
        raise LifecycleError(
            f"expected exact changes {sorted(allowed)}, found {sorted(changed)}"
        )
    unexpected = changed - allowed
    if unexpected:
        raise LifecycleError(f"unexpected project changes: {sorted(unexpected)}")
    return changed


def require_markers(path: Path, markers: tuple[str, ...]) -> str:
    if not path.is_file():
        raise LifecycleError(f"required durable file is missing: {path.name}")
    text = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise LifecycleError(f"{path.name} is missing markers: {missing}")
    return text


def scenario_map(support: Path) -> dict[str, dict[str, Any]]:
    scenarios = json.loads(
        (support / "live-scenarios.json").read_text(encoding="utf-8")
    )
    result = {
        item["id"]: item
        for item in scenarios
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if set(result) != EXPECTED_SCENARIOS or len(scenarios) != 4:
        raise LifecycleError("writable lifecycle scenario inventory drift")
    return result


def build_codex_command(
    project: Path,
    schema_path: Path,
    output_path: Path,
) -> list[str]:
    return [
        carrier.codex_executable(),
        "--ask-for-approval",
        "never",
        "-c",
        f'default_permissions="{BUILT_IN_PERMISSION_PROFILE}"',
        "-c",
        f'model_reasoning_effort="{LIVE_REASONING_EFFORT}"',
        "--model",
        LIVE_MODEL,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--json",
        "--color",
        "never",
        "--cd",
        str(project),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
        "-",
    ]


def validate_codex_command(command: list[str]) -> None:
    required = {
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--output-schema",
        "--output-last-message",
    }
    missing = required - set(command)
    if missing:
        raise LifecycleError(f"Codex command is missing boundaries: {sorted(missing)}")
    try:
        approval = command[command.index("--ask-for-approval") + 1]
    except (ValueError, IndexError) as exc:
        raise LifecycleError("Codex command boundary is malformed") from exc
    if approval != "never":
        raise LifecycleError("Codex command must not request interactive approval")
    if command.index("--ask-for-approval") > command.index("exec"):
        raise LifecycleError("ask-for-approval must precede exec")
    try:
        model = command[command.index("--model") + 1]
    except (ValueError, IndexError) as exc:
        raise LifecycleError("Codex command model boundary is malformed") from exc
    if model != LIVE_MODEL or command.index("--model") > command.index("exec"):
        raise LifecycleError("Codex command must pin the compatible live model")
    effort_override = f'model_reasoning_effort="{LIVE_REASONING_EFFORT}"'
    if effort_override not in command:
        raise LifecycleError("Codex command must pin compatible reasoning effort")
    effort_index = command.index(effort_override)
    if effort_index == 0 or command[effort_index - 1] != "-c":
        raise LifecycleError("reasoning effort override is malformed")
    if effort_index > command.index("exec"):
        raise LifecycleError("reasoning effort override must precede exec")
    permission_override = f'default_permissions="{BUILT_IN_PERMISSION_PROFILE}"'
    if permission_override not in command:
        raise LifecycleError("Codex command must select the built-in workspace profile")
    override_index = command.index(permission_override)
    if override_index == 0 or command[override_index - 1] != "-c":
        raise LifecycleError("workspace permission profile override is malformed")
    if override_index > command.index("exec"):
        raise LifecycleError("workspace permission profile must precede exec")
    if "--sandbox" in command:
        raise LifecycleError(
            "legacy sandbox policy must not override permission profile"
        )
    forbidden = {
        "danger-full-access",
        ":danger-no-sandbox",
        'default_permissions=":danger-no-sandbox"',
        "--dangerously-bypass-approvals-and-sandbox",
    }
    if forbidden & set(command):
        raise LifecycleError("Codex command widens the approved sandbox")


def verify_static(fixture: Path) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    support = fixture / "support"
    project = fixture / PROJECTS_DIR / FRESH_PROJECT
    if LIVE_EXECUTION_DEFERRED is not True:
        raise LifecycleError("live execution must remain deferred in this baseline")
    protected_snapshot = carrier.protected_global_snapshot()
    for key in ("codex_config_stat", "codex_auth_stat"):
        if key not in protected_snapshot:
            raise LifecycleError(f"protected snapshot is missing {key}")
        metadata = protected_snapshot[key]
        if set(metadata) - {"exists", "size", "mtime_ns"}:
            raise LifecycleError(f"{key} must remain stat-only")
    actual_template_files = set(carrier.file_manifest(support))
    if actual_template_files != EXPECTED_TEMPLATE_FILES:
        raise LifecycleError("writable lifecycle support inventory drift")
    if carrier.file_manifest(TEMPLATE_ROOT) != carrier.file_manifest(support):
        raise LifecycleError(
            "copied lifecycle support differs from repository template"
        )

    installed = project / ".agents" / "skills"
    if carrier.file_manifest(installed) != carrier.file_manifest(carrier.SOURCE_ROOT):
        raise LifecycleError("fixture Skill files differ from repository source")
    if len(carrier.file_manifest(installed)) != 30:
        raise LifecycleError("fixture must contain exactly 30 Skill files")
    discovered_skills = {path.name for path in installed.iterdir() if path.is_dir()}
    if discovered_skills != carrier.EXPECTED_SKILLS:
        raise LifecycleError("fixture Skill directory inventory drift")

    top_level = Path(git(project, "rev-parse", "--show-toplevel").stdout.strip())
    if top_level.resolve() != project.resolve():
        raise LifecycleError("fixture project is not an isolated nested Git repository")
    if git(project, "status", "--porcelain").stdout:
        raise LifecycleError("prepared fixture project must start clean")
    scenario_map(support)

    probe = build_codex_command(
        project,
        support / "lifecycle-result.schema.json",
        fixture / "runs" / "probe.json",
    )
    validate_codex_command(probe)
    return {
        "skills": len(discovered_skills),
        "skill_files": len(carrier.file_manifest(installed)),
        "support_files": len(actual_template_files),
        "scenarios": len(EXPECTED_SCENARIOS),
    }


def expect_lifecycle_error(action: Any, label: str) -> None:
    try:
        action()
    except LifecycleError:
        return
    raise LifecycleError(f"negative mutation was not rejected: {label}")


def run_negative_mutations(fixture: Path) -> int:
    fixture = guarded_fixture(fixture)
    project = fixture / PROJECTS_DIR / FRESH_PROJECT
    support = fixture / "support"
    command = build_codex_command(
        project,
        support / "lifecycle-result.schema.json",
        fixture / "runs" / "negative.json",
    )
    cases = 0

    expect_lifecycle_error(
        lambda: guarded_fixture(ROOT / "escaped-lifecycle-fixture"),
        "fixture path escape",
    )
    cases += 1

    missing_ephemeral = [item for item in command if item != "--ephemeral"]
    expect_lifecycle_error(
        lambda: validate_codex_command(missing_ephemeral),
        "missing ephemeral boundary",
    )
    cases += 1

    missing_profile = [
        item
        for item in command
        if item != f'default_permissions="{BUILT_IN_PERMISSION_PROFILE}"'
    ]
    expect_lifecycle_error(
        lambda: validate_codex_command(missing_profile),
        "missing workspace permission profile",
    )
    cases += 1

    widened = list(command)
    profile_index = widened.index(
        f'default_permissions="{BUILT_IN_PERMISSION_PROFILE}"'
    )
    widened[profile_index] = 'default_permissions=":danger-no-sandbox"'
    expect_lifecycle_error(
        lambda: validate_codex_command(widened),
        "widened permission profile",
    )
    cases += 1

    before = {"README.md": "a", "STATUS.md": "old"}
    product_mutation = {"README.md": "b", "STATUS.md": "new"}
    expect_lifecycle_error(
        lambda: assert_allowed_changes(
            before,
            product_mutation,
            CONTROL_PLANE_ALLOWED_CHANGES,
        ),
        "protected product mutation",
    )
    cases += 1

    unexpected_file = {**before, "notes.tmp": "new"}
    expect_lifecycle_error(
        lambda: assert_allowed_changes(
            before,
            unexpected_file,
            CONTROL_PLANE_ALLOWED_CHANGES,
        ),
        "unexpected file creation",
    )
    cases += 1

    pending = support / "negative-pending.md"
    pending.write_text("id: L22-Q1\nselected_option: 1\n", encoding="utf-8")
    try:
        expect_lifecycle_error(
            lambda: require_markers(
                pending,
                ("id: L22-Q1", "selected_option: null"),
            ),
            "pending option selection",
        )
    finally:
        pending.unlink()
    cases += 1
    return cases


def validate_result(scenario_id: str, result: dict[str, Any]) -> None:
    expected = {
        "fresh-init": ("fresh_init", {"continue_ready"}),
        "current-resume": ("current_resume", {"continue_ready"}),
        "pending-decision": ("blocked_human_decision", {"human_needed"}),
        "partial-repair": (
            "partial_repair",
            {"continue_ready", "review_pending"},
        ),
    }
    expected_mode, expected_readiness = expected[scenario_id]
    if result.get("scenario_id") != scenario_id:
        raise LifecycleError(f"{scenario_id}: scenario id mismatch")
    if result.get("invoked_skill") != "cotend-init":
        raise LifecycleError(f"{scenario_id}: invoked Skill mismatch")
    if result.get("auto_mode") != expected_mode:
        raise LifecycleError(f"{scenario_id}: Auto Mode mismatch")
    if result.get("readiness") not in expected_readiness:
        raise LifecycleError(f"{scenario_id}: readiness mismatch")
    if result.get("adoption_profile") != "lite":
        raise LifecycleError(f"{scenario_id}: expected lite profile")
    if result.get("protected_product_files_modified") is not False:
        raise LifecycleError(f"{scenario_id}: model reported product modification")
    if result.get("git_commit_created") is not False:
        raise LifecycleError(f"{scenario_id}: model reported a Git commit")

    if scenario_id == "pending-decision":
        pending_expected = {
            "pending_question_id": PENDING_QUESTION_ID,
            "bare_continue_answered_question": False,
            "selected_option": None,
        }
        for key, value in pending_expected.items():
            if result.get(key) != value:
                raise LifecycleError(f"{scenario_id}: result mismatch for {key}")
    if scenario_id == "partial-repair" and result.get("repair_applied") is not True:
        raise LifecycleError("partial-repair: repair was not reported")


def validate_project_result(
    scenario_id: str,
    project: Path,
    before: dict[str, str],
    after: dict[str, str],
) -> set[str]:
    if scenario_id == "fresh-init":
        changed = assert_allowed_changes(
            before,
            after,
            FRESH_ALLOWED_CHANGES,
            exact=True,
        )
        require_markers(
            project / "STATUS.md",
            (
                "cotend-collaboration-v1.52",
                "auto_mode: fresh_init",
                "adoption_profile: lite",
                "readiness: continue_ready",
            ),
        )
        require_markers(project / "REVIEW-LOG.md", ("CodexSelf",))
        return changed

    changed = assert_allowed_changes(
        before,
        after,
        CONTROL_PLANE_ALLOWED_CHANGES,
    )
    if scenario_id == "current-resume":
        require_markers(
            project / "STATUS.md",
            ("cotend-collaboration-v1.52", "adoption_profile: lite"),
        )
    elif scenario_id == "pending-decision":
        require_markers(
            project / "STATUS.md",
            (
                f"id: {PENDING_QUESTION_ID}",
                "readiness: human_needed",
                "selected_option: null",
            ),
        )
    elif scenario_id == "partial-repair":
        require_markers(project / "REVIEW-LOG.md", ("CodexSelf",))
    return changed


def run_live_scenario(
    fixture: Path,
    project: Path,
    scenario: dict[str, Any],
    *,
    command_runner: Any = None,
    global_snapshot: Any = None,
) -> dict[str, Any]:
    if command_runner is None:
        require_live_execution_enabled()
    scenario_id = scenario["id"]
    run_root = fixture / "runs" / scenario_id
    run_root.mkdir(parents=True, exist_ok=True)
    output_path = run_root / "last-message.json"
    stdout_path = run_root / "events.jsonl"
    stderr_path = run_root / "stderr.txt"
    schema_path = fixture / "support" / "lifecycle-result.schema.json"

    project_before = project_manifest(project)
    head_before = git_head(project)
    repository_before = repository_outside_fixture_manifest()
    execute_command = command_runner or subprocess.run
    snapshot_global = global_snapshot or carrier.protected_global_snapshot
    global_before = snapshot_global()
    command = build_codex_command(project, schema_path, output_path)
    validate_codex_command(command)
    result: dict[str, Any] | None = None
    changed: set[str] | None = None
    scenario_error: Exception | None = None
    try:
        completed = execute_command(
            command,
            cwd=project,
            input=scenario["prompt"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        if completed.returncode != 0:
            raise LifecycleError(
                f"{scenario_id}: codex exec failed with {completed.returncode}; "
                "see ignored run evidence"
            )
        if not output_path.is_file():
            raise LifecycleError(f"{scenario_id}: no final structured result")
        result = json.loads(output_path.read_text(encoding="utf-8"))
        validate_result(scenario_id, result)

        project_after = project_manifest(project)
        changed = validate_project_result(
            scenario_id,
            project,
            project_before,
            project_after,
        )
    except Exception as exc:
        scenario_error = exc

    project_after = project_manifest(project)
    allowed_project_changes = (
        FRESH_ALLOWED_CHANGES
        if scenario_id == "fresh-init"
        else CONTROL_PLANE_ALLOWED_CHANGES
    )
    unexpected_project_changes = sorted(
        changed_paths(project_before, project_after) - allowed_project_changes
    )
    head_after = git_head(project)
    repository_after = repository_outside_fixture_manifest()
    global_after = snapshot_global()
    global_changed_keys = sorted(
        key
        for key in global_before.keys() | global_after.keys()
        if global_before.get(key) != global_after.get(key)
    )
    boundary_result = {
        "project_protected_files_unchanged": not unexpected_project_changes,
        "unexpected_project_changed_paths": unexpected_project_changes,
        "nested_git_head_unchanged": head_after == head_before,
        "repository_outside_fixture_unchanged": repository_after == repository_before,
        "protected_global_state_unchanged": not global_changed_keys,
        "protected_global_changed_keys": global_changed_keys,
    }
    (run_root / "boundary-result.json").write_text(
        json.dumps(boundary_result, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    boundary_violations = [
        name for name, passed in boundary_result.items() if passed is False
    ]
    if unexpected_project_changes:
        boundary_violations.append(
            "unexpected_project_changed_paths=" + ",".join(unexpected_project_changes)
        )
    if global_changed_keys:
        boundary_violations.append(
            "protected_global_changed_keys=" + ",".join(global_changed_keys)
        )
    if boundary_violations:
        prior = f"; prior scenario error: {scenario_error}" if scenario_error else ""
        raise LifecycleError(
            f"{scenario_id}: protected boundary failure: "
            f"{'; '.join(boundary_violations)}{prior}"
        ) from scenario_error
    if scenario_error is not None:
        raise scenario_error
    if result is None or changed is None:
        raise LifecycleError(f"{scenario_id}: missing validated scenario result")
    return {
        "id": scenario_id,
        "permission_profile": BUILT_IN_PERMISSION_PROFILE,
        "model": LIVE_MODEL,
        "reasoning_effort": LIVE_REASONING_EFFORT,
        "ephemeral": True,
        "changed_paths": sorted(changed),
        **boundary_result,
        "result": result,
    }


def run_boundary_fault_injections(fixture: Path) -> int:
    fixture = guarded_fixture(fixture)
    case_fixture = guarded_fixture(fixture / "boundary-fault-injection")
    base_snapshot = {
        "codex_config_stat": {"exists": True, "size": 10, "mtime_ns": 1},
        "codex_auth_stat": {"exists": True, "size": 20, "mtime_ns": 1},
    }
    changed_snapshot = {
        "codex_config_stat": {"exists": True, "size": 10, "mtime_ns": 2},
        "codex_auth_stat": {"exists": True, "size": 20, "mtime_ns": 1},
    }
    cases = (
        ("global-stat", False, changed_snapshot),
        ("protected-product", True, base_snapshot),
    )
    passed = 0
    try:
        for case_id, mutate_product, after_snapshot in cases:
            if case_fixture.exists():
                remove_fixture_tree(case_fixture)
            project = prepare_fixture(case_fixture)
            scenario = scenario_map(case_fixture / "support")["fresh-init"]
            snapshots = iter((base_snapshot, after_snapshot))

            def injected_snapshot() -> dict[str, Any]:
                return next(snapshots)

            def injected_runner(
                command: list[str],
                *args: Any,
                **kwargs: Any,
            ) -> subprocess.CompletedProcess[str]:
                del args, kwargs
                if mutate_product:
                    (project / "USER-NOTES.md").write_text(
                        "injected protected mutation\n",
                        encoding="utf-8",
                    )
                output_path = Path(command[command.index("--output-last-message") + 1])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(
                    json.dumps(
                        {
                            "scenario_id": "fresh-init",
                            "invoked_skill": "cotend-init",
                            "auto_mode": "fresh_init",
                            "readiness": "human_needed",
                            "adoption_profile": "lite",
                            "durable_files_created": [],
                            "durable_files_updated": [],
                            "protected_product_files_modified": False,
                            "git_commit_created": False,
                            "pending_question_id": None,
                            "bare_continue_answered_question": None,
                            "selected_option": None,
                            "repair_applied": False,
                            "summary": "injected semantic failure",
                        }
                    ),
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, "", "")

            try:
                run_live_scenario(
                    case_fixture,
                    project,
                    scenario,
                    command_runner=injected_runner,
                    global_snapshot=injected_snapshot,
                )
            except LifecycleError as exc:
                message = str(exc)
                if "protected boundary failure" not in message:
                    raise LifecycleError(
                        f"{case_id}: boundary failure did not take priority"
                    ) from exc
                if "readiness mismatch" not in message:
                    raise LifecycleError(
                        f"{case_id}: prior semantic failure was not retained"
                    ) from exc
            else:
                raise LifecycleError(f"{case_id}: injected boundary failure passed")

            boundary = json.loads(
                (
                    case_fixture / "runs" / "fresh-init" / "boundary-result.json"
                ).read_text(encoding="utf-8")
            )
            if case_id == "global-stat":
                if boundary["protected_global_changed_keys"] != ["codex_config_stat"]:
                    raise LifecycleError("global stat injection was not captured")
            elif boundary["unexpected_project_changed_paths"] != ["USER-NOTES.md"]:
                raise LifecycleError("protected product injection was not captured")
            passed += 1
    finally:
        if case_fixture.exists():
            remove_fixture_tree(case_fixture)
    return passed


def clone_initialized_project(
    fixture: Path,
    source: Path,
    scenario_id: str,
) -> Path:
    target = fixture / PROJECTS_DIR / scenario_id
    shutil.copytree(source, target)
    if git(target, "status", "--porcelain").stdout:
        raise LifecycleError(f"{scenario_id}: cloned initialized project is dirty")
    return target


def add_pending_gate(project: Path) -> None:
    status = project / "STATUS.md"
    with status.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(
            "\n## Current Human Gate\n\n"
            "This is the latest authoritative project state and supersedes any "
            "earlier readiness line.\n\n"
            "```yaml\n"
            "readiness: human_needed\n"
            "can_continue_with_continue: no\n"
            "pending_human_decision:\n"
            f"  id: {PENDING_QUESTION_ID}\n"
            "  question: Choose the persistence strategy before development.\n"
            "  options:\n"
            "    - local_json\n"
            "    - sqlite\n"
            "  selected_option: null\n"
            "```\n"
        )
    commit_fixture_state(project, "fixture: add pending human decision")


def remove_required_review_log(project: Path) -> None:
    review_log = project / "REVIEW-LOG.md"
    if not review_log.is_file():
        raise LifecycleError("cannot prepare repair scenario without REVIEW-LOG.md")
    review_log.unlink()
    commit_fixture_state(project, "fixture: remove required review log")


def run_live_suite(fixture: Path, requested: str) -> list[dict[str, Any]]:
    require_live_execution_enabled()
    scenarios = scenario_map(fixture / "support")
    fresh_project = fixture / PROJECTS_DIR / FRESH_PROJECT
    results = [run_live_scenario(fixture, fresh_project, scenarios["fresh-init"])]
    if requested == "fresh-init":
        return results

    commit_fixture_state(fresh_project, "fixture: accept generated init baseline")
    selected = (
        ["current-resume", "pending-decision", "partial-repair"]
        if requested == "all"
        else [requested]
    )
    for scenario_id in selected:
        project = clone_initialized_project(fixture, fresh_project, scenario_id)
        if scenario_id == "pending-decision":
            add_pending_gate(project)
        elif scenario_id == "partial-repair":
            remove_required_review_log(project)
        result = run_live_scenario(fixture, project, scenarios[scenario_id])
        results.append(result)
    return results


def write_evidence(path: Path | None, evidence: dict[str, Any]) -> None:
    if path is None:
        return
    target = guarded_fixture(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(evidence, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the writable CoTend project lifecycle"
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Git-ignored fixture path under .private-provenance",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="rebuild the writable fixture before static checks",
    )
    parser.add_argument(
        "--negative-mutations",
        action="store_true",
        help="run nine deterministic guardrail failure cases",
    )
    parser.add_argument(
        "--live",
        choices=["all", *sorted(EXPECTED_SCENARIOS)],
        help="reserved for future platform revalidation; currently deferred",
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        help="write redacted JSON under the ignored fixture",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture = guarded_fixture(args.fixture)
    evidence: dict[str, Any] = {}
    try:
        if args.live:
            require_live_execution_enabled()
        if args.prepare or args.live:
            prepare_fixture(fixture)
        static = verify_static(fixture)
        evidence["static"] = static
        print(
            "WRITABLE_LIFECYCLE_STATIC_OK "
            f"skills={static['skills']} skill_files={static['skill_files']} "
            f"support_files={static['support_files']} "
            f"scenarios={static['scenarios']}"
        )

        if args.negative_mutations:
            mutations = run_negative_mutations(fixture)
            boundary_mutations = run_boundary_fault_injections(fixture)
            total_mutations = mutations + boundary_mutations
            evidence["negative_mutations"] = {
                "passed": total_mutations,
                "total": 9,
                "boundary_priority": boundary_mutations,
            }
            print(
                "WRITABLE_LIFECYCLE_NEGATIVE_MUTATIONS_OK " f"cases={total_mutations}"
            )

        if args.live:
            live_results = run_live_suite(fixture, args.live)
            evidence["live"] = live_results
            for result in live_results:
                print(
                    f"WRITABLE_LIFECYCLE_LIVE_OK id={result['id']} "
                    f"permission_profile={BUILT_IN_PERMISSION_PROFILE} "
                    f"model={LIVE_MODEL} reasoning={LIVE_REASONING_EFFORT}"
                )
        write_evidence(args.evidence, evidence)
    except (
        LifecycleError,
        carrier.CarrierError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print("WRITABLE_LIFECYCLE_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
