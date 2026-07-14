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
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS_ROOT = ROOT / "skills"
PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_FIXTURE = PRIVATE_ROOT / "L31-isolated-codex-plugin"
PLUGIN_ID = "cotend"
PLUGIN_VERSION = "0.0.0-dev.1+codex.fixture"
MARKETPLACE_NAME = "cotend-fixture-local"
EXPECTED_SKILLS = (
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-init",
    "cotend-model-upgrade",
    "cotend-project-init",
    "grill-me",
    "karpathy-guidelines",
)
EXPECTED_FILE_COUNT = 30
PACKAGE_SUPPORT_FILES = {
    "LICENSE": ROOT / "LICENSE",
    "NOTICE": ROOT / "NOTICE",
    "THIRD-PARTY-NOTICES.md": ROOT / "THIRD-PARTY-NOTICES.md",
    "THIRD-PARTY-LICENSES/grill-me-MIT.txt": (
        ROOT / "THIRD-PARTY-LICENSES" / "grill-me-MIT.txt"
    ),
    "THIRD-PARTY-LICENSES/karpathy-guidelines-MIT.txt": (
        ROOT / "THIRD-PARTY-LICENSES" / "karpathy-guidelines-MIT.txt"
    ),
}
SOURCE_LOCKS = (
    ROOT / "delivery" / "codex-artifact.lock.json",
    ROOT / "upstream" / "framework.lock.json",
)
WRITE_ROOT_ENV_KEYS = (
    "CODEX_HOME",
    "HOME",
    "USERPROFILE",
    "TEMP",
    "TMP",
    "TMPDIR",
    "APPDATA",
    "LOCALAPPDATA",
    "XDG_CACHE_HOME",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_STATE_HOME",
    "NPM_CONFIG_CACHE",
    "PIP_CACHE_DIR",
    "PYTHONPYCACHEPREFIX",
)
SAFE_INHERITED_ENV_KEYS = {
    "COMSPEC",
    "LANG",
    "LC_ALL",
    "NUMBER_OF_PROCESSORS",
    "OS",
    "PATH",
    "PATHEXT",
    "PROCESSOR_ARCHITECTURE",
    "PROCESSOR_IDENTIFIER",
    "PROCESSOR_LEVEL",
    "PROCESSOR_REVISION",
    "PSModulePath",
    "SYSTEMDRIVE",
    "SYSTEMROOT",
    "TERM",
    "WINDIR",
}
PHASE_B_NOT_RUN = (
    "local_cachebuster_update",
    "enable_disable",
    "new_thread_refresh",
    "desktop_rendering_and_uninstall",
    "model_invocation",
    "portal_archive",
    "public_submission_release_or_publish",
)


class PluginFixtureError(RuntimeError):
    pass


@dataclass(frozen=True)
class PluginLifecycleIdentity:
    plugin_id: str
    plugin_version: str
    marketplace_name: str
    expected_skills: tuple[str, ...]

    @property
    def selector(self) -> str:
        return f"{self.plugin_id}@{self.marketplace_name}"


