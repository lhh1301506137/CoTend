from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "fe21e970bc2bdc69de5e2ce1710aef2dd156a54d"
SOURCE_BASE_COMMIT = "c14d4133bf0438d435048858554c88c89a7870a3"
SOURCE_ROOT = "skills-backup/codex"
SOURCE_TREE = "076099a1c6888ede804189e1aa125eba92380e94"
SOURCE_IDENTITY = f"exact-source:{SOURCE_COMMIT}"
HANDOFF_ID = "2026.08.12.2"
HANDOFF_HASHES = {
    "HANDOFF.json": "1367e88f6dd9ec73482ec537cb17149681d7d00c88ed8473745d8ac5d1137b48",
    "HANDOFF.md": "6626cf9720bc871009e5d3866555def48eefaca275433f9f952f5835c0d2083e",
    "SHA256SUMS": "b58045caf8ba36bc391e13aeef1336049a6f006c2774457965a2e76445a80208",
}
SOURCE_SKILLS = {
    "diagnose-only": {
        "target": "cotend-diagnose-only",
        "tree": "7bb5b228c675f778ce4b62a46385a9e507a3691f",
        "files": 2,
    },
    "dual-ai-collaboration": {
        "target": "cotend-collaboration",
        "tree": "335e3f0fe98ef2bb6a3f26fce83dc955e518bed0",
        "files": 43,
    },
    "dual-ai-init": {
        "target": "cotend-init",
        "tree": "0447d65ef270153d69858953b174e97e2666e409",
        "files": 2,
    },
    "dual-ai-project-init": {
        "target": "cotend-project-init",
        "tree": "1b3d56e52d489cbc6241d4e1e8e71268ea01147d",
        "files": 19,
    },
    "dual-ai-semantic-alignment": {
        "target": "cotend-semantic-alignment",
        "tree": "59508c69b48143f22ebb5fea8c932511caa457cd",
        "files": 3,
    },
    "dual-ai-session-handoff": {
        "target": "cotend-session-handoff",
        "tree": "b5fd5ac0604e24cd842cd70c34946af1df16daa3",
        "files": 3,
    },
    "dual-ai-tooling": {
        "target": "cotend-tooling",
        "tree": "aec8d2f776962a15697700e2634b9843187aa047",
        "files": 14,
    },
    "dual-model-upgrade": {
        "target": "cotend-model-upgrade",
        "tree": "809e7f5a32943b8a60bb6d29d364bf81cf3ef008",
        "files": 7,
    },
    "grill-me": {
        "target": "grill-me",
        "tree": "70df660726ef12349a40dc0353a681c82414fe95",
        "files": 1,
    },
}
PRODUCT_SKILLS = (
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-init",
    "cotend-model-upgrade",
    "cotend-project-init",
    "cotend-semantic-alignment",
    "cotend-session-handoff",
    "cotend-tooling",
    "grill-me",
    "karpathy-guidelines",
)
SOURCE_FILE_COUNT = 94
PRODUCT_FILE_COUNT = 104
PATH_MAPPINGS = {
    (
        "dual-ai-collaboration",
        "references/private-dual-adapter.md",
    ): "references/cotend-adapter.md",
    (
        "dual-ai-project-init",
        "scripts/check_private_dual_governance_language.py",
    ): "scripts/check_cotend_governance_language.py",
}
SOURCE_OMISSIONS = {
    (
        "dual-ai-project-init",
        "scripts/test_check_private_dual_governance_language.py",
    ),
}
REQUIRED_PRODUCT_PATHS = {
    "cotend-collaboration/references/implementation-pass.md",
    "cotend-collaboration/references/verification-pass.md",
    "cotend-collaboration/references/closeout-pass.md",
    "cotend-collaboration/references/cotend-adapter.md",
    "cotend-collaboration/references/project-intelligence.md",
    "cotend-collaboration/references/adaptive-development-experience.md",
    "cotend-collaboration/references/governance-carrier-lifecycle.md",
    "cotend-collaboration/references/semantic-contract-templates.md",
    "cotend-collaboration/references/semantic-reconciliation.md",
    "cotend-collaboration/scripts/development_experience.py",
    "cotend-collaboration/scripts/governance_history.py",
    "cotend-collaboration/scripts/validate_understanding_artifacts.py",
    "cotend-project-init/references/framework-maintenance/external-reviewer-sync.md",
}
REQUIRED_MARKERS = {
    "cotend-collaboration/SKILL.md": (
        "Protocol version: `cotend-collaboration-v2.01`",
        "references/project-intelligence.md",
        "references/cotend-adapter.md",
    ),
    "cotend-project-init/SKILL.md": (
        "Protocol target: `cotend-collaboration-v2.01`",
        "upstream Dual handoff/adoption/install",
        "references/framework-maintenance/external-reviewer-sync.md",
    ),
    "cotend-collaboration/references/cotend-adapter.md": (
        "runtime_profile: full",
        "user_facing_language: en",
        "continuous_risk: medium",
        "disabled_requires_explicit_project_record",
    ),
    "cotend-collaboration/references/runtime-profiles.md": (
        "v2.01-full",
        "v2.01-A",
        "Native Implementation Pass -> Native Verification Pass",
    ),
    "cotend-collaboration/references/project-intelligence.md": (
        "full_current_project",
        "actual-byte",
        "Unknown",
    ),
    "cotend-collaboration/references/continuous-and-unattended.md": (
        "local_closeout_authorization.status: active",
        "Native Closeout Pass",
    ),
    "cotend-model-upgrade/SKILL.md": (
        "cotend-model-upgrade-v1.16",
        "cotend-collaboration-v2.01",
    ),
    "cotend-tooling/SKILL.md": (
        "intake",
        "evaluate",
        "inventory",
        "refresh",
        "retire",
    ),
}


