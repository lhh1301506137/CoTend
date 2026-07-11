from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "dual-ai-collaboration-skill-share"
TAG = "dual-ai-share-2026.07.11.3"

SKILLS = {
    "dual-ai-init": {
        "target": "cotend-init",
        "tree": "cb233ade310c37e0cd038ff5752eeced92a303f0",
        "mode": "adapted",
        "files": 2,
    },
    "dual-ai-project-init": {
        "target": "cotend-project-init",
        "tree": "1f2fdd44e90f31fec310eaf78b02e48de4fed53c",
        "mode": "adapted",
        "files": 2,
    },
    "dual-ai-collaboration": {
        "target": "cotend-collaboration",
        "tree": "b75114a7e0fd2027943ed98217a0f9d581cbdae9",
        "mode": "adapted",
        "files": 19,
    },
    "diagnose-only": {
        "target": "cotend-diagnose-only",
        "tree": "88dc2e47dba438720a336c38103308aeae3d635e",
        "mode": "adapted",
        "files": 2,
    },
    "dual-model-upgrade": {
        "target": "cotend-model-upgrade",
        "tree": "dfb25bd4464e0266b665af138a5f3902b44ce281",
        "mode": "adapted",
        "files": 3,
    },
    "grill-me": {
        "target": "grill-me",
        "tree": "70df660726ef12349a40dc0353a681c82414fe95",
        "mode": "adopted",
        "files": 1,
    },
    "karpathy-guidelines": {
        "target": "karpathy-guidelines",
        "tree": "e119339197d600aa39a24fd7a95c946800c9c949",
        "mode": "adopted",
        "files": 1,
    },
}

DISPLAY_NAMES = {
    "cotend-init": "CoTend Init",
    "cotend-project-init": "CoTend Project Init",
    "cotend-collaboration": "CoTend Collaboration",
    "cotend-diagnose-only": "CoTend Diagnose Only",
    "cotend-model-upgrade": "CoTend Model Upgrade",
}

