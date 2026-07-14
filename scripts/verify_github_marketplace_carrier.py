from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import verify_isolated_codex_plugin as lifecycle  # noqa: E402


PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_RUN_ROOT = PRIVATE_ROOT / "L54-github-marketplace-carrier"
PUBLIC_PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
PUBLIC_MARKETPLACE_MANIFEST = ROOT / ".agents" / "plugins" / "marketplace.json"
MARKETPLACE_NAME = "cotend"
PATH_REWRITES = {
    ("interface", "composerIcon"): (
        "./packaging/codex-plugin/cotend/assets/cotend-logo.png"
    ),
    ("interface", "logo"): (
        "./packaging/codex-plugin/cotend/assets/cotend-logo.png"
    ),
    ("interface", "logoDark"): (
        "./packaging/codex-plugin/cotend/assets/cotend-logo-dark.png"
    ),
}
POST_PUSH_NOT_RUN = (
    "owner_repo_marketplace_fetch",
    "git_backed_marketplace_upgrade",
    "clean_environment_novice_install",
    "desktop_visible_install_and_restart_behavior",
    "release_publish_or_push",
)
CARRIER_IDENTITY = lifecycle.PluginLifecycleIdentity(
    plugin_id=package.PLUGIN_NAME,
    plugin_version=package.PLUGIN_VERSION,
    marketplace_name=MARKETPLACE_NAME,
    expected_skills=package.EXPECTED_SKILLS,
)
EXTERNAL_PROJECT_PREFIX = "cotend-L54-projects-"


def guarded_run_root(path: Path) -> Path:
    resolved = lifecycle.guarded_fixture(path)
    relative = resolved.relative_to(PRIVATE_ROOT.resolve())
    if not relative.parts[0].startswith("L54-"):
        raise lifecycle.PluginFixtureError(
            "GitHub carrier run root must use an L54-prefixed private directory"
        )
    return resolved


def reset_run_root(path: Path) -> Path:
    resolved = guarded_run_root(path)
    if resolved.exists():
        lifecycle.reject_symlink_tree(resolved, label="L54 run root")
        remove_tree_with_readonly_retry(resolved)
    resolved.mkdir(parents=True)
    return resolved


def remove_tree_with_readonly_retry(
    path: Path, *, timeout_seconds: float = 45.0
) -> int:
    root = lifecycle.guarded_fixture(path)
    lifecycle.reject_symlink_tree(root, label="L54 removable tree")
    deadline = time.monotonic() + timeout_seconds
    retries = 0

    def make_writable_and_retry(function: Any, raw_path: str, _: Any) -> None:
        target = Path(raw_path).resolve(strict=False)
        try:
            target.relative_to(root.resolve())
        except ValueError as exc:
            raise lifecycle.PluginFixtureError(
                "read-only cleanup target escaped the L54 tree"
            ) from exc
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
            time.sleep(0.1)
    return retries


def purge_isolated_write_roots(
    fixture: Path, env: dict[str, str]
) -> dict[str, Any]:
    fixture = lifecycle.guarded_fixture(fixture)
    lifecycle.validate_isolated_env(fixture, env)
    roots = sorted(
        {Path(env[key]).resolve() for key in lifecycle.WRITE_ROOT_ENV_KEYS},
        key=lambda item: len(item.parts),
    )
    minimal_roots: list[Path] = []
    for root in roots:
        lifecycle.assert_fixture_path(fixture, root, "isolated cleanup root")
        if not any(
            root == parent or root.is_relative_to(parent) for parent in minimal_roots
        ):
            minimal_roots.append(root)
    removed: list[str] = []
    retry_count = 0
    for root in minimal_roots:
        if not root.exists():
            continue
        retry_count += remove_tree_with_readonly_retry(root)
        removed.append(root.relative_to(fixture).as_posix())
    remaining = [
        key
        for key in lifecycle.WRITE_ROOT_ENV_KEYS
        if Path(env[key]).resolve().exists()
    ]
    if remaining:
        raise lifecycle.PluginFixtureError(
            "isolated write roots remained after cleanup: " + ", ".join(remaining)
        )
    return {
        "write_root_keys": len(lifecycle.WRITE_ROOT_ENV_KEYS),
        "minimal_roots_removed": sorted(removed),
        "windows_handle_release_retries": retry_count,
        "read_only_git_objects_supported": True,
        "all_write_roots_absent": True,
    }