FIXTURE_LIFECYCLE_IDENTITY = PluginLifecycleIdentity(
    plugin_id=PLUGIN_ID,
    plugin_version=PLUGIN_VERSION,
    marketplace_name=MARKETPLACE_NAME,
    expected_skills=EXPECTED_SKILLS,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_manifest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def guarded_fixture(path: Path) -> Path:
    private_root = PRIVATE_ROOT.resolve()
    resolved = path.expanduser().resolve()
    try:
        relative = resolved.relative_to(private_root)
    except ValueError as exc:
        raise PluginFixtureError("fixture must stay under the private fixture root") from exc
    if not relative.parts:
        raise PluginFixtureError("fixture cannot be the private fixture root")
    return resolved


def assert_fixture_path(fixture: Path, path: Path, label: str) -> Path:
    fixture = guarded_fixture(fixture)
    resolved = path.expanduser().resolve()
    try:
        relative = resolved.relative_to(fixture)
    except ValueError as exc:
        raise PluginFixtureError(f"{label} escapes the fixture") from exc
    if not relative.parts:
        raise PluginFixtureError(f"{label} cannot be the fixture root")
    return resolved


def reject_symlink_tree(root: Path, *, label: str = "fixture") -> None:
    if root.is_symlink():
        raise PluginFixtureError(f"{label} root cannot be a symlink")
    for path in root.rglob("*"):
        if path.is_symlink():
            raise PluginFixtureError(
                f"symlink is not allowed in {label}: "
                f"{path.relative_to(root).as_posix()}"
            )


def remove_fixture_tree(path: Path) -> None:
    resolved = guarded_fixture(path)
    if resolved.exists():
        reject_symlink_tree(resolved)
        shutil.rmtree(resolved)


def stat_only(path: Path) -> dict[str, Any]:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return {"exists": False}
    return {
        "exists": True,
        "kind": (
            "directory"
            if stat.S_ISDIR(metadata.st_mode)
            else "file"
            if stat.S_ISREG(metadata.st_mode)
            else "other"
        ),
        "size": metadata.st_size,
        "mtime_ns": metadata.st_mtime_ns,
    }


def protected_user_paths() -> dict[str, Path]:
    user_home = Path.home().resolve()
    default_codex_home = (user_home / ".codex").resolve()
    configured_codex_home = Path(
        os.environ.get("CODEX_HOME", str(default_codex_home))
    ).expanduser().resolve()
    paths = {
        "user_codex_root": default_codex_home,
        "user_codex_config": default_codex_home / "config.toml",
        "user_codex_auth": default_codex_home / "auth.json",
        "user_codex_plugins": default_codex_home / "plugins",
        "user_codex_skills": default_codex_home / "skills",
        "user_agents_root": user_home / ".agents",
        "user_agents_plugins": user_home / ".agents" / "plugins",
        "user_agents_skills": user_home / ".agents" / "skills",
    }
    if configured_codex_home != default_codex_home:
        paths.update(
            {
                "configured_codex_root": configured_codex_home,
                "configured_codex_config": configured_codex_home / "config.toml",
                "configured_codex_auth": configured_codex_home / "auth.json",
                "configured_codex_plugins": configured_codex_home / "plugins",
                "configured_codex_skills": configured_codex_home / "skills",
            }
        )
    return paths


def protected_user_snapshot() -> dict[str, dict[str, Any]]:
    # Deliberately stat-only: config, auth, plugin, and Skill contents are never opened.
    return {label: stat_only(path) for label, path in protected_user_paths().items()}


def assert_protected_unchanged(
    expected: dict[str, dict[str, Any]],
) -> None:
    actual = protected_user_snapshot()
    if actual != expected:
        changed = sorted(
            key
            for key in expected.keys() | actual.keys()
            if expected.get(key) != actual.get(key)
        )
        raise PluginFixtureError(
            "protected user metadata changed: " + ", ".join(changed)
        )


def validate_repository_source_boundary() -> None:
    reject_symlink_tree(SOURCE_SKILLS_ROOT, label="repository Skill source")
    for source in (*PACKAGE_SUPPORT_FILES.values(), *SOURCE_LOCKS):
        if source.is_symlink() or not source.is_file():
            raise PluginFixtureError(
                "repository source boundary contains a missing or linked file: "
                + source.relative_to(ROOT).as_posix()
            )


def source_state_snapshot() -> dict[str, Any]:
    validate_repository_source_boundary()
    return {
        "skills": file_manifest(SOURCE_SKILLS_ROOT),
        "locks": {
            path.relative_to(ROOT).as_posix(): sha256(path) for path in SOURCE_LOCKS
        },
        "git_head": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
    }


def codex_executable() -> str:
    executable = shutil.which("codex")
    if executable is None:
        raise PluginFixtureError("codex executable is unavailable")
    return str(Path(executable).resolve())


def plugin_creator_script(filename: str) -> Path:
    explicit_root = os.environ.get("CODEX_PLUGIN_CREATOR_ROOT")
    candidates = []
    if explicit_root:
        candidates.append(Path(explicit_root).expanduser())
    candidates.extend(
        [
            Path.home() / ".codex" / "skills" / ".system" / "plugin-creator",
            Path.home() / ".agents" / "skills" / ".system" / "plugin-creator",
        ]
    )
    for root in candidates:
        path = root / "scripts" / filename
        if path.is_file():
            return path.resolve()
    raise PluginFixtureError(f"plugin-creator tool is unavailable: {filename}")


def build_isolated_env(fixture: Path) -> dict[str, str]:
    fixture = guarded_fixture(fixture)
    process_home = fixture / "process-home"
    mappings = {
        "CODEX_HOME": fixture / "codex-home",
        "HOME": process_home,
        "USERPROFILE": process_home,
        "TEMP": fixture / "temp",
        "TMP": fixture / "temp",
        "TMPDIR": fixture / "temp",
        "APPDATA": process_home / "AppData" / "Roaming",
        "LOCALAPPDATA": process_home / "AppData" / "Local",
        "XDG_CACHE_HOME": fixture / "cache" / "xdg",
        "XDG_CONFIG_HOME": fixture / "config" / "xdg",
        "XDG_DATA_HOME": fixture / "data" / "xdg",
        "XDG_STATE_HOME": fixture / "state" / "xdg",
        "NPM_CONFIG_CACHE": fixture / "cache" / "npm",
        "PIP_CACHE_DIR": fixture / "cache" / "pip",
        "PYTHONPYCACHEPREFIX": fixture / "cache" / "pycache",
    }
    env = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in {item.upper() for item in SAFE_INHERITED_ENV_KEYS}
    }
    env.update({key: str(path) for key, path in mappings.items()})
    if process_home.drive:
        env["HOMEDRIVE"] = process_home.drive
        env["HOMEPATH"] = str(process_home)[len(process_home.drive) :]
    env.update(
        {
            "CI": "true",
            "DO_NOT_TRACK": "1",
            "OTEL_SDK_DISABLED": "true",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "HTTP_PROXY": "http://127.0.0.1:9",
            "HTTPS_PROXY": "http://127.0.0.1:9",
            "ALL_PROXY": "http://127.0.0.1:9",
            "NO_PROXY": "",
        }
    )
    for path in mappings.values():
        assert_fixture_path(fixture, path, "isolated environment root")
        path.mkdir(parents=True, exist_ok=True)
    return env


def validate_isolated_env(fixture: Path, env: dict[str, str]) -> None:
    fixture = guarded_fixture(fixture)
    for key in WRITE_ROOT_ENV_KEYS:
        raw = env.get(key)
        if not raw:
            raise PluginFixtureError(f"isolated environment is missing {key}")
        assert_fixture_path(fixture, Path(raw), f"environment root {key}")
    inherited_names = {key.upper() for key in env}
    secret_fragments = ("TOKEN", "SECRET", "PASSWORD", "API_KEY", "AUTH")
    unsafe = sorted(
        key
        for key in inherited_names
        if any(fragment in key for fragment in secret_fragments)
    )
    if unsafe:
        raise PluginFixtureError(
            "isolated environment inherited secret-like variables: " + ", ".join(unsafe)
        )


