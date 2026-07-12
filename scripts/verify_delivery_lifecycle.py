from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cotend_delivery import Artifact, DeliveryError, DeliveryManager  # noqa: E402


PRIVATE_ROOT = ROOT / ".private-provenance"
DEFAULT_FIXTURE = PRIVATE_ROOT / "L24-codex-delivery"
CLI = ROOT / "scripts" / "cotend_delivery.py"


class LifecycleError(RuntimeError):
    pass


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


def reset_fixture(path: Path) -> Path:
    fixture = guarded_fixture(path)
    if fixture.exists():
        shutil.rmtree(fixture)
    fixture.mkdir(parents=True)
    return fixture


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_owned_path(relative: Path, managed_skills: set[str]) -> bool:
    parts = relative.parts
    if len(parts) >= 2 and parts[:2] == (".agents", ".cotend-delivery"):
        return True
    return (
        len(parts) >= 3
        and parts[:2] == (".agents", "skills")
        and parts[2] in managed_skills
    )


def tree_snapshot(
    root: Path,
    *,
    managed_skills: set[str] | None = None,
) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if managed_skills is not None and is_owned_path(relative, managed_skills):
            continue
        key = relative.as_posix()
        if path.is_symlink():
            snapshot[key] = f"symlink:{path.readlink()}"
        elif path.is_dir():
            snapshot[key] = "directory"
        elif path.is_file():
            snapshot[key] = f"sha256:{file_sha256(path)}"
    return snapshot