def wait_for_protected_quiet_window(
    *, stable_seconds: float = 2.0, timeout_seconds: float = 30.0
) -> dict[str, dict[str, Any]]:
    current = lifecycle.protected_user_snapshot()
    stable_since = time.monotonic()
    deadline = stable_since + timeout_seconds
    while time.monotonic() < deadline:
        time.sleep(0.25)
        observed = lifecycle.protected_user_snapshot()
        if observed != current:
            current = observed
            stable_since = time.monotonic()
            continue
        if time.monotonic() - stable_since >= stable_seconds:
            return current
    raise lifecycle.PluginFixtureError(
        "protected user metadata did not enter a quiet window"
    )


def changed_boundary_labels(
    before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]
) -> list[str]:
    return sorted(
        key
        for key in before.keys() | after.keys()
        if before.get(key) != after.get(key)
    )


def guarded_external_project_root(path: Path) -> Path:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.expanduser().resolve()
    try:
        relative = resolved.relative_to(temp_root)
    except ValueError as exc:
        raise lifecycle.PluginFixtureError(
            "external project root must stay under the system temp root"
        ) from exc
    if len(relative.parts) != 1 or not relative.name.startswith(EXTERNAL_PROJECT_PREFIX):
        raise lifecycle.PluginFixtureError("external project root identity is invalid")
    return resolved


def create_external_project_root() -> Path:
    return guarded_external_project_root(
        Path(tempfile.mkdtemp(prefix=EXTERNAL_PROJECT_PREFIX))
    )


def remove_external_project_root(
    path: Path, *, timeout_seconds: float = 45.0, retry_seconds: float = 0.1
) -> int:
    root = guarded_external_project_root(path)
    if not root.exists():
        return 0
    lifecycle.reject_symlink_tree(root, label="external L54 project fixture")
    deadline = time.monotonic() + timeout_seconds
    retries = 0

    def make_writable_and_retry(function: Any, raw_path: str, _: Any) -> None:
        target = Path(raw_path).resolve(strict=False)
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise lifecycle.PluginFixtureError(
                "external cleanup target escaped the guarded project root"
            ) from exc
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


def _set_path(payload: dict[str, Any], path: tuple[str, ...], value: str) -> None:
    target: dict[str, Any] = payload
    for part in path[:-1]:
        child = target.get(part)
        if not isinstance(child, dict):
            raise lifecycle.PluginFixtureError(
                "production Plugin manifest structure drifted"
            )
        target = child
    target[path[-1]] = value


def carrier_manifest() -> dict[str, Any]:
    production_manifest = package.validate_contract()["manifest"]
    candidate = copy.deepcopy(production_manifest)
    for path, value in PATH_REWRITES.items():
        _set_path(candidate, path, value)
    return candidate