def run_process(
    command: list[str],
    *,
    env: dict[str, str],
    cwd: Path,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def run_preflight(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    validate_isolated_env(fixture, env)
    probe = (
        "import json, os, pathlib, tempfile; "
        "print(json.dumps({'home': str(pathlib.Path.home()), "
        "'temp': tempfile.gettempdir(), "
        "'roots': {k: os.environ.get(k) for k in "
        + repr(list(WRITE_ROOT_ENV_KEYS))
        + "}}))"
    )
    completed = run_process(
        [sys.executable, "-c", probe],
        env=env,
        cwd=fixture,
    )
    if completed.returncode != 0:
        raise PluginFixtureError(f"process-home probe failed: {completed.stderr[:200]}")
    payload = json.loads(completed.stdout)
    assert_fixture_path(fixture, Path(payload["home"]), "resolved process home")
    assert_fixture_path(fixture, Path(payload["temp"]), "resolved process temp")
    for key, raw in payload["roots"].items():
        if not raw:
            raise PluginFixtureError(f"process-home probe did not resolve {key}")
        assert_fixture_path(fixture, Path(raw), f"resolved process root {key}")

    version = run_process(
        [codex_executable(), "--version"],
        env=env,
        cwd=fixture,
    )
    if version.returncode != 0:
        raise PluginFixtureError(f"isolated codex version probe failed: {version.stderr[:200]}")
    assert_protected_unchanged(protected_before)
    return {
        "write_root_count": len(WRITE_ROOT_ENV_KEYS),
        "all_roots_inside_fixture": True,
        "secret_like_variables_inherited": False,
        "protected_user_metadata_unchanged": True,
        "codex_version": version.stdout.strip(),
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def plugin_manifest() -> dict[str, Any]:
    return {
        "name": PLUGIN_ID,
        "version": PLUGIN_VERSION,
        "description": "Fixture-only validation package for CoTend Skills.",
        "author": {"name": "CoTend contributors"},
        "homepage": "https://github.com/lhh1301506137/CoTend",
        "repository": "https://github.com/lhh1301506137/CoTend",
        "license": "Apache-2.0",
        "keywords": ["ai-development", "project-governance", "skills"],
        "skills": "./skills/",
        "interface": {
            "displayName": "CoTend Fixture",
            "shortDescription": "Fixture-only CoTend Plugin validation",
            "longDescription": (
                "Disposable local package for validating CoTend Plugin packaging, "
                "discovery, and lifecycle behavior."
            ),
            "developerName": "CoTend contributors",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": ["Initialize or resume this project with CoTend."],
        },
    }


def marketplace_manifest() -> dict[str, Any]:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "CoTend Fixture Local"},
        "plugins": [
            {
                "name": PLUGIN_ID,
                "source": {"source": "local", "path": f"./plugins/{PLUGIN_ID}"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        ],
    }


def materialize_fixture_payload(fixture: Path) -> dict[str, Path]:
    fixture = guarded_fixture(fixture)
    validate_repository_source_boundary()
    marketplace_root = fixture / "source-marketplace"
    plugin_root = marketplace_root / "plugins" / PLUGIN_ID
    marketplace_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    write_json(plugin_root / ".codex-plugin" / "plugin.json", plugin_manifest())
    write_json(marketplace_path, marketplace_manifest())
    skills_root = plugin_root / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    for skill in EXPECTED_SKILLS:
        shutil.copytree(SOURCE_SKILLS_ROOT / skill, skills_root / skill)
    for relative, source in PACKAGE_SUPPORT_FILES.items():
        target = plugin_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    empty_project = fixture / "project-empty"
    empty_project.mkdir(parents=True, exist_ok=True)
    (empty_project / "README.md").write_text("# Empty fixture project\n", encoding="utf-8")
    coexist_project = fixture / "project-with-standalone-skills"
    coexist_project.mkdir(parents=True, exist_ok=True)
    (coexist_project / "README.md").write_text(
        "# Coexistence fixture project\n", encoding="utf-8"
    )
    standalone_root = coexist_project / ".agents" / "skills"
    for skill in EXPECTED_SKILLS:
        shutil.copytree(SOURCE_SKILLS_ROOT / skill, standalone_root / skill)
    (fixture / "evidence" / "commands").mkdir(parents=True, exist_ok=True)
    return {
        "plugin_root": plugin_root,
        "marketplace_root": marketplace_root,
        "empty_project": empty_project,
        "coexist_project": coexist_project,
    }


def prepare_fixture(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    validate_isolated_env(fixture, env)
    marketplace_root = assert_fixture_path(
        fixture, fixture / "source-marketplace", "marketplace root"
    )
    plugin_parent = marketplace_root / "plugins"
    marketplace_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    scaffold = plugin_creator_script("create_basic_plugin.py")
    command = [
        sys.executable,
        str(scaffold),
        PLUGIN_ID,
        "--path",
        str(plugin_parent),
        "--with-skills",
        "--with-marketplace",
        "--marketplace-path",
        str(marketplace_path),
        "--marketplace-name",
        MARKETPLACE_NAME,
        "--category",
        "Developer Tools",
    ]
    completed = run_process(command, env=env, cwd=fixture)
    if completed.returncode != 0:
        raise PluginFixtureError(f"official Plugin scaffold failed: {completed.stderr[:300]}")

    paths = materialize_fixture_payload(fixture)
    assert_protected_unchanged(protected_before)
    return {
        "scaffold_used": True,
        **paths,
    }


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PluginFixtureError(f"invalid {label}") from exc
    if not isinstance(payload, dict):
        raise PluginFixtureError(f"{label} must contain an object")
    return payload


def frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<header>.*?)\n---(?:\n|$)", text, re.DOTALL)
    if match is None:
        raise PluginFixtureError(f"missing Skill frontmatter: {path.parent.name}")
    payload = yaml.safe_load(match.group("header"))
    if not isinstance(payload, dict) or not isinstance(payload.get("name"), str):
        raise PluginFixtureError(f"invalid Skill frontmatter: {path.parent.name}")
    return payload["name"].strip()


def verify_static(
    fixture: Path,
    *,
    run_official: bool = True,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    validate_repository_source_boundary()
    reject_symlink_tree(fixture)
    marketplace_root = fixture / "source-marketplace"
    plugin_root = marketplace_root / "plugins" / PLUGIN_ID
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = load_json_object(manifest_path, "Plugin manifest")
    if manifest != plugin_manifest():
        raise PluginFixtureError("Plugin manifest differs from the fixture contract")
    marketplace = load_json_object(
        marketplace_root / ".agents" / "plugins" / "marketplace.json",
        "Marketplace manifest",
    )
    if marketplace != marketplace_manifest():
        raise PluginFixtureError("Marketplace manifest differs from the fixture contract")

    source_manifest = file_manifest(SOURCE_SKILLS_ROOT)
    if len(source_manifest) != EXPECTED_FILE_COUNT:
        raise PluginFixtureError(
            f"expected {EXPECTED_FILE_COUNT} source Skill files, found {len(source_manifest)}"
        )
    skill_names: list[str] = []
    for skill in EXPECTED_SKILLS:
        skill_file = plugin_root / "skills" / skill / "SKILL.md"
        if not skill_file.is_file():
            raise PluginFixtureError(f"missing Skill file: {skill}")
        skill_names.append(frontmatter_name(skill_file))
    if len(set(skill_names)) != len(skill_names):
        raise PluginFixtureError("duplicate adopted Skill frontmatter name")
    if tuple(skill_names) != EXPECTED_SKILLS:
        raise PluginFixtureError("Skill directory and frontmatter names differ")

    packaged_skill_manifest = file_manifest(plugin_root / "skills")
    if packaged_skill_manifest != source_manifest:
        raise PluginFixtureError("packaged Skill bytes differ from repository source")
    for relative, source in PACKAGE_SUPPORT_FILES.items():
        target = plugin_root / relative
        if not target.is_file() or sha256(target) != sha256(source):
            raise PluginFixtureError(f"package support file mismatch: {relative}")

    expected_files = {
        ".codex-plugin/plugin.json",
        *{f"skills/{path}" for path in source_manifest},
        *PACKAGE_SUPPORT_FILES.keys(),
    }
    actual_files = set(file_manifest(plugin_root))
    if actual_files != expected_files:
        extra = sorted(actual_files - expected_files)
        missing = sorted(expected_files - actual_files)
        raise PluginFixtureError(
            f"package allowlist mismatch; extra={extra}; missing={missing}"
        )
    for forbidden in ("hooks", "assets", "scripts", ".app.json", ".mcp.json"):
        if (plugin_root / forbidden).exists():
            raise PluginFixtureError(f"undeclared Plugin capability present: {forbidden}")

    official_validation = "not_run"
    if run_official:
        validator = plugin_creator_script("validate_plugin.py")
        completed = subprocess.run(
            [sys.executable, str(validator), str(plugin_root)],
            cwd=fixture,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        if completed.returncode != 0:
            raise PluginFixtureError(
                "official Plugin validation failed: "
                + (completed.stdout + completed.stderr)[-500:]
            )
        official_validation = "passed"
    return {
        "plugin_id": PLUGIN_ID,
        "fixture_version": PLUGIN_VERSION,
        "skills": len(EXPECTED_SKILLS),
        "skill_files": len(packaged_skill_manifest),
        "package_files": len(actual_files),
        "official_validator": official_validation,
        "source_bytes_identical": True,
        "license_and_notice_files": len(PACKAGE_SUPPORT_FILES),
        "undeclared_capabilities": 0,
    }


def expect_fixture_error(action: Callable[[], Any], label: str) -> str:
    try:
        action()
    except PluginFixtureError as exc:
        return str(exc)
    raise PluginFixtureError(f"negative mutation was not rejected: {label}")


def run_negative_mutations(fixture: Path) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    cases_root = fixture / "negative-cases"
    if cases_root.exists():
        shutil.rmtree(cases_root)
    cases_root.mkdir(parents=True)
    base_marketplace = fixture / "source-marketplace"
    passed: list[str] = []

    def mutate_case(case_id: str, mutate: Callable[[Path], None]) -> None:
        case = cases_root / case_id
        shutil.copytree(base_marketplace, case / "source-marketplace")
        mutate(case)
        expect_fixture_error(
            lambda: verify_static(case, run_official=False),
            case_id,
        )
        passed.append(case_id)

    mutate_case(
        "missing_manifest",
        lambda case: (
            case
            / "source-marketplace"
            / "plugins"
            / PLUGIN_ID
            / ".codex-plugin"
            / "plugin.json"
        ).unlink(),
    )

    def mutate_manifest(case: Path, value: str) -> None:
        path = (
            case
            / "source-marketplace"
            / "plugins"
            / PLUGIN_ID
            / ".codex-plugin"
            / "plugin.json"
        )
        payload = load_json_object(path, "mutation manifest")
        payload["skills"] = value
        write_json(path, payload)

    mutate_case("wrong_skills_path", lambda case: mutate_manifest(case, "./skillz/"))
    mutate_case("traversal_skills_path", lambda case: mutate_manifest(case, "../skills"))
    mutate_case(
        "missing_skill_file",
        lambda case: (
            case
            / "source-marketplace"
            / "plugins"
            / PLUGIN_ID
            / "skills"
            / "cotend-init"
            / "SKILL.md"
        ).unlink(),
    )

    def append_skill(case: Path) -> None:
        path = (
            case
            / "source-marketplace"
            / "plugins"
            / PLUGIN_ID
            / "skills"
            / "cotend-init"
            / "SKILL.md"
        )
        path.write_text(path.read_text(encoding="utf-8") + "\nmutation\n", encoding="utf-8")

    mutate_case("skill_byte_drift", append_skill)

    def duplicate_name(case: Path) -> None:
        path = (
            case
            / "source-marketplace"
            / "plugins"
            / PLUGIN_ID
            / "skills"
            / "cotend-diagnose-only"
            / "SKILL.md"
        )
        text = path.read_text(encoding="utf-8")
        path.write_text(
            re.sub(
                r"^name:\s*cotend-diagnose-only\s*$",
                "name: cotend-init",
                text,
                count=1,
                flags=re.MULTILINE,
            ),
            encoding="utf-8",
        )

    mutate_case("duplicate_frontmatter_name", duplicate_name)
    mutate_case(
        "missing_mit_license",
        lambda case: (
            case
            / "source-marketplace"
            / "plugins"
            / PLUGIN_ID
            / "THIRD-PARTY-LICENSES"
            / "grill-me-MIT.txt"
        ).unlink(),
    )

    def inject_restricted_file(case: Path) -> None:
        path = case / "source-marketplace" / "plugins" / PLUGIN_ID / "STATUS.md"
        path.write_text("local governance must not ship\n", encoding="utf-8")

    mutate_case("restricted_file_injection", inject_restricted_file)

    def network_source(case: Path) -> None:
        path = case / "source-marketplace" / ".agents" / "plugins" / "marketplace.json"
        payload = load_json_object(path, "mutation Marketplace manifest")
        payload["plugins"][0]["source"] = {
            "source": "git",
            "url": "https://invalid.example/plugin.git",
        }
        write_json(path, payload)

    mutate_case("network_marketplace_source", network_source)

    expect_fixture_error(
        lambda: assert_fixture_path(
            fixture,
            Path.home() / ".agents" / "plugins" / "marketplace.json",
            "Marketplace target",
        ),
        "outside_marketplace_target",
    )
    passed.append("outside_marketplace_target")
    expect_fixture_error(
        lambda: assert_fixture_path(fixture, ROOT, "project target"),
        "outside_project_target",
    )
    passed.append("outside_project_target")
    invalid_env = build_isolated_env(fixture)
    invalid_env["CODEX_HOME"] = str(Path.home() / ".codex")
    expect_fixture_error(
        lambda: validate_isolated_env(fixture, invalid_env),
        "nonisolated_codex_home",
    )
    passed.append("nonisolated_codex_home")
    shutil.rmtree(cases_root)
    return {"passed": len(passed), "total": 12, "case_ids": passed}


def parse_json_stdout(completed: subprocess.CompletedProcess[str], label: str) -> Any:
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise PluginFixtureError(f"{label} did not return JSON") from exc


def require_json_object(payload: Any, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise PluginFixtureError(f"{label} must be a JSON object")
    return payload


def validate_marketplace_add_payload(
    payload: Any,
    fixture: Path,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
) -> None:
    item = require_json_object(payload, "Marketplace add output")
    if item.get("marketplaceName") != identity.marketplace_name:
        raise PluginFixtureError("Marketplace add identity mismatch")
    installed_root = Path(str(item.get("installedRoot", ""))).resolve()
    if installed_root != (fixture / "source-marketplace").resolve():
        raise PluginFixtureError("Marketplace add root mismatch")
    if item.get("alreadyAdded") is not False:
        raise PluginFixtureError("fresh fixture Marketplace was already configured")


def validate_marketplace_list_payload(
    payload: Any,
    *,
    present: bool,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
) -> None:
    root = require_json_object(payload, "Marketplace list output")
    entries = root.get("marketplaces")
    if not isinstance(entries, list):
        raise PluginFixtureError("Marketplace list omitted marketplaces")
    matches = [
        entry for entry in entries if entry.get("name") == identity.marketplace_name
    ]
    if bool(matches) != present:
        raise PluginFixtureError("Marketplace configured-state mismatch")


def validate_plugin_add_payload(
    payload: Any,
    fixture: Path,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
) -> None:
    item = require_json_object(payload, "Plugin add output")
    expected = {
        "pluginId": identity.selector,
        "name": identity.plugin_id,
        "marketplaceName": identity.marketplace_name,
        "version": identity.plugin_version,
        "authPolicy": "ON_INSTALL",
    }
    for key, value in expected.items():
        if item.get(key) != value:
            raise PluginFixtureError(f"Plugin add output mismatch: {key}")
    installed_path = Path(str(item.get("installedPath", ""))).resolve()
    expected_root = fixture / "codex-home" / "plugins" / "cache"
    try:
        installed_path.relative_to(expected_root.resolve())
    except ValueError as exc:
        raise PluginFixtureError("Plugin cache path escaped isolated CODEX_HOME") from exc
    if installed_path.name != identity.plugin_version:
        raise PluginFixtureError("Plugin cache version directory mismatch")


def validate_plugin_list_payload(
    payload: Any,
    fixture: Path,
    *,
    installed: bool,
    available: bool,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
) -> None:
    root = require_json_object(payload, "Plugin list output")
    installed_items = root.get("installed")
    available_items = root.get("available")
    if not isinstance(installed_items, list) or not isinstance(available_items, list):
        raise PluginFixtureError("Plugin list omitted installed or available arrays")
    installed_matches = [
        item for item in installed_items if item.get("pluginId") == identity.selector
    ]
    available_matches = [
        item for item in available_items if item.get("pluginId") == identity.selector
    ]
    if bool(installed_matches) != installed or bool(available_matches) != available:
        raise PluginFixtureError("Plugin list state mismatch")
    for item, expected_installed, expected_enabled in (
        *[(value, True, True) for value in installed_matches],
        *[(value, False, False) for value in available_matches],
    ):
        expected = {
            "name": identity.plugin_id,
            "marketplaceName": identity.marketplace_name,
            "version": identity.plugin_version,
            "installed": expected_installed,
            "enabled": expected_enabled,
            "installPolicy": "AVAILABLE",
            "authPolicy": "ON_INSTALL",
        }
        for key, value in expected.items():
            if item.get(key) != value:
                raise PluginFixtureError(f"Plugin list output mismatch: {key}")
        source = require_json_object(item.get("source"), "Plugin source")
        if source.get("source") != "local":
            raise PluginFixtureError("Plugin list source is not local")
        source_path = Path(str(source.get("path", ""))).resolve()
        if source_path != (
            fixture / "source-marketplace" / "plugins" / identity.plugin_id
        ).resolve():
            raise PluginFixtureError("Plugin list source path mismatch")


def validate_plugin_remove_payload(
    payload: Any,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
) -> None:
    item = require_json_object(payload, "Plugin remove output")
    expected = {
        "pluginId": identity.selector,
        "name": identity.plugin_id,
        "marketplaceName": identity.marketplace_name,
    }
    for key, value in expected.items():
        if item.get(key) != value:
            raise PluginFixtureError(f"Plugin remove output mismatch: {key}")


def run_cli_step(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    step: str,
    arguments: list[str],
) -> Any:
    fixture = guarded_fixture(fixture)
    command = [
        codex_executable(),
        "--disable",
        "remote_plugin",
        "plugin",
        *arguments,
    ]
    completed = run_process(command, env=env, cwd=fixture, timeout=90)
    write_json(
        fixture / "evidence" / "commands" / f"{step}.json",
        {
            "argv": ["codex", "--disable", "remote_plugin", "plugin", *arguments],
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        },
    )
    assert_protected_unchanged(protected_before)
    if completed.returncode != 0:
        raise PluginFixtureError(
            f"{step} failed with {completed.returncode}: {completed.stderr[-400:]}"
        )
    return parse_json_stdout(completed, step)


def app_server_request(
    fixture: Path,
    env: dict[str, str],
    cwd: Path,
    request: dict[str, Any],
    *,
    cwd_boundary: Path | None = None,
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    if cwd_boundary is None:
        assert_fixture_path(fixture, cwd, "app-server cwd")
    else:
        boundary = cwd_boundary.expanduser().resolve()
        resolved_cwd = cwd.expanduser().resolve()
        try:
            relative = resolved_cwd.relative_to(boundary)
        except ValueError as exc:
            raise PluginFixtureError("app-server cwd escapes its explicit boundary") from exc
        if not relative.parts or not boundary.is_dir():
            raise PluginFixtureError("app-server cwd boundary is invalid")
    process = subprocess.Popen(
        [codex_executable(), "--disable", "remote_plugin", "app-server", "--stdio"],
        cwd=cwd,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.stdin is None or process.stdout is None or process.stderr is None:
        raise PluginFixtureError("failed to open Codex app-server pipes")
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

    threading.Thread(target=read_stdout, daemon=True).start()
    stderr_reader = threading.Thread(target=read_stderr, daemon=True)
    stderr_reader.start()
    messages = [
        {
            "method": "initialize",
            "id": 0,
            "params": {
                "clientInfo": {
                    "name": "cotend_plugin_fixture_validator",
                    "title": "CoTend Plugin Fixture Validator",
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
                raise PluginFixtureError("Codex app-server response timed out") from exc
            if line is None:
                break
            message = json.loads(line)
            if message.get("id") == request["id"]:
                response = message
                break
    finally:
        try:
            process.stdin.close()
        except OSError:
            pass
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        stderr_reader.join(timeout=1)
    if response is None:
        stderr_reader.join(timeout=1)
        raise PluginFixtureError(
            "Codex app-server returned no response: " + "".join(stderr_lines)[-300:]
        )
    if "error" in response:
        raise PluginFixtureError(f"Codex app-server error: {response['error']}")
    result = response.get("result")
    if not isinstance(result, dict):
        raise PluginFixtureError("Codex app-server returned an invalid result")
    return result


def discover_skills(
    fixture: Path,
    env: dict[str, str],
    project: Path,
    *,
    expect_plugin: bool,
    expect_standalone: bool,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
    cwd_boundary: Path | None = None,
) -> dict[str, Any]:
    result = app_server_request(
        fixture,
        env,
        project,
        {
            "method": "skills/list",
            "id": 31,
            "params": {"cwds": [str(project.resolve())], "forceReload": True},
        },
        cwd_boundary=cwd_boundary,
    )
    entries = result.get("data")
    if not isinstance(entries, list) or len(entries) != 1:
        raise PluginFixtureError("skills/list did not return one project entry")
    entry = entries[0]
    if entry.get("errors"):
        raise PluginFixtureError(f"skills/list reported errors: {entry['errors']}")
    skills = entry.get("skills", [])
    expected_plugin_names = {
        f"{identity.plugin_id}:{skill}" for skill in identity.expected_skills
    }
    expected_standalone_names = set(identity.expected_skills)
    plugin_items = {
        item.get("name"): item
        for item in skills
        if item.get("name") in expected_plugin_names
    }
    standalone_items = {
        item.get("name"): item
        for item in skills
        if item.get("name") in expected_standalone_names
        and Path(str(item.get("path", ""))).resolve().is_relative_to(project.resolve())
    }
    if set(plugin_items) != (expected_plugin_names if expect_plugin else set()):
        raise PluginFixtureError(
            "Plugin Skill discovery mismatch: " + ", ".join(sorted(plugin_items))
        )
    if set(standalone_items) != (
        expected_standalone_names if expect_standalone else set()
    ):
        observed = [
            {
                "name": item.get("name"),
                "scope": item.get("scope"),
                "path": str(item.get("path", "")),
            }
            for item in skills
            if item.get("name") in expected_standalone_names
        ]
        raise PluginFixtureError(
            "standalone Skill discovery mismatch: "
            + json.dumps(observed, ensure_ascii=True, sort_keys=True)
        )

    plugin_scopes: set[str] = set()
    for name, item in plugin_items.items():
        path = Path(str(item.get("path", ""))).resolve()
        assert_fixture_path(fixture, path, f"discovered Plugin Skill {name}")
        source_name = str(name).split(":", 1)[1]
        if not path.is_file() or sha256(path) != sha256(
            SOURCE_SKILLS_ROOT / source_name / "SKILL.md"
        ):
            raise PluginFixtureError(f"discovered Plugin Skill bytes mismatch: {name}")
        if item.get("enabled") is not True:
            raise PluginFixtureError(f"discovered Plugin Skill is disabled: {name}")
        plugin_scopes.add(str(item.get("scope")))
    standalone_scopes: set[str] = set()
    for name, item in standalone_items.items():
        path = Path(str(item.get("path", ""))).resolve()
        expected_path = project / ".agents" / "skills" / str(name) / "SKILL.md"
        if path != expected_path.resolve() or sha256(path) != sha256(
            SOURCE_SKILLS_ROOT / str(name) / "SKILL.md"
        ):
            raise PluginFixtureError(f"standalone Skill bytes mismatch: {name}")
        if item.get("enabled") is not True:
            raise PluginFixtureError(f"standalone Skill is disabled: {name}")
        standalone_scopes.add(str(item.get("scope")))
    return {
        "plugin_skill_count": len(plugin_items),
        "standalone_skill_count": len(standalone_items),
        "plugin_names": sorted(plugin_items),
        "standalone_names": sorted(standalone_items),
        "plugin_scopes": sorted(plugin_scopes),
        "standalone_scopes": sorted(standalone_scopes),
        "namespace_pattern": f"{identity.plugin_id}:<skill>",
    }


def run_phase_a(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    source_before: dict[str, Any],
    *,
    identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY,
    fail_after_step: str | None = None,
    projects_root: Path | None = None,
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    marketplace_root = fixture / "source-marketplace"
    if projects_root is None:
        empty_project = fixture / "project-empty"
        coexist_project = fixture / "project-with-standalone-skills"
        cwd_boundary: Path | None = None
    else:
        cwd_boundary = projects_root.expanduser().resolve()
        if not cwd_boundary.is_dir():
            raise PluginFixtureError("external lifecycle project root is invalid")
        empty_project = cwd_boundary / "project-empty"
        coexist_project = cwd_boundary / "project-with-standalone-skills"
    steps: list[str] = []

    def mark(step: str) -> None:
        steps.append(step)
        if fail_after_step == step:
            raise PluginFixtureError(f"injected lifecycle failure after {step}")

    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-add",
        ["marketplace", "add", str(marketplace_root), "--json"],
    )
    validate_marketplace_add_payload(payload, fixture, identity)
    mark("marketplace_add")
    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-list",
        ["marketplace", "list", "--json"],
    )
    validate_marketplace_list_payload(payload, present=True, identity=identity)
    mark("marketplace_list")
    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-available",
        ["list", "--marketplace", identity.marketplace_name, "--available", "--json"],
    )
    validate_plugin_list_payload(
        payload, fixture, installed=False, available=True, identity=identity
    )
    mark("plugin_available")
    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-add",
        ["add", identity.selector, "--json"],
    )
    validate_plugin_add_payload(payload, fixture, identity)
    mark("plugin_add")
    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-list-installed",
        ["list", "--marketplace", identity.marketplace_name, "--json"],
    )
    validate_plugin_list_payload(
        payload, fixture, installed=True, available=False, identity=identity
    )
    mark("plugin_list_installed")

    installed_empty = discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=True,
        expect_standalone=False,
        identity=identity,
        cwd_boundary=cwd_boundary,
    )
    assert_protected_unchanged(protected_before)
    mark("discovery_installed")
    coexist = discover_skills(
        fixture,
        env,
        coexist_project,
        expect_plugin=True,
        expect_standalone=True,
        identity=identity,
        cwd_boundary=cwd_boundary,
    )
    assert_protected_unchanged(protected_before)
    mark("discovery_coexistence")

    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-remove",
        ["remove", identity.selector, "--json"],
    )
    validate_plugin_remove_payload(payload, identity)
    mark("plugin_remove")
    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-list-after-remove",
        ["list", "--marketplace", identity.marketplace_name, "--json"],
    )
    validate_plugin_list_payload(
        payload, fixture, installed=False, available=False, identity=identity
    )
    mark("plugin_list_after_remove")
    removed_empty = discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=False,
        expect_standalone=False,
        identity=identity,
        cwd_boundary=cwd_boundary,
    )
    removed_coexist = discover_skills(
        fixture,
        env,
        coexist_project,
        expect_plugin=False,
        expect_standalone=True,
        identity=identity,
        cwd_boundary=cwd_boundary,
    )
    assert_protected_unchanged(protected_before)
    mark("discovery_after_remove")

    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-reinstall",
        ["add", identity.selector, "--json"],
    )
    validate_plugin_add_payload(payload, fixture, identity)
    mark("plugin_reinstall")
    reinstalled = discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=True,
        expect_standalone=False,
        identity=identity,
        cwd_boundary=cwd_boundary,
    )
    assert_protected_unchanged(protected_before)
    mark("discovery_after_reinstall")

    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-final-remove",
        ["remove", identity.selector, "--json"],
    )
    validate_plugin_remove_payload(payload, identity)
    mark("plugin_final_remove")
    payload = run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-list-after-final-remove",
        ["list", "--marketplace", identity.marketplace_name, "--json"],
    )
    validate_plugin_list_payload(
        payload, fixture, installed=False, available=False, identity=identity
    )
    mark("plugin_list_after_final_remove")
    final_discovery = discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=False,
        expect_standalone=False,
        identity=identity,
        cwd_boundary=cwd_boundary,
    )
    assert_protected_unchanged(protected_before)
    mark("final_discovery_absent")
    run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-remove",
        ["marketplace", "remove", identity.marketplace_name, "--json"],
    )
    mark("marketplace_remove_cleanup")
    final_marketplaces = run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-list-final",
        ["marketplace", "list", "--json"],
    )
    validate_marketplace_list_payload(
        final_marketplaces, present=False, identity=identity
    )
    mark("marketplace_final_absent")

    if source_state_snapshot() != source_before:
        raise PluginFixtureError("repository Skill source, locks, or Git HEAD changed")
    reject_symlink_tree(fixture)
    return {
        "status": "passed",
        "steps": steps,
        "step_count": len(steps),
        "installed_discovery": installed_empty,
        "coexistence_discovery": coexist,
        "removed_discovery": removed_empty,
        "removed_coexistence_discovery": removed_coexist,
        "reinstalled_discovery": reinstalled,
        "final_discovery": final_discovery,
        "final_plugin_installed": False,
        "final_marketplace_configured": False,
        "protected_user_metadata_unchanged": True,
        "source_and_locks_unchanged": True,
    }


