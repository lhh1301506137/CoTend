from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import verify_github_marketplace_carrier as local_carrier  # noqa: E402
import verify_isolated_codex_plugin as lifecycle  # noqa: E402


PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_RUN_ROOT = PRIVATE_ROOT / "L55-remote-github-marketplace"
REMOTE_SLUG = "lhh1301506137/CoTend"
REMOTE_URL = "https://github.com/lhh1301506137/CoTend.git"
MARKETPLACE_NAME = local_carrier.MARKETPLACE_NAME
IDENTITY = local_carrier.CARRIER_IDENTITY
EXTERNAL_PROJECT_PREFIX = "cotend-L55-projects-"
INSTALL_METADATA_NAME = ".codex-marketplace-install.json"
PROXY_KEYS = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY")
POST_VALIDATION_NOT_RUN = (
    "desktop_visible_install_and_restart_behavior",
    "real_user_scope_install",
    "github_release",
    "second_public_push",
    "public_plugin_directory_submission",
)


def guarded_run_root(path: Path) -> Path:
    resolved = lifecycle.guarded_fixture(path)
    relative = resolved.relative_to(PRIVATE_ROOT.resolve())
    if not relative.parts[0].startswith("L55-"):
        raise lifecycle.PluginFixtureError(
            "remote GitHub run root must use an L55-prefixed private directory"
        )
    return resolved


def reset_run_root(path: Path) -> Path:
    resolved = guarded_run_root(path)
    if resolved.exists():
        lifecycle.reject_symlink_tree(resolved, label="L55 run root")
        local_carrier.remove_tree_with_readonly_retry(resolved)
    resolved.mkdir(parents=True)
    return resolved