REQUIRED_MARKERS = {
    "cotend-init": (
        "Load and follow `cotend-project-init` Auto Mode",
        ".codex\\skills\\cotend-project-init\\SKILL.md",
        ".codex/skills/cotend-project-init/SKILL.md",
    ),
    "cotend-project-init": (
        "Protocol target: `cotend-collaboration-v1.52`",
        "**cotend-collaboration** owns collaboration governance",
        "`cotend-diagnose-only` when the user wants root cause analysis",
        "`karpathy-guidelines` for coding behavior",
        "`grill-me` when requirements are fuzzy",
        "cotend-collaboration/references/goal-completion.md",
        "cotend-collaboration/references/release-hardening.md",
        "cotend-collaboration/references/code-context-harness.md",
    ),
    "cotend-collaboration": (
        "Protocol version: `cotend-collaboration-v1.52`",
        "**cotend-collaboration** owns collaboration governance",
        "load `cotend-project-init` and use its Auto Mode",
        "use `$cotend-diagnose-only`",
    ),
    "cotend-diagnose-only": (
        "Default: **read-only investigation**",
        "Do not change files",
    ),
    "cotend-model-upgrade": (
        "packet_version: cotend-model-upgrade-v1.7",
        "cotend-collaboration/references/authority-and-triggers.md",
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

LEGACY_ALLOWLIST = {
    "codex-skills/cotend-init/SKILL.md": ("legacy",),
    "codex-skills/cotend-project-init/SKILL.md": ("legacy", "Old dual-ai"),
    "codex-skills/cotend-collaboration/SKILL.md": ("legacy",),
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


def tagged_file(repo: Path, relative_path: str) -> bytes:
    return git_bytes(repo, "show", f"{TAG}:{PACKAGE_ROOT}/{relative_path}")


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def tagged_inventory(repo: Path, source_id: str) -> list[str]:
    prefix = f"{PACKAGE_ROOT}/codex-skills/{source_id}"
    paths = git_text(
        repo,
        "ls-tree",
        "-r",
        "--name-only",
        TAG,
        "--",
        prefix,
    ).splitlines()
    return sorted(path.removeprefix(f"{prefix}/") for path in paths if path)


def target_inventory(target_dir: Path) -> list[str]:
    return sorted(
        path.relative_to(target_dir).as_posix()
        for path in target_dir.rglob("*")
        if path.is_file()
    )


def frontmatter(skill_text: str) -> tuple[str | None, set[str]]:
    parts = skill_text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return None, set()
    block = parts[1]
    name_match = re.search(r"^name:\s*([^\s]+)\s*$", block, re.MULTILINE)
    keys = set(re.findall(r"^([A-Za-z][A-Za-z0-9_-]*):", block, re.MULTILINE))
    return (name_match.group(1) if name_match else None), keys


def metadata_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*([^\s#]+)", text, re.MULTILINE)
    return match.group(1) if match else None


def verify_source_topology(upstream_repo: Path, errors: list[str]) -> None:
    for source_id, record in SKILLS.items():
        target_id = str(record["target"])
        target_dir = ROOT / "codex-skills" / target_id
        if not target_dir.is_dir():
            errors.append(f"target Skill directory is missing: {target_id}")
            continue
        try:
            source_tree = git_text(
                upstream_repo,
                "rev-parse",
                f"{TAG}:{PACKAGE_ROOT}/codex-skills/{source_id}",
            )
            source_files = tagged_inventory(upstream_repo, source_id)
        except subprocess.CalledProcessError as exc:
            errors.append(f"cannot resolve tagged source Skill {source_id}: {exc}")
            continue
        if source_tree != record["tree"]:
            errors.append(f"tagged source tree drift: {source_id}")
        target_files = target_inventory(target_dir)
        if source_files != target_files:
            errors.append(
                f"source/target file topology drift: {source_id} -> {target_id}"
            )
        if len(target_files) != record["files"]:
            errors.append(f"target file count drift: {target_id}")


def verify_skill_metadata(errors: list[str]) -> None:
    for record in SKILLS.values():
        target_id = str(record["target"])
        skill_path = ROOT / "codex-skills" / target_id / "SKILL.md"
        if not skill_path.is_file():
            continue
        text = skill_path.read_text(encoding="utf-8")
        name, keys = frontmatter(text)
        if name != target_id:
            errors.append(f"Skill frontmatter name mismatch: {target_id}")
        if "description" not in keys:
            errors.append(f"Skill frontmatter description is missing: {target_id}")
        if record["mode"] == "adapted" and keys != {"name", "description"}:
            errors.append(
                f"adapted Skill frontmatter has unsupported keys: {target_id}"
            )
        for marker in REQUIRED_MARKERS[target_id]:
            if marker not in text:
                errors.append(f"Skill behavior marker missing: {target_id}: {marker}")

        agent_path = skill_path.parent / "agents" / "openai.yaml"
        if target_id in DISPLAY_NAMES:
            if not agent_path.is_file():
                errors.append(f"agents/openai.yaml is missing: {target_id}")
                continue
            agent_text = agent_path.read_text(encoding="utf-8")
            display = re.search(
                r'^\s*display_name:\s*"([^"]+)"', agent_text, re.MULTILINE
            )
            short = re.search(
                r'^\s*short_description:\s*"([^"]+)"', agent_text, re.MULTILINE
            )
            prompt = re.search(
                r'^\s*default_prompt:\s*"(.+)"\s*$', agent_text, re.MULTILINE
            )
            if display is None or display.group(1) != DISPLAY_NAMES[target_id]:
                errors.append(f"agent display_name mismatch: {target_id}")
            if short is None or not 25 <= len(short.group(1)) <= 64:
                errors.append(f"agent short_description length mismatch: {target_id}")
            if prompt is None or f"${target_id}" not in prompt.group(1):
                errors.append(
                    f"agent default_prompt does not invoke Skill: {target_id}"
                )
        elif agent_path.exists():
            errors.append(
                f"directly adopted third-party Skill gained agent metadata: {target_id}"
            )


def verify_references(errors: list[str]) -> None:
    collaboration = ROOT / "codex-skills" / "cotend-collaboration"
    skill_path = collaboration / "SKILL.md"
    references_dir = collaboration / "references"
    if not skill_path.is_file() or not references_dir.is_dir():
        errors.append("cotend-collaboration Skill or references directory is missing")
        return
    reference_names = {path.name for path in references_dir.glob("*.md")}
    skill_text = skill_path.read_text(encoding="utf-8")
    for name in reference_names:
        if f"references/{name}" not in skill_text:
            errors.append(
                f"collaboration reference is not discoverable from SKILL.md: {name}"
            )
    if len(reference_names) != 17:
        errors.append("cotend-collaboration reference count must be 17")
    packet = (
        ROOT
        / "codex-skills"
        / "cotend-model-upgrade"
        / "references"
        / "packet-templates.md"
    )
    if not packet.is_file():
        errors.append("cotend-model-upgrade packet templates are missing")


def verify_legacy_brand_boundary(errors: list[str]) -> None:
    private_patterns = (
        re.compile(r"\bstartskills\b", re.IGNORECASE),
        re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    )
    maintainer_residue_patterns = (
        re.compile(r"\bthis user's\b", re.IGNORECASE),
        re.compile(r"\bon this machine\b", re.IGNORECASE),
        re.compile(r"codegraph-mcp\.ps1", re.IGNORECASE),
        re.compile(r"\bDEC-\d{3}\b"),
        re.compile(r"\bv1\.50\b", re.IGNORECASE),
        re.compile(r"skills-backup|SKILLS-INDEX|command-backups", re.IGNORECASE),
        re.compile(
            r"report in Chinese|written in Chinese|must be Chinese", re.IGNORECASE
        ),
        re.compile(r"^\s*language:\s*zh-CN\s*$", re.IGNORECASE),
    )
    for path in (ROOT / "codex-skills").rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(text.splitlines(), start=1):
            if re.search(r"dual-ai", line, re.IGNORECASE):
                allowed = LEGACY_ALLOWLIST.get(relative, ())
                if not any(fragment.lower() in line.lower() for fragment in allowed):
                    errors.append(
                        f"legacy brand outside allowlist: {relative}:{number}"
                    )
            if re.search(r"Dual AI|Dual Model", line):
                errors.append(f"legacy display brand remains: {relative}:{number}")
            if any(pattern.search(line) for pattern in private_patterns):
                errors.append(
                    f"private path or identifier in Skill: {relative}:{number}"
                )
            if any(pattern.search(line) for pattern in maintainer_residue_patterns):
                errors.append(
                    f"private maintainer residue in Skill: {relative}:{number}"
                )


def verify_third_party(upstream_repo: Path, errors: list[str]) -> None:
    for skill_id in ("grill-me", "karpathy-guidelines"):
        target = ROOT / "codex-skills" / skill_id / "SKILL.md"
        try:
            expected = tagged_file(upstream_repo, f"codex-skills/{skill_id}/SKILL.md")
        except subprocess.CalledProcessError as exc:
            errors.append(f"cannot read tagged third-party Skill {skill_id}: {exc}")
            continue
        if not target.is_file() or target.read_bytes() != expected:
            errors.append(f"third-party Skill is not byte-identical: {skill_id}")
        license_name = f"{skill_id}-MIT.txt"
        license_path = ROOT / "THIRD-PARTY-LICENSES" / license_name
        try:
            expected_license = tagged_file(
                upstream_repo, f"THIRD-PARTY-LICENSES/{license_name}"
            )
        except subprocess.CalledProcessError as exc:
            errors.append(
                f"cannot read tagged third-party license {license_name}: {exc}"
            )
            continue
        if not license_path.is_file() or license_path.read_bytes() != expected_license:
            errors.append(f"third-party license is not byte-identical: {license_name}")

    try:
        registry = load_json(ROOT / "THIRD-PARTY-SOURCES.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load third-party source registry: {exc}")
        return
    components = registry.get("components")
    if not isinstance(components, list) or len(components) != 2:
        errors.append("third-party source registry must contain exactly two components")
        return
    by_name = {
        item.get("component"): item for item in components if isinstance(item, dict)
    }
    for skill_id in ("grill-me", "karpathy-guidelines"):
        item = by_name.get(skill_id)
        if item is None:
            errors.append(f"third-party registry entry is missing: {skill_id}")
            continue
        if item.get("source_tree") != SKILLS[skill_id]["tree"]:
            errors.append(f"third-party registry source tree drift: {skill_id}")
        if item.get("license") != "MIT":
            errors.append(f"third-party registry license drift: {skill_id}")
        if item.get("content_policy") != "byte_identical_to_tagged_release":
            errors.append(f"third-party registry content policy drift: {skill_id}")
        if item.get("line_ending_policy") != "text_eol_lf":
            errors.append(f"third-party registry line-ending policy drift: {skill_id}")
    attributes_path = ROOT / ".gitattributes"
    if not attributes_path.is_file():
        errors.append(".gitattributes is missing for protected third-party files")
    else:
        attributes = attributes_path.read_text(encoding="utf-8")
        for protected_path in (
            "/codex-skills/grill-me/SKILL.md",
            "/codex-skills/karpathy-guidelines/SKILL.md",
            "/THIRD-PARTY-LICENSES/grill-me-MIT.txt",
            "/THIRD-PARTY-LICENSES/karpathy-guidelines-MIT.txt",
        ):
            if f"{protected_path} text eol=lf" not in attributes:
                errors.append(
                    f"protected third-party LF policy is missing: {protected_path}"
                )
    notice_path = ROOT / "THIRD-PARTY-NOTICES.md"
    if not notice_path.is_file():
        errors.append("third-party notice is missing")
        return
    notice = notice_path.read_text(encoding="utf-8")
    for marker in ("## grill-me", "## karpathy-guidelines", "does not relicense"):
        if marker not in notice:
            errors.append(f"third-party notice marker is missing: {marker}")
    cotend_notice = ROOT / "NOTICE"
    if not cotend_notice.is_file() or not cotend_notice.read_text(
        encoding="utf-8"
    ).startswith("CoTend\n"):
        errors.append("NOTICE does not identify CoTend")


def verify_capability_map(errors: list[str], final: bool) -> None:
    try:
        mapping = load_json(ROOT / "upstream" / "CAPABILITY-IMPLEMENTATION-MAP.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load capability implementation map: {exc}")
        return
    expected_state = "adopted_verified" if final else "implementation_in_progress"
    if mapping.get("status") != expected_state:
        errors.append("capability implementation map status mismatch")
    capabilities = mapping.get("capabilities")
    if not isinstance(capabilities, list):
        errors.append("capability implementation map entries are invalid")
        return
    by_id = {
        item.get("capability_id"): item
        for item in capabilities
        if isinstance(item, dict)
    }
    expected_ids = {f"C{number:02d}" for number in range(1, 20)}
    if set(by_id) != expected_ids:
        errors.append("capability implementation map must contain C01-C19")
        return
    for capability_id, item in by_id.items():
        if item.get("upstream_productization_trace") != "mapped":
            errors.append(f"capability trace is not mapped: {capability_id}")
        mode = item.get("implementation_mode")
        if mode not in {"platform_adaptation", "mixed"}:
            errors.append(f"capability implementation mode is invalid: {capability_id}")
        expected_coverage = "mapped_partial" if capability_id == "C16" else "mapped"
        if item.get("coverage_status") != expected_coverage:
            errors.append(f"capability coverage status mismatch: {capability_id}")
        if capability_id == "C16" and not item.get("deferred_gap"):
            errors.append("C16 must record the deferred live-delivery gap")
        owners = item.get("owners")
        if not isinstance(owners, list) or not owners:
            errors.append(f"capability owners are missing: {capability_id}")
        else:
            for owner in owners:
                if not isinstance(owner, str) or not (ROOT / owner).is_file():
                    errors.append(
                        f"capability owner path is invalid: {capability_id}: {owner}"
                    )
        spec_path = next(
            (ROOT / "docs" / "behavior-specs").glob(f"{capability_id}-*.md"), None
        )
        if spec_path is None:
            errors.append(f"behavior spec is missing: {capability_id}")
            continue
        spec_text = spec_path.read_text(encoding="utf-8")
        if metadata_value(spec_text, "upstream_productization_trace") != "mapped":
            errors.append(f"behavior spec trace mismatch: {capability_id}")
        if metadata_value(spec_text, "implementation_mode") != mode:
            errors.append(
                f"behavior spec implementation mode mismatch: {capability_id}"
            )


def verify_final_records(errors: list[str], allow_uncommitted_anchor: bool) -> None:
    try:
        lock = load_json(ROOT / "upstream" / "framework.lock.json")
        candidate = load_json(ROOT / "upstream" / "FRAMEWORK-CANDIDATE.json")
        role_map = load_json(ROOT / "upstream" / "CODEX-SKILL-ROLE-MAP.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load final adoption records: {exc}")
        return
    expected_lock = {
        "schema": "cotend.framework-lock",
        "release_id": "2026.07.11.3",
        "framework_protocol": "cotend-collaboration-v1.52",
        "model_upgrade_packet_family": "cotend-model-upgrade-v1.7",
        "skill_count": 7,
        "capability_map": "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        "adoption_record": (
            "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
        ),
    }
    for key, expected in expected_lock.items():
        if lock.get(key) != expected:
            errors.append(f"framework lock mismatch: {key}")
    expected_source_release = {
        "tag": TAG,
        "tag_object": "cef8add414a6d9704d3f58785a128bc56f44b263",
        "release_commit": "71e45d9ebeff4d9d61c180711c25267b9fe31549",
        "source_framework_commit": "5496073e19e239ef19eb055f2b470185fab25d3a",
        "package_tree": "a70231e0445d9795a00212e8e6c53c149bfbc431",
        "manifest_sha256": (
            "919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006"
        ),
    }
    if lock.get("status") != "adopted_verified":
        errors.append("framework lock status is not adopted_verified")
    if lock.get("source_release") != expected_source_release:
        errors.append("framework lock source release drift")
    if (
        lock.get("source_carrier") != "codex-skills/"
        or lock.get("skill_file_count") != 30
    ):
        errors.append("framework lock source carrier or file count drift")
    expected_trees = {source_id: record["tree"] for source_id, record in SKILLS.items()}
    if lock.get("source_skill_trees") != expected_trees:
        errors.append("framework lock source Skill tree inventory drift")
    mappings = lock.get("skill_mapping")
    if not isinstance(mappings, list):
        errors.append("framework lock Skill mapping is invalid")
    else:
        by_source = {
            item.get("source"): item for item in mappings if isinstance(item, dict)
        }
        if len(mappings) != 7 or len(by_source) != 7 or set(by_source) != set(SKILLS):
            errors.append("framework lock must map exactly seven source Skills")
        for source_id, record in SKILLS.items():
            item = by_source.get(source_id)
            if item is None:
                continue
            expected_disposition = (
                "adapted" if record["mode"] == "adapted" else "adopted"
            )
            expected_mode = (
                "rename_only"
                if source_id == "dual-ai-init"
                else "direct_adoption"
                if record["mode"] == "adopted"
                else "platform_adaptation"
            )
            if (
                item.get("target"),
                item.get("disposition"),
                item.get("implementation_mode"),
            ) != (record["target"], expected_disposition, expected_mode):
                errors.append(f"framework lock Skill mapping drift: {source_id}")
    boundaries = lock.get("delivery_boundaries")
    if boundaries != {
        "repository_source_adopted": True,
        "live_install_performed": False,
        "plugin_or_marketplace_carrier": "deferred",
        "claude_carrier": "deferred",
        "push_release_or_publish": "not_performed",
    }:
        errors.append("framework lock delivery boundaries drift")
    for forbidden_key in (
        "adoption_commit",
        "resulting_commit",
        "containing_commit_hash",
    ):
        if forbidden_key in lock:
            errors.append(
                f"framework lock embeds a forbidden self hash: {forbidden_key}"
            )
    anchor = lock.get("adoption_anchor")
    if anchor != {"type": "containing_commit", "path": "upstream/framework.lock.json"}:
        errors.append("framework lock containing-commit anchor mismatch")
    if (
        candidate.get("status") != "adopted_verified"
        or candidate.get("candidate_only") is not False
    ):
        errors.append("framework candidate record is not finalized as adopted")
    candidate_adoption = candidate.get("adoption")
    if (
        not isinstance(candidate_adoption, dict)
        or candidate_adoption.get("state") != "adopted"
    ):
        errors.append("framework candidate adoption state is not adopted")
    else:
        imported = candidate_adoption.get("imported_files")
        adapted = candidate_adoption.get("adapted_files")
        if not isinstance(imported, list) or not isinstance(adapted, list):
            errors.append("framework candidate file-level inventory is invalid")
        else:
            recorded = set(imported) | set(adapted)
            actual = {
                path.relative_to(ROOT).as_posix()
                for path in (ROOT / "codex-skills").rglob("*")
                if path.is_file()
            }
            if (
                len(imported) != len(set(imported))
                or len(adapted) != len(set(adapted))
                or set(imported) & set(adapted)
                or recorded != actual
                or len(actual) != 30
            ):
                errors.append(
                    "framework candidate inventory does not equal the 30 Skill files"
                )
        if candidate_adoption.get("final_framework_lock_exists") is not True:
            errors.append("framework candidate does not record the final lock")
        if candidate_adoption.get("required_before_lock") != []:
            errors.append(
                "framework candidate retains unresolved pre-lock requirements"
            )
    if role_map.get("status") != "adopted_verified":
        errors.append("Codex role map is not finalized as adopted")
    role_adoption = role_map.get("adoption")
    if not isinstance(role_adoption, dict) or role_adoption.get("state") != "adopted":
        errors.append("Codex role-map adoption state is not adopted")
    else:
        if role_adoption.get("live_install_performed") is not False:
            errors.append("Codex role map incorrectly claims a live install")
        if role_adoption.get("final_framework_lock_exists") is not True:
            errors.append("Codex role map does not record the final lock")
    if role_map.get("public_interface_authority") != (
        "codex_skill_source_set_adopted_live_delivery_pending"
    ):
        errors.append("Codex role map interface authority drift")
    entries = role_map.get("skills")
    if not isinstance(entries, list):
        errors.append("Codex role map Skill entries are invalid")
    else:
        by_source = {
            item.get("source_skill_id"): item
            for item in entries
            if isinstance(item, dict)
        }
        if len(entries) != 7 or len(by_source) != 7 or set(by_source) != set(SKILLS):
            errors.append("Codex role map must contain exactly seven source Skills")
        for source_id, record in SKILLS.items():
            item = by_source.get(source_id)
            if item is None:
                errors.append(f"Codex role map Skill is missing: {source_id}")
                continue
            expected_disposition = (
                "adapted" if record["mode"] == "adapted" else "adopted"
            )
            expected_mode = (
                "rename_only"
                if source_id == "dual-ai-init"
                else "direct_adoption"
                if record["mode"] == "adopted"
                else "platform_adaptation"
            )
            if (
                item.get("target_skill_id"),
                item.get("adoption_status"),
                item.get("implementation_mode"),
            ) != (record["target"], expected_disposition, expected_mode):
                errors.append(f"Codex role map target mapping drift: {source_id}")
    adoption_log = ROOT / "upstream" / "FRAMEWORK-ADOPTION-LOG.md"
    if not adoption_log.is_file():
        errors.append("framework adoption log is missing")
    else:
        log_text = adoption_log.read_text(encoding="utf-8")
        for marker in (
            "## release-2026-07-11-3-initial-adoption",
            "status: adopted_verified",
            "resulting_CoTend_commit: containing_commit",
        ):
            if marker not in log_text:
                errors.append(f"framework adoption log marker is missing: {marker}")

    if allow_uncommitted_anchor:
        return
    try:
        head = git_text(ROOT, "rev-parse", "HEAD")
        lock_status = git_text(
            ROOT,
            "status",
            "--porcelain",
            "--",
            "upstream/framework.lock.json",
        )
        lock_commit = git_text(
            ROOT,
            "log",
            "-1",
            "--format=%H",
            "--",
            "upstream/framework.lock.json",
        )
        changed_paths = set(
            git_text(
                ROOT,
                "show",
                "--pretty=format:",
                "--name-only",
                lock_commit,
            ).splitlines()
        )
    except subprocess.CalledProcessError as exc:
        errors.append(f"cannot resolve containing-commit anchor: {exc}")
        return
    if lock_status:
        errors.append("framework lock has uncommitted changes")
    try:
        git_text(ROOT, "merge-base", "--is-ancestor", lock_commit, head)
    except subprocess.CalledProcessError:
        errors.append("framework lock containing commit is not an ancestor of HEAD")
    for path in (
        "upstream/framework.lock.json",
        "upstream/FRAMEWORK-ADOPTION-LOG.md",
    ):
        if path not in changed_paths:
            errors.append(f"containing adoption commit does not change {path}")
    if not any(path.startswith("codex-skills/") for path in changed_paths):
        errors.append(
            "containing adoption commit does not change the adopted Skill set"
        )


def verify(
    upstream_repo: Path,
    *,
    pre_lock: bool,
    allow_uncommitted_anchor: bool,
) -> list[str]:
    errors: list[str] = []
    try:
        if git_text(upstream_repo, "cat-file", "-t", TAG) != "tag":
            errors.append("source release anchor is not an annotated tag")
    except subprocess.CalledProcessError as exc:
        return [f"cannot resolve source release tag: {exc}"]
    verify_source_topology(upstream_repo, errors)
    verify_skill_metadata(errors)
    verify_references(errors)
    verify_legacy_brand_boundary(errors)
    verify_third_party(upstream_repo, errors)
    verify_capability_map(errors, final=not pre_lock)
    lock_path = ROOT / "upstream" / "framework.lock.json"
    if pre_lock:
        if lock_path.exists():
            errors.append("framework lock exists during pre-lock verification")
    else:
        verify_final_records(errors, allow_uncommitted_anchor)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CoTend's adopted Codex Skill set against tagged upstream Git objects."
    )
    parser.add_argument("--upstream-repo", type=Path, required=True)
    parser.add_argument("--pre-lock", action="store_true")
    parser.add_argument("--allow-uncommitted-anchor", action="store_true")
    args = parser.parse_args()
    if args.pre_lock and args.allow_uncommitted_anchor:
        parser.error("--allow-uncommitted-anchor is only valid for final verification")
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
        "skills=7 files=30 capabilities=19"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
