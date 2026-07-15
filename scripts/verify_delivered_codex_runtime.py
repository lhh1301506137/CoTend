from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SCRIPTS = ROOT / "scripts"
for import_root in (SRC, SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from cotend_delivery import Artifact, DeliveryError, DeliveryManager  # noqa: E402
import verify_isolated_codex_carrier as carrier  # noqa: E402
from verify_delivery_lifecycle import tree_snapshot  # noqa: E402


PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_FIXTURE = PRIVATE_ROOT / "L25-delivered-codex-runtime"
UNRELATED_SKILL = "user-skill"


class BridgeError(RuntimeError):
    pass


def guarded_fixture(path: Path) -> Path:
    try:
        return carrier.guarded_fixture(path)
    except carrier.CarrierError as exc:
        raise BridgeError(str(exc)) from exc


def remove_fixture_tree(path: Path) -> None:
    target = guarded_fixture(path)
    if not target.exists():
        return

    def make_writable_and_retry(function: Any, failed_path: str, _: Any) -> None:
        os.chmod(failed_path, stat.S_IWRITE)
        function(failed_path)

    shutil.rmtree(target, onerror=make_writable_and_retry)


def assert_snapshot_equal(
    expected: dict[str, Any],
    actual: dict[str, Any],
    label: str,
) -> None:
    if expected == actual:
        return
    changed = sorted(
        key
        for key in set(expected) | set(actual)
        if expected.get(key) != actual.get(key)
    )
    raise BridgeError(f"{label} changed: {changed}")


def repository_worktree_snapshot() -> dict[str, Any]:
    listed = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout
    files: dict[str, str] = {}
    for relative in sorted(path for path in listed.split("\0") if path):
        target = ROOT / relative
        if target.is_symlink():
            files[relative] = f"symlink:{target.readlink()}"
        elif target.is_file():
            files[relative] = carrier.sha256(target)
        elif target.exists():
            files[relative] = "non_file"
        else:
            files[relative] = "missing"
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    return {"head": head, "files": files}


def nested_git_head(fixture: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=fixture,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def protected_project_snapshot(fixture: Path, skills: set[str]) -> dict[str, str]:
    snapshot = tree_snapshot(fixture, managed_skills=skills)
    return {
        path: value
        for path, value in snapshot.items()
        if path.split("/", 1)[0] not in {".git", "runs"}
    }


def active_delivery_snapshot(fixture: Path) -> dict[str, str]:
    manifest = carrier.file_manifest(fixture, exclude={".git", "runs"})
    return {
        path: digest
        for path, digest in manifest.items()
        if not path.startswith(".agents/.cotend-delivery/rollback/")
    }


def write_unrelated_skill(fixture: Path) -> None:
    skill_root = fixture / ".agents" / "skills" / UNRELATED_SKILL
    skill_root.mkdir(parents=True, exist_ok=True)
    (skill_root / "SKILL.md").write_text(
        "---\n"
        f"name: {UNRELATED_SKILL}\n"
        "description: Fixture-owned unrelated Skill for coexistence validation.\n"
        "---\n\n"
        "# User Skill\n\n"
        "This fixture Skill is not owned by CoTend.\n",
        encoding="utf-8",
    )


def initialize_nested_repository(fixture: Path) -> str:
    subprocess.run(
        ["git", "init", "--quiet", "--initial-branch=main", str(fixture)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "add", "-A"],
        cwd=fixture,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=CoTend Fixture",
            "-c",
            "user.email=cotend-fixture@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "fixture baseline",
        ],
        cwd=fixture,
        check=True,
        capture_output=True,
        text=True,
    )
    return nested_git_head(fixture)


def validate_delivery_state(
    manager: DeliveryManager,
    artifact: Artifact,
) -> dict[str, Any]:
    state = manager.inspect(artifact)
    expected = {
        "receipt_valid": True,
        "installation": "complete",
        "enablement": "enabled",
        "candidate_relation": "same_as_current",
        "transition": "stable",
        "source_release_id": artifact.source_release_id,
        "artifact_lineage": artifact.lineage,
        "artifact_id": artifact.artifact_id,
        "target_revision": artifact.revision,
        "protocol": artifact.protocol,
        "manifest_sha256": artifact.manifest_sha256,
        "managed_files": len(artifact.files),
    }
    mismatches = {
        key: {"expected": value, "actual": state.get(key)}
        for key, value in expected.items()
        if state.get(key) != value
    }
    if mismatches:
        raise BridgeError(f"delivered carrier state mismatch: {mismatches}")
    if tuple(state.get("managed_skills", [])) != artifact.skills:
        raise BridgeError("delivered carrier Skill inventory mismatch")
    if any(state.get(key) for key in ("missing", "modified", "unexpected")):
        raise BridgeError("delivered carrier contains missing, modified, or unknown files")
    if state.get("transition_artifacts"):
        raise BridgeError("delivered carrier contains unfinished transition artifacts")

    try:
        receipt = json.loads(manager.receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BridgeError("delivery receipt is missing or unreadable") from exc
    receipt_expected = {
        "schema": "cotend.delivery-receipt",
        "schema_version": 2,
        "platform": "Codex",
        "scope": "project",
        "source_release_id": artifact.source_release_id,
        "artifact_lineage": artifact.lineage,
        "artifact_id": artifact.artifact_id,
        "target_revision": artifact.revision,
        "protocol": artifact.protocol,
        "manifest_sha256": artifact.manifest_sha256,
        "skills": list(artifact.skills),
        "files": artifact.files,
        "enabled": True,
    }
    receipt_mismatches = {
        key: {"expected": value, "actual": receipt.get(key)}
        for key, value in receipt_expected.items()
        if receipt.get(key) != value
    }
    if receipt_mismatches:
        raise BridgeError(f"delivery receipt provenance mismatch: {receipt_mismatches}")
    return {
        "source_release_id": state["source_release_id"],
        "artifact_id": state["artifact_id"],
        "target_revision": state["target_revision"],
        "protocol": state["protocol"],
        "manifest_sha256": state["manifest_sha256"],
        "installation": state["installation"],
        "enablement": state["enablement"],
        "receipt_schema": receipt["schema"],
    }


def validate_bridge_discovery(
    discovery: dict[str, Any],
    *,
    expected_unrelated: set[str] | None = None,
) -> None:
    expected_unrelated = expected_unrelated or set()
    managed = discovery.get("fixture_skills")
    unrelated = discovery.get("unrelated_fixture_skills")
    if not isinstance(managed, list) or not isinstance(unrelated, list):
        raise BridgeError("Codex discovery result is missing fixture Skill lists")
    managed_names = {item.get("name") for item in managed if isinstance(item, dict)}
    unrelated_names = {
        item.get("name") for item in unrelated if isinstance(item, dict)
    }
    if managed_names != carrier.EXPECTED_SKILLS:
        raise BridgeError(f"Codex managed discovery mismatch: {sorted(managed_names)}")
    if unrelated_names != expected_unrelated:
        raise BridgeError(
            f"Codex unrelated discovery mismatch: {sorted(unrelated_names)}"
        )
    for item in managed + unrelated:
        if not isinstance(item, dict):
            raise BridgeError("Codex discovery returned an invalid Skill item")
        if item.get("scope") != "repo" or item.get("enabled") is not True:
            raise BridgeError(f"Codex discovery boundary mismatch: {item.get('name')}")
    if discovery.get("fixture_skill_count") != len(carrier.EXPECTED_SKILLS):
        raise BridgeError("Codex managed discovery count mismatch")
    if discovery.get("unrelated_fixture_skill_count") != len(expected_unrelated):
        raise BridgeError("Codex unrelated discovery count mismatch")


def prepare_delivered_fixture(
    fixture: Path,
    artifact: Artifact,
) -> dict[str, Any]:
    fixture = guarded_fixture(fixture)
    global_before = carrier.protected_global_snapshot()
    repository_before = repository_worktree_snapshot()
    if fixture.exists():
        remove_fixture_tree(fixture)
    shutil.copytree(carrier.TEMPLATE_ROOT, fixture)
    (fixture / "USER-NOTES.md").write_text(
        "fixture user file; CoTend must preserve it\n",
        encoding="utf-8",
    )
    write_unrelated_skill(fixture)
    head = initialize_nested_repository(fixture)

    manager = DeliveryManager(fixture)
    skills = set(artifact.skills)
    protected_before = protected_project_snapshot(fixture, skills)
    files_before = carrier.file_manifest(fixture, exclude={".git", "runs"})
    preview = manager.execute("install", artifact)
    if preview.get("status") != "planned" or preview.get("applied") is not False:
        raise BridgeError("delivery install did not default to dry-run")
    assert_snapshot_equal(
        files_before,
        carrier.file_manifest(fixture, exclude={".git", "runs"}),
        "install dry-run fixture",
    )
    installed = manager.execute("install", artifact, apply=True)
    if installed.get("status") != "applied" or installed.get("applied") is not True:
        raise BridgeError("delivery install was not applied")
    state = validate_delivery_state(manager, artifact)
    static = carrier.verify_static(fixture, allow_unrelated_skills=True)
    assert_snapshot_equal(
        protected_before,
        protected_project_snapshot(fixture, skills),
        "protected project paths during install",
    )
    if nested_git_head(fixture) != head:
        raise BridgeError("nested Git HEAD changed during delivery")
    assert_snapshot_equal(
        global_before,
        carrier.protected_global_snapshot(),
        "protected global Codex state during delivery",
    )
    assert_snapshot_equal(
        repository_before,
        repository_worktree_snapshot(),
        "CoTend repository outside fixture during delivery",
    )
    return {
        "dry_run": "passed_no_change",
        "install": "applied",
        "nested_git_head_unchanged": True,
        "protected_project_paths_unchanged": True,
        "protected_global_state_unchanged": True,
        "repository_outside_fixture_unchanged": True,
        "state": state,
        "static": static,
    }


def verify_runtime(
    fixture: Path,
    *,
    discover: bool,
    live: bool,
) -> dict[str, Any]:
    skills = set(carrier.EXPECTED_SKILLS)
    fixture_before = carrier.file_manifest(fixture, exclude={".git", "runs"})
    protected_before = protected_project_snapshot(fixture, skills)
    global_before = carrier.protected_global_snapshot()
    repository_before = repository_worktree_snapshot()
    head_before = nested_git_head(fixture)
    result: dict[str, Any] = {}

    if discover or live:
        discovery = carrier.discover_skills(
            fixture,
            allow_unrelated_skills=True,
        )
        validate_bridge_discovery(
            discovery,
            expected_unrelated={UNRELATED_SKILL},
        )
        result["discovery"] = discovery
    if live:
        scenario = next(
            item for item in carrier.load_scenarios() if item["id"] == "diagnose-only"
        )
        result["live"] = carrier.run_live_scenario(fixture, scenario)

    assert_snapshot_equal(
        fixture_before,
        carrier.file_manifest(fixture, exclude={".git", "runs"}),
        "delivered fixture during runtime",
    )
    assert_snapshot_equal(
        protected_before,
        protected_project_snapshot(fixture, skills),
        "protected project paths during runtime",
    )
    if nested_git_head(fixture) != head_before:
        raise BridgeError("nested Git HEAD changed during runtime")
    assert_snapshot_equal(
        global_before,
        carrier.protected_global_snapshot(),
        "protected global Codex state during runtime",
    )
    assert_snapshot_equal(
        repository_before,
        repository_worktree_snapshot(),
        "CoTend repository outside fixture during runtime",
    )
    result["boundaries"] = {
        "fixture_unchanged_outside_runs": True,
        "protected_project_paths_unchanged": True,
        "nested_git_head_unchanged": True,
        "protected_global_state_unchanged": True,
        "repository_outside_fixture_unchanged": True,
    }
    return result


def verify_uninstall_rollback(
    fixture: Path,
    artifact: Artifact,
) -> dict[str, Any]:
    manager = DeliveryManager(fixture)
    skills = set(artifact.skills)
    fixture_before = active_delivery_snapshot(fixture)
    protected_before = protected_project_snapshot(fixture, skills)
    global_before = carrier.protected_global_snapshot()
    repository_before = repository_worktree_snapshot()
    head_before = nested_git_head(fixture)

    uninstalled = manager.execute("uninstall", apply=True)
    state_after_uninstall = uninstalled.get("state_after", {})
    if (
        state_after_uninstall.get("installation") != "absent"
        or state_after_uninstall.get("rollback_available") is not True
    ):
        raise BridgeError("uninstall did not leave an absent rollback-ready state")
    rolled_back = manager.execute("rollback", apply=True)
    if rolled_back.get("status") != "applied":
        raise BridgeError("rollback was not applied")
    state = validate_delivery_state(manager, artifact)
    carrier.verify_static(fixture, allow_unrelated_skills=True)
    restored = manager.inspect(artifact)
    if restored.get("rollback_available") is not False:
        raise BridgeError("consumed one-step rollback checkpoint is still present")

    assert_snapshot_equal(
        fixture_before,
        active_delivery_snapshot(fixture),
        "active delivery after uninstall rollback",
    )
    assert_snapshot_equal(
        protected_before,
        protected_project_snapshot(fixture, skills),
        "protected project paths after uninstall rollback",
    )
    if nested_git_head(fixture) != head_before:
        raise BridgeError("nested Git HEAD changed during uninstall rollback")
    assert_snapshot_equal(
        global_before,
        carrier.protected_global_snapshot(),
        "protected global Codex state during uninstall rollback",
    )
    assert_snapshot_equal(
        repository_before,
        repository_worktree_snapshot(),
        "CoTend repository outside fixture during uninstall rollback",
    )
    return {
        "uninstall": "absent_with_rollback",
        "rollback": "restored_exact_active_delivery",
        "one_step_checkpoint_consumed": True,
        "protected_boundaries_unchanged": True,
        "state": state,
    }


def expect_rejected(action: Any, label: str) -> None:
    try:
        action()
    except (BridgeError, DeliveryError, carrier.CarrierError):
        return
    raise BridgeError(f"negative bridge case was not rejected: {label}")


def prepare_negative_project(root: Path, name: str) -> Path:
    project = root / name
    project.mkdir(parents=True)
    (project / "USER-NOTES.md").write_text("preserve me\n", encoding="utf-8")
    write_unrelated_skill(project)
    return project


def valid_discovery_sample() -> dict[str, Any]:
    managed = [
        {"name": name, "scope": "repo", "enabled": True}
        for name in sorted(carrier.EXPECTED_SKILLS)
    ]
    unrelated = [{"name": UNRELATED_SKILL, "scope": "repo", "enabled": True}]
    return {
        "fixture_skills": managed,
        "fixture_skill_count": len(managed),
        "unrelated_fixture_skills": unrelated,
        "unrelated_fixture_skill_count": len(unrelated),
    }


def run_negative_mutations(fixture: Path, artifact: Artifact) -> int:
    root = guarded_fixture(fixture.with_name(f"{fixture.name}-negative-mutations"))
    global_before = carrier.protected_global_snapshot()
    repository_before = repository_worktree_snapshot()
    cases = 0
    try:
        if root.exists():
            remove_fixture_tree(root)
        root.mkdir(parents=True)

        missing_receipt = prepare_negative_project(root, "missing-receipt")
        missing_manager = DeliveryManager(missing_receipt)
        missing_manager.execute("install", artifact, apply=True)
        missing_manager.receipt_path.unlink()
        expect_rejected(
            lambda: missing_manager.execute("install", artifact, apply=True),
            "receipt-less managed collision",
        )
        cases += 1

        damaged = prepare_negative_project(root, "damaged-payload")
        damaged_manager = DeliveryManager(damaged)
        damaged_manager.execute("install", artifact, apply=True)
        damaged_skill = damaged / ".agents" / "skills" / "cotend-init" / "SKILL.md"
        damaged_skill.write_text("damaged\n", encoding="utf-8")
        expect_rejected(
            lambda: validate_delivery_state(damaged_manager, artifact),
            "damaged delivered payload",
        )
        cases += 1

        partial = prepare_negative_project(root, "partial-payload")
        partial_manager = DeliveryManager(partial)
        partial_manager.execute("install", artifact, apply=True)
        shutil.rmtree(partial / ".agents" / "skills" / "cotend-model-upgrade")
        expect_rejected(
            lambda: validate_delivery_state(partial_manager, artifact),
            "partial delivered payload",
        )
        cases += 1

        protected = prepare_negative_project(root, "protected-project")
        protected_before = protected_project_snapshot(protected, set(artifact.skills))
        (protected / "USER-NOTES.md").write_text("changed\n", encoding="utf-8")
        expect_rejected(
            lambda: assert_snapshot_equal(
                protected_before,
                protected_project_snapshot(protected, set(artifact.skills)),
                "protected project negative",
            ),
            "protected project mutation",
        )
        cases += 1

        simulated_global_after = copy.deepcopy(global_before)
        config_stat = simulated_global_after.setdefault("codex_config_stat", {})
        config_stat["mtime_ns"] = int(config_stat.get("mtime_ns", 0)) + 1
        expect_rejected(
            lambda: assert_snapshot_equal(
                global_before,
                simulated_global_after,
                "protected global negative",
            ),
            "protected global mutation signal",
        )
        cases += 1

        missing_discovery = valid_discovery_sample()
        missing_discovery["fixture_skills"] = missing_discovery["fixture_skills"][1:]
        missing_discovery["fixture_skill_count"] -= 1
        expect_rejected(
            lambda: validate_bridge_discovery(
                missing_discovery,
                expected_unrelated={UNRELATED_SKILL},
            ),
            "missing managed Skill discovery",
        )
        cases += 1

        wrong_scope = valid_discovery_sample()
        wrong_scope["fixture_skills"][0]["scope"] = "user"
        expect_rejected(
            lambda: validate_bridge_discovery(
                wrong_scope,
                expected_unrelated={UNRELATED_SKILL},
            ),
            "wrong discovery scope",
        )
        cases += 1
    finally:
        if root.exists():
            remove_fixture_tree(root)

    assert_snapshot_equal(
        global_before,
        carrier.protected_global_snapshot(),
        "protected global Codex state during negative cases",
    )
    assert_snapshot_equal(
        repository_before,
        repository_worktree_snapshot(),
        "CoTend repository outside negative fixtures",
    )
    return cases


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate L24-delivered CoTend Skills in the Codex runtime"
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
        help="rebuild the nested Git fixture and install through the delivery API",
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="call Codex app-server skills/list against delivered bytes",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="run only the bounded read-only diagnose-only scenario",
    )
    parser.add_argument(
        "--negative-mutations",
        action="store_true",
        help="run seven deterministic bridge guard failures",
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        help="write redacted JSON under the fixture",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture = guarded_fixture(args.fixture)
    evidence: dict[str, Any] = {
        "schema": "cotend.delivered-codex-runtime-evidence",
        "schema_version": 1,
    }
    try:
        artifact = Artifact.from_repository(ROOT)
        evidence["artifact"] = {
            "source_release_id": artifact.source_release_id,
            "artifact_id": artifact.artifact_id,
            "target_revision": artifact.revision,
            "protocol": artifact.protocol,
            "manifest_sha256": artifact.manifest_sha256,
            "skills": len(artifact.skills),
            "files": len(artifact.files),
        }
        if args.prepare:
            evidence["delivery"] = prepare_delivered_fixture(fixture, artifact)
        if not fixture.is_dir():
            raise BridgeError("fixture is missing; run with --prepare")

        manager = DeliveryManager(fixture)
        evidence["delivered_state"] = validate_delivery_state(manager, artifact)
        evidence["static"] = carrier.verify_static(
            fixture,
            allow_unrelated_skills=True,
        )
        runtime = verify_runtime(
            fixture,
            discover=args.discover,
            live=args.live,
        )
        evidence["runtime"] = runtime
        evidence["lifecycle_tail"] = verify_uninstall_rollback(fixture, artifact)

        if args.discover or args.live:
            version = subprocess.run(
                [carrier.codex_executable(), "--version"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.strip()
            evidence["codex_version"] = version
        if args.negative_mutations:
            negative_cases = run_negative_mutations(fixture, artifact)
            evidence["negative_mutations"] = {
                "passed": negative_cases,
                "total": 7,
            }
            print(f"DELIVERED_CODEX_RUNTIME_NEGATIVE_OK cases={negative_cases}")

        carrier.write_evidence(args.evidence, evidence)
        print(
            "DELIVERED_CODEX_RUNTIME_OK "
            f"skills={len(artifact.skills)} files={len(artifact.files)} "
            f"unrelated=1 discovery={'passed' if args.discover or args.live else 'not_run'} "
            f"live={'diagnose-only' if args.live else 'not_run'}"
        )
    except (
        BridgeError,
        carrier.CarrierError,
        DeliveryError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print("DELIVERED_CODEX_RUNTIME_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