def guarded_external_project_root(path: Path) -> Path:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.expanduser().resolve()
    try:
        relative = resolved.relative_to(temp_root)
    except ValueError as exc:
        raise lifecycle.PluginFixtureError(
            "remote project root must stay under the system temp root"
        ) from exc
    if len(relative.parts) != 1 or not relative.name.startswith(
        EXTERNAL_PROJECT_PREFIX
    ):
        raise lifecycle.PluginFixtureError(
            "remote project root identity is invalid"
        )
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
    lifecycle.reject_symlink_tree(root, label="external L55 project fixture")
    deadline = time.monotonic() + timeout_seconds
    retries = 0

    def make_writable_and_retry(function: Any, raw_path: str, _: Any) -> None:
        target = Path(raw_path).resolve(strict=False)
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise lifecycle.PluginFixtureError(
                "remote project cleanup escaped its guarded root"
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


def configure_network_git_env(fixture: Path, env: dict[str, str]) -> None:
    fixture = lifecycle.guarded_fixture(fixture)
    config = fixture / "gitconfig-network-isolated"
    config.write_text(
        "[core]\n"
        "\tautocrlf = false\n"
        "\teol = lf\n"
        "[credential]\n"
        "\thelper =\n",
        encoding="utf-8",
    )
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = str(config)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "Never"


def build_network_isolated_env(fixture: Path) -> dict[str, str]:
    fixture = lifecycle.guarded_fixture(fixture)
    env = lifecycle.build_isolated_env(fixture)
    for key in (*PROXY_KEYS, "NO_PROXY"):
        env.pop(key, None)
    env.update(validated_loopback_proxy_env(os.environ))
    configure_network_git_env(fixture, env)
    validate_network_isolated_env(fixture, env)
    return env


def validated_loopback_proxy_env(source: dict[str, str] | os._Environ[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key in PROXY_KEYS:
        value = source.get(key, "")
        if not value:
            continue
        parsed = urlsplit(value)
        try:
            port = parsed.port
        except ValueError as exc:
            raise lifecycle.PluginFixtureError(
                f"remote verifier proxy port is invalid: {key}"
            ) from exc
        if (
            parsed.scheme not in {"http", "https", "socks5", "socks5h"}
            or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed.username is not None
            or parsed.password is not None
            or port is None
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            raise lifecycle.PluginFixtureError(
                f"remote verifier only permits credential-free loopback proxy: {key}"
            )
        result[key] = value
    return result


def validate_network_isolated_env(
    fixture: Path, env: dict[str, str]
) -> None:
    lifecycle.validate_isolated_env(fixture, env)
    validated_loopback_proxy_env(env)
    if "NO_PROXY" in env:
        raise lifecycle.PluginFixtureError(
            "remote verifier proxy policy drifted"
        )
    expected = {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GCM_INTERACTIVE": "Never",
    }
    for key, value in expected.items():
        if env.get(key) != value:
            raise lifecycle.PluginFixtureError(
                f"remote verifier Git safety control drifted: {key}"
            )
    config = Path(env.get("GIT_CONFIG_GLOBAL", "")).resolve()
    lifecycle.assert_fixture_path(fixture, config, "remote Git config")
    text = config.read_text(encoding="utf-8")
    if "[credential]" not in text or "helper =" not in text:
        raise lifecycle.PluginFixtureError(
            "remote verifier must disable Git credential helpers"
        )


def validate_remote_slug(value: str) -> str:
    if value != REMOTE_SLUG:
        raise lifecycle.PluginFixtureError(
            "remote verifier only permits the canonical CoTend repository"
        )
    return value


def validate_expected_head(value: str) -> str:
    normalized = value.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", normalized):
        raise lifecycle.PluginFixtureError(
            "expected remote head must be a full Git commit"
        )
    return normalized


def git_text(
    command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    completed = lifecycle.run_process(command, env=env, cwd=cwd, timeout=90)
    if completed.returncode != 0:
        raise lifecycle.PluginFixtureError(
            "Git command failed: " + (completed.stdout + completed.stderr)[-500:]
        )
    return completed.stdout.strip()


def local_git_head() -> str:
    return validate_expected_head(git_text(["git", "rev-parse", "HEAD"]))


def expected_clone_root(fixture: Path) -> Path:
    fixture = lifecycle.guarded_fixture(fixture)
    return (fixture / "codex-home" / ".tmp" / "marketplaces" / MARKETPLACE_NAME).resolve()


def validate_marketplace_add_payload(payload: Any, fixture: Path) -> Path:
    root = lifecycle.require_json_object(payload, "remote Marketplace add output")
    clone_root = Path(str(root.get("installedRoot", ""))).resolve()
    if (
        root.get("marketplaceName") != MARKETPLACE_NAME
        or root.get("alreadyAdded") is not False
        or clone_root != expected_clone_root(fixture)
    ):
        raise lifecycle.PluginFixtureError(
            "remote Marketplace add output drifted"
        )
    lifecycle.assert_fixture_path(fixture, clone_root, "remote Marketplace clone")
    return clone_root


def validate_marketplace_list_payload(
    payload: Any, fixture: Path, *, present: bool
) -> None:
    root = lifecycle.require_json_object(payload, "remote Marketplace list output")
    items = root.get("marketplaces")
    if not isinstance(items, list):
        raise lifecycle.PluginFixtureError(
            "remote Marketplace list omitted marketplaces"
        )
    matches = [
        lifecycle.require_json_object(item, "remote Marketplace entry")
        for item in items
        if isinstance(item, dict) and item.get("name") == MARKETPLACE_NAME
    ]
    if bool(matches) != present:
        raise lifecycle.PluginFixtureError(
            "remote Marketplace presence mismatch"
        )
    if not present:
        return
    if len(matches) != 1:
        raise lifecycle.PluginFixtureError(
            "remote Marketplace must appear exactly once"
        )
    item = matches[0]
    source = lifecycle.require_json_object(
        item.get("marketplaceSource"), "remote Marketplace source"
    )
    if (
        Path(str(item.get("root", ""))).resolve()
        != expected_clone_root(fixture)
        or source != {"sourceType": "git", "source": REMOTE_URL}
    ):
        raise lifecycle.PluginFixtureError(
            "remote Marketplace source or root drifted"
        )


def validate_remote_git_state(
    origin: str, head: str, expected_head: str
) -> dict[str, str]:
    normalized_origin = origin.strip().rstrip("/")
    if normalized_origin != REMOTE_URL:
        raise lifecycle.PluginFixtureError(
            "remote Marketplace clone origin drifted"
        )
    actual_head = validate_expected_head(head)
    expected = validate_expected_head(expected_head)
    if actual_head != expected:
        raise lifecycle.PluginFixtureError(
            "remote Marketplace clone head does not match the approved commit"
        )
    return {"origin": normalized_origin, "head": actual_head}


def validate_install_metadata(
    clone_root: Path, expected_head: str
) -> dict[str, Any]:
    path = clone_root / INSTALL_METADATA_NAME
    if not path.is_file() or path.is_symlink():
        raise lifecycle.PluginFixtureError(
            "Codex Marketplace install metadata is missing or unsafe"
        )
    payload = lifecycle.load_json_object(
        path, "Codex Marketplace install metadata"
    )
    expected = {
        "source_type": "git",
        "source": REMOTE_URL,
        "ref_name": None,
        "sparse_paths": [],
        "revision": validate_expected_head(expected_head),
    }
    if payload != expected:
        raise lifecycle.PluginFixtureError(
            "Codex Marketplace install metadata drifted"
        )
    return {"path": INSTALL_METADATA_NAME, "schema": "exact_expected_values"}


def inspect_remote_clone(
    fixture: Path,
    env: dict[str, str],
    clone_root: Path,
    expected_head: str,
    *,
    allow_install_metadata: bool = False,
) -> dict[str, Any]:
    lifecycle.assert_fixture_path(fixture, clone_root, "remote Marketplace clone")
    lifecycle.reject_symlink_tree(clone_root, label="remote Marketplace clone")
    origin = git_text(
        ["git", "-C", str(clone_root), "remote", "get-url", "origin"],
        cwd=fixture,
        env=env,
    )
    head = git_text(
        ["git", "-C", str(clone_root), "rev-parse", "HEAD"],
        cwd=fixture,
        env=env,
    )
    status = git_text(
        ["git", "-C", str(clone_root), "status", "--porcelain"],
        cwd=fixture,
        env=env,
    )
    expected_status = f"?? {INSTALL_METADATA_NAME}" if allow_install_metadata else ""
    if status != expected_status:
        raise lifecycle.PluginFixtureError(
            "remote Marketplace clone worktree drifted"
        )
    result: dict[str, Any] = validate_remote_git_state(
        origin, head, expected_head
    )
    result["worktree"] = (
        "platform_install_metadata_only" if allow_install_metadata else "clean"
    )
    if allow_install_metadata:
        result["install_metadata"] = validate_install_metadata(
            clone_root, expected_head
        )
    return result


def validate_remote_plugin_list_payload(
    payload: Any,
    fixture: Path,
    *,
    installed: bool,
    available: bool,
) -> None:
    root = lifecycle.require_json_object(payload, "remote Plugin list output")
    installed_items = root.get("installed")
    available_items = root.get("available")
    if not isinstance(installed_items, list) or not isinstance(
        available_items, list
    ):
        raise lifecycle.PluginFixtureError(
            "remote Plugin list omitted installed or available arrays"
        )
    installed_matches = [
        lifecycle.require_json_object(item, "installed remote Plugin")
        for item in installed_items
        if isinstance(item, dict) and item.get("pluginId") == IDENTITY.selector
    ]
    available_matches = [
        lifecycle.require_json_object(item, "available remote Plugin")
        for item in available_items
        if isinstance(item, dict) and item.get("pluginId") == IDENTITY.selector
    ]
    if bool(installed_matches) != installed or bool(
        available_matches
    ) != available:
        raise lifecycle.PluginFixtureError("remote Plugin state mismatch")
    for item, is_installed in (
        *[(value, True) for value in installed_matches],
        *[(value, False) for value in available_matches],
    ):
        expected = {
            "name": package.PLUGIN_NAME,
            "marketplaceName": MARKETPLACE_NAME,
            "version": package.PLUGIN_VERSION if is_installed else None,
            "installed": is_installed,
            "enabled": is_installed,
            "installPolicy": "AVAILABLE",
            "authPolicy": "ON_INSTALL",
        }
        for key, value in expected.items():
            if item.get(key) != value:
                raise lifecycle.PluginFixtureError(
                    f"remote Plugin list mismatch: {key}"
                )
        source = lifecycle.require_json_object(
            item.get("source"), "remote Plugin source"
        )
        marketplace_source = lifecycle.require_json_object(
            item.get("marketplaceSource"), "remote Plugin Marketplace source"
        )
        if source != {
            "source": "git",
            "url": str(expected_clone_root(fixture)),
        } or marketplace_source != {
            "sourceType": "git",
            "source": REMOTE_URL,
        }:
            raise lifecycle.PluginFixtureError(
                "remote Plugin source provenance drifted"
            )


def validate_upgrade_payload(payload: Any, clone_root: Path) -> None:
    root = lifecycle.require_json_object(payload, "remote Marketplace upgrade output")
    upgraded = root.get("upgradedRoots")
    if (
        root.get("selectedMarketplaces") != [MARKETPLACE_NAME]
        or root.get("errors") != []
        or not isinstance(upgraded, list)
        or [Path(str(value)).resolve() for value in upgraded] != [clone_root.resolve()]
    ):
        raise lifecycle.PluginFixtureError(
            "remote Marketplace upgrade output drifted"
        )


def materialize_external_project(projects_root: Path) -> Path:
    root = guarded_external_project_root(projects_root)
    project = root / "clean-novice-project"
    project.mkdir(parents=True)
    (project / "README.md").write_text(
        "# Clean remote Marketplace validation project\n", encoding="utf-8"
    )
    return project


def prepare_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, Any], Path, Path]:
    fixture = lifecycle.guarded_fixture(fixture)
    fixture.mkdir(parents=True, exist_ok=True)
    env: dict[str, str] | None = None
    projects_root: Path | None = None
    try:
        env = build_network_isolated_env(fixture)
        projects_root = create_external_project_root()
        preflight = lifecycle.run_preflight(fixture, env, protected_before)
        project = materialize_external_project(projects_root)
        (fixture / "evidence" / "commands").mkdir(parents=True)
        lifecycle.assert_protected_unchanged(protected_before)
        return env, {
            "preflight": preflight,
            "network_policy": "public_GitHub_only_by_exact_command",
            "credential_inheritance": False,
            "project_fixture_boundary": "owned_external_system_temp_root",
        }, projects_root, project
    except Exception:
        try:
            if env is None:
                local_carrier.remove_tree_with_readonly_retry(fixture)
            else:
                local_carrier.purge_isolated_write_roots(fixture, env)
        finally:
            if projects_root is not None:
                remove_external_project_root(projects_root)
        raise


def run_remote_lifecycle(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    source_before: dict[str, Any],
    *,
    expected_head: str,
    projects_root: Path,
    project: Path,
    fail_after_step: str | None = None,
) -> dict[str, Any]:
    steps: list[str] = []

    def mark(step: str) -> None:
        steps.append(step)
        if fail_after_step == step:
            raise lifecycle.PluginFixtureError(
                f"injected remote lifecycle failure after {step}"
            )

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-marketplace-add",
        ["marketplace", "add", validate_remote_slug(REMOTE_SLUG), "--json"],
    )
    clone_root = validate_marketplace_add_payload(payload, fixture)
    mark("marketplace_add")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-marketplace-list",
        ["marketplace", "list", "--json"],
    )
    validate_marketplace_list_payload(payload, fixture, present=True)
    mark("marketplace_list")
    remote_git = inspect_remote_clone(
        fixture, env, clone_root, expected_head
    )
    mark("remote_head_verified")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-plugin-available",
        ["list", "--marketplace", MARKETPLACE_NAME, "--available", "--json"],
    )
    validate_remote_plugin_list_payload(
        payload, fixture, installed=False, available=True
    )
    mark("plugin_available")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-marketplace-upgrade",
        ["marketplace", "upgrade", MARKETPLACE_NAME, "--json"],
    )
    validate_upgrade_payload(payload, clone_root)
    upgraded_git = inspect_remote_clone(
        fixture,
        env,
        clone_root,
        expected_head,
        allow_install_metadata=True,
    )
    mark("git_backed_marketplace_upgrade")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-plugin-add",
        ["add", IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_add_payload(payload, fixture, IDENTITY)
    mark("plugin_add")
    discovery = lifecycle.discover_skills(
        fixture,
        env,
        project,
        expect_plugin=True,
        expect_standalone=False,
        identity=IDENTITY,
        cwd_boundary=projects_root,
    )
    lifecycle.assert_protected_unchanged(protected_before)
    mark("plugin_discovery")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-plugin-list-installed",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    validate_remote_plugin_list_payload(
        payload, fixture, installed=True, available=False
    )
    mark("plugin_list_installed")

    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-plugin-remove",
        ["remove", IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_remove_payload(payload, IDENTITY)
    mark("plugin_remove")
    removed = lifecycle.discover_skills(
        fixture,
        env,
        project,
        expect_plugin=False,
        expect_standalone=False,
        identity=IDENTITY,
        cwd_boundary=projects_root,
    )
    lifecycle.assert_protected_unchanged(protected_before)
    mark("plugin_discovery_absent")
    lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-marketplace-remove",
        ["marketplace", "remove", MARKETPLACE_NAME, "--json"],
    )
    mark("marketplace_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-marketplace-list-final",
        ["marketplace", "list", "--json"],
    )
    validate_marketplace_list_payload(payload, fixture, present=False)
    mark("marketplace_absent")

    if local_carrier.source_snapshot() != source_before:
        raise lifecycle.PluginFixtureError(
            "repository carrier inputs changed during remote validation"
        )
    lifecycle.assert_protected_unchanged(protected_before)
    return {
        "status": "passed",
        "steps": steps,
        "step_count": len(steps),
        "remote_git_before_upgrade": remote_git,
        "remote_git_after_upgrade": upgraded_git,
        "discovery": discovery,
        "removed_discovery": removed,
        "final_plugin_installed": False,
        "final_marketplace_configured": False,
    }


