from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "skills"
TEMPLATE_ROOT = ROOT / "tests" / "fixtures" / "codex-carrier"
PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_FIXTURE = PRIVATE_ROOT / "L21-isolated-codex-carrier"
EXTERNAL_RUNTIME_PREFIX = "cotend-L21-runtime-"
EXPECTED_SKILLS = {
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-init",
    "cotend-model-upgrade",
    "cotend-project-init",
    "grill-me",
    "karpathy-guidelines",
}
EXPECTED_INTERFACES = {
    "cotend-collaboration": (
        "CoTend Collaboration",
        "CodexSelf-first AI review",
    ),
    "cotend-diagnose-only": (
        "CoTend Diagnose Only",
        "Read-only root-cause analysis",
    ),
    "cotend-init": (
        "CoTend Init",
        "Auto init/update workflow",
    ),
    "cotend-model-upgrade": (
        "CoTend Model Upgrade",
        "Premium model project handoff",
    ),
    "cotend-project-init": (
        "CoTend Project Init",
        "Route and init AI workflow",
    ),
}
LIVE_SCENARIO_IDS = {"init-delegation", "pending-decision", "diagnose-only"}


class CarrierError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_manifest(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    excluded = exclude or set()
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not any(part in excluded for part in path.relative_to(root).parts)
    }


def metadata_snapshot(path: Path, *, contents: bool = True) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False}
    stat = path.stat()
    result: dict[str, Any] = {
        "exists": True,
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }
    if contents and path.is_file():
        result["sha256"] = sha256(path)
    elif contents and path.is_dir():
        result["manifest"] = file_manifest(path)
    return result


def protected_global_snapshot() -> dict[str, Any]:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    return {
        "user_agent_skills": metadata_snapshot(home / ".agents" / "skills"),
        "codex_skills": metadata_snapshot(codex_home / "skills"),
        # Stat only: the harness must never open or hash config or credential contents.
        "codex_config_stat": metadata_snapshot(
            codex_home / "config.toml", contents=False
        ),
        "codex_auth_stat": metadata_snapshot(codex_home / "auth.json", contents=False),
    }


def guarded_fixture(path: Path) -> Path:
    private_root = PRIVATE_ROOT.resolve()
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(private_root)
    except ValueError as exc:
        raise CarrierError("fixture must stay under .private-provenance") from exc
    if not relative.parts:
        raise CarrierError("fixture cannot be the .private-provenance root")
    return resolved


def guarded_external_runtime_root(path: Path) -> Path:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.expanduser().resolve()
    try:
        relative = resolved.relative_to(temp_root)
    except ValueError as exc:
        raise CarrierError("external runtime root must stay under system temp") from exc
    if len(relative.parts) != 1 or not relative.name.startswith(
        EXTERNAL_RUNTIME_PREFIX
    ):
        raise CarrierError("external runtime root identity is invalid")
    return resolved


def reject_symlink_tree(root: Path) -> None:
    if root.is_symlink():
        raise CarrierError("external runtime root cannot be a symlink")
    for path in root.rglob("*"):
        if path.is_symlink():
            raise CarrierError("external runtime tree cannot contain symlinks")


def create_external_runtime_copy(fixture: Path) -> tuple[Path, Path]:
    fixture = guarded_fixture(fixture)
    runtime_root = guarded_external_runtime_root(
        Path(tempfile.mkdtemp(prefix=EXTERNAL_RUNTIME_PREFIX))
    )
    runtime_fixture = runtime_root / "project"
    try:
        shutil.copytree(fixture, runtime_fixture)
        if file_manifest(fixture, exclude={"runs"}) != file_manifest(
            runtime_fixture, exclude={"runs"}
        ):
            raise CarrierError("external runtime copy differs from ignored fixture")
        return runtime_root, runtime_fixture
    except Exception:
        remove_external_runtime_root(runtime_root)
        raise


