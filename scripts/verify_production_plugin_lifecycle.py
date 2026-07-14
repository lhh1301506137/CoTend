from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import unittest
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
DEFAULT_RUN_ROOT = PRIVATE_ROOT / "L46-isolated-production-plugin-lifecycle"
MARKETPLACE_NAME = "cotend-production-candidate-local"
EXPECTED_PACKAGE_DIGEST = (
    "e23febd663c4abd82c7de2a2afde5ccd7599454c141669e238b8d1a336a6f066"
)
PRODUCTION_IDENTITY = lifecycle.PluginLifecycleIdentity(
    plugin_id=package.PLUGIN_NAME,
    plugin_version=package.PLUGIN_VERSION,
    marketplace_name=MARKETPLACE_NAME,
    expected_skills=package.EXPECTED_SKILLS,
)


def guarded_run_root(path: Path) -> Path:
    resolved = lifecycle.guarded_fixture(path)
    relative = resolved.relative_to(PRIVATE_ROOT.resolve())
    if not relative.parts[0].startswith("L46-"):
        raise lifecycle.PluginFixtureError(
            "production lifecycle root must use an L46-prefixed private directory"
        )
    return resolved


def reset_run_root(path: Path) -> Path:
    resolved = guarded_run_root(path)
    if resolved.exists():
        lifecycle.reject_symlink_tree(resolved, label="L46 run root")
        remove_tree_with_retry(resolved)
    resolved.mkdir(parents=True)
    return resolved


def remove_tree_with_retry(path: Path, *, timeout_seconds: float = 45.0) -> int:
    deadline = time.monotonic() + timeout_seconds
    retries = 0
    while path.exists():
        try:
            shutil.rmtree(path)
        except OSError as exc:
            if getattr(exc, "winerror", None) not in {5, 32}:
                raise
            if time.monotonic() >= deadline:
                raise
            retries += 1
            time.sleep(0.1)
    return retries


def marketplace_manifest() -> dict[str, Any]:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "CoTend Production Candidate Local"},
        "plugins": [
            {
                "name": package.PLUGIN_NAME,
                "source": {
                    "source": "local",
                    "path": f"./plugins/{package.PLUGIN_NAME}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        ],
    }


def production_source_snapshot() -> dict[str, Any]:
    contract = package.validate_contract()
    return {
        "git_head": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "source_manifest": contract["source_manifest"],
        "package_input_manifest": contract["expected_package_manifest"],
        "package_lock_sha256": package.sha256_file(package.PACKAGE_LOCK_PATH),
        "artifact_lock_sha256": package.sha256_file(package.TARGET_ARTIFACT_LOCK),
        "lifecycle_source_state": lifecycle.source_state_snapshot(),
    }


def materialize_scenario(fixture: Path) -> dict[str, Any]:
    fixture = lifecycle.guarded_fixture(fixture)
    marketplace_root = fixture / "source-marketplace"
    plugin_root = marketplace_root / "plugins" / package.PLUGIN_NAME
    build = package.build_package(plugin_root)
    if build["package_manifest_sha256"] != EXPECTED_PACKAGE_DIGEST:
        raise lifecycle.PluginFixtureError("production package digest drifted")
    package.verify_package(plugin_root)

    marketplace_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    lifecycle.write_json(marketplace_path, marketplace_manifest())

    empty_project = fixture / "project-empty"
    empty_project.mkdir(parents=True)
    (empty_project / "README.md").write_text(
        "# Empty production-candidate lifecycle project\n", encoding="utf-8"
    )
    coexist_project = fixture / "project-with-standalone-skills"
    coexist_project.mkdir(parents=True)
    (coexist_project / "README.md").write_text(
        "# Production-candidate coexistence project\n", encoding="utf-8"
    )
    standalone_root = coexist_project / ".agents" / "skills"
    for skill in package.EXPECTED_SKILLS:
        shutil.copytree(package.SOURCE_SKILLS_ROOT / skill, standalone_root / skill)
    (fixture / "evidence" / "commands").mkdir(parents=True)
    return {
        "plugin_root": plugin_root,
        "marketplace_root": marketplace_root,
        "package": build,
    }


def prepare_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, Any]]:
    fixture = lifecycle.guarded_fixture(fixture)
    fixture.mkdir(parents=True, exist_ok=True)
    env = lifecycle.build_isolated_env(fixture)
    try:
        preflight = lifecycle.run_preflight(fixture, env, protected_before)
        materialized = materialize_scenario(fixture)
        validator = lifecycle.plugin_creator_script("validate_plugin.py")
        official = package.run_official_validator(
            materialized["plugin_root"], validator
        )
        lifecycle.assert_protected_unchanged(protected_before)
        return env, {
            "preflight": preflight,
            "package": materialized["package"],
            "official_validator": official,
        }
    except Exception:
        purge_isolated_write_roots(fixture, env)
        raise


