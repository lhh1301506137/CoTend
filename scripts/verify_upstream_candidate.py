from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "c14d4133bf0438d435048858554c88c89a7870a3"
SOURCE_ROOT = "skills-backup/codex"
SOURCE_TREE = "a6824559e087f87da90a55bcc6403576db1027c1"
SOURCE_IDENTITY = f"exact-source:{SOURCE_COMMIT}"
DUAL_PROTOCOL = "dual-ai-" + "collaboration-v1.79"
ADOPTION_BASE_COMMIT = "774aab64e778d2e3a57b66cfd65d808ac8235e14"
ADOPTION_BASE_TREE = "ebcc0b2930146aca1ce299215f9a2f936b12d4c8"
BASELINE_COMMIT = "4540f9e0543e85c6a7cceb1d7501467feee8b440"
BASELINE_TAG = "dual-ai-share-2026.07.28.2"
BASELINE_TAG_OBJECT = "d26994355921b9c43956f7300069c892884496e0"
BASELINE_SOURCE_TREE = "2eae0ca4447cace17bdf93df3b04b665293deecb"
PACKAGE_ROOT = "dual-ai-collaboration-skill-share"
PACKAGE_TREE = "686a507d904b08c6a43ef6c5d40c1d43083d8f1b"
HANDOFF_ROOT = Path("consumer-handoffs/cotend/2026.08.01.1")
HANDOFF_HASHES = {
    "HANDOFF.json": "4d16e8a1ba29a2a71e0974e79f0967b2ec4cfa8afe42e0d24c43b32102df47af",
    "HANDOFF.md": "fe8dfcbd787cfa9116567f6f2730dd3bb345b0774a882c1a4987614394d6c52c",
    "SHA256SUMS": "6ea9ad1602d3cc331314b2ec8b06e7f29019b6715dfc553da7c1481d9cd3ea3a",
}


def git_bytes(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
    )
    return result.stdout


def git_text(repo: Path, *args: str) -> str:
    return git_bytes(repo, *args).decode("utf-8").strip()


def object_file(repo: Path, ref: str, relative_path: str) -> bytes:
    return git_bytes(repo, "show", f"{ref}:{relative_path}")


def tagged_package_file(repo: Path, relative_path: str) -> bytes:
    return object_file(repo, BASELINE_TAG, f"{PACKAGE_ROOT}/{relative_path}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_handoff(upstream_repo: Path, errors: list[str]) -> dict[str, Any] | None:
    handoff_dir = upstream_repo / HANDOFF_ROOT
    for name, expected in HANDOFF_HASHES.items():
        path = handoff_dir / name
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"consumer handoff hash mismatch: {name}")
    try:
        handoff = load_json(handoff_dir / "HANDOFF.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load exact-source consumer handoff: {exc}")
        return None
    target = handoff.get("target")
    baseline = handoff.get("baseline")
    coverage = handoff.get("commit_coverage")
    if not all(isinstance(item, dict) for item in (target, baseline, coverage)):
        errors.append("consumer handoff target, baseline, or coverage is invalid")
        return handoff
    assert isinstance(target, dict)
    assert isinstance(baseline, dict)
    assert isinstance(coverage, dict)
    if target != {
        "anchor_ref": SOURCE_COMMIT,
        "anchor_type": "exact_source_commit",
        "commit": SOURCE_COMMIT,
        "dual_model_upgrade_version": "1.14",
        "framework_protocol": DUAL_PROTOCOL,
        "latest_public_release": target.get("latest_public_release"),
        "publication_state": "not_public_release",
        "source_tree": SOURCE_TREE,
        "source_tree_path": SOURCE_ROOT,
    }:
        errors.append("consumer handoff exact-source target drift")
    latest_public = target.get("latest_public_release")
    if not isinstance(latest_public, dict) or (
        latest_public.get("release_id"),
        latest_public.get("tag_object"),
        latest_public.get("commit"),
        latest_public.get("canonical_source_tree"),
    ) != (
        "2026.07.28.2",
        BASELINE_TAG_OBJECT,
        BASELINE_COMMIT,
        BASELINE_SOURCE_TREE,
    ):
        errors.append("consumer handoff latest-public-release history drift")
    if (
        baseline.get("commit") != ADOPTION_BASE_COMMIT
        or baseline.get("carrier_tree") != ADOPTION_BASE_TREE
        or baseline.get("anchor_type") != "exact_source_commit"
        or baseline.get("carrier_protocol")
        != "dual-ai-" + "collaboration-v1.76"
    ):
        errors.append("consumer handoff baseline drift")
    commits = coverage.get("commits")
    if not isinstance(commits, list) or coverage.get("accounted_count") != 13:
        errors.append("consumer handoff commit coverage count drift")
    else:
        dispositions = [
            item.get("disposition") for item in commits if isinstance(item, dict)
        ]
        if (
            len(dispositions) != 13
            or dispositions.count("included_change") != 3
            or dispositions.count("evidence_only") != 10
            or dispositions.count("consumer_not_applicable") != 0
        ):
            errors.append("consumer handoff commit disposition coverage drift")
    if handoff.get("target_publication_state") != "not_public_release":
        errors.append("consumer handoff falsely describes the target as a release")
    return handoff