def git_bytes(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
    ).stdout


def git_text(repo: Path, *args: str) -> str:
    return git_bytes(repo, *args).decode("utf-8").strip()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_inventory(repo: Path, source_id: str) -> list[str]:
    prefix = f"{SOURCE_ROOT}/{source_id}"
    output = git_text(
        repo,
        "ls-tree",
        "-r",
        "--name-only",
        SOURCE_COMMIT,
        "--",
        prefix,
    )
    return sorted(
        line.removeprefix(f"{prefix}/")
        for line in output.splitlines()
        if line
    )


def product_inventory() -> list[str]:
    root = ROOT / "skills"
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def manifest_digest(paths: list[str]) -> str:
    root = ROOT / "skills"
    files = {
        path: hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in paths
    }
    payload = json.dumps(
        files,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_source(upstream_repo: Path, errors: list[str]) -> None:
    try:
        if git_text(upstream_repo, "cat-file", "-t", SOURCE_COMMIT) != "commit":
            errors.append("exact source target is not a commit")
        if (
            git_text(upstream_repo, "rev-parse", f"{SOURCE_COMMIT}:{SOURCE_ROOT}")
            != SOURCE_TREE
        ):
            errors.append("exact source canonical tree drift")
        subprocess.run(
            [
                "git",
                "-C",
                str(upstream_repo),
                "merge-base",
                "--is-ancestor",
                SOURCE_BASE_COMMIT,
                SOURCE_COMMIT,
            ],
            check=True,
            capture_output=True,
        )
        range_count = int(
            git_text(
                upstream_repo,
                "rev-list",
                "--count",
                f"{SOURCE_BASE_COMMIT}..{SOURCE_COMMIT}",
            )
        )
        if range_count != 188:
            errors.append(f"exact source range count drift: {range_count}")
    except (subprocess.CalledProcessError, ValueError) as exc:
        errors.append(f"cannot resolve exact source identity: {exc}")
        return

    total = 0
    for source_id, record in SOURCE_SKILLS.items():
        try:
            tree = git_text(
                upstream_repo,
                "rev-parse",
                f"{SOURCE_COMMIT}:{SOURCE_ROOT}/{source_id}",
            )
            files = source_inventory(upstream_repo, source_id)
        except subprocess.CalledProcessError as exc:
            errors.append(f"cannot resolve source Skill {source_id}: {exc}")
            continue
        if tree != record["tree"]:
            errors.append(f"source Skill tree drift: {source_id}")
        if len(files) != record["files"]:
            errors.append(f"source Skill file count drift: {source_id}")
        total += len(files)
        target = str(record["target"])
        for relative in files:
            if (source_id, relative) in SOURCE_OMISSIONS:
                continue
            mapped = PATH_MAPPINGS.get((source_id, relative), relative)
            if not (ROOT / "skills" / target / mapped).is_file():
                errors.append(
                    f"source behavior has no CoTend carrier: {source_id}/{relative}"
                )
    if total != SOURCE_FILE_COUNT:
        errors.append(f"source Skill file total drift: {total}")


def verify_handoff(upstream_repo: Path, errors: list[str]) -> None:
    root = upstream_repo / "consumer-handoffs" / "cotend" / HANDOFF_ID
    for name, expected in HANDOFF_HASHES.items():
        path = root / name
        if not path.is_file():
            errors.append(f"handoff file missing: {name}")
        elif sha256(path) != expected:
            errors.append(f"handoff hash drift: {name}")


def verify_product(errors: list[str]) -> tuple[list[str], str]:
    skill_root = ROOT / "skills"
    actual_skills = tuple(
        sorted(path.name for path in skill_root.iterdir() if path.is_dir())
    )
    if actual_skills != PRODUCT_SKILLS:
        errors.append(
            f"product Skill inventory drift: {actual_skills!r}"
        )
    paths = product_inventory()
    if len(paths) != PRODUCT_FILE_COUNT:
        errors.append(f"product Skill file count drift: {len(paths)}")
    missing = sorted(REQUIRED_PRODUCT_PATHS - set(paths))
    if missing:
        errors.append(f"required native product paths missing: {missing}")

    for skill in PRODUCT_SKILLS:
        skill_path = skill_root / skill / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"SKILL.md missing: {skill}")
            continue
        text = skill_path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        name = None
        if len(parts) == 3 and not parts[0].strip():
            match = re.search(r"^name:\s*([^\s]+)\s*$", parts[1], re.MULTILINE)
            name = match.group(1) if match else None
        if name != skill:
            errors.append(f"Skill frontmatter name mismatch: {skill}")

    for relative, markers in REQUIRED_MARKERS.items():
        path = skill_root / relative
        if not path.is_file():
            errors.append(f"required marker file missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"required marker missing: {relative}: {marker}")

    forbidden: list[str] = []
    private_path = "private-dual-adapter"
    for path in skill_root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "trellis" in text.casefold() or private_path in text.casefold():
            forbidden.append(relative)
    if forbidden:
        errors.append(f"legacy/private carrier residue in product Skills: {forbidden}")

    catalog_path = skill_root / "cotend-tooling/references/capability-catalog.json"
    catalog = load_json(catalog_path)
    optional_records = [
        item
        for item in catalog.get("records", [])
        if isinstance(item, dict) and item.get("id") == "karpathy-guidelines"
    ]
    if len(optional_records) != 1 or (
        optional_records[0].get("adoption_disposition"),
        optional_records[0].get("runtime_state"),
        optional_records[0].get("eligible_routes"),
    ) != ("adopt_partial", "available", ["call"]):
        errors.append("optional Karpathy catalog boundary drift")

    routed_karpathy = []
    for path in skill_root.rglob("*"):
        if (
            not path.is_file()
            or "karpathy-guidelines" in path.parts
            or path.name == "framework-impact-index.json"
            or path == catalog_path
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "karpathy-guidelines" in text.casefold():
            routed_karpathy.append(path.relative_to(ROOT).as_posix())
    if routed_karpathy:
        errors.append(f"optional Karpathy companion remains routed: {routed_karpathy}")
    return paths, manifest_digest(paths)


def verify_records(paths: list[str], digest: str, errors: list[str]) -> None:
    lock = load_json(ROOT / "upstream" / "framework.lock.json")
    artifact = load_json(ROOT / "delivery" / "codex-artifact.lock.json")
    candidate = load_json(ROOT / "upstream" / "FRAMEWORK-CANDIDATE.json")
    role_map = load_json(ROOT / "upstream" / "CODEX-SKILL-ROLE-MAP.json")
    capability = load_json(ROOT / "upstream" / "CAPABILITY-IMPLEMENTATION-MAP.json")

    if (
        lock.get("status") != "adopted_verified"
        or lock.get("release_id") != SOURCE_IDENTITY
        or lock.get("framework_protocol") != "cotend-collaboration-v2.01"
        or lock.get("model_upgrade_packet_family")
        != "cotend-model-upgrade-v1.16"
        or lock.get("skill_count") != 10
        or lock.get("source_skill_count") != 9
        or lock.get("skill_file_count") != SOURCE_FILE_COUNT
    ):
        errors.append("framework lock current identity/count drift")
    anchor = lock.get("source_anchor")
    if not isinstance(anchor, dict) or (
        anchor.get("commit"),
        anchor.get("canonical_source_tree"),
    ) != (SOURCE_COMMIT, SOURCE_TREE):
        errors.append("framework lock source anchor drift")
    expected_trees = {
        source: record["tree"] for source, record in SOURCE_SKILLS.items()
    }
    if lock.get("source_skill_trees") != expected_trees:
        errors.append("framework lock source Skill tree inventory drift")
    mappings = lock.get("skill_mapping")
    if not isinstance(mappings, list) or {
        item.get("target") for item in mappings if isinstance(item, dict)
    } != set(PRODUCT_SKILLS):
        errors.append("framework lock target mapping drift")
    companions = lock.get("retained_optional_companions")
    if (
        not isinstance(companions, list)
        or len(companions) != 1
        or companions[0].get("target") != "karpathy-guidelines"
        or companions[0].get("routing") != "non_default_non_owner"
    ):
        errors.append("framework lock optional companion boundary drift")

    source = artifact.get("source")
    target = artifact.get("target")
    predecessors = artifact.get("predecessor_targets")
    if not isinstance(source, dict) or not isinstance(target, dict):
        errors.append("artifact lock sections invalid")
    else:
        if (
            source.get("release_id"),
            source.get("framework_protocol"),
        ) != (SOURCE_IDENTITY, "cotend-collaboration-v2.01"):
            errors.append("artifact source identity drift")
        if (
            target.get("artifact_id"),
            target.get("revision"),
            target.get("manifest_sha256"),
        ) != ("cotend-codex-r000017", 17, digest):
            errors.append("artifact target identity or manifest drift")
    if (
        artifact.get("skill_count"),
        artifact.get("skill_file_count"),
    ) != (10, PRODUCT_FILE_COUNT):
        errors.append("artifact product count drift")
    if (
        not isinstance(predecessors, list)
        or not predecessors
        or predecessors[0].get("artifact_id") != "cotend-codex-r000016"
        or predecessors[0].get("revision") != 16
        or predecessors[0].get("source_release_id")
        != f"exact-source:{SOURCE_BASE_COMMIT}"
        or predecessors[0].get("manifest_sha256")
        != "a7f7ece2522a5901030e19cd5944359f80c027482f66f822a2053fc5080dcfb5"
    ):
        errors.append("r16 predecessor lock drift")

    expected_status = "adopted_verified"
    for label, value in (
        ("candidate", candidate),
        ("role map", role_map),
        ("capability map", capability),
    ):
        if value.get("status") != expected_status:
            errors.append(f"{label} status is not adopted_verified")
        if value.get("source_anchor", value.get("source_release")) not in (
            SOURCE_COMMIT,
            SOURCE_IDENTITY,
        ):
            errors.append(f"{label} source anchor drift")
    if candidate.get("candidate_release") != SOURCE_IDENTITY:
        errors.append("candidate release identity drift")
    adoption = candidate.get("adoption")
    if not isinstance(adoption, dict):
        errors.append("candidate adoption record missing")
    else:
        recorded = set(adoption.get("imported_files", [])) | set(
            adoption.get("adapted_files", [])
        )
        expected = {f"skills/{path}" for path in paths}
        if recorded != expected:
            errors.append("candidate file inventory differs from product Skills")
    if role_map.get("skill_count") != 10:
        errors.append("role map product Skill count drift")
    if capability.get("capability_count") != 19:
        errors.append("capability count drift")


def verify_containing_commit(errors: list[str], *, allow_uncommitted: bool) -> None:
    if allow_uncommitted:
        return
    try:
        lock_status = git_text(
            ROOT,
            "status",
            "--porcelain",
            "--",
            "upstream/framework.lock.json",
        )
        if lock_status:
            errors.append("framework lock has uncommitted changes")
            return
        lock_commit = git_text(
            ROOT,
            "log",
            "-1",
            "--format=%H",
            "--",
            "upstream/framework.lock.json",
        )
        paths = set(
            git_text(
                ROOT,
                "show",
                "--pretty=format:",
                "--name-only",
                lock_commit,
            ).splitlines()
        )
    except subprocess.CalledProcessError as exc:
        errors.append(f"cannot resolve containing commit: {exc}")
        return
    for required in (
        "upstream/framework.lock.json",
        "upstream/FRAMEWORK-ADOPTION-LOG.md",
    ):
        if required not in paths:
            errors.append(f"containing commit does not include {required}")
    if not any(path.startswith("skills/") for path in paths):
        errors.append("containing commit does not include product Skills")


def verify(
    upstream_repo: Path,
    *,
    pre_lock: bool,
    allow_uncommitted_anchor: bool,
) -> list[str]:
    errors: list[str] = []
    verify_source(upstream_repo, errors)
    verify_handoff(upstream_repo, errors)
    paths, digest = verify_product(errors)
    if not pre_lock:
        verify_records(paths, digest, errors)
        verify_containing_commit(
            errors,
            allow_uncommitted=allow_uncommitted_anchor,
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CoTend v2.01/r17 against the exact Dual source handoff."
    )
    parser.add_argument("--upstream-repo", type=Path, required=True)
    parser.add_argument("--pre-lock", action="store_true")
    parser.add_argument("--allow-uncommitted-anchor", action="store_true")
    args = parser.parse_args()
    if args.pre_lock and args.allow_uncommitted_anchor:
        parser.error("--allow-uncommitted-anchor is final-verification only")
    errors = verify(
        args.upstream_repo.resolve(),
        pre_lock=args.pre_lock,
        allow_uncommitted_anchor=args.allow_uncommitted_anchor,
    )
    if errors:
        print("ADOPTED_SKILL_SET_VERIFICATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "ADOPTED_SKILL_SET_VERIFICATION_OK "
        f"mode={'pre_lock' if args.pre_lock else 'final'} "
        "source_skills=9 source_files=94 product_skills=10 product_files=104 "
        "capabilities=19"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