def purge_isolated_write_roots(
    fixture: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    fixture = lifecycle.guarded_fixture(fixture)
    lifecycle.validate_isolated_env(fixture, env)
    roots = sorted(
        {Path(env[key]).resolve() for key in lifecycle.WRITE_ROOT_ENV_KEYS},
        key=lambda path: len(path.parts),
    )
    minimal_roots: list[Path] = []
    for root in roots:
        lifecycle.assert_fixture_path(fixture, root, "isolated cleanup root")
        if not any(root == parent or root.is_relative_to(parent) for parent in minimal_roots):
            minimal_roots.append(root)
    removed: list[str] = []
    retry_count = 0
    for root in minimal_roots:
        if not root.exists():
            continue
        lifecycle.reject_symlink_tree(root, label="isolated runtime root")
        retry_count += remove_tree_with_retry(root)
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
        "all_write_roots_absent": True,
    }


def recover_after_injected_failure(
    fixture: Path,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    steps: list[str] = []
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "recovery-plugin-remove",
        ["remove", PRODUCTION_IDENTITY.selector, "--json"],
    )
    lifecycle.validate_plugin_remove_payload(payload, PRODUCTION_IDENTITY)
    steps.append("plugin_remove")
    payload = lifecycle.run_cli_step(
        fixture,
        env,
        protected_before,
        "recovery-plugin-list",
        ["list", "--marketplace", MARKETPLACE_NAME, "--json"],
    )
    lifecycle.validate_plugin_list_payload(
        payload,
        fixture,
        installed=False,
        available=False,
        identity=PRODUCTION_IDENTITY,
    )
    steps.append("plugin_absent")
    discovery = lifecycle.discover_skills(
        fixture,
        env,
        fixture / "project-empty",
        expect_plugin=False,
        expect_standalone=False,
        identity=PRODUCTION_IDENTITY,
    )
    lifecycle.assert_protected_unchanged(protected_before)
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
        payload, present=False, identity=PRODUCTION_IDENTITY
    )
    steps.append("marketplace_absent")
    return {"steps": steps, "step_count": len(steps), "discovery": discovery}


def run_success_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    env, preparation = prepare_scenario(fixture, protected_before)
    source_before = lifecycle.source_state_snapshot()
    try:
        phase = lifecycle.run_phase_a(
            fixture,
            env,
            protected_before,
            source_before,
            identity=PRODUCTION_IDENTITY,
        )
    finally:
        cleanup = purge_isolated_write_roots(fixture, env)
    lifecycle.assert_protected_unchanged(protected_before)
    return {"preparation": preparation, "lifecycle": phase, "cleanup": cleanup}