def verify(upstream_repo: Path, candidate_path: Path, role_map_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        candidate = load_json(candidate_path)
        role_map = load_json(role_map_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"cannot load candidate mapping records: {exc}"]

    verify_handoff(upstream_repo, errors)
    try:
        if git_text(upstream_repo, "cat-file", "-t", SOURCE_COMMIT) != "commit":
            errors.append("exact source anchor is not a commit")
        if git_text(upstream_repo, "rev-parse", f"{SOURCE_COMMIT}:{SOURCE_ROOT}") != SOURCE_TREE:
            errors.append("exact source canonical tree mismatch")
        if git_text(upstream_repo, "cat-file", "-t", BASELINE_TAG) != "tag":
            errors.append("latest public release anchor is not an annotated tag")
        if git_text(upstream_repo, "rev-parse", BASELINE_TAG) != BASELINE_TAG_OBJECT:
            errors.append("latest public release tag object mismatch")
        if git_text(upstream_repo, "rev-parse", f"{BASELINE_TAG}^{{commit}}") != BASELINE_COMMIT:
            errors.append("latest public release commit mismatch")
        if git_text(upstream_repo, "rev-parse", f"{BASELINE_TAG}:{PACKAGE_ROOT}") != PACKAGE_TREE:
            errors.append("latest public release package tree mismatch")
        if (
            git_text(upstream_repo, "rev-parse", f"{BASELINE_COMMIT}:{SOURCE_ROOT}")
            != BASELINE_SOURCE_TREE
        ):
            errors.append("latest public release canonical source tree mismatch")
        git_text(
            upstream_repo,
            "merge-base",
            "--is-ancestor",
            ADOPTION_BASE_COMMIT,
            SOURCE_COMMIT,
        )
        if (
            git_text(
                upstream_repo,
                "rev-list",
                "--count",
                f"{ADOPTION_BASE_COMMIT}..{SOURCE_COMMIT}",
            )
            != "13"
        ):
            errors.append("exact-source handoff range is not the recorded 13 commits")
    except subprocess.CalledProcessError as exc:
        return errors + [f"cannot resolve exact source or release-history anchor: {exc}"]

    release_anchor = candidate.get("release_anchor")
    if not isinstance(release_anchor, dict):
        return errors + ["candidate release_anchor must be an object"]
    if (
        candidate.get("status") != "adopted_verified"
        or candidate.get("candidate_only") is not False
        or candidate.get("release_id") != SOURCE_IDENTITY
        or candidate.get("target_publication_state") != "not_public_release"
        or candidate.get("framework_protocol_version") != "1.79"
        or candidate.get("dual_model_upgrade_version") != "1.14"
    ):
        errors.append("candidate exact-source identity or finalized state drift")
    if (
        release_anchor.get("type"),
        release_anchor.get("publication_state"),
        release_anchor.get("commit"),
        release_anchor.get("canonical_source_tree"),
        release_anchor.get("canonical_source_tree_path"),
    ) != (
        "exact_source_commit",
        "not_public_release",
        SOURCE_COMMIT,
        SOURCE_TREE,
        SOURCE_ROOT,
    ):
        errors.append("candidate exact-source anchor drift")
    latest_public = release_anchor.get("latest_public_release")
    if not isinstance(latest_public, dict) or (
        latest_public.get("tag"),
        latest_public.get("tag_object"),
        latest_public.get("release_commit"),
        latest_public.get("canonical_source_tree"),
        latest_public.get("package_tree"),
    ) != (
        BASELINE_TAG,
        BASELINE_TAG_OBJECT,
        BASELINE_COMMIT,
        BASELINE_SOURCE_TREE,
        PACKAGE_TREE,
    ):
        errors.append("candidate latest-public-release history drift")

    carriers = candidate.get("carriers")
    if not isinstance(carriers, dict):
        return errors + ["candidate carriers record is missing"]
    codex = carriers.get("codex")
    claude = carriers.get("claude")
    if not isinstance(codex, dict) or not isinstance(claude, dict):
        return errors + ["candidate carrier records are invalid"]
    codex_trees = codex.get("skill_trees")
    claude_trees = claude.get("skill_trees")
    if not isinstance(codex_trees, dict) or not isinstance(claude_trees, dict):
        return errors + ["candidate Skill tree maps are invalid"]
    if codex.get("skill_count") != 10 or codex.get("skill_file_count") != 69:
        errors.append("candidate exact-source Codex inventory drift")
    for skill_id, expected_tree in codex_trees.items():
        try:
            actual_tree = git_text(
                upstream_repo,
                "rev-parse",
                f"{SOURCE_COMMIT}:{SOURCE_ROOT}/{skill_id}",
            )
        except subprocess.CalledProcessError as exc:
            errors.append(f"cannot resolve exact-source Codex Skill {skill_id}: {exc}")
            continue
        if actual_tree != expected_tree:
            errors.append(f"exact-source Codex Skill tree mismatch: {skill_id}")
    for skill_id, expected_tree in claude_trees.items():
        try:
            actual_tree = git_text(
                upstream_repo,
                "rev-parse",
                f"{BASELINE_TAG}:{PACKAGE_ROOT}/claude-skills/{skill_id}",
            )
        except subprocess.CalledProcessError as exc:
            errors.append(f"cannot resolve historical Claude Skill {skill_id}: {exc}")
            continue
        if actual_tree != expected_tree:
            errors.append(f"historical Claude Skill tree mismatch: {skill_id}")

    try:
        source_registry = json.loads(
            tagged_package_file(upstream_repo, "THIRD-PARTY-SOURCES.json")
        )
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return errors + [f"cannot read latest public third-party metadata: {exc}"]
    components = source_registry.get("components") if isinstance(source_registry, dict) else None
    source_by_skill: dict[str, dict[str, Any]] = {}
    if isinstance(components, list):
        for component in components:
            if not isinstance(component, dict):
                continue
            packaged_skill = component.get("packaged_skill")
            if isinstance(packaged_skill, str) and packaged_skill.startswith("codex/"):
                source_by_skill[packaged_skill.removeprefix("codex/")] = component

    role_entries = role_map.get("skills")
    if (
        role_map.get("status") != "adopted_verified"
        or role_map.get("candidate_release") != SOURCE_IDENTITY
        or role_map.get("candidate_publication_state") != "not_public_release"
        or role_map.get("skill_count") != 10
        or not isinstance(role_entries, list)
    ):
        return errors + ["role map exact-source identity or inventory drift"]
    by_source = {
        entry.get("source_skill_id"): entry
        for entry in role_entries
        if isinstance(entry, dict)
    }
    if set(by_source) != set(codex_trees) or len(role_entries) != 10:
        errors.append("role map does not cover the exact ten-Skill source set")

    required_markers = {
        "dual-ai-collaboration": (
            DUAL_PROTOCOL,
            "active_route_continuous",
            "authorized_task_closure",
        ),
        "dual-ai-project-init": (f"Protocol target: `{DUAL_PROTOCOL}`",),
        "dual-ai-semantic-alignment": (
            f"Companion version: `{DUAL_PROTOCOL}`",
        ),
        "dual-ai-session-handoff": (
            "Evaluate only whether the current user input contains the exact literal",
            "$dual-ai-session-handoff",
            "same_primary_session_takeover_result",
            "not_started | current | stale | conflict",
        ),
        "dual-model-upgrade": ("packet_version: dual-model-upgrade-v1.14",),
        "dual-ai-tooling": (
            "# Dual AI Tooling",
            "call -> compose -> adapt -> build",
            "Select at most three relevant records",
            "Inventory is read-only discovery",
        ),
    }
    for skill_id, entry in by_source.items():
        if entry.get("source_tree") != codex_trees.get(skill_id):
            errors.append(f"role map tree does not match candidate: {skill_id}")
        try:
            skill_text = object_file(
                upstream_repo,
                SOURCE_COMMIT,
                f"{SOURCE_ROOT}/{skill_id}/SKILL.md",
            ).decode("utf-8")
        except (subprocess.CalledProcessError, UnicodeDecodeError) as exc:
            errors.append(f"cannot read exact-source Skill {skill_id}: {exc}")
            continue
        if skill_id == "dual-ai-session-handoff":
            try:
                skill_text += "\n" + object_file(
                    upstream_repo,
                    SOURCE_COMMIT,
                    (
                        f"{SOURCE_ROOT}/{skill_id}/references/"
                        "session-handoff-workflow.md"
                    ),
                ).decode("utf-8")
            except (subprocess.CalledProcessError, UnicodeDecodeError) as exc:
                errors.append(
                    f"cannot read exact-source session-handoff workflow: {exc}"
                )
        parts = skill_text.split("---", 2)
        if len(parts) != 3 or f"name: {skill_id}" not in parts[1]:
            errors.append(f"exact-source Skill frontmatter mismatch: {skill_id}")
        for marker in required_markers.get(str(skill_id), ()):
            if marker not in skill_text:
                errors.append(f"exact-source Skill marker missing: {skill_id}: {marker}")
        source = source_by_skill.get(str(skill_id))
        if source is not None:
            expected_relationship = (
                "adapted_third_party"
                if skill_id == "karpathy-guidelines"
                else source.get("relationship")
            )
            if (
                entry.get("source_relationship") != expected_relationship
                or entry.get("license") != source.get("license")
            ):
                errors.append(f"role-map third-party provenance mismatch: {skill_id}")

    lock_path = ROOT / "upstream" / "framework.lock.json"
    try:
        framework_lock = load_json(lock_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return errors + [f"cannot load final framework lock: {exc}"]
    if (
        framework_lock.get("release_id") != SOURCE_IDENTITY
        or framework_lock.get("source_skill_trees") != codex_trees
        or framework_lock.get("source_anchor")
        != {
            "type": "exact_source_commit",
            "publication_state": "not_public_release",
            "commit": SOURCE_COMMIT,
            "canonical_source_tree": SOURCE_TREE,
            "canonical_source_tree_path": SOURCE_ROOT,
            "consumer_handoff": release_anchor.get("consumer_handoff"),
        }
    ):
        errors.append("framework lock does not match the exact-source candidate")
    if framework_lock.get("adoption_anchor") != {
        "type": "containing_commit",
        "path": "upstream/framework.lock.json",
    }:
        errors.append("framework lock containing-commit anchor mismatch")
    boundaries = framework_lock.get("delivery_boundaries")
    if not isinstance(boundaries, dict) or boundaries.get("live_install_performed") is not False:
        errors.append("framework lock incorrectly claims a live install")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify CoTend's adopted exact-source records, consumer handoff, "
            "and retained public-release history against upstream Git objects."
        )
    )
    parser.add_argument("--upstream-repo", type=Path, required=True)
    parser.add_argument(
        "--candidate",
        type=Path,
        default=ROOT / "upstream" / "FRAMEWORK-CANDIDATE.json",
    )
    parser.add_argument(
        "--role-map",
        type=Path,
        default=ROOT / "upstream" / "CODEX-SKILL-ROLE-MAP.json",
    )
    args = parser.parse_args()
    errors = verify(
        args.upstream_repo.resolve(),
        args.candidate.resolve(),
        args.role_map.resolve(),
    )
    if errors:
        print("UPSTREAM_CANDIDATE_VERIFICATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    candidate = load_json(args.candidate.resolve())
    role_map = load_json(args.role_map.resolve())
    print(
        "UPSTREAM_CANDIDATE_VERIFICATION_OK "
        f"source={candidate['release_id']} "
        "publication=not_public_release "
        f"codex_skills={role_map['skill_count']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