def remove_external_runtime_root(
    path: Path, *, timeout_seconds: float = 45.0, retry_seconds: float = 0.1
) -> int:
    root = guarded_external_runtime_root(path)
    if not root.exists():
        return 0
    reject_symlink_tree(root)
    deadline = time.monotonic() + timeout_seconds
    retries = 0

    def make_writable_and_retry(function: Any, raw_path: str, _: Any) -> None:
        target = Path(raw_path).resolve(strict=False)
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise CarrierError("external runtime cleanup escaped its root") from exc
        os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
        function(raw_path)

    while root.exists():
        try:
            shutil.rmtree(root, onerror=make_writable_and_retry)
        except OSError as exc:
            if getattr(exc, "winerror", None) not in {5, 32}:
                raise
            if time.monotonic() >= deadline:
                raise
            retries += 1
            time.sleep(retry_seconds)
    return retries


def codex_executable() -> str:
    executable = shutil.which("codex")
    if executable is None:
        raise CarrierError("codex executable is unavailable")
    return executable


def prepare_fixture(fixture: Path) -> None:
    fixture = guarded_fixture(fixture)
    if fixture.exists():
        shutil.rmtree(fixture)
    shutil.copytree(TEMPLATE_ROOT, fixture)
    target_root = fixture / ".agents" / "skills"
    target_root.mkdir(parents=True)
    for skill in sorted(EXPECTED_SKILLS):
        shutil.copytree(SOURCE_ROOT / skill, target_root / skill)
    subprocess.run(
        ["git", "init", "--quiet", "--initial-branch=main", str(fixture)],
        check=True,
        capture_output=True,
        text=True,
    )


