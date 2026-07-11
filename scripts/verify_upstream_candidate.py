from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "dual-ai-collaboration-skill-share"


def git_bytes(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
    )
    return result.stdout


def git_text(repo: Path, *args: str) -> str:
    return git_bytes(repo, *args).decode("utf-8").strip()


def tagged_file(repo: Path, tag: str, relative_path: str) -> bytes:
    return git_bytes(repo, "show", f"{tag}:{PACKAGE_ROOT}/{relative_path}")


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def verify(upstream_repo: Path, candidate_path: Path, role_map_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        candidate = load_json(candidate_path)
        role_map = load_json(role_map_path)
    except (OSError, ValueError) as exc:
        return [f"cannot load candidate mapping records: {exc}"]
    release_anchor = candidate.get("release_anchor")
    if not isinstance(release_anchor, dict):
        return ["candidate release_anchor must be an object"]
    tag = release_anchor.get("tag")
    if not isinstance(tag, str):
        return ["candidate release tag is missing"]

    try:
        if git_text(upstream_repo, "cat-file", "-t", tag) != "tag":
            errors.append("release anchor is not an annotated tag object")
        tag_object = git_text(upstream_repo, "rev-parse", tag)
        release_commit = git_text(upstream_repo, "rev-parse", f"{tag}^{{commit}}")
        package_tree = git_text(upstream_repo, "rev-parse", f"{tag}:{PACKAGE_ROOT}")
    except subprocess.CalledProcessError as exc:
        return [f"cannot resolve upstream release anchor: {exc}"]

    for key, actual in (
        ("tag_object", tag_object),
        ("release_commit", release_commit),
        ("package_tree", package_tree),
    ):
        if release_anchor.get(key) != actual:
            errors.append(f"candidate release anchor mismatch: {key}")

    try:
        descriptor = json.loads(tagged_file(upstream_repo, tag, "FRAMEWORK-RELEASE.json"))
        source_registry = json.loads(
            tagged_file(upstream_repo, tag, "THIRD-PARTY-SOURCES.json")
        )
        manifest = tagged_file(upstream_repo, tag, "SHA256SUMS")
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return [f"cannot read tagged release metadata: {exc}"]
    if not isinstance(descriptor, dict) or not isinstance(source_registry, dict):
        return ["tagged release metadata must contain JSON objects"]

    if descriptor.get("release_id") != candidate.get("release_id"):
        errors.append("candidate release_id does not match tagged descriptor")
    if descriptor.get("source_framework_commit") != candidate.get("source_framework_commit"):
        errors.append("candidate source framework commit does not match descriptor")
    protocol = descriptor.get("framework_protocol")
    if not isinstance(protocol, str) or not protocol.endswith(
        f"v{candidate.get('framework_protocol_version')}"
    ):
        errors.append("candidate framework protocol version does not match descriptor")

    integrity = candidate.get("integrity")
    if not isinstance(integrity, dict):
        errors.append("candidate integrity record is missing")
    else:
        manifest_hash = hashlib.sha256(manifest).hexdigest()
        if integrity.get("manifest_sha256") != manifest_hash:
            errors.append("candidate manifest hash does not match tagged manifest")
        manifest_entries = [line for line in manifest.decode("utf-8").splitlines() if line]
        if integrity.get("manifest_entries") != len(manifest_entries):
            errors.append("candidate manifest entry count does not match tagged manifest")

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
    for platform, trees in (("codex", codex_trees), ("claude", claude_trees)):
        for skill_id, expected_tree in trees.items():
            actual_tree = git_text(
                upstream_repo,
                "rev-parse",
                f"{tag}:{PACKAGE_ROOT}/{platform}-skills/{skill_id}",
            )
            if actual_tree != expected_tree:
                errors.append(f"{platform} Skill tree mismatch: {skill_id}")

    components = source_registry.get("components")
    if not isinstance(components, list):
        return errors + ["tagged source registry components are invalid"]
    source_by_skill: dict[str, dict[str, object]] = {}
    for component in components:
        if not isinstance(component, dict):
            continue
        packaged_skill = component.get("packaged_skill")
        if isinstance(packaged_skill, str) and packaged_skill.startswith("codex/"):
            source_by_skill[packaged_skill.removeprefix("codex/")] = component

    role_entries = role_map.get("skills")
    if not isinstance(role_entries, list):
        return errors + ["role map skills are invalid"]

    required_markers = {
        "dual-ai-init": (
            "short visible entry point",
            "Load and follow `dual-ai-project-init` Auto Mode",
        ),
        "dual-ai-project-init": (
            "Default behavior is automatic",
            "dual-ai-collaboration** owns collaboration governance",
        ),
        "dual-ai-collaboration": (
            "dual-ai-collaboration** owns collaboration governance",
            "must decide whether Trellis should be active",
        ),
        "diagnose-only": (
            "Default: **read-only investigation**",
            "Do not change files",
        ),
        "dual-model-upgrade": (
            "advisor_only",
            "primary_model_reverted_or_downgraded",
            "milestone re-entry",
        ),
        "grill-me": (
            "Ask the questions one at a time",
            "replying only `1` means",
        ),
        "karpathy-guidelines": (
            "Simplicity First",
            "Surgical Changes",
            "Goal-Driven Execution",
        ),
    }

    for entry in role_entries:
        if not isinstance(entry, dict):
            errors.append("role map contains a non-object entry")
            continue
        skill_id = entry.get("source_skill_id")
        if not isinstance(skill_id, str):
            errors.append("role map entry lacks source_skill_id")
            continue
        if entry.get("source_tree") != codex_trees.get(skill_id):
            errors.append(f"role map tree does not match candidate: {skill_id}")
        source = source_by_skill.get(skill_id)
        if source is None:
            errors.append(f"tagged source registry lacks Codex Skill: {skill_id}")
        else:
            if entry.get("source_relationship") != source.get("relationship"):
                errors.append(f"role-map source relationship mismatch: {skill_id}")
            if entry.get("license") != source.get("license"):
                errors.append(f"role-map license mismatch: {skill_id}")

        try:
            skill_text = tagged_file(
                upstream_repo, tag, f"codex-skills/{skill_id}/SKILL.md"
            ).decode("utf-8")
        except (subprocess.CalledProcessError, UnicodeDecodeError) as exc:
            errors.append(f"cannot read tagged Skill {skill_id}: {exc}")
            continue
        frontmatter_parts = skill_text.split("---", 2)
        if len(frontmatter_parts) != 3:
            errors.append(f"tagged Skill frontmatter is malformed: {skill_id}")
        elif f"name: {skill_id}" not in frontmatter_parts[1]:
            errors.append(f"tagged Skill frontmatter name mismatch: {skill_id}")
        for marker in required_markers.get(skill_id, ()):
            if marker not in skill_text:
                errors.append(f"tagged Skill role marker missing: {skill_id}: {marker}")

    if (ROOT / "upstream" / "framework.lock.json").exists():
        errors.append("final framework lock exists before actual adoption")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CoTend's candidate and role map against tagged upstream Git objects."
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
        f"release={candidate['release_id']} "
        f"codex_skills={role_map['skill_count']} claude_skills=3"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