def run_failure_recovery_scenario(
    fixture: Path,
    protected_before: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    env, preparation = prepare_scenario(fixture, protected_before)
    source_before = lifecycle.source_state_snapshot()
    injected_error = ""
    recovery: dict[str, Any] | None = None
    try:
        try:
            lifecycle.run_phase_a(
                fixture,
                env,
                protected_before,
                source_before,
                identity=PRODUCTION_IDENTITY,
                fail_after_step="plugin_add",
            )
        except lifecycle.PluginFixtureError as exc:
            injected_error = str(exc)
            if injected_error != "injected lifecycle failure after plugin_add":
                raise
        else:
            raise lifecycle.PluginFixtureError("injected lifecycle failure did not fire")
        recovery = recover_after_injected_failure(fixture, env, protected_before)
    finally:
        cleanup = purge_isolated_write_roots(fixture, env)
    if recovery is None:
        raise lifecycle.PluginFixtureError("failure recovery did not complete")
    lifecycle.assert_protected_unchanged(protected_before)
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
            "production lifecycle evidence must stay under the L46 run root"
        ) from exc
    if not relative.parts:
        raise lifecycle.PluginFixtureError("evidence path cannot be the run root")
    lifecycle.write_json(target, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the exact CoTend production-candidate Plugin lifecycle."
    )
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--evidence", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_root = reset_run_root(args.run_root)
        evidence_path = args.evidence or run_root / "RESULT.json"
        protected_before = lifecycle.protected_user_snapshot()
        source_before = production_source_snapshot()

        suite = unittest.defaultTestLoader.loadTestsFromName(
            "tests.test_production_plugin_lifecycle"
        )
        tests = unittest.TextTestRunner(verbosity=1).run(suite)
        if not tests.wasSuccessful():
            return 1

        success = run_success_scenario(run_root / "success", protected_before)
        failure = run_failure_recovery_scenario(
            run_root / "failure-recovery", protected_before
        )
        if production_source_snapshot() != source_before:
            raise lifecycle.PluginFixtureError(
                "production package source, locks, or Git HEAD changed"
            )
        lifecycle.assert_protected_unchanged(protected_before)

        evidence = {
            "status": "passed_isolated_production_plugin_lifecycle",
            "plugin": {
                "name": package.PLUGIN_NAME,
                "version": package.PLUGIN_VERSION,
                "marketplace": MARKETPLACE_NAME,
                "identity_authority": "initial_submission_identity_confirmed_not_release",
            },
            "package": {
                "files": success["preparation"]["package"]["package_files"],
                "skills": success["preparation"]["package"]["skills"],
                "skill_files": success["preparation"]["package"]["skill_files"],
                "manifest_sha256": success["preparation"]["package"][
                    "package_manifest_sha256"
                ],
                "source_bytes_identical": True,
                "official_validator": success["preparation"][
                    "official_validator"
                ],
            },
            "success_scenario": success,
            "failure_recovery_scenario": failure,
            "verification": {
                "unit_tests": tests.testsRun,
                "write_roots_redirected": len(lifecycle.WRITE_ROOT_ENV_KEYS),
                "protected_user_boundaries": len(protected_before),
                "protected_user_metadata_unchanged": True,
                "production_source_and_locks_unchanged": True,
                "runtime_write_roots_purged": True,
            },
            "not_run": [
                "real_user_plugin_or_marketplace_write",
                "desktop_selector_or_restart",
                "portal_submission",
                "public_installation",
                "release_publish_or_push",
            ],
        }
        write_evidence(evidence_path, run_root, evidence)
        print(
            "PRODUCTION_PLUGIN_LIFECYCLE_OK "
            f"version={package.PLUGIN_VERSION} files={evidence['package']['files']} "
            f"steps={success['lifecycle']['step_count']} "
            f"recovery={failure['recovery']['step_count']} "
            f"tests={tests.testsRun} roots={len(lifecycle.WRITE_ROOT_ENV_KEYS)} "
            "purged=true protected_unchanged=true"
        )
        return 0
    except (
        lifecycle.PluginFixtureError,
        package.PluginPackageError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print(f"PRODUCTION_PLUGIN_LIFECYCLE_FAILED {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