def write_evidence(path: Path | None, fixture: Path, evidence: dict[str, Any]) -> None:
    if path is None:
        return
    target = assert_fixture_path(fixture, path, "evidence output")
    write_json(target, evidence)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an isolated fixture-only CoTend Codex Plugin"
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Git-ignored fixture path under the private fixture root",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="rebuild the fixture after process-isolation preflight",
    )
    parser.add_argument(
        "--phase-a",
        action="store_true",
        help="run isolated local Marketplace and Plugin lifecycle checks",
    )
    parser.add_argument(
        "--negative-mutations",
        action="store_true",
        help="run twelve deterministic boundary and package failure cases",
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        help="write detailed JSON under the ignored fixture",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture = guarded_fixture(args.fixture)
    evidence: dict[str, Any] = {
        "fixture_identity": {
            "plugin_id": PLUGIN_ID,
            "version": PLUGIN_VERSION,
            "marketplace": MARKETPLACE_NAME,
            "release_identity_confirmed": False,
        },
        "phase_b": {"status": "not_run", "items": list(PHASE_B_NOT_RUN)},
    }
    protected_before = protected_user_snapshot()
    source_before = source_state_snapshot()
    try:
        if args.prepare:
            remove_fixture_tree(fixture)
        fixture.mkdir(parents=True, exist_ok=True)
        env = build_isolated_env(fixture)
        evidence["preflight"] = run_preflight(fixture, env, protected_before)
        print(
            "ISOLATED_CODEX_PLUGIN_PREFLIGHT_OK "
            f"roots={evidence['preflight']['write_root_count']} "
            f"version={evidence['preflight']['codex_version'].replace(' ', '_')}"
        )
        if args.prepare:
            prepared = prepare_fixture(fixture, env, protected_before)
            evidence["preparation"] = {"scaffold_used": prepared["scaffold_used"]}
        evidence["static"] = verify_static(fixture, env=env)
        assert_protected_unchanged(protected_before)
        print(
            "ISOLATED_CODEX_PLUGIN_STATIC_OK "
            f"skills={evidence['static']['skills']} "
            f"skill_files={evidence['static']['skill_files']} "
            f"package_files={evidence['static']['package_files']}"
        )
        if args.negative_mutations:
            evidence["negative_mutations"] = run_negative_mutations(fixture)
            assert_protected_unchanged(protected_before)
            print(
                "ISOLATED_CODEX_PLUGIN_NEGATIVE_MUTATIONS_OK "
                f"cases={evidence['negative_mutations']['passed']}"
            )
        if args.phase_a:
            evidence["phase_a"] = run_phase_a(
                fixture, env, protected_before, source_before
            )
            print(
                "ISOLATED_CODEX_PLUGIN_PHASE_A_OK "
                f"steps={evidence['phase_a']['step_count']} "
                f"plugin_skills={evidence['phase_a']['installed_discovery']['plugin_skill_count']} "
                f"coexistence={evidence['phase_a']['coexistence_discovery']['standalone_skill_count']}"
            )
        if source_state_snapshot() != source_before:
            raise PluginFixtureError("repository source state changed")
        assert_protected_unchanged(protected_before)
        evidence["final_boundary"] = {
            "protected_user_metadata_unchanged": True,
            "source_and_locks_unchanged": True,
            "all_fixture_paths_local": True,
        }
        write_evidence(args.evidence, fixture, evidence)
    except (
        PluginFixtureError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
        yaml.YAMLError,
    ) as exc:
        print("ISOLATED_CODEX_PLUGIN_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