def recover_after_injected_failure(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    projects_root: Path,
    project: Path,
) -> dict[str, Any]:
    steps: list[str] = []
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-recovery-plugin-remove",
        ["remove", IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_remove_payload(payload, IDENTITY)
    steps.append("plugin_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-recovery-plugin-list",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    validate_remote_plugin_list_payload(
        payload, fixture, installed=False, available=False
    )
    steps.append("plugin_absent")
    discovery = lifecycle.discover_skills(
        fixture,
        env,
        project,
        expect_plugin=False,
        expect_standalone=False,
        identity=IDENTITY,
        cwd_boundary=projects_root,
    )
    lifecycle.assert_protected_unchanged(protected_before)
    steps.append("discovery_absent")
    lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-recovery-marketplace-remove",
        ["marketplace", "remove", MARKETPLACE_NAME, "--json"],
    )
    steps.append("marketplace_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "remote-recovery-marketplace-list",
        ["marketplace", "list", "--json"],
    )
    validate_marketplace_list_payload(payload, fixture, present=False)
    steps.append("marketplace_absent")
    return {"steps": steps, "step_count": len(steps), "discovery": discovery}


def cleanup_scenario(
    fixture: Path, env: dict[str, str], projects_root: Path
) -> dict[str, Any]:
    try:
        cleanup = local_carrier.purge_isolated_write_roots(fixture, env)
    finally:
        external_retries = remove_external_project_root(projects_root)
    cleanup["external_project_root_removed"] = True
    cleanup["external_project_handle_release_retries"] = external_retries
    return cleanup


def run_success_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
    expected_head: str,
) -> dict[str, Any]:
    source_before = local_carrier.source_snapshot()
    env, preparation, projects_root, project = prepare_scenario(
        fixture, protected_before
    )
    try:
        result = run_remote_lifecycle(
            fixture,
            env,
            protected_before,
            source_before,
            expected_head=expected_head,
            projects_root=projects_root,
            project=project,
        )
    finally:
        cleanup = cleanup_scenario(fixture, env, projects_root)
    return {"preparation": preparation, "lifecycle": result, "cleanup": cleanup}