def frontmatter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^---\s*$.*?^name:\s*([^\s#]+)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def frontmatter_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(?P<header>.*?)\n---\s*\n", text, re.DOTALL)
    if match is None:
        raise CarrierError(f"missing frontmatter: {path.name}")
    header = match.group("header")
    folded = re.search(
        r"^description:\s*>-\s*\n(?P<body>(?:[ \t]+.+\n?)+)",
        header,
        re.MULTILINE,
    )
    if folded:
        return " ".join(line.strip() for line in folded.group("body").splitlines())
    plain = re.search(r"^description:\s*(.+)$", header, re.MULTILINE)
    if plain:
        return plain.group(1).strip().strip('"')
    raise CarrierError(f"missing description: {path.name}")


def parse_interface(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(
            r'^  (display_name|short_description|default_prompt):\s*(".*")\s*$',
            line,
        )
        if match:
            values[match.group(1)] = json.loads(match.group(2))
    return values


def validate_interface_values(skill: str, values: dict[str, str]) -> None:
    display_name, short_description = EXPECTED_INTERFACES[skill]
    if values.get("display_name") != display_name:
        raise CarrierError(f"display name mismatch: {skill}")
    if values.get("short_description") != short_description:
        raise CarrierError(f"short description mismatch: {skill}")
    default_prompt = values.get("default_prompt", "")
    if not default_prompt.startswith(f"Use ${skill}"):
        raise CarrierError(f"default prompt mismatch: {skill}")
    if len(default_prompt) > 1024:
        raise CarrierError(f"default prompt exceeds Codex limit: {skill}")


def verify_static(
    fixture: Path,
    *,
    allow_unrelated_skills: bool = False,
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    source_manifest = file_manifest(SOURCE_ROOT)
    target_root = fixture / ".agents" / "skills"
    target_manifest = file_manifest(target_root)
    invalid_root_entries = sorted(
        path.name
        for path in target_root.iterdir()
        if path.is_symlink() or not path.is_dir()
    )
    if invalid_root_entries:
        raise CarrierError(
            f"installed Skill root contains invalid entries: {invalid_root_entries}"
        )
    target_skills = {path.name for path in target_root.iterdir() if path.is_dir()}
    missing_skills = EXPECTED_SKILLS - target_skills
    unrelated_skills = target_skills - EXPECTED_SKILLS
    if missing_skills or (unrelated_skills and not allow_unrelated_skills):
        raise CarrierError(f"unexpected installed Skill set: {sorted(target_skills)}")

    managed_manifest = {
        path: digest
        for path, digest in target_manifest.items()
        if path.split("/", 1)[0] in EXPECTED_SKILLS
    }
    if source_manifest != managed_manifest:
        raise CarrierError("installed Skill files differ from repository source")
    if len(managed_manifest) != 30:
        raise CarrierError(f"expected 30 managed Skill files, found {len(managed_manifest)}")

    for skill in sorted(EXPECTED_SKILLS):
        skill_file = target_root / skill / "SKILL.md"
        if frontmatter_name(skill_file) != skill:
            raise CarrierError(f"Skill name mismatch: {skill}")
        frontmatter_description(skill_file)
        agent_file = target_root / skill / "agents" / "openai.yaml"
        if skill in EXPECTED_INTERFACES:
            values = parse_interface(agent_file)
            validate_interface_values(skill, values)
        elif agent_file.exists():
            raise CarrierError(
                f"companion Skill unexpectedly has OpenAI metadata: {skill}"
            )

    for skill in sorted(unrelated_skills):
        skill_file = target_root / skill / "SKILL.md"
        if not skill_file.is_file() or frontmatter_name(skill_file) != skill:
            raise CarrierError(f"unrelated fixture Skill is invalid: {skill}")
        frontmatter_description(skill_file)

    git_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=fixture,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if Path(git_root).resolve() != fixture:
        raise CarrierError("fixture is not an isolated nested Git repository")
    return {
        "skills": len(EXPECTED_SKILLS),
        "files": len(managed_manifest),
        "interfaces": len(EXPECTED_INTERFACES),
        "fixture_skills": len(target_skills),
        "fixture_files": len(target_manifest),
        "unrelated_skills": sorted(unrelated_skills),
    }


def expect_carrier_error(action: Any, label: str) -> None:
    try:
        action()
    except CarrierError:
        return
    raise CarrierError(f"negative mutation was not rejected: {label}")


def run_negative_mutations(fixture: Path) -> int:
    negative_fixture = guarded_fixture(
        fixture.with_name(f"{fixture.name}-negative-mutations")
    )
    cases = 0
    try:
        prepare_fixture(negative_fixture)
        tampered = negative_fixture / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        tampered.write_text(
            tampered.read_text(encoding="utf-8") + "\nmutation\n",
            encoding="utf-8",
        )
        expect_carrier_error(lambda: verify_static(negative_fixture), "file tamper")
        cases += 1

        prepare_fixture(negative_fixture)
        missing = negative_fixture / ".agents" / "skills" / "cotend-model-upgrade"
        shutil.rmtree(missing)
        expect_carrier_error(lambda: verify_static(negative_fixture), "missing Skill")
        cases += 1

        prepare_fixture(negative_fixture)
        shutil.rmtree(negative_fixture / ".git")
        expect_carrier_error(
            lambda: verify_static(negative_fixture),
            "missing nested Git isolation",
        )
        cases += 1

        display_name, short_description = EXPECTED_INTERFACES["cotend-init"]
        overlong = {
            "display_name": display_name,
            "short_description": short_description,
            "default_prompt": "Use $cotend-init " + ("x" * 1024),
        }
        expect_carrier_error(
            lambda: validate_interface_values("cotend-init", overlong),
            "overlong default prompt",
        )
        cases += 1
    finally:
        if negative_fixture.exists():
            shutil.rmtree(negative_fixture)
    return cases


def app_server_request(fixture: Path, request: dict[str, Any]) -> dict[str, Any]:
    command = [codex_executable(), "app-server", "--stdio"]
    process = subprocess.Popen(
        command,
        cwd=fixture,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.stdin is None or process.stdout is None or process.stderr is None:
        raise CarrierError("failed to open Codex app-server pipes")

    output: queue.Queue[str | None] = queue.Queue()
    stderr_lines: list[str] = []

    def read_stdout() -> None:
        assert process.stdout is not None
        for line in process.stdout:
            output.put(line)
        output.put(None)

    def read_stderr() -> None:
        assert process.stderr is not None
        stderr_lines.extend(process.stderr)

    reader = threading.Thread(target=read_stdout, daemon=True)
    stderr_reader = threading.Thread(target=read_stderr, daemon=True)
    reader.start()
    stderr_reader.start()
    messages = [
        {
            "method": "initialize",
            "id": 0,
            "params": {
                "clientInfo": {
                    "name": "cotend_carrier_validator",
                    "title": "CoTend Carrier Validator",
                    "version": "0.1.0",
                }
            },
        },
        {"method": "initialized", "params": {}},
        request,
    ]
    for message in messages:
        process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
    process.stdin.flush()

    response: dict[str, Any] | None = None
    deadline = time.monotonic() + 30
    try:
        while time.monotonic() < deadline:
            try:
                line = output.get(timeout=max(0.1, deadline - time.monotonic()))
            except queue.Empty as exc:
                raise CarrierError("Codex app-server response timed out") from exc
            if line is None:
                break
            message = json.loads(line)
            if message.get("id") == request["id"]:
                response = message
                break
    finally:
        if process.stdin is not None and not process.stdin.closed:
            process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
    if response is None:
        stderr_reader.join(timeout=1)
        stderr = "".join(stderr_lines).strip()
        raise CarrierError(f"Codex app-server returned no response: {stderr[:300]}")
    if "error" in response:
        raise CarrierError(f"Codex app-server error: {response['error']}")
    return response["result"]


def discover_skills(
    fixture: Path,
    *,
    allow_unrelated_skills: bool = False,
) -> dict[str, Any]:
    scenario_cwd = (fixture / "scenarios" / "fresh").resolve()
    result = app_server_request(
        fixture,
        {
            "method": "skills/list",
            "id": 25,
            "params": {"cwds": [str(scenario_cwd)], "forceReload": True},
        },
    )
    entries = result.get("data", [])
    if len(entries) != 1:
        raise CarrierError("skills/list did not return exactly one cwd entry")
    entry = entries[0]
    if entry.get("errors"):
        raise CarrierError(f"skills/list reported errors: {entry['errors']}")

    installed_root = (fixture / ".agents" / "skills").resolve()
    discovered: dict[str, dict[str, Any]] = {}
    for item in entry.get("skills", []):
        path = Path(item["path"]).resolve()
        try:
            path.relative_to(installed_root)
        except ValueError:
            continue
        if item["name"] in discovered:
            raise CarrierError(f"duplicate fixture Skill discovered: {item['name']}")
        discovered[item["name"]] = item
    discovered_names = set(discovered)
    missing_skills = EXPECTED_SKILLS - discovered_names
    unrelated_skills = discovered_names - EXPECTED_SKILLS
    if missing_skills or (unrelated_skills and not allow_unrelated_skills):
        raise CarrierError(f"Codex discovery mismatch: {sorted(discovered)}")

    redacted_skills: list[dict[str, Any]] = []
    redacted_unrelated_skills: list[dict[str, Any]] = []
    for name in sorted(discovered):
        item = discovered[name]
        if item.get("scope") != "repo" or item.get("enabled") is not True:
            raise CarrierError(f"Codex scope/enabled mismatch: {name}")
        installed_skill_file = installed_root / name / "SKILL.md"
        if frontmatter_name(installed_skill_file) != name:
            raise CarrierError(f"Codex discovered invalid fixture Skill: {name}")
        source_description = frontmatter_description(installed_skill_file)
        if item.get("description") != source_description:
            raise CarrierError(f"Codex description mismatch: {name}")
        interface = item.get("interface")
        if name in EXPECTED_INTERFACES:
            display_name, short_description = EXPECTED_INTERFACES[name]
            if not isinstance(interface, dict):
                raise CarrierError(f"Codex interface metadata missing: {name}")
            if interface.get("displayName") != display_name:
                raise CarrierError(f"Codex displayName mismatch: {name}")
            if interface.get("shortDescription") != short_description:
                raise CarrierError(f"Codex shortDescription mismatch: {name}")
            if not interface.get("defaultPrompt", "").startswith(f"Use ${name}"):
                raise CarrierError(f"Codex defaultPrompt mismatch: {name}")
        elif name in EXPECTED_SKILLS and interface is not None:
            raise CarrierError(f"companion interface should be null: {name}")
        redacted = {
            "name": name,
            "path": Path(item["path"]).resolve().relative_to(fixture).as_posix(),
            "scope": item["scope"],
            "enabled": item["enabled"],
            "interface": interface,
        }
        if name in EXPECTED_SKILLS:
            redacted_skills.append(redacted)
        else:
            redacted_unrelated_skills.append(redacted)
    return {
        "fixture_skills": redacted_skills,
        "fixture_skill_count": len(redacted_skills),
        "unrelated_fixture_skills": redacted_unrelated_skills,
        "unrelated_fixture_skill_count": len(redacted_unrelated_skills),
        "all_visible_skill_count": len(entry.get("skills", [])),
    }


def load_scenarios() -> list[dict[str, Any]]:
    return json.loads(
        (TEMPLATE_ROOT / "live-scenarios.json").read_text(encoding="utf-8")
    )


def validate_live_result(scenario: dict[str, Any], result: dict[str, Any]) -> None:
    scenario_id = scenario["id"]
    expected_skill = scenario["skill"]
    if result.get("invoked_skill") != expected_skill:
        raise CarrierError(f"{scenario_id}: invoked Skill mismatch")
    normalized_path = str(result.get("invoked_skill_path", "")).replace("\\", "/")
    expected_suffix = f"/.agents/skills/{expected_skill}/SKILL.md"
    if not normalized_path.endswith(expected_suffix):
        raise CarrierError(f"{scenario_id}: project-local Skill path not reported")
    if result.get("files_modified") is not False:
        raise CarrierError(f"{scenario_id}: model reported file modification")
    if scenario_id == "init-delegation":
        expected = {
            "delegated_skill": "cotend-project-init",
            "shared_governance_skill": "cotend-collaboration",
            "classification": "fresh_init",
        }
    elif scenario_id == "pending-decision":
        expected = {
            "delegated_skill": "cotend-project-init",
            "pending_question_id": "FIXTURE-Q1",
            "readiness": "human_needed",
            "bare_continue_answered_question": False,
            "selected_option": None,
        }
    else:
        expected = {}
        if (
            "division" not in result.get("likely_root_cause", "").lower()
            and "zero" not in result.get("likely_root_cause", "").lower()
        ):
            raise CarrierError("diagnose-only: expected division-by-zero diagnosis")
        if not result.get("recommended_fix_route", "").strip():
            raise CarrierError("diagnose-only: missing recommended fix route")
    for key, value in expected.items():
        if result.get(key) != value:
            raise CarrierError(f"{scenario_id}: result mismatch for {key}")


def run_live_scenario(fixture: Path, scenario: dict[str, Any]) -> dict[str, Any]:
    run_root = fixture / "runs" / scenario["id"]
    run_root.mkdir(parents=True, exist_ok=True)
    output_path = run_root / "last-message.json"
    jsonl_path = run_root / "events.jsonl"
    stderr_path = run_root / "stderr.txt"
    scenario_cwd = fixture / scenario["cwd"]
    schema_path = fixture / scenario["schema"]

    fixture_before = file_manifest(fixture, exclude={".git", "runs"})
    global_before = protected_global_snapshot()
    command = [
        codex_executable(),
        "--ask-for-approval",
        "never",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--json",
        "--color",
        "never",
        "--sandbox",
        "read-only",
        "--cd",
        str(scenario_cwd),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
        "-",
    ]
    completed = subprocess.run(
        command,
        cwd=scenario_cwd,
        input=scenario["prompt"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    jsonl_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        raise CarrierError(
            f"{scenario['id']}: codex exec failed with {completed.returncode}; "
            f"see ignored run evidence"
        )
    if not output_path.exists():
        raise CarrierError(f"{scenario['id']}: no final message was produced")
    result = json.loads(output_path.read_text(encoding="utf-8"))
    validate_live_result(scenario, result)

    fixture_after = file_manifest(fixture, exclude={".git", "runs"})
    global_after = protected_global_snapshot()
    if fixture_before != fixture_after:
        raise CarrierError(f"{scenario['id']}: fixture changed outside runs/")
    if global_before != global_after:
        raise CarrierError(f"{scenario['id']}: protected global Codex state changed")
    return {
        "id": scenario["id"],
        "skill": scenario["skill"],
        "sandbox": "read-only",
        "ephemeral": True,
        "fixture_unchanged": True,
        "protected_global_state_unchanged": True,
        "result": result,
    }


def write_evidence(path: Path | None, evidence: dict[str, Any]) -> None:
    if path is None:
        return
    target = guarded_fixture(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(evidence, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the isolated CoTend Codex carrier"
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Git-ignored fixture path under .private-provenance",
    )
    parser.add_argument(
        "--prepare", action="store_true", help="rebuild the fixture first"
    )
    parser.add_argument(
        "--discover", action="store_true", help="call Codex app-server skills/list"
    )
    parser.add_argument(
        "--negative-mutations",
        action="store_true",
        help="run four deterministic failure cases in a separate ignored fixture",
    )
    parser.add_argument(
        "--live",
        choices=["all", *sorted(LIVE_SCENARIO_IDS)],
        help="run bounded read-only codex exec scenario(s)",
    )
    parser.add_argument(
        "--evidence", type=Path, help="write redacted JSON under the fixture"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture = guarded_fixture(args.fixture)
    evidence: dict[str, Any] = {}
    runtime_root: Path | None = None
    runtime_fixture: Path | None = None
    try:
        if args.prepare:
            prepare_fixture(fixture)
        static = verify_static(fixture)
        evidence["static"] = static
        print(
            "ISOLATED_CODEX_CARRIER_OK "
            f"skills={static['skills']} files={static['files']} interfaces={static['interfaces']}"
        )

        if args.negative_mutations:
            negative_cases = run_negative_mutations(fixture)
            evidence["negative_mutations"] = {"passed": negative_cases, "total": 4}
            print(
                "ISOLATED_CODEX_CARRIER_NEGATIVE_MUTATIONS_OK "
                f"cases={negative_cases}"
            )

        if args.discover or args.live:
            runtime_root, runtime_fixture = create_external_runtime_copy(fixture)
            evidence["runtime_isolation"] = {
                "external_system_temp_project": True,
                "parent_repository_context_inherited": False,
            }

        if args.discover:
            if runtime_fixture is None:
                raise CarrierError("external discovery fixture was not created")
            discovery = discover_skills(runtime_fixture)
            evidence["discovery"] = discovery
            version = subprocess.run(
                [codex_executable(), "--version"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            evidence["codex_version"] = version
            print(
                "CODEX_SKILL_DISCOVERY_OK "
                f"version={version.replace(' ', '_')} "
                f"repo_skills={discovery['fixture_skill_count']}"
            )

        if args.live:
            if runtime_fixture is None:
                raise CarrierError("external live fixture was not created")
            scenarios = load_scenarios()
            selected = (
                scenarios
                if args.live == "all"
                else [item for item in scenarios if item["id"] == args.live]
            )
            live_results = []
            for scenario in selected:
                result = run_live_scenario(runtime_fixture, scenario)
                live_results.append(result)
                print(
                    f"CODEX_LIVE_SCENARIO_OK id={scenario['id']} "
                    f"skill={scenario['skill']}"
                )
            evidence["live"] = live_results
        if runtime_root is not None:
            retries = remove_external_runtime_root(runtime_root)
            runtime_root = None
            evidence.setdefault("runtime_isolation", {})[
                "windows_handle_release_retries"
            ] = retries
        write_evidence(args.evidence, evidence)
    except (
        CarrierError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print("ISOLATED_CODEX_CARRIER_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    finally:
        if runtime_root is not None:
            remove_external_runtime_root(runtime_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