def prepare_project(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text("user readme\n", encoding="utf-8")
    (path / "USER-NOTES.md").write_text("keep me\n", encoding="utf-8")
    (path / "STATUS.md").write_text("project truth\n", encoding="utf-8")
    unrelated = path / ".agents" / "skills" / "user-skill"
    unrelated.mkdir(parents=True)
    (unrelated / "SKILL.md").write_text("user-owned skill\n", encoding="utf-8")
    return path


def make_updated_artifact(fixture: Path, baseline: Artifact) -> Artifact:
    source = fixture / "artifacts" / "candidate-v2"
    shutil.copytree(ROOT / "codex-skills", source)
    changed = source / "cotend-init" / "SKILL.md"
    changed.write_text(
        changed.read_text(encoding="utf-8") + "\n<!-- L24 integration candidate -->\n",
        encoding="utf-8",
    )
    return Artifact.from_directory(
        source,
        source_release_id=baseline.source_release_id,
        artifact_id="cotend-codex-r000002",
        revision=2,
        protocol=baseline.protocol,
    )


def write_legacy_receipt(
    manager: DeliveryManager,
    artifact: Artifact,
    *,
    artifact_id: str | None = None,
) -> dict[str, Any]:
    mapping = artifact.legacy_receipt_mappings[0]
    receipt = json.loads(manager.receipt_path.read_text(encoding="utf-8"))
    legacy = {
        key: value
        for key, value in receipt.items()
        if key not in {"source_release_id", "artifact_lineage", "target_revision"}
    }
    legacy.update(
        {
            "schema_version": 1,
            "artifact_id": artifact_id or mapping.artifact_id,
            "protocol": mapping.protocol,
            "manifest_sha256": mapping.manifest_sha256,
        }
    )
    manager.receipt_path.write_text(
        json.dumps(legacy, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return legacy


def cli_command(
    operation: str,
    project: Path,
    *,
    apply: bool,
    artifact: Artifact | None = None,
) -> list[str]:
    command = [
        sys.executable,
        str(CLI),
        operation,
        "--project",
        str(project),
    ]
    if artifact is not None:
        command.extend(
            [
                "--source",
                str(artifact.root),
                "--source-release-id",
                artifact.source_release_id,
                "--artifact-id",
                artifact.artifact_id,
                "--revision",
                str(artifact.revision),
                "--protocol",
                artifact.protocol,
            ]
        )
    if apply:
        command.append("--apply")
    return command


def run_cli(
    operation: str,
    project: Path,
    *,
    apply: bool = False,
    artifact: Artifact | None = None,
    expect_error: str | None = None,
) -> dict[str, Any]:
    completed = subprocess.run(
        cli_command(operation, project, apply=apply, artifact=artifact),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    if expect_error is None:
        if completed.returncode != 0:
            raise LifecycleError(
                f"{operation} failed with {completed.returncode}: {completed.stderr.strip()}"
            )
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise LifecycleError(f"{operation} returned invalid JSON") from exc

    if completed.returncode != 2:
        raise LifecycleError(
            f"{operation} expected a blocked result, got {completed.returncode}"
        )
    try:
        result = json.loads(completed.stderr)
    except json.JSONDecodeError as exc:
        raise LifecycleError(f"{operation} returned invalid error JSON") from exc
    if result.get("error") != expect_error:
        raise LifecycleError(
            f"{operation} expected {expect_error}, found {result.get('error')}"
        )
    return result


def assert_protected_unchanged(
    project: Path,
    managed_skills: set[str],
    expected: dict[str, str],
) -> None:
    actual = tree_snapshot(project, managed_skills=managed_skills)
    if actual != expected:
        changed = sorted(
            path
            for path in set(actual) | set(expected)
            if actual.get(path) != expected.get(path)
        )
        raise LifecycleError(f"protected project paths changed: {changed}")


def assert_payload(
    project: Path,
    artifact: Artifact,
    *,
    enabled: bool,
) -> None:
    root = (
        project / ".agents" / "skills"
        if enabled
        else project / ".agents" / ".cotend-delivery" / "disabled-skills"
    )
    actual = {
        path.relative_to(root).as_posix(): file_sha256(path)
        for skill in artifact.skills
        for path in sorted((root / skill).rglob("*"))
        if path.is_file()
    }
    if actual != artifact.files:
        raise LifecycleError("managed payload differs from the expected artifact")


def require_state(
    manager: DeliveryManager,
    candidate: Artifact,
    *,
    installation: str,
    enablement: str,
    artifact_id: str | None,
) -> dict[str, Any]:
    state = manager.inspect(candidate)
    expected = {
        "installation": installation,
        "enablement": enablement,
        "artifact_id": artifact_id,
    }
    mismatches = {
        key: {"expected": value, "actual": state.get(key)}
        for key, value in expected.items()
        if state.get(key) != value
    }
    if mismatches:
        raise LifecycleError(f"delivery state mismatch: {mismatches}")
    return state


def verify_positive_lifecycle(
    fixture: Path,
    baseline: Artifact,
    updated: Artifact,
) -> dict[str, Any]:
    project = prepare_project(fixture / "projects" / "positive")
    manager = DeliveryManager(project)
    skills = set(baseline.skills)
    protected = tree_snapshot(project, managed_skills=skills)
    initial = tree_snapshot(project)
    steps: list[str] = []

    preview = run_cli("install", project)
    if preview.get("status") != "planned" or preview.get("applied") is not False:
        raise LifecycleError("install did not default to dry-run")
    if tree_snapshot(project) != initial:
        raise LifecycleError("install dry-run changed the project")
    steps.append("install_dry_run")

    run_cli("install", project, apply=True)
    require_state(
        manager,
        baseline,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    assert_payload(project, baseline, enabled=True)
    assert_protected_unchanged(project, skills, protected)
    steps.append("install")

    repeated = run_cli("install", project, apply=True)
    if repeated.get("status") != "current_no_change":
        raise LifecycleError("repeated install was not idempotent")
    steps.append("install_idempotent")

    run_cli("disable", project, apply=True)
    require_state(
        manager,
        baseline,
        installation="complete",
        enablement="disabled",
        artifact_id=baseline.artifact_id,
    )
    assert_payload(project, baseline, enabled=False)
    assert_protected_unchanged(project, skills, protected)
    steps.append("disable")

    run_cli("enable", project, apply=True)
    require_state(
        manager,
        baseline,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    assert_payload(project, baseline, enabled=True)
    steps.append("enable")

    modified = project / ".agents" / "skills" / "cotend-init" / "SKILL.md"
    missing = project / ".agents" / "skills" / "grill-me" / "SKILL.md"
    modified.write_text("damaged\n", encoding="utf-8")
    missing.unlink()
    damaged = manager.inspect(baseline)
    if not damaged["modified"] or not damaged["missing"]:
        raise LifecycleError("damage inspection did not report both fault classes")
    run_cli("repair", project, apply=True)
    require_state(
        manager,
        baseline,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    assert_payload(project, baseline, enabled=True)
    assert_protected_unchanged(project, skills, protected)
    steps.append("repair")

    before_update_preview = tree_snapshot(project)
    update_preview = run_cli("update", project, artifact=updated)
    if update_preview.get("status") != "planned":
        raise LifecycleError("update did not default to dry-run")
    if tree_snapshot(project) != before_update_preview:
        raise LifecycleError("update dry-run changed the project")
    steps.append("update_dry_run")

    run_cli("update", project, apply=True, artifact=updated)
    require_state(
        manager,
        updated,
        installation="complete",
        enablement="enabled",
        artifact_id=updated.artifact_id,
    )
    assert_payload(project, updated, enabled=True)
    assert_protected_unchanged(project, skills, protected)
    steps.append("update")

    run_cli("rollback", project, apply=True, artifact=updated)
    require_state(
        manager,
        updated,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    assert_payload(project, baseline, enabled=True)
    assert_protected_unchanged(project, skills, protected)
    steps.append("rollback_update")

    run_cli("uninstall", project, apply=True)
    absent = require_state(
        manager,
        baseline,
        installation="absent",
        enablement="not_applicable",
        artifact_id=None,
    )
    if absent["rollback_available"] is not True:
        raise LifecycleError("uninstall did not preserve a rollback checkpoint")
    assert_protected_unchanged(project, skills, protected)
    steps.append("uninstall")

    run_cli("rollback", project, apply=True)
    require_state(
        manager,
        baseline,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    assert_payload(project, baseline, enabled=True)
    assert_protected_unchanged(project, skills, protected)
    steps.append("rollback_uninstall")

    return {
        "status": "pass",
        "steps": steps,
        "managed_skills": len(baseline.skills),
        "managed_files": len(baseline.files),
        "protected_paths": len(protected),
    }


def verify_identity_migration_lifecycle(
    fixture: Path,
    baseline: Artifact,
) -> dict[str, Any]:
    project = prepare_project(fixture / "projects" / "identity-migration")
    manager = DeliveryManager(project)
    skills = set(baseline.skills)
    protected = tree_snapshot(project, managed_skills=skills)
    steps: list[str] = []

    run_cli("install", project, apply=True)
    legacy_receipt = write_legacy_receipt(manager, baseline)
    payload_before = tree_snapshot(manager.enabled_root)
    before_preview = tree_snapshot(project)
    state = manager.inspect(baseline)
    if state["candidate_relation"] != "identity_migration_available":
        raise LifecycleError("mapped legacy receipt was not offered identity migration")
    steps.append("legacy_detected")

    preview = run_cli("migrate_identity", project)
    if preview.get("status") != "planned" or preview.get("applied") is not False:
        raise LifecycleError("identity migration did not default to dry-run")
    if tree_snapshot(project) != before_preview:
        raise LifecycleError("identity migration dry-run changed the project")
    steps.append("migration_dry_run")

    run_cli("migrate_identity", project, apply=True)
    migrated = require_state(
        manager,
        baseline,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    receipt = json.loads(manager.receipt_path.read_text(encoding="utf-8"))
    checkpoint = json.loads(
        (manager.rollback_path / "checkpoint.json").read_text(encoding="utf-8")
    )
    if (
        migrated["candidate_relation"] != "same_as_current"
        or receipt.get("schema_version") != 2
        or checkpoint.get("payload_mode") != "preserve_existing"
        or (manager.rollback_path / "enabled-skills").exists()
        or tree_snapshot(manager.enabled_root) != payload_before
    ):
        raise LifecycleError("identity migration did not preserve exact payload semantics")
    assert_protected_unchanged(project, skills, protected)
    steps.append("migration")

    run_cli("rollback", project, apply=True)
    restored = manager.inspect(baseline)
    if (
        restored["candidate_relation"] != "identity_migration_available"
        or json.loads(manager.receipt_path.read_text(encoding="utf-8")) != legacy_receipt
        or tree_snapshot(manager.enabled_root) != payload_before
    ):
        raise LifecycleError("identity migration rollback did not restore legacy identity")
    assert_protected_unchanged(project, skills, protected)
    steps.append("migration_rollback")

    managed = manager.enabled_root / "cotend-init" / "SKILL.md"
    managed.write_text("damaged mapped legacy payload\n", encoding="utf-8")
    run_cli("repair", project, apply=True)
    repaired = manager.inspect(baseline)
    if (
        repaired["installation"] != "complete"
        or repaired["candidate_relation"] != "same_as_current"
        or json.loads(manager.receipt_path.read_text(encoding="utf-8")).get(
            "schema_version"
        )
        != 2
    ):
        raise LifecycleError("mapped legacy repair did not migrate to schema v2")
    assert_payload(project, baseline, enabled=True)
    assert_protected_unchanged(project, skills, protected)
    steps.append("damaged_repair_and_migration")

    return {
        "status": "pass",
        "steps": steps,
        "payload_mode": "preserve_existing",
        "legacy_schema": 1,
        "current_schema": 2,
    }


def expect_guard_failure(action: Any, label: str) -> None:
    try:
        action()
    except LifecycleError:
        return
    raise LifecycleError(f"negative guard did not fail: {label}")


def verify_negative_guards(
    fixture: Path,
    baseline: Artifact,
    updated: Artifact,
) -> dict[str, Any]:
    skills = set(baseline.skills)
    passed: list[str] = []

    expect_guard_failure(
        lambda: guarded_fixture(ROOT / "escaped-L24-fixture"),
        "fixture_path_escape",
    )
    passed.append("fixture_path_escape")

    collision_project = prepare_project(fixture / "projects" / "collision")
    collision = collision_project / ".agents" / "skills" / "cotend-init"
    collision.mkdir()
    collision_file = collision / "SKILL.md"
    collision_file.write_text("user collision\n", encoding="utf-8")
    collision_snapshot = tree_snapshot(collision_project)
    run_cli(
        "install",
        collision_project,
        apply=True,
        expect_error="operation_blocked",
    )
    if tree_snapshot(collision_project) != collision_snapshot:
        raise LifecycleError("blocked collision install changed the project")
    passed.append("unowned_collision")

    extra_project = prepare_project(fixture / "projects" / "extra-file")
    extra_protected = tree_snapshot(extra_project, managed_skills=skills)
    run_cli("install", extra_project, apply=True)
    unexpected = (
        extra_project
        / ".agents"
        / "skills"
        / "cotend-init"
        / "USER-EXTENSION.md"
    )
    unexpected.write_text("do not delete\n", encoding="utf-8")
    run_cli(
        "repair",
        extra_project,
        apply=True,
        expect_error="operation_blocked",
    )
    run_cli(
        "uninstall",
        extra_project,
        apply=True,
        expect_error="operation_blocked",
    )
    run_cli(
        "rollback",
        extra_project,
        apply=True,
        expect_error="operation_blocked",
    )
    if unexpected.read_text(encoding="utf-8") != "do not delete\n":
        raise LifecycleError("blocked operations changed the unexpected user file")
    assert_protected_unchanged(extra_project, skills, extra_protected)
    passed.append("unexpected_file")

    checkpoint_project = prepare_project(fixture / "projects" / "corrupt-checkpoint")
    checkpoint_protected = tree_snapshot(checkpoint_project, managed_skills=skills)
    run_cli("install", checkpoint_project, apply=True)
    run_cli("update", checkpoint_project, apply=True, artifact=updated)
    checkpoint_file = (
        checkpoint_project
        / ".agents"
        / ".cotend-delivery"
        / "rollback"
        / "enabled-skills"
        / "cotend-init"
        / "SKILL.md"
    )
    checkpoint_file.write_text("corrupt checkpoint\n", encoding="utf-8")
    run_cli(
        "rollback",
        checkpoint_project,
        apply=True,
        artifact=updated,
        expect_error="checkpoint_invalid",
    )
    require_state(
        DeliveryManager(checkpoint_project),
        updated,
        installation="complete",
        enablement="enabled",
        artifact_id=updated.artifact_id,
    )
    assert_protected_unchanged(checkpoint_project, skills, checkpoint_protected)
    passed.append("corrupt_checkpoint")

    receipt_project = prepare_project(fixture / "projects" / "invalid-receipt")
    receipt_protected = tree_snapshot(receipt_project, managed_skills=skills)
    run_cli("install", receipt_project, apply=True)
    receipt = receipt_project / ".agents" / ".cotend-delivery" / "receipt.json"
    receipt.write_text("{broken", encoding="utf-8")
    run_cli(
        "update",
        receipt_project,
        apply=True,
        artifact=updated,
        expect_error="operation_blocked",
    )
    run_cli("rollback", receipt_project, apply=True)
    require_state(
        DeliveryManager(receipt_project),
        baseline,
        installation="absent",
        enablement="not_applicable",
        artifact_id=None,
    )
    assert_protected_unchanged(receipt_project, skills, receipt_protected)
    passed.append("invalid_receipt_recovery")

    fault_project = prepare_project(fixture / "projects" / "fault-rollback")
    fault_protected = tree_snapshot(fault_project, managed_skills=skills)
    manager = DeliveryManager(fault_project)
    manager.execute("install", baseline, apply=True)
    with mock.patch.object(
        manager,
        "_write_receipt",
        side_effect=OSError("injected receipt failure"),
    ):
        try:
            manager.execute("update", updated, apply=True)
        except DeliveryError as exc:
            if exc.code != "transition_failed_rolled_back":
                raise LifecycleError("fault injection returned the wrong error") from exc
        else:
            raise LifecycleError("fault-injected update unexpectedly succeeded")
    restored = require_state(
        manager,
        baseline,
        installation="complete",
        enablement="enabled",
        artifact_id=baseline.artifact_id,
    )
    if restored["rollback_available"] is not True:
        raise LifecycleError("failed update did not restore the prior rollback")
    manager.execute("rollback", baseline, apply=True)
    require_state(
        manager,
        baseline,
        installation="absent",
        enablement="not_applicable",
        artifact_id=None,
    )
    assert_protected_unchanged(fault_project, skills, fault_protected)
    passed.append("transition_failure_atomicity")

    downgrade_project = prepare_project(fixture / "projects" / "downgrade")
    downgrade_protected = tree_snapshot(downgrade_project, managed_skills=skills)
    run_cli("install", downgrade_project, apply=True)
    run_cli("update", downgrade_project, apply=True, artifact=updated)
    before_downgrade = tree_snapshot(downgrade_project)
    run_cli(
        "update",
        downgrade_project,
        apply=True,
        artifact=baseline,
        expect_error="operation_blocked",
    )
    state = DeliveryManager(downgrade_project).inspect(baseline)
    if (
        state["candidate_relation"] != "downgrade_candidate"
        or tree_snapshot(downgrade_project) != before_downgrade
    ):
        raise LifecycleError("blocked downgrade changed state or lost its relation")
    assert_protected_unchanged(downgrade_project, skills, downgrade_protected)
    passed.append("downgrade_not_update")

    preserved_project = prepare_project(
        fixture / "projects" / "preserved-checkpoint-drift"
    )
    preserved_protected = tree_snapshot(preserved_project, managed_skills=skills)
    preserved_manager = DeliveryManager(preserved_project)
    run_cli("install", preserved_project, apply=True)
    write_legacy_receipt(preserved_manager, baseline)
    run_cli("migrate_identity", preserved_project, apply=True)
    preserved_receipt = preserved_manager.receipt_path.read_bytes()
    managed = preserved_manager.enabled_root / "cotend-init" / "SKILL.md"
    managed.write_text("payload drift after identity migration\n", encoding="utf-8")
    run_cli(
        "rollback",
        preserved_project,
        apply=True,
        expect_error="checkpoint_invalid",
    )
    if (
        preserved_manager.receipt_path.read_bytes() != preserved_receipt
        or managed.read_text(encoding="utf-8")
        != "payload drift after identity migration\n"
    ):
        raise LifecycleError("blocked preserved checkpoint rollback changed the project")
    assert_protected_unchanged(preserved_project, skills, preserved_protected)
    passed.append("preserved_checkpoint_payload_drift")

    return {"status": "pass", "cases": passed, "count": len(passed)}


def run_concurrency_worker(
    *,
    mode: str,
    project: Path,
    source: Path,
    event: Path,
) -> int:
    project = guarded_fixture(project)
    source = guarded_fixture(source)
    event = guarded_fixture(event)
    baseline = Artifact.from_repository(ROOT)
    candidate = Artifact.from_directory(
        source,
        source_release_id=baseline.source_release_id,
        artifact_id="cotend-codex-r000002",
        revision=2,
        protocol=baseline.protocol,
    )
    manager = DeliveryManager(project)

    def signal_and_wait() -> None:
        event.parent.mkdir(parents=True, exist_ok=True)
        event.write_text("ready\n", encoding="utf-8")
        time.sleep(60)

    if mode == "before_checkpoint":
        original_checkpoint = manager._create_checkpoint

        def held_checkpoint(operation: str) -> None:
            signal_and_wait()
            original_checkpoint(operation)

        manager._create_checkpoint = held_checkpoint  # type: ignore[method-assign]
    elif mode == "before_receipt":
        original_receipt = manager._write_receipt

        def held_receipt(receipt: dict[str, Any]) -> None:
            signal_and_wait()
            original_receipt(receipt)

        manager._write_receipt = held_receipt  # type: ignore[method-assign]
    else:
        raise LifecycleError(f"unknown worker mode: {mode}")

    manager.execute("update", candidate, apply=True)
    return 0


def start_concurrency_worker(
    *,
    mode: str,
    project: Path,
    source: Path,
    event: Path,
) -> subprocess.Popen[str]:
    return subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker-mode",
            mode,
            "--worker-project",
            str(project),
            "--worker-source",
            str(source),
            "--worker-event",
            str(event),
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def wait_for_worker_event(
    worker: subprocess.Popen[str],
    event: Path,
    *,
    timeout: float = 20,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if event.is_file():
            return
        if worker.poll() is not None:
            stdout, stderr = worker.communicate()
            raise LifecycleError(
                "concurrency worker exited before its hold point: "
                f"stdout={stdout.strip()} stderr={stderr.strip()}"
            )
        time.sleep(0.05)
    raise LifecycleError("concurrency worker did not reach its hold point")


def terminate_worker(worker: subprocess.Popen[str]) -> None:
    if worker.poll() is None:
        worker.terminate()
        try:
            worker.wait(timeout=10)
        except subprocess.TimeoutExpired:
            worker.kill()
            worker.wait(timeout=10)
    worker.communicate(timeout=5)


def verify_concurrent_transitions(
    fixture: Path,
    baseline: Artifact,
    updated: Artifact,
) -> dict[str, Any]:
    skills = set(baseline.skills)
    passed: list[str] = []
    events = fixture / "events"

    contention_project = prepare_project(
        fixture / "projects" / "concurrent-contention"
    )
    contention_protected = tree_snapshot(
        contention_project,
        managed_skills=skills,
    )
    run_cli("install", contention_project, apply=True)
    contention_event = events / "contention-ready.txt"
    worker = start_concurrency_worker(
        mode="before_checkpoint",
        project=contention_project,
        source=updated.root,
        event=contention_event,
    )
    try:
        wait_for_worker_event(worker, contention_event)
        state = DeliveryManager(contention_project).inspect(updated)
        if (
            state["mutation_lock"]["state"] != "active"
            or state["transition"] != "staged"
        ):
            raise LifecycleError("live contention lock was not reported as active")
        before_contender = tree_snapshot(contention_project)
        run_cli(
            "update",
            contention_project,
            apply=True,
            artifact=updated,
            expect_error="operation_blocked",
        )
        if tree_snapshot(contention_project) != before_contender:
            raise LifecycleError("blocked competing process changed the project")
        passed.append("same_project_contender_zero_write")

        independent_project = prepare_project(
            fixture / "projects" / "concurrent-independent"
        )
        independent_protected = tree_snapshot(
            independent_project,
            managed_skills=skills,
        )
        run_cli("install", independent_project, apply=True)
        require_state(
            DeliveryManager(independent_project),
            baseline,
            installation="complete",
            enablement="enabled",
            artifact_id=baseline.artifact_id,
        )
        assert_protected_unchanged(
            independent_project,
            skills,
            independent_protected,
        )
        passed.append("different_projects_are_independent")
    finally:
        terminate_worker(worker)

    contention_after_kill = DeliveryManager(contention_project).inspect(updated)
    contention_owner = contention_after_kill["mutation_lock"]["owner"]
    if (
        contention_after_kill["mutation_lock"]["state"] != "recovery_required"
        or not contention_after_kill["mutation_lock"]["interrupted"]
        or contention_owner is None
        or contention_owner["phase"] != "checkpointing"
        or contention_owner["process_liveness"] == "alive"
    ):
        raise LifecycleError("terminated pre-checkpoint owner was not preserved")
    assert_protected_unchanged(
        contention_project,
        skills,
        contention_protected,
    )
    passed.append("terminated_precheckpoint_detected")

    interrupted_project = prepare_project(
        fixture / "projects" / "concurrent-interrupted"
    )
    interrupted_protected = tree_snapshot(
        interrupted_project,
        managed_skills=skills,
    )
    run_cli("install", interrupted_project, apply=True)
    interrupted_event = events / "interrupted-ready.txt"
    worker = start_concurrency_worker(
        mode="before_receipt",
        project=interrupted_project,
        source=updated.root,
        event=interrupted_event,
    )
    try:
        wait_for_worker_event(worker, interrupted_event)
    finally:
        terminate_worker(worker)

    interrupted_manager = DeliveryManager(interrupted_project)
    before_inspect = tree_snapshot(interrupted_project)
    interrupted = interrupted_manager.inspect(updated)
    if tree_snapshot(interrupted_project) != before_inspect:
        raise LifecycleError("inspect mutated an interrupted project")
    owner = interrupted["mutation_lock"]["owner"]
    if (
        interrupted["transition"] != "recovery_required"
        or interrupted["mutation_lock"]["state"] != "recovery_required"
        or not interrupted["mutation_lock"]["interrupted"]
        or owner is None
        or owner["phase"] != "mutating"
        or owner["process_liveness"] == "alive"
        or interrupted["rollback_available"] is not True
        or not interrupted["transition_artifacts"]
        or interrupted["recommended_operation"] != "manual_recovery_required"
    ):
        raise LifecycleError("mid-mutation termination was not classified safely")
    passed.append("terminated_midmutation_detected")
    passed.append("interrupted_inspect_is_read_only")

    blocked_snapshot = tree_snapshot(interrupted_project)
    run_cli(
        "rollback",
        interrupted_project,
        apply=True,
        expect_error="operation_blocked",
    )
    run_cli(
        "repair",
        interrupted_project,
        apply=True,
        artifact=updated,
        expect_error="operation_blocked",
    )
    if tree_snapshot(interrupted_project) != blocked_snapshot:
        raise LifecycleError("stale-lock recovery commands changed the project")
    assert_protected_unchanged(
        interrupted_project,
        skills,
        interrupted_protected,
    )
    passed.append("stale_lock_blocks_recovery_mutations")

    return {"status": "pass", "cases": passed, "count": len(passed)}


def write_evidence(path: Path, evidence: dict[str, Any]) -> None:
    target = guarded_fixture(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(evidence, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the deterministic CoTend project delivery lifecycle"
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="ignored fixture path under .private-provenance",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="rebuild the disposable fixture before verification",
    )
    parser.add_argument(
        "--negative-mutations",
        action="store_true",
        help="run deterministic failure and recovery cases",
    )
    parser.add_argument(
        "--concurrency",
        action="store_true",
        help="run independent-process contention and termination cases",
    )
    parser.add_argument(
        "--worker-mode",
        choices=("before_checkpoint", "before_receipt"),
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--worker-project", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--worker-source", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--worker-event", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "--evidence",
        type=Path,
        help="write JSON evidence under the fixture (default: evidence.json)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.worker_mode is not None:
            if not args.worker_project or not args.worker_source or not args.worker_event:
                raise LifecycleError("worker mode requires project, source, and event")
            return run_concurrency_worker(
                mode=args.worker_mode,
                project=args.worker_project,
                source=args.worker_source,
                event=args.worker_event,
            )
        fixture = reset_fixture(args.fixture) if args.prepare else guarded_fixture(args.fixture)
        if not fixture.is_dir():
            raise LifecycleError("fixture is missing; run with --prepare")
        baseline = Artifact.from_repository(ROOT)
        updated = make_updated_artifact(fixture, baseline)
        evidence: dict[str, Any] = {
            "schema": "cotend.delivery-lifecycle-evidence",
            "baseline_artifact": baseline.artifact_id,
            "protocol": baseline.protocol,
            "positive": verify_positive_lifecycle(fixture, baseline, updated),
            "identity_migration": verify_identity_migration_lifecycle(
                fixture,
                baseline,
            ),
        }
        print(
            "DELIVERY_LIFECYCLE_OK "
            f"steps={len(evidence['positive']['steps'])} "
            f"skills={len(baseline.skills)} files={len(baseline.files)}"
        )
        print(
            "DELIVERY_IDENTITY_MIGRATION_OK "
            f"steps={len(evidence['identity_migration']['steps'])}"
        )
        if args.negative_mutations:
            evidence["negative"] = verify_negative_guards(fixture, baseline, updated)
            print(
                "DELIVERY_LIFECYCLE_NEGATIVE_OK "
                f"cases={evidence['negative']['count']}"
            )
        if args.concurrency:
            evidence["concurrency"] = verify_concurrent_transitions(
                fixture,
                baseline,
                updated,
            )
            print(
                "DELIVERY_CONCURRENCY_OK "
                f"cases={evidence['concurrency']['count']}"
            )
        evidence_path = args.evidence or fixture / "evidence.json"
        write_evidence(evidence_path, evidence)
    except (
        DeliveryError,
        LifecycleError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print("DELIVERY_LIFECYCLE_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