def run_failure_recovery_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
    expected_head: str,
) -> dict[str, Any]:
    source_before = local_carrier.source_snapshot()
    env, preparation, projects_root, project = prepare_scenario(
        fixture, protected_before
    )
    recovery: dict[str, Any] | None = None
    injected_error = ""
    try:
        try:
            run_remote_lifecycle(
                fixture,
                env,
                protected_before,
                source_before,
                expected_head=expected_head,
                projects_root=projects_root,
                project=project,
                fail_after_step="plugin_add",
            )
        except lifecycle.PluginFixtureError as exc:
            injected_error = str(exc)
            if injected_error != (
                "injected remote lifecycle failure after plugin_add"
            ):
                raise
        else:
            raise lifecycle.PluginFixtureError(
                "injected remote lifecycle failure did not fire"
            )
        recovery = recover_after_injected_failure(
            fixture, env, protected_before, projects_root, project
        )
    finally:
        cleanup = cleanup_scenario(fixture, env, projects_root)
    if recovery is None:
        raise lifecycle.PluginFixtureError(
            "remote failure recovery did not complete"
        )
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
            "remote GitHub evidence must stay under the L55 run root"
        ) from exc
    if not relative.parts:
        raise lifecycle.PluginFixtureError("evidence path cannot be the run root")
    lifecycle.write_json(target, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate CoTend from its real GitHub Marketplace source."
    )
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--expected-remote-head")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        expected_head = validate_expected_head(
            args.expected_remote_head or local_git_head()
        )
        run_root = reset_run_root(args.run_root)
        evidence_path = args.evidence or run_root / "RESULT.json"
        source_before = local_carrier.source_snapshot()
        success_boundary = local_carrier.wait_for_protected_quiet_window()
        success = run_success_scenario(
            run_root / "success", success_boundary, expected_head
        )
        failure_boundary = local_carrier.wait_for_protected_quiet_window()
        failure = run_failure_recovery_scenario(
            run_root / "failure-recovery", failure_boundary, expected_head
        )
        if local_carrier.source_snapshot() != source_before:
            raise lifecycle.PluginFixtureError(
                "repository carrier inputs changed during remote validation"
            )
        lifecycle.assert_protected_unchanged(failure_boundary)
        evidence = {
            "status": "passed_real_github_marketplace_lifecycle",
            "evidence_type": "executed",
            "remote": {
                "slug": REMOTE_SLUG,
                "url": REMOTE_URL,
                "expected_head": expected_head,
            },
            "plugin": {
                "name": package.PLUGIN_NAME,
                "version": package.PLUGIN_VERSION,
                "marketplace": MARKETPLACE_NAME,
            },
            "success_scenario": success,
            "failure_recovery_scenario": failure,
            "verification": {
                "skills": len(package.EXPECTED_SKILLS),
                "write_roots_redirected": len(lifecycle.WRITE_ROOT_ENV_KEYS),
                "credential_inheritance": False,
                "proxy_policy": "direct_or_credential_free_loopback",
                "git_terminal_prompt": False,
                "protected_user_metadata_unchanged_during_each_scenario": True,
                "runtime_write_roots_purged": True,
                "clean_external_project": True,
            },
            "not_run": list(POST_VALIDATION_NOT_RUN),
        }
        write_evidence(evidence_path, run_root, evidence)
        print(
            "REMOTE_GITHUB_MARKETPLACE_OK "
            f"head={expected_head} "
            f"steps={success['lifecycle']['step_count']} "
            f"recovery={failure['recovery']['step_count']} "
            f"skills={len(package.EXPECTED_SKILLS)} "
            f"roots={len(lifecycle.WRITE_ROOT_ENV_KEYS)} "
            "purged=true protected_unchanged=true real_user_write=false"
        )
        return 0
    except (
        lifecycle.PluginFixtureError,
        package.PluginPackageError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print(f"REMOTE_GITHUB_MARKETPLACE_FAILED {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
