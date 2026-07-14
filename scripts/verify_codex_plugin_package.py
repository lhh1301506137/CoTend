from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
from verify_isolated_codex_plugin import plugin_creator_script  # noqa: E402
from verify_user_skill_delivery import (  # noqa: E402
    protected_boundaries,
    stat_only_snapshot,
)


PRIVATE_ROOT = (
    ROOT / ".private-provenance" / "L44-codex-plugin-production-package"
)
DEFAULT_EVIDENCE = PRIVATE_ROOT / "evidence" / "result.json"
NEGATIVE_CASES = 17


def source_state() -> dict[str, Any]:
    return {
        "git_head": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "skills": package.path_hash_manifest_sha256(
            package.source_skill_manifest()
        ),
        "target_artifact_lock": package.sha256_file(package.TARGET_ARTIFACT_LOCK),
        "framework_lock": package.sha256_file(
            ROOT / "upstream" / "framework.lock.json"
        ),
    }


def reset_private_root() -> None:
    resolved = PRIVATE_ROOT.resolve(strict=False)
    if not resolved.is_relative_to((ROOT / ".private-provenance").resolve()):
        raise package.PluginPackageError("L44 fixture root escaped private provenance")
    if resolved.exists():
        package.reject_link_tree(resolved, label="L44 verification fixture")
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def write_evidence(path: Path, payload: dict[str, Any]) -> None:
    resolved = path.expanduser().resolve(strict=False)
    if not resolved.is_relative_to(PRIVATE_ROOT.resolve()):
        raise package.PluginPackageError("L44 evidence must stay inside its private root")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(
        json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the isolated CoTend Codex Plugin production candidate."
    )
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reset_private_root()
    boundaries = protected_boundaries()
    protected_before = {
        label: stat_only_snapshot(path) for label, path in boundaries.items()
    }
    source_before = source_state()

    suite = unittest.defaultTestLoader.loadTestsFromName(
        "tests.test_codex_plugin_package"
    )
    tests = unittest.TextTestRunner(verbosity=1).run(suite)
    if not tests.wasSuccessful():
        return 1

    first = PRIVATE_ROOT / "determinism-a" / package.PLUGIN_NAME
    second = PRIVATE_ROOT / "determinism-b" / package.PLUGIN_NAME
    first_result = package.build_package(first)
    package.build_package(second)
    first_manifest = package.path_hash_manifest(first)
    second_manifest = package.path_hash_manifest(second)
    if first_manifest != second_manifest:
        print("CODEX_PLUGIN_PACKAGE_NONDETERMINISTIC", file=sys.stderr)
        return 2

    validator = plugin_creator_script("validate_plugin.py")
    official = package.run_official_validator(first, validator)
    source_after = source_state()
    if source_before != source_after:
        print("CODEX_PLUGIN_PACKAGE_SOURCE_CHANGED", file=sys.stderr)
        return 3
    protected_after = {
        label: stat_only_snapshot(path) for label, path in boundaries.items()
    }
    changed = sorted(
        label
        for label in boundaries
        if protected_before[label] != protected_after[label]
    )
    if changed:
        print(
            "CODEX_PLUGIN_PACKAGE_BOUNDARY_CHANGED labels=" + ",".join(changed),
            file=sys.stderr,
        )
        return 4

    evidence = {
        "status": "passed_isolated_production_candidate_contract",
        "plugin": {
            "name": first_result["plugin_name"],
            "version": first_result["plugin_version"],
            "identity_authority": "initial_submission_identity_confirmed_not_release",
        },
        "package": {
            "builds_compared": 2,
            "files": first_result["package_files"],
            "skills": first_result["skills"],
            "skill_files": first_result["skill_files"],
            "friendly_display_names": first_result["friendly_display_names"],
            "source_bytes_identical": first_result["source_bytes_identical"],
            "source_manifest_sha256": first_result["source_manifest_sha256"],
            "package_manifest_sha256": first_result["package_manifest_sha256"],
            "deterministic": first_manifest == second_manifest,
        },
        "verification": {
            "unit_tests": tests.testsRun,
            "negative_cases": NEGATIVE_CASES,
            "official_plugin_creator_validator": official,
            "protected_boundaries": len(boundaries),
            "protected_boundaries_unchanged": True,
            "source_and_locks_unchanged": True,
        },
        "forbidden_actions": {
            "plugin_installation": "not_run",
            "marketplace_write": "not_run",
            "submission": "not_run",
            "release": "not_run",
            "publish": "not_run",
            "push": "not_run",
        },
    }
    write_evidence(args.evidence, evidence)
    print(
        "CODEX_PLUGIN_PRODUCTION_PACKAGE_OK "
        f"builds=2 files={first_result['package_files']} "
        f"skills={first_result['skills']} skill_files={first_result['skill_files']} "
        f"tests={tests.testsRun} negatives={NEGATIVE_CASES} "
        f"validator={official['status']} boundaries={len(boundaries)} unchanged=true "
        f"digest={first_result['package_manifest_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