def marketplace_manifest() -> dict[str, Any]:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "CoTend"},
        "plugins": [
            {
                "name": package.PLUGIN_NAME,
                "source": {"source": "url", "url": "./"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        ],
    }


def _manifest_path(root: Path, value: str, label: str) -> Path:
    if not value.startswith("./") or "\\" in value:
        raise lifecycle.PluginFixtureError(f"{label} must use a ./ POSIX path")
    target = (root / value[2:]).resolve(strict=False)
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise lifecycle.PluginFixtureError(f"{label} escapes the Plugin root") from exc
    return target


def validate_carrier_manifest(
    manifest: dict[str, Any], *, plugin_root: Path | None = None
) -> dict[str, Any]:
    expected = carrier_manifest()
    if manifest != expected:
        raise lifecycle.PluginFixtureError(
            "root carrier manifest differs from the mechanical production transform"
        )
    interface = manifest["interface"]
    assert isinstance(interface, dict)
    relative_paths = {
        "skills": str(manifest["skills"]),
        "composerIcon": str(interface["composerIcon"]),
        "logo": str(interface["logo"]),
        "logoDark": str(interface["logoDark"]),
    }
    if plugin_root is not None:
        root = plugin_root.resolve()
        for label, value in relative_paths.items():
            target = _manifest_path(root, value, label)
            if label == "skills" and not target.is_dir():
                raise lifecycle.PluginFixtureError("carrier Skill root is missing")
            if label != "skills" and not target.is_file():
                raise lifecycle.PluginFixtureError(f"carrier asset is missing: {label}")
    return {
        "mechanically_derived": True,
        "allowed_path_rewrites": len(PATH_REWRITES),
        "semantic_metadata_equal": True,
        "paths": relative_paths,
    }


def validate_marketplace_manifest(manifest: dict[str, Any]) -> None:
    if manifest != marketplace_manifest():
        raise lifecycle.PluginFixtureError("root Marketplace manifest drifted")
    source = manifest["plugins"][0]["source"]
    if source != {"source": "url", "url": "./"}:
        raise lifecycle.PluginFixtureError("root Marketplace source must be url ./")


def _copy_carrier_payload(plugin_root: Path) -> None:
    lifecycle.write_json(
        plugin_root / ".codex-plugin" / "plugin.json", carrier_manifest()
    )
    lifecycle.write_json(
        plugin_root / ".agents" / "plugins" / "marketplace.json",
        marketplace_manifest(),
    )
    shutil.copytree(package.SOURCE_SKILLS_ROOT, plugin_root / "skills")
    for relative, source in package.PACKAGE_SUPPORT_FILES.items():
        target = plugin_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    asset_root = plugin_root / "packaging" / "codex-plugin" / "cotend" / "assets"
    for relative, record in package.PACKAGE_BRAND_ASSETS.items():
        source = record["source"]
        assert isinstance(source, Path)
        target = asset_root / Path(relative).name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def verify_carrier_root(plugin_root: Path) -> dict[str, Any]:
    lifecycle.reject_symlink_tree(plugin_root, label="root carrier")
    manifest = lifecycle.load_json_object(
        plugin_root / ".codex-plugin" / "plugin.json", "carrier Plugin manifest"
    )
    manifest_result = validate_carrier_manifest(manifest, plugin_root=plugin_root)
    marketplace = lifecycle.load_json_object(
        plugin_root / ".agents" / "plugins" / "marketplace.json",
        "carrier Marketplace manifest",
    )
    validate_marketplace_manifest(marketplace)
    if (plugin_root / "codex-skills").exists():
        raise lifecycle.PluginFixtureError(
            "root carrier must not contain a second codex-skills/ source tree"
        )
    actual_skills = lifecycle.file_manifest(plugin_root / "skills")
    expected_skills = package.source_skill_manifest()
    if actual_skills != expected_skills:
        raise lifecycle.PluginFixtureError("root carrier Skill bytes drifted")
    for relative, source in package.PACKAGE_SUPPORT_FILES.items():
        if lifecycle.sha256(plugin_root / relative) != lifecycle.sha256(source):
            raise lifecycle.PluginFixtureError(
                f"root carrier support file drifted: {relative}"
            )
    asset_root = plugin_root / "packaging" / "codex-plugin" / "cotend" / "assets"
    for relative, record in package.PACKAGE_BRAND_ASSETS.items():
        source = record["source"]
        assert isinstance(source, Path)
        if lifecycle.sha256(asset_root / Path(relative).name) != lifecycle.sha256(source):
            raise lifecycle.PluginFixtureError(
                f"root carrier asset drifted: {relative}"
            )
    return {
        "manifest": manifest_result,
        "marketplace_source": "url_relative_root",
        "skills": len(package.EXPECTED_SKILLS),
        "skill_files": len(actual_skills),
        "source_bytes_identical": True,
        "duplicate_skill_tree": False,
        "brand_assets": len(package.PACKAGE_BRAND_ASSETS),
    }


def verify_repository_carrier() -> dict[str, Any]:
    if not PUBLIC_PLUGIN_MANIFEST.is_file() or not PUBLIC_MARKETPLACE_MANIFEST.is_file():
        raise lifecycle.PluginFixtureError(
            "repository root carrier files are not materialized"
        )
    manifest = lifecycle.load_json_object(
        PUBLIC_PLUGIN_MANIFEST, "repository carrier Plugin manifest"
    )
    marketplace = lifecycle.load_json_object(
        PUBLIC_MARKETPLACE_MANIFEST, "repository carrier Marketplace manifest"
    )
    validate_carrier_manifest(manifest, plugin_root=ROOT)
    validate_marketplace_manifest(marketplace)
    if (ROOT / "codex-skills").exists():
        raise lifecycle.PluginFixtureError(
            "repository root must use skills/ as its only semantic Skill source"
        )
    return {
        "status": "present_and_valid",
        "plugin_manifest": PUBLIC_PLUGIN_MANIFEST.relative_to(ROOT).as_posix(),
        "marketplace_manifest": PUBLIC_MARKETPLACE_MANIFEST.relative_to(ROOT).as_posix(),
        "single_semantic_skill_source": True,
    }


def materialize_scenario(
    fixture: Path, projects_root: Path | None = None
) -> dict[str, Any]:
    fixture = lifecycle.guarded_fixture(fixture)
    project_parent = fixture if projects_root is None else guarded_external_project_root(
        projects_root
    )
    marketplace_root = fixture / "source-marketplace"
    _copy_carrier_payload(marketplace_root)
    carrier = verify_carrier_root(marketplace_root)

    empty_project = project_parent / "project-empty"
    empty_project.mkdir(parents=True)
    (empty_project / "README.md").write_text(
        "# Empty root-carrier lifecycle project\n", encoding="utf-8"
    )
    coexist_project = project_parent / "project-with-standalone-skills"
    coexist_project.mkdir(parents=True)
    (coexist_project / "README.md").write_text(
        "# Root-carrier coexistence project\n", encoding="utf-8"
    )
    standalone_root = coexist_project / ".agents" / "skills"
    for skill in package.EXPECTED_SKILLS:
        shutil.copytree(package.SOURCE_SKILLS_ROOT / skill, standalone_root / skill)
    (fixture / "evidence" / "commands").mkdir(parents=True)
    return {"marketplace_root": marketplace_root, "carrier": carrier}


def initialize_fixture_git_repository(
    fixture: Path, env: dict[str, str], repository: Path
) -> dict[str, str]:
    lifecycle.assert_fixture_path(fixture, repository, "fixture Git repository")
    isolated_env = dict(env)
    hooks = fixture / "git-hooks-empty"
    hooks.mkdir(exist_ok=True)
    commands = (
        ["git", "init", str(repository)],
        [
            "git",
            "-C",
            str(repository),
            "-c",
            "core.autocrlf=false",
            "add",
            "--all",
        ],
        [
            "git",
            "-C",
            str(repository),
            "-c",
            "user.name=CoTend Fixture",
            "-c",
            "user.email=cotend-fixture@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "-c",
            f"core.hooksPath={hooks}",
            "commit",
            "-m",
            "fixture root carrier",
        ],
    )
    for command in commands:
        completed = lifecycle.run_process(
            command, env=isolated_env, cwd=fixture, timeout=60
        )
        if completed.returncode != 0:
            raise lifecycle.PluginFixtureError(
                "isolated root-carrier Git fixture failed: "
                + (completed.stdout + completed.stderr)[-500:]
            )
    head = lifecycle.run_process(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        env=isolated_env,
        cwd=fixture,
    )
    status = lifecycle.run_process(
        ["git", "-C", str(repository), "status", "--porcelain"],
        env=isolated_env,
        cwd=fixture,
    )
    if head.returncode != 0 or status.returncode != 0 or status.stdout:
        raise lifecycle.PluginFixtureError("isolated Git fixture is not clean")
    return {"status": "clean_local_git_fixture", "head": head.stdout.strip()}


def configure_isolated_git_env(fixture: Path, env: dict[str, str]) -> None:
    config = fixture / "gitconfig-isolated"
    config.write_text(
        "[core]\n\tautocrlf = false\n\teol = lf\n",
        encoding="utf-8",
    )
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = str(config)


def run_official_validator(
    fixture: Path, env: dict[str, str], plugin_root: Path
) -> dict[str, str]:
    validator = lifecycle.plugin_creator_script("validate_plugin.py")
    completed = lifecycle.run_process(
        [sys.executable, str(validator), str(plugin_root)],
        env=env,
        cwd=fixture,
        timeout=60,
    )
    if completed.returncode != 0:
        raise lifecycle.PluginFixtureError(
            "Plugin Creator validator failed for root carrier: "
            + (completed.stdout + completed.stderr)[-800:]
        )
    return {
        "status": "passed",
        "validator_sha256": lifecycle.sha256(validator),
    }


def source_snapshot() -> dict[str, Any]:
    contract = package.validate_contract()
    root_files: dict[str, str] = {}
    for path in (PUBLIC_PLUGIN_MANIFEST, PUBLIC_MARKETPLACE_MANIFEST):
        if path.is_file():
            root_files[path.relative_to(ROOT).as_posix()] = lifecycle.sha256(path)
    return {
        "git_head": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "source_manifest": contract["source_manifest"],
        "production_manifest_sha256": package.sha256_file(package.MANIFEST_SOURCE),
        "package_lock_sha256": package.sha256_file(package.PACKAGE_LOCK_PATH),
        "artifact_lock_sha256": package.sha256_file(package.TARGET_ARTIFACT_LOCK),
        "root_carrier_files": root_files,
    }


def prepare_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, Any], Path]:
    fixture = lifecycle.guarded_fixture(fixture)
    fixture.mkdir(parents=True, exist_ok=True)
    env = lifecycle.build_isolated_env(fixture)
    configure_isolated_git_env(fixture, env)
    projects_root = create_external_project_root()
    try:
        preflight = lifecycle.run_preflight(fixture, env, protected_before)
        materialized = materialize_scenario(fixture, projects_root)
        git_fixture = initialize_fixture_git_repository(
            fixture, env, materialized["marketplace_root"]
        )
        official = run_official_validator(
            fixture, env, materialized["marketplace_root"]
        )
        lifecycle.assert_protected_unchanged(protected_before)
        return env, {
            "preflight": preflight,
            "carrier": materialized["carrier"],
            "git_fixture": git_fixture,
            "project_fixture_boundary": "owned_external_system_temp_root",
            "official_validator": official,
        }, projects_root
    except Exception:
        try:
            purge_isolated_write_roots(fixture, env)
        finally:
            remove_external_project_root(projects_root)
        raise


def validate_root_plugin_source(source: Any, fixture: Path) -> str:
    item = lifecycle.require_json_object(source, "root carrier Plugin source")
    if item == {"source": "url", "url": "./"}:
        return "url_relative_root"
    if item.get("source") == "local":
        source_path = Path(str(item.get("path", ""))).resolve()
        if source_path == (fixture / "source-marketplace").resolve():
            return "normalized_local_root"
    if item.get("source") == "git":
        source_path = Path(str(item.get("url", ""))).resolve()
        if source_path == (fixture / "source-marketplace").resolve():
            return "normalized_git_root"
    raise lifecycle.PluginFixtureError(
        "Plugin source did not resolve to the Marketplace root"
    )


def validate_root_plugin_list_payload(
    payload: Any,
    fixture: Path,
    *,
    installed: bool,
    available: bool,
) -> dict[str, Any]:
    root = lifecycle.require_json_object(payload, "root carrier Plugin list output")
    installed_items = root.get("installed")
    available_items = root.get("available")
    if not isinstance(installed_items, list) or not isinstance(available_items, list):
        raise lifecycle.PluginFixtureError(
            "root carrier Plugin list omitted installed or available arrays"
        )
    installed_matches = [
        item
        for item in installed_items
        if item.get("pluginId") == CARRIER_IDENTITY.selector
    ]
    available_matches = [
        item
        for item in available_items
        if item.get("pluginId") == CARRIER_IDENTITY.selector
    ]
    if bool(installed_matches) != installed or bool(available_matches) != available:
        raise lifecycle.PluginFixtureError("root carrier Plugin state mismatch")
    source_forms: set[str] = set()
    for item, expected_installed, expected_enabled in (
        *[(value, True, True) for value in installed_matches],
        *[(value, False, False) for value in available_matches],
    ):
        expected = {
            "name": package.PLUGIN_NAME,
            "marketplaceName": MARKETPLACE_NAME,
            "version": package.PLUGIN_VERSION if expected_installed else None,
            "installed": expected_installed,
            "enabled": expected_enabled,
            "installPolicy": "AVAILABLE",
            "authPolicy": "ON_INSTALL",
        }
        for key, value in expected.items():
            if item.get(key) != value:
                raise lifecycle.PluginFixtureError(
                    f"root carrier Plugin list mismatch: {key}"
                )
        source_forms.add(validate_root_plugin_source(item.get("source"), fixture))
    return {"source_forms": sorted(source_forms)}


def observe_cli_step(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    step: str,
    arguments: list[str],
) -> dict[str, Any]:
    command = [
        lifecycle.codex_executable(),
        "--disable",
        "remote_plugin",
        "plugin",
        *arguments,
    ]
    completed = lifecycle.run_process(command, env=env, cwd=fixture, timeout=90)
    record: dict[str, Any] = {
        "argv": ["codex", "--disable", "remote_plugin", "plugin", *arguments],
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    try:
        record["json"] = json.loads(completed.stdout)
    except json.JSONDecodeError:
        record["json"] = None
    lifecycle.write_json(fixture / "evidence" / "commands" / f"{step}.json", record)
    lifecycle.assert_protected_unchanged(protected_before)
    return record


def validate_repeat_add_observation(record: dict[str, Any]) -> str:
    if record["returncode"] == 0:
        payload = lifecycle.require_json_object(record.get("json"), "repeat add output")
        if payload.get("marketplaceName") != MARKETPLACE_NAME:
            raise lifecycle.PluginFixtureError("repeat add Marketplace mismatch")
        if payload.get("alreadyAdded") is not True:
            raise lifecycle.PluginFixtureError("repeat add did not report alreadyAdded")
        return "idempotent_success"
    combined = (str(record.get("stdout", "")) + str(record.get("stderr", ""))).lower()
    if "already" not in combined:
        raise lifecycle.PluginFixtureError("repeat add failed for an unknown reason")
    return "explicit_already_configured"


def validate_local_refresh_observation(record: dict[str, Any]) -> str:
    if record["returncode"] == 0:
        payload = lifecycle.require_json_object(record.get("json"), "local refresh output")
        serialized = json.dumps(payload, sort_keys=True)
        if MARKETPLACE_NAME not in serialized:
            raise lifecycle.PluginFixtureError("local refresh omitted Marketplace identity")
        return "local_refresh_success"
    combined = (str(record.get("stdout", "")) + str(record.get("stderr", ""))).lower()
    expected = f"marketplace `{MARKETPLACE_NAME}` is not configured as a git marketplace"
    if expected not in combined:
        raise lifecycle.PluginFixtureError("local refresh failed for an unknown reason")
    return "local_marketplace_not_git_upgradeable"


def run_lifecycle(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    source_before: dict[str, Any],
    *,
    projects_root: Path,
    fail_after_step: str | None = None,
) -> dict[str, Any]:
    marketplace_root = fixture / "source-marketplace"
    projects_root = guarded_external_project_root(projects_root)
    empty_project = projects_root / "project-empty"
    coexist_project = projects_root / "project-with-standalone-skills"
    steps: list[str] = []

    def mark(step: str) -> None:
        steps.append(step)
        if fail_after_step == step:
            raise lifecycle.PluginFixtureError(
                f"injected root-carrier lifecycle failure after {step}"
            )

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-add",
        ["marketplace", "add", str(marketplace_root), "--json"],
    )
    lifecycle.validate_marketplace_add_payload(payload, fixture, CARRIER_IDENTITY)
    mark("marketplace_add")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-list",
        ["marketplace", "list", "--json"],
    )
    lifecycle.validate_marketplace_list_payload(
        payload, present=True, identity=CARRIER_IDENTITY
    )
    mark("marketplace_list")

    repeated = observe_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-repeat-add",
        ["marketplace", "add", str(marketplace_root), "--json"],
    )
    repeat_result = validate_repeat_add_observation(repeated)
    mark("marketplace_repeat_add")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-available",
        ["list", "--marketplace", MARKETPLACE_NAME, "--available", "--json"],
    )
    available_source = validate_root_plugin_list_payload(
        payload, fixture, installed=False, available=True
    )
    mark("plugin_available")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-add",
        ["add", CARRIER_IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_add_payload(payload, fixture, CARRIER_IDENTITY)
    mark("plugin_add")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-list-installed",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    installed_source = validate_root_plugin_list_payload(
        payload, fixture, installed=True, available=False
    )
    mark("plugin_list_installed")

    installed = lifecycle.discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=True,
        expect_standalone=False,
        identity=CARRIER_IDENTITY,
        cwd_boundary=projects_root,
    )
    mark("discovery_installed")
    coexistence = lifecycle.discover_skills(
        fixture,
        env,
        coexist_project,
        expect_plugin=True,
        expect_standalone=True,
        identity=CARRIER_IDENTITY,
        cwd_boundary=projects_root,
    )
    mark("discovery_coexistence")

    refresh = observe_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-local-refresh",
        ["marketplace", "upgrade", MARKETPLACE_NAME, "--json"],
    )
    refresh_result = validate_local_refresh_observation(refresh)
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-list-after-refresh",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    validate_root_plugin_list_payload(payload, fixture, installed=True, available=False)
    mark("local_refresh_state_preserved")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-remove",
        ["remove", CARRIER_IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_remove_payload(payload, CARRIER_IDENTITY)
    mark("plugin_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-list-after-remove",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    validate_root_plugin_list_payload(payload, fixture, installed=False, available=False)
    removed = lifecycle.discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=False,
        expect_standalone=False,
        identity=CARRIER_IDENTITY,
        cwd_boundary=projects_root,
    )
    mark("plugin_removed_and_undiscoverable")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-reinstall",
        ["add", CARRIER_IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_add_payload(payload, fixture, CARRIER_IDENTITY)
    reinstalled = lifecycle.discover_skills(
        fixture,
        env,
        empty_project,
        expect_plugin=True,
        expect_standalone=False,
        identity=CARRIER_IDENTITY,
        cwd_boundary=projects_root,
    )
    mark("plugin_reinstalled_and_discovered")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "plugin-final-remove",
        ["remove", CARRIER_IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_remove_payload(payload, CARRIER_IDENTITY)
    mark("plugin_final_remove")
    lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-remove",
        ["marketplace", "remove", MARKETPLACE_NAME, "--json"],
    )
    mark("marketplace_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "marketplace-list-final",
        ["marketplace", "list", "--json"],
    )
    lifecycle.validate_marketplace_list_payload(
        payload, present=False, identity=CARRIER_IDENTITY
    )
    mark("marketplace_final_absent")

    if source_snapshot() != source_before:
        raise lifecycle.PluginFixtureError(
            "repository carrier inputs, locks, or Git HEAD changed"
        )
    lifecycle.assert_protected_unchanged(protected_before)
    return {
        "status": "passed",
        "steps": steps,
        "step_count": len(steps),
        "repeat_add": repeat_result,
        "local_refresh": refresh_result,
        "available_source": available_source,
        "installed_source": installed_source,
        "installed_discovery": installed,
        "coexistence_discovery": coexistence,
        "removed_discovery": removed,
        "reinstalled_discovery": reinstalled,
        "final_plugin_installed": False,
        "final_marketplace_configured": False,
    }


def recover_after_injected_failure(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    projects_root: Path,
) -> dict[str, Any]:
    steps: list[str] = []
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "recovery-plugin-remove",
        ["remove", CARRIER_IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_remove_payload(payload, CARRIER_IDENTITY)
    steps.append("plugin_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "recovery-plugin-list",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    validate_root_plugin_list_payload(payload, fixture, installed=False, available=False)
    steps.append("plugin_absent")
    discovery = lifecycle.discover_skills(
        fixture,
        env,
        guarded_external_project_root(projects_root) / "project-empty",
        expect_plugin=False,
        expect_standalone=False,
        identity=CARRIER_IDENTITY,
        cwd_boundary=projects_root,
    )
    steps.append("discovery_absent")
    lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "recovery-marketplace-remove",
        ["marketplace", "remove", MARKETPLACE_NAME, "--json"],
    )
    steps.append("marketplace_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "recovery-marketplace-list",
        ["marketplace", "list", "--json"],
    )
    lifecycle.validate_marketplace_list_payload(
        payload, present=False, identity=CARRIER_IDENTITY
    )
    steps.append("marketplace_absent")
    return {"steps": steps, "step_count": len(steps), "discovery": discovery}


def run_success_scenario(
    fixture: Path, protected_before: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    source_before = source_snapshot()
    env, preparation, projects_root = prepare_scenario(fixture, protected_before)
    try:
        result = run_lifecycle(
            fixture,
            env,
            protected_before,
            source_before,
            projects_root=projects_root,
        )
    finally:
        try:
            cleanup = purge_isolated_write_roots(fixture, env)
        finally:
            external_retries = remove_external_project_root(projects_root)
        cleanup["external_project_root_removed"] = True
        cleanup["external_project_handle_release_retries"] = external_retries
    return {"preparation": preparation, "lifecycle": result, "cleanup": cleanup}


def run_failure_recovery_scenario(
    fixture: Path, protected_before: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    source_before = source_snapshot()
    env, preparation, projects_root = prepare_scenario(fixture, protected_before)
    injected_error = ""
    recovery: dict[str, Any] | None = None
    try:
        try:
            run_lifecycle(
                fixture,
                env,
                protected_before,
                source_before,
                projects_root=projects_root,
                fail_after_step="plugin_add",
            )
        except lifecycle.PluginFixtureError as exc:
            injected_error = str(exc)
            if injected_error != (
                "injected root-carrier lifecycle failure after plugin_add"
            ):
                raise
        else:
            raise lifecycle.PluginFixtureError("injected failure did not fire")
        recovery = recover_after_injected_failure(
            fixture, env, protected_before, projects_root
        )
    finally:
        try:
            cleanup = purge_isolated_write_roots(fixture, env)
        finally:
            external_retries = remove_external_project_root(projects_root)
        cleanup["external_project_root_removed"] = True
        cleanup["external_project_handle_release_retries"] = external_retries
    if recovery is None:
        raise lifecycle.PluginFixtureError("root-carrier failure recovery did not finish")
    return {
        "preparation": preparation,
        "injected_after": "plugin_add",
        "injected_error": injected_error,
        "recovery": recovery,
        "cleanup": cleanup,
    }


def write_evidence(path: Path, run_root: Path, payload: dict[str, Any]) -> None:
    target = path.expanduser().resolve(strict=False)
    run_root = guarded_run_root(run_root)
    try:
        relative = target.relative_to(run_root)
    except ValueError as exc:
        raise lifecycle.PluginFixtureError(
            "GitHub carrier evidence must stay under the L54 run root"
        ) from exc
    if not relative.parts:
        raise lifecycle.PluginFixtureError("evidence path cannot be the run root")
    lifecycle.write_json(target, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the CoTend GitHub Marketplace root carrier."
    )
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument(
        "--fixture-only",
        action="store_true",
        help="Run the pre-materialization fixture gate without requiring root files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_root = reset_run_root(args.run_root)
        evidence_path = args.evidence or run_root / "RESULT.json"
        repository_carrier = (
            {"status": "not_materialized_fixture_gate"}
            if args.fixture_only
            else verify_repository_carrier()
        )
        source_before = source_snapshot()
        success_boundary = wait_for_protected_quiet_window()
        success = run_success_scenario(run_root / "success", success_boundary)
        failure_boundary = wait_for_protected_quiet_window()
        failure = run_failure_recovery_scenario(
            run_root / "failure-recovery", failure_boundary
        )
        if source_snapshot() != source_before:
            raise lifecycle.PluginFixtureError(
                "repository carrier inputs changed during validation"
            )
        lifecycle.assert_protected_unchanged(failure_boundary)
        between_scenario_changes = changed_boundary_labels(
            success_boundary, failure_boundary
        )
        evidence = {
            "status": "passed_isolated_github_marketplace_root_carrier",
            "evidence_type": "executed",
            "repository_carrier": repository_carrier,
            "plugin": {
                "name": package.PLUGIN_NAME,
                "version": package.PLUGIN_VERSION,
                "marketplace": MARKETPLACE_NAME,
            },
            "success_scenario": success,
            "failure_recovery_scenario": failure,
            "verification": {
                "skills": len(package.EXPECTED_SKILLS),
                "skill_files": len(package.source_skill_manifest()),
                "write_roots_redirected": len(lifecycle.WRITE_ROOT_ENV_KEYS),
                "protected_user_boundaries": len(success_boundary),
                "protected_user_metadata_unchanged_during_each_scenario": True,
                "between_scenario_metadata_changes": between_scenario_changes,
                "runtime_write_roots_purged": True,
                "single_semantic_skill_source": True,
            },
            "not_run": list(POST_PUSH_NOT_RUN),
        }
        write_evidence(evidence_path, run_root, evidence)
        print(
            "GITHUB_MARKETPLACE_CARRIER_OK "
            f"version={package.PLUGIN_VERSION} "
            f"steps={success['lifecycle']['step_count']} "
            f"recovery={failure['recovery']['step_count']} "
            f"skills={len(package.EXPECTED_SKILLS)} "
            f"roots={len(lifecycle.WRITE_ROOT_ENV_KEYS)} "
            "purged=true protected_unchanged=true remote_git=not_run"
        )
        return 0
    except (
        lifecycle.PluginFixtureError,
        package.PluginPackageError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print(f"GITHUB_MARKETPLACE_CARRIER_FAILED {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
