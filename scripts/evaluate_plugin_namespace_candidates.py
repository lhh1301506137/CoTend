from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

import verify_isolated_codex_plugin as base


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = (
    ROOT / ".private-provenance" / "L32-plugin-namespace-evaluation"
)
PLUGIN_ID = "cotend"
SHORT_NAME_MAP = {
    "cotend-collaboration": "collaboration",
    "cotend-diagnose-only": "diagnose-only",
    "cotend-init": "init",
    "cotend-model-upgrade": "model-upgrade",
    "cotend-project-init": "project-init",
}
USER_OWNED_SKILLS = tuple(SHORT_NAME_MAP)
COMPANION_SKILLS = tuple(
    skill for skill in base.EXPECTED_SKILLS if skill not in SHORT_NAME_MAP
)
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".toml", ".txt", ".py"}
NOT_RUN = (
    "desktop_search_render_sort_and_truncation",
    "natural_language_or_implicit_invocation",
    "model_mediated_cross_skill_delegation",
    "real_user_or_real_project_installation",
    "cachebuster_update_enable_disable_or_new_thread_refresh",
    "production_identity_version_namespace_or_package",
    "public_submission_release_or_publish",
)
VOLATILE_CONTAINER_LABELS = {
    "user_codex_root",
    "configured_codex_root",
}


class NamespaceEvaluationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    root_name: str
    marketplace: str
    version: str
    short_names: bool

    @property
    def selector(self) -> str:
        return f"{PLUGIN_ID}@{self.marketplace}"


CANDIDATES = (
    Candidate(
        candidate_id="N1-preserve",
        root_name="N1-preserve",
        marketplace="cotend-namespace-preserve-local",
        version="0.0.0-dev.2+codex.namespace-preserve",
        short_names=False,
    ),
    Candidate(
        candidate_id="N2-short",
        root_name="N2-short",
        marketplace="cotend-namespace-short-local",
        version="0.0.0-dev.2+codex.namespace-short",
        short_names=True,
    ),
)


def protected_product_state(
    snapshot: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    source = snapshot if snapshot is not None else base.protected_user_snapshot()
    return {
        label: metadata
        for label, metadata in source.items()
        if label not in VOLATILE_CONTAINER_LABELS
    }


def assert_protected_product_state_unchanged(
    expected: dict[str, dict[str, Any]],
) -> None:
    before = protected_product_state(expected)
    after = protected_product_state()
    if before != after:
        changed = sorted(
            label
            for label in before.keys() | after.keys()
            if before.get(label) != after.get(label)
        )
        raise NamespaceEvaluationError(
            "protected config/auth/Plugin/Skill metadata changed: "
            + ", ".join(changed)
        )


def protected_boundary_summary(
    expected: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    actual = base.protected_user_snapshot()
    assert_protected_product_state_unchanged(expected)
    observed_container_changes = sorted(
        label
        for label in VOLATILE_CONTAINER_LABELS
        if label in expected or label in actual
        if expected.get(label) != actual.get(label)
    )
    return {
        "config_auth_plugin_skill_and_agents_metadata_unchanged": True,
        "volatile_container_labels_excluded_from_unchanged_claim": sorted(
            label
            for label in VOLATILE_CONTAINER_LABELS
            if label in expected or label in actual
        ),
        "observed_volatile_container_changes": observed_container_changes,
        "container_metadata_claim": "not_used_as_product_state_boundary",
    }


def target_skill_name(source_name: str, *, short_names: bool) -> str:
    if short_names:
        return SHORT_NAME_MAP.get(source_name, source_name)
    return source_name


def source_skill_name(target_name: str, *, short_names: bool) -> str:
    if not short_names:
        return target_name
    inverse = {target: source for source, target in SHORT_NAME_MAP.items()}
    return inverse.get(target_name, target_name)


def plugin_manifest(candidate: Candidate) -> dict[str, Any]:
    label = "Short-name" if candidate.short_names else "Preserve-name"
    return {
        "name": PLUGIN_ID,
        "version": candidate.version,
        "description": f"{label} namespace evaluation fixture for CoTend Skills.",
        "author": {"name": "CoTend contributors"},
        "homepage": "https://github.com/lhh1301506137/CoTend",
        "repository": "https://github.com/lhh1301506137/CoTend",
        "license": "Apache-2.0",
        "keywords": ["ai-development", "namespace-evaluation", "skills"],
        "skills": "./skills/",
        "interface": {
            "displayName": f"CoTend Namespace {label} Fixture",
            "shortDescription": f"{label} Plugin namespace evaluation",
            "longDescription": (
                "Disposable local package for comparing CoTend Plugin canonical "
                "names, interface metadata, coexistence, and migration cost."
            ),
            "developerName": "CoTend contributors",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": ["Initialize or resume this project with CoTend."],
        },
    }


def marketplace_manifest(candidate: Candidate) -> dict[str, Any]:
    return {
        "name": candidate.marketplace,
        "interface": {"displayName": f"CoTend {candidate.candidate_id} Local"},
        "plugins": [
            {
                "name": PLUGIN_ID,
                "source": {"source": "local", "path": f"./plugins/{PLUGIN_ID}"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        ],
    }


def classify_identifier_occurrence(
    relative_path: str,
    line: str,
    identifier: str,
) -> str:
    stripped = line.strip()
    if relative_path.endswith("/SKILL.md") or relative_path == "SKILL.md":
        if re.fullmatch(rf"name:\s*{re.escape(identifier)}", stripped):
            return "frontmatter_name"
    if f"${identifier}" in line:
        if relative_path.endswith("agents/openai.yaml") and re.search(
            rf"default_prompt:.*?Use \${re.escape(identifier)}(?:\s|\b)",
            line,
        ):
            return "agent_self_prompt"
        return "explicit_invocation"
    if re.search(
        rf"(?:skills[\\/]|\.codex[\\/]skills[\\/]|\.agents[\\/]skills[\\/])"
        rf"{re.escape(identifier)}(?:[\\/]|\b)",
        line,
        re.IGNORECASE,
    ):
        return "fallback_path"
    if re.search(rf"{re.escape(identifier)}-v\d", line):
        return "protocol_or_version"
    if re.search(rf"{re.escape(identifier)}/references(?:/|\b)", line):
        return "reference_path"
    return "plain_reference"


def identifier_inventory(root: Path, identifiers: tuple[str, ...]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for identifier in identifiers:
                for _ in re.finditer(rf"(?<![a-z0-9-]){re.escape(identifier)}", line):
                    records.append(
                        {
                            "path": relative,
                            "line": line_number,
                            "identifier": identifier,
                            "category": classify_identifier_occurrence(
                                relative, line, identifier
                            ),
                        }
                    )
    by_identifier = {
        identifier: sum(1 for item in records if item["identifier"] == identifier)
        for identifier in identifiers
    }
    categories = sorted({item["category"] for item in records})
    by_category = {
        category: sum(1 for item in records if item["category"] == category)
        for category in categories
    }
    return {
        "occurrences": len(records),
        "files": len({item["path"] for item in records}),
        "by_identifier": by_identifier,
        "by_category": by_category,
        "records": records,
    }


def replace_exact_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise NamespaceEvaluationError(
            f"{label} expected one exact replacement, found {count}"
        )
    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
        newline="\n",
    )


def scaffold_candidate(
    candidate_root: Path,
    candidate: Candidate,
    env: dict[str, str],
) -> None:
    marketplace_root = candidate_root / "source-marketplace"
    plugin_parent = marketplace_root / "plugins"
    marketplace_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    scaffold = base.plugin_creator_script("create_basic_plugin.py")
    completed = base.run_process(
        [
            sys.executable,
            str(scaffold),
            PLUGIN_ID,
            "--path",
            str(plugin_parent),
            "--with-skills",
            "--with-marketplace",
            "--marketplace-path",
            str(marketplace_path),
            "--marketplace-name",
            candidate.marketplace,
            "--category",
            "Developer Tools",
        ],
        env=env,
        cwd=candidate_root,
    )
    if completed.returncode != 0:
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: official scaffold failed: "
            f"{completed.stderr[-300:]}"
        )


def materialize_candidate_payload(
    candidate_root: Path,
    candidate: Candidate,
) -> dict[str, Any]:
    candidate_root = base.guarded_fixture(candidate_root)
    base.validate_repository_source_boundary()
    marketplace_root = candidate_root / "source-marketplace"
    plugin_root = marketplace_root / "plugins" / PLUGIN_ID
    marketplace_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    base.write_json(plugin_root / ".codex-plugin" / "plugin.json", plugin_manifest(candidate))
    base.write_json(marketplace_path, marketplace_manifest(candidate))
    skills_root = plugin_root / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    transform_records: list[dict[str, str]] = []
    for source_name in base.EXPECTED_SKILLS:
        target_name = target_skill_name(
            source_name, short_names=candidate.short_names
        )
        target_root = skills_root / target_name
        shutil.copytree(base.SOURCE_SKILLS_ROOT / source_name, target_root)
        if source_name != target_name:
            skill_file = target_root / "SKILL.md"
            replace_exact_once(
                skill_file,
                f"name: {source_name}",
                f"name: {target_name}",
                f"{source_name} frontmatter",
            )
            transform_records.append(
                {
                    "source": f"{source_name}/SKILL.md",
                    "target": f"{target_name}/SKILL.md",
                    "change": "frontmatter_name",
                }
            )
            agent_file = target_root / "agents" / "openai.yaml"
            replace_exact_once(
                agent_file,
                f"Use ${source_name}",
                f"Use ${PLUGIN_ID}:{target_name}",
                f"{source_name} agent self prompt",
            )
            transform_records.append(
                {
                    "source": f"{source_name}/agents/openai.yaml",
                    "target": f"{target_name}/agents/openai.yaml",
                    "change": "agent_self_prompt",
                }
            )
    for relative, source in base.PACKAGE_SUPPORT_FILES.items():
        target = plugin_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    empty_project = candidate_root / "project-empty"
    empty_project.mkdir(parents=True, exist_ok=True)
    (empty_project / "README.md").write_text(
        f"# {candidate.candidate_id} empty project\n", encoding="utf-8"
    )
    coexist_project = candidate_root / "project-with-standalone-skills"
    coexist_project.mkdir(parents=True, exist_ok=True)
    (coexist_project / "README.md").write_text(
        f"# {candidate.candidate_id} coexistence project\n", encoding="utf-8"
    )
    standalone_root = coexist_project / ".agents" / "skills"
    for skill in base.EXPECTED_SKILLS:
        shutil.copytree(base.SOURCE_SKILLS_ROOT / skill, standalone_root / skill)
    (candidate_root / "evidence" / "commands").mkdir(parents=True, exist_ok=True)
    return {
        "marketplace_root": marketplace_root,
        "plugin_root": plugin_root,
        "empty_project": empty_project,
        "coexist_project": coexist_project,
        "transforms": transform_records,
    }


def mapped_source_comparison(
    plugin_root: Path,
    candidate: Candidate,
) -> dict[str, Any]:
    source_manifest = base.file_manifest(base.SOURCE_SKILLS_ROOT)
    target_manifest = base.file_manifest(plugin_root / "skills")
    mapped: dict[str, str] = {}
    moved_paths: list[dict[str, str]] = []
    for source_relative, digest in source_manifest.items():
        source_skill, separator, tail = source_relative.partition("/")
        target_skill = target_skill_name(
            source_skill, short_names=candidate.short_names
        )
        target_relative = target_skill + (separator + tail if separator else "")
        mapped[target_relative] = digest
        if target_relative != source_relative:
            moved_paths.append(
                {"source": source_relative, "target": target_relative}
            )
    if set(mapped) != set(target_manifest):
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: mapped Skill topology mismatch"
        )
    byte_changes = sorted(
        path for path, digest in target_manifest.items() if mapped[path] != digest
    )
    return {
        "source_files": len(source_manifest),
        "target_files": len(target_manifest),
        "moved_path_count": len(moved_paths),
        "moved_paths": moved_paths,
        "byte_changed_file_count": len(byte_changes),
        "byte_changed_files": byte_changes,
        "byte_identical": not moved_paths and not byte_changes,
    }


def verify_candidate_static(
    candidate_root: Path,
    candidate: Candidate,
    *,
    env: dict[str, str] | None,
    run_official: bool = True,
) -> dict[str, Any]:
    candidate_root = base.guarded_fixture(candidate_root)
    base.reject_symlink_tree(candidate_root)
    base.validate_repository_source_boundary()
    marketplace_root = candidate_root / "source-marketplace"
    plugin_root = marketplace_root / "plugins" / PLUGIN_ID
    manifest = base.load_json_object(
        plugin_root / ".codex-plugin" / "plugin.json", "Plugin manifest"
    )
    if manifest != plugin_manifest(candidate):
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: Plugin manifest drift"
        )
    marketplace = base.load_json_object(
        marketplace_root / ".agents" / "plugins" / "marketplace.json",
        "Marketplace manifest",
    )
    if marketplace != marketplace_manifest(candidate):
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: Marketplace manifest drift"
        )

    expected_targets = {
        target_skill_name(skill, short_names=candidate.short_names)
        for skill in base.EXPECTED_SKILLS
    }
    actual_targets = {
        path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()
    }
    if actual_targets != expected_targets:
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: target Skill set mismatch"
        )
    for target_name in sorted(actual_targets):
        skill_file = plugin_root / "skills" / target_name / "SKILL.md"
        if base.frontmatter_name(skill_file) != target_name:
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: frontmatter mismatch for {target_name}"
            )
    comparison = mapped_source_comparison(plugin_root, candidate)
    expected_files = {
        ".codex-plugin/plugin.json",
        *{
            f"skills/{path}"
            for path in base.file_manifest(plugin_root / "skills")
        },
        *base.PACKAGE_SUPPORT_FILES.keys(),
    }
    actual_files = set(base.file_manifest(plugin_root))
    if actual_files != expected_files:
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: package allowlist mismatch"
        )
    official = "not_run"
    if run_official:
        if env is None:
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: isolated environment is required "
                "for official validation"
            )
        validator = base.plugin_creator_script("validate_plugin.py")
        completed = base.run_process(
            [sys.executable, str(validator), str(plugin_root)],
            env=env,
            cwd=candidate_root,
        )
        if completed.returncode != 0:
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: official validator failed: "
                f"{(completed.stdout + completed.stderr)[-500:]}"
            )
        official = "passed"
    target_entrypoints: list[dict[str, str]] = []
    for source_name in USER_OWNED_SKILLS:
        target_name = target_skill_name(
            source_name, short_names=candidate.short_names
        )
        interface = load_agent_interface(
            plugin_root / "skills" / target_name / "agents" / "openai.yaml",
            f"{candidate.candidate_id}/{target_name}",
        )
        expected_token = (
            f"${PLUGIN_ID}:{target_name}"
            if candidate.short_names
            else f"${source_name}"
        )
        prompt = str(interface.get("default_prompt", ""))
        if not prompt.startswith(f"Use {expected_token}"):
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: static agent invocation mismatch "
                f"for {target_name}"
            )
        target_entrypoints.append(
            {
                "source_name": source_name,
                "target_name": target_name,
                "canonical_name": f"{PLUGIN_ID}:{target_name}",
                "agent_self_invocation_token": expected_token,
            }
        )
    residual_source = identifier_inventory(
        plugin_root / "skills", USER_OWNED_SKILLS
    )
    residual_non_protocol = sum(
        count
        for category, count in residual_source["by_category"].items()
        if category not in {"protocol_or_version"}
    )
    plugin_sensitive_references = sum(
        residual_source["by_category"].get(category, 0)
        for category in {
            "agent_self_prompt",
            "explicit_invocation",
            "fallback_path",
        }
    )
    return {
        "candidate_id": candidate.candidate_id,
        "skills": len(actual_targets),
        "skill_files": comparison["target_files"],
        "package_files": len(actual_files),
        "official_validator": official,
        "source_comparison": comparison,
        "target_entrypoints": target_entrypoints,
        "residual_source_identifier_inventory": residual_source,
        "residual_migration_review_required": (
            residual_non_protocol if candidate.short_names else 0
        ),
        "plugin_sensitive_reference_count": plugin_sensitive_references,
    }


def parse_json_stdout(completed: subprocess.CompletedProcess[str], label: str) -> Any:
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise NamespaceEvaluationError(f"{label}: CLI output is not JSON") from exc


def run_cli_step(
    candidate_root: Path,
    candidate: Candidate,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    step: str,
    arguments: list[str],
) -> Any:
    completed = base.run_process(
        [
            base.codex_executable(),
            "--disable",
            "remote_plugin",
            "plugin",
            *arguments,
        ],
        env=env,
        cwd=candidate_root,
        timeout=90,
    )
    base.write_json(
        candidate_root / "evidence" / "commands" / f"{step}.json",
        {
            "argv": ["codex", "--disable", "remote_plugin", "plugin", *arguments],
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        },
    )
    assert_protected_product_state_unchanged(protected_before)
    if completed.returncode != 0:
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}/{step} failed: {completed.stderr[-400:]}"
        )
    return parse_json_stdout(completed, f"{candidate.candidate_id}/{step}")


def require_object(payload: Any, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise NamespaceEvaluationError(f"{label}: expected JSON object")
    return payload


def validate_marketplace_add(
    payload: Any,
    candidate_root: Path,
    candidate: Candidate,
) -> None:
    item = require_object(payload, "Marketplace add")
    if item.get("marketplaceName") != candidate.marketplace:
        raise NamespaceEvaluationError("Marketplace add identity mismatch")
    if Path(str(item.get("installedRoot", ""))).resolve() != (
        candidate_root / "source-marketplace"
    ).resolve():
        raise NamespaceEvaluationError("Marketplace add root mismatch")
    if item.get("alreadyAdded") is not False:
        raise NamespaceEvaluationError("fresh candidate Marketplace already existed")


def validate_plugin_add(
    payload: Any,
    candidate_root: Path,
    candidate: Candidate,
) -> None:
    item = require_object(payload, "Plugin add")
    expected = {
        "pluginId": candidate.selector,
        "name": PLUGIN_ID,
        "marketplaceName": candidate.marketplace,
        "version": candidate.version,
        "authPolicy": "ON_INSTALL",
    }
    for key, value in expected.items():
        if item.get(key) != value:
            raise NamespaceEvaluationError(f"Plugin add mismatch: {key}")
    installed = Path(str(item.get("installedPath", ""))).resolve()
    expected_cache = candidate_root / "codex-home" / "plugins" / "cache"
    try:
        installed.relative_to(expected_cache.resolve())
    except ValueError as exc:
        raise NamespaceEvaluationError("Plugin cache escaped candidate root") from exc


def validate_plugin_list(
    payload: Any,
    candidate_root: Path,
    candidate: Candidate,
    *,
    installed: bool,
) -> None:
    root = require_object(payload, "Plugin list")
    installed_items = root.get("installed")
    available_items = root.get("available")
    if not isinstance(installed_items, list) or not isinstance(available_items, list):
        raise NamespaceEvaluationError("Plugin list omitted state arrays")
    matches = [
        item for item in installed_items if item.get("pluginId") == candidate.selector
    ]
    available_matches = [
        item for item in available_items if item.get("pluginId") == candidate.selector
    ]
    if len(matches) != int(installed) or available_matches:
        raise NamespaceEvaluationError("Plugin installed state mismatch")
    for item in matches:
        expected = {
            "name": PLUGIN_ID,
            "marketplaceName": candidate.marketplace,
            "version": candidate.version,
            "installed": True,
            "enabled": True,
            "installPolicy": "AVAILABLE",
            "authPolicy": "ON_INSTALL",
        }
        for key, value in expected.items():
            if item.get(key) != value:
                raise NamespaceEvaluationError(f"Plugin list mismatch: {key}")
        source = require_object(item.get("source"), "Plugin source")
        if source.get("source") != "local":
            raise NamespaceEvaluationError("candidate Plugin source is not local")
        expected_source = (
            candidate_root / "source-marketplace" / "plugins" / PLUGIN_ID
        ).resolve()
        if Path(str(source.get("path", ""))).resolve() != expected_source:
            raise NamespaceEvaluationError("candidate Plugin source path mismatch")


def validate_plugin_remove(payload: Any, candidate: Candidate) -> None:
    item = require_object(payload, "Plugin remove")
    expected = {
        "pluginId": candidate.selector,
        "name": PLUGIN_ID,
        "marketplaceName": candidate.marketplace,
    }
    for key, value in expected.items():
        if item.get(key) != value:
            raise NamespaceEvaluationError(f"Plugin remove mismatch: {key}")


def validate_marketplace_remove(payload: Any, candidate: Candidate) -> None:
    item = require_object(payload, "Marketplace remove")
    if item.get("marketplaceName") != candidate.marketplace:
        raise NamespaceEvaluationError("Marketplace remove identity mismatch")
    if item.get("installedRoot") is not None:
        raise NamespaceEvaluationError("Marketplace remove retained an installed root")


def load_agent_interface(path: Path, label: str) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("interface"), dict):
        raise NamespaceEvaluationError(f"missing agent interface: {label}")
    return payload["interface"]


def load_source_interfaces() -> dict[str, dict[str, Any]]:
    interfaces: dict[str, dict[str, Any]] = {}
    for source_name in USER_OWNED_SKILLS:
        path = base.SOURCE_SKILLS_ROOT / source_name / "agents" / "openai.yaml"
        interfaces[source_name] = load_agent_interface(path, source_name)
    return interfaces


def discover_candidate(
    candidate_root: Path,
    candidate: Candidate,
    env: dict[str, str],
    project: Path,
    *,
    expect_plugin: bool,
    expect_standalone: bool,
) -> dict[str, Any]:
    result = base.app_server_request(
        candidate_root,
        env,
        project,
        {
            "method": "skills/list",
            "id": 32,
            "params": {"cwds": [str(project.resolve())], "forceReload": True},
        },
    )
    entries = result.get("data")
    if not isinstance(entries, list) or len(entries) != 1:
        raise NamespaceEvaluationError("skills/list did not return one project")
    entry = entries[0]
    if entry.get("errors"):
        raise NamespaceEvaluationError(f"skills/list errors: {entry['errors']}")
    items = entry.get("skills", [])
    target_names = {
        target_skill_name(skill, short_names=candidate.short_names)
        for skill in base.EXPECTED_SKILLS
    }
    expected_plugin_names = {f"{PLUGIN_ID}:{name}" for name in target_names}
    plugin_items = {
        item.get("name"): item
        for item in items
        if item.get("name") in expected_plugin_names
    }
    expected_standalone_names = set(base.EXPECTED_SKILLS)
    standalone_items = {
        item.get("name"): item
        for item in items
        if item.get("name") in expected_standalone_names
        and Path(str(item.get("path", ""))).resolve().is_relative_to(project.resolve())
    }
    if set(plugin_items) != (expected_plugin_names if expect_plugin else set()):
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: Plugin discovery mismatch"
        )
    if set(standalone_items) != (
        expected_standalone_names if expect_standalone else set()
    ):
        raise NamespaceEvaluationError(
            f"{candidate.candidate_id}: standalone discovery mismatch"
        )

    source_interfaces = load_source_interfaces()
    interface_rows: list[dict[str, Any]] = []
    plugin_root = candidate_root / "source-marketplace" / "plugins" / PLUGIN_ID
    for canonical_name, item in sorted(plugin_items.items()):
        target_name = str(canonical_name).split(":", 1)[1]
        source_name = source_skill_name(
            target_name, short_names=candidate.short_names
        )
        path = Path(str(item.get("path", ""))).resolve()
        base.assert_fixture_path(
            candidate_root, path, f"discovered Skill {canonical_name}"
        )
        expected_skill_file = plugin_root / "skills" / target_name / "SKILL.md"
        if not path.is_file() or base.sha256(path) != base.sha256(expected_skill_file):
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: discovered bytes mismatch {canonical_name}"
            )
        if item.get("scope") != "user" or item.get("enabled") is not True:
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: scope/enabled mismatch {canonical_name}"
            )
        interface = item.get("interface")
        if source_name in USER_OWNED_SKILLS:
            if not isinstance(interface, dict):
                raise NamespaceEvaluationError(f"missing interface: {canonical_name}")
            source_interface = source_interfaces[source_name]
            if interface.get("displayName") != source_interface.get("display_name"):
                raise NamespaceEvaluationError(f"displayName mismatch: {canonical_name}")
            if interface.get("shortDescription") != source_interface.get(
                "short_description"
            ):
                raise NamespaceEvaluationError(
                    f"shortDescription mismatch: {canonical_name}"
                )
            prompt = str(interface.get("defaultPrompt", ""))
            expected_token = (
                f"${PLUGIN_ID}:{target_name}"
                if candidate.short_names
                else f"${source_name}"
            )
            if not prompt.startswith(f"Use {expected_token}"):
                raise NamespaceEvaluationError(
                    f"defaultPrompt invocation mismatch: {canonical_name}"
                )
            interface_rows.append(
                {
                    "canonical_name": canonical_name,
                    "display_name": interface.get("displayName"),
                    "short_description": interface.get("shortDescription"),
                    "self_invocation_token": expected_token,
                }
            )
        elif interface is not None:
            raise NamespaceEvaluationError(
                f"companion interface should be null: {canonical_name}"
            )
    for name, item in standalone_items.items():
        if item.get("scope") != "repo" or item.get("enabled") is not True:
            raise NamespaceEvaluationError(
                f"standalone scope/enabled mismatch: {name}"
            )
    return {
        "plugin_skill_count": len(plugin_items),
        "plugin_names": sorted(plugin_items),
        "plugin_scope": "user" if plugin_items else None,
        "standalone_skill_count": len(standalone_items),
        "standalone_names": sorted(standalone_items),
        "standalone_scope": "repo" if standalone_items else None,
        "interface_count": len(interface_rows),
        "interfaces": interface_rows,
    }


def run_candidate_lifecycle(
    candidate_root: Path,
    candidate: Candidate,
    env: dict[str, str],
    protected_before: dict[str, dict[str, Any]],
    source_before: dict[str, Any],
) -> dict[str, Any]:
    marketplace_root = candidate_root / "source-marketplace"
    empty_project = candidate_root / "project-empty"
    coexist_project = candidate_root / "project-with-standalone-skills"
    steps: list[str] = []
    payload = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "marketplace-add",
        ["marketplace", "add", str(marketplace_root), "--json"],
    )
    validate_marketplace_add(payload, candidate_root, candidate)
    steps.append("marketplace_add")
    payload = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "plugin-add",
        ["add", candidate.selector, "--json"],
    )
    validate_plugin_add(payload, candidate_root, candidate)
    steps.append("plugin_add")
    payload = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "plugin-list-installed",
        ["list", "--marketplace", candidate.marketplace, "--json"],
    )
    validate_plugin_list(payload, candidate_root, candidate, installed=True)
    steps.append("plugin_list_installed")
    installed = discover_candidate(
        candidate_root,
        candidate,
        env,
        empty_project,
        expect_plugin=True,
        expect_standalone=False,
    )
    steps.append("discovery_installed")
    coexist = discover_candidate(
        candidate_root,
        candidate,
        env,
        coexist_project,
        expect_plugin=True,
        expect_standalone=True,
    )
    steps.append("discovery_coexistence")
    payload = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "plugin-remove",
        ["remove", candidate.selector, "--json"],
    )
    validate_plugin_remove(payload, candidate)
    steps.append("plugin_remove")
    payload = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "plugin-list-after-remove",
        ["list", "--marketplace", candidate.marketplace, "--json"],
    )
    validate_plugin_list(payload, candidate_root, candidate, installed=False)
    steps.append("plugin_list_after_remove")
    removed = discover_candidate(
        candidate_root,
        candidate,
        env,
        coexist_project,
        expect_plugin=False,
        expect_standalone=True,
    )
    steps.append("discovery_after_remove")
    payload = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "marketplace-remove",
        ["marketplace", "remove", candidate.marketplace, "--json"],
    )
    validate_marketplace_remove(payload, candidate)
    steps.append("marketplace_remove")
    final_marketplaces = run_cli_step(
        candidate_root,
        candidate,
        env,
        protected_before,
        "marketplace-list-final",
        ["marketplace", "list", "--json"],
    )
    final_root = require_object(final_marketplaces, "final Marketplace list")
    marketplace_items = final_root.get("marketplaces")
    if not isinstance(marketplace_items, list):
        raise NamespaceEvaluationError("final Marketplace list omitted marketplaces")
    if any(
        item.get("name") == candidate.marketplace
        for item in marketplace_items
    ):
        raise NamespaceEvaluationError("candidate Marketplace remained configured")
    steps.append("marketplace_final_absent")
    assert_protected_product_state_unchanged(protected_before)
    if base.source_state_snapshot() != source_before:
        raise NamespaceEvaluationError("repository source or lock changed")
    return {
        "status": "passed",
        "steps": steps,
        "step_count": len(steps),
        "installed": installed,
        "coexistence": coexist,
        "after_remove": removed,
        "final_plugin_installed": False,
        "final_marketplace_configured": False,
    }


def display_led_overlay(n1_result: dict[str, Any]) -> dict[str, Any]:
    interfaces = n1_result["lifecycle"]["installed"]["interfaces"]
    canonical_names = n1_result["lifecycle"]["installed"]["plugin_names"]
    display_names = [str(item["display_name"]) for item in interfaces]
    query_tokens = ("cotend", "init", "diagnose", "model", "collaboration")
    token_coverage = {
        token: {
            "canonical_fields": sum(token in name.lower() for name in canonical_names),
            "display_fields": sum(token in name.lower() for name in display_names),
        }
        for token in query_tokens
    }
    plugin_interface = plugin_manifest(CANDIDATES[0])["interface"]
    return {
        "candidate_id": "N3-display-led",
        "physical_package": "N1-preserve",
        "additional_package_bytes": 0,
        "friendly_display_name_count": len(display_names),
        "display_names_unique": len(set(display_names)) == len(display_names),
        "all_display_names_brand_prefixed": all(
            name.startswith("CoTend ") for name in display_names
        ),
        "plugin_display_name": plugin_interface["displayName"],
        "plugin_short_description": plugin_interface["shortDescription"],
        "plugin_default_prompt": plugin_interface["defaultPrompt"][0],
        "field_token_coverage": token_coverage,
        "canonical_double_prefix_remains": True,
        "desktop_or_natural_language_result": "not_run",
        "claim_to_evidence": {
            "canonical_and_skill_interface_metadata": "executed",
            "plugin_manifest_interface": "inspection",
            "display_led_novice_utility": "inspection",
            "desktop_search_render_and_natural_language": "not_run",
        },
    }


def candidate_isolation_record(
    candidate_root: Path,
    candidate: Candidate,
    env: dict[str, str],
) -> dict[str, Any]:
    candidate_root = base.guarded_fixture(candidate_root)
    base.validate_isolated_env(candidate_root, env)
    write_root_relatives: dict[str, str] = {}
    for key in base.WRITE_ROOT_ENV_KEYS:
        resolved = base.assert_fixture_path(
            candidate_root, Path(env[key]), f"{candidate.candidate_id} write root {key}"
        )
        write_root_relatives[key] = resolved.relative_to(candidate_root).as_posix()
    state_paths = {
        "codex_home": Path(env["CODEX_HOME"]),
        "process_home": Path(env["HOME"]),
        "temp": Path(env["TEMP"]),
        "cache": candidate_root / "cache",
        "marketplace": candidate_root / "source-marketplace",
        "empty_project": candidate_root / "project-empty",
        "coexist_project": candidate_root / "project-with-standalone-skills",
    }
    state_path_relatives: dict[str, str] = {}
    for label, path in state_paths.items():
        resolved = base.assert_fixture_path(
            candidate_root, path, f"{candidate.candidate_id} state path {label}"
        )
        state_path_relatives[label] = resolved.relative_to(candidate_root).as_posix()
    return {
        "candidate_root": candidate.root_name,
        "write_root_key_count": len(write_root_relatives),
        "unique_write_root_count": len(set(write_root_relatives.values())),
        "write_root_relatives": write_root_relatives,
        "state_path_count": len(state_path_relatives),
        "state_path_relatives": state_path_relatives,
        "all_paths_inside_candidate_root": True,
    }


def verify_candidate_isolation(
    evaluation_root: Path,
    results: dict[str, Any],
) -> dict[str, Any]:
    evaluation_root = base.guarded_fixture(evaluation_root)
    expected_ids = {candidate.candidate_id for candidate in CANDIDATES}
    if set(results) != expected_ids:
        raise NamespaceEvaluationError("candidate isolation result set mismatch")
    path_groups: dict[str, set[Path]] = {}
    for candidate in CANDIDATES:
        record = results[candidate.candidate_id].get("isolation")
        if not isinstance(record, dict):
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: isolation record is missing"
            )
        if record.get("candidate_root") != candidate.root_name:
            raise NamespaceEvaluationError(
                f"{candidate.candidate_id}: candidate root identity mismatch"
            )
        candidate_root = base.guarded_fixture(evaluation_root / candidate.root_name)
        paths = {candidate_root}
        for relative in record.get("state_path_relatives", {}).values():
            paths.add(
                base.assert_fixture_path(
                    candidate_root,
                    candidate_root / str(relative),
                    f"{candidate.candidate_id} isolation state",
                )
            )
        for relative in record.get("write_root_relatives", {}).values():
            paths.add(
                base.assert_fixture_path(
                    candidate_root,
                    candidate_root / str(relative),
                    f"{candidate.candidate_id} isolation write root",
                )
            )
        path_groups[candidate.candidate_id] = paths
    first, second = CANDIDATES
    for first_path in path_groups[first.candidate_id]:
        for second_path in path_groups[second.candidate_id]:
            if (
                first_path == second_path
                or first_path.is_relative_to(second_path)
                or second_path.is_relative_to(first_path)
            ):
                raise NamespaceEvaluationError(
                    "candidate roots or state paths overlap across fixtures"
                )
    return {
        "physical_candidate_count": len(CANDIDATES),
        "candidate_roots_disjoint": True,
        "codex_home_process_home_temp_cache_marketplace_and_projects_disjoint": True,
        "write_root_keys_per_candidate": len(base.WRITE_ROOT_ENV_KEYS),
        "cross_candidate_path_overlaps": 0,
    }


def prepare_candidate(
    evaluation_root: Path,
    candidate: Candidate,
    source_before: dict[str, Any],
) -> dict[str, Any]:
    candidate_root = base.guarded_fixture(evaluation_root / candidate.root_name)
    candidate_root.mkdir(parents=True, exist_ok=True)
    protected_before = base.protected_user_snapshot()
    env = base.build_isolated_env(candidate_root)
    preflight = base.run_preflight(candidate_root, env, protected_before)
    isolation = candidate_isolation_record(candidate_root, candidate, env)
    scaffold_candidate(candidate_root, candidate, env)
    materialized = materialize_candidate_payload(candidate_root, candidate)
    assert_protected_product_state_unchanged(protected_before)
    static = verify_candidate_static(
        candidate_root,
        candidate,
        env=env,
        run_official=True,
    )
    lifecycle = run_candidate_lifecycle(
        candidate_root,
        candidate,
        env,
        protected_before,
        source_before,
    )
    protected_boundary = protected_boundary_summary(protected_before)
    return {
        "candidate": {
            "id": candidate.candidate_id,
            "plugin_id": PLUGIN_ID,
            "marketplace": candidate.marketplace,
            "version": candidate.version,
            "production_authority": False,
        },
        "preflight": preflight,
        "isolation": isolation,
        "protected_boundary": protected_boundary,
        "transforms": materialized["transforms"],
        "static": static,
        "lifecycle": lifecycle,
    }


def write_evidence(path: Path | None, root: Path, payload: dict[str, Any]) -> None:
    if path is None:
        return
    target = base.assert_fixture_path(root, path, "namespace evidence")
    base.write_json(target, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate isolated CoTend Plugin namespace candidates"
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="ignored evaluation root under the private fixture directory",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="rebuild independent N1 and N2 candidate roots",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="run isolated Plugin lifecycle and discovery for both candidates",
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        help="write detailed JSON under the ignored evaluation root",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evaluation_root = base.guarded_fixture(args.fixture)
    try:
        if not args.prepare or not args.execute:
            raise NamespaceEvaluationError(
                "--prepare and --execute are both required so every result starts "
                "from independent fresh fixtures"
            )
        base.remove_fixture_tree(evaluation_root)
        evaluation_root.mkdir(parents=True, exist_ok=True)
        source_before = base.source_state_snapshot()
        protected_before_all = base.protected_user_snapshot()
        source_inventory = identifier_inventory(
            base.SOURCE_SKILLS_ROOT, USER_OWNED_SKILLS
        )
        print(
            "PLUGIN_NAMESPACE_SOURCE_INVENTORY_OK "
            f"occurrences={source_inventory['occurrences']} "
            f"files={source_inventory['files']}"
        )
        results: dict[str, Any] = {}
        for candidate in CANDIDATES:
            result = prepare_candidate(evaluation_root, candidate, source_before)
            results[candidate.candidate_id] = result
            print(
                "PLUGIN_NAMESPACE_CANDIDATE_OK "
                f"id={candidate.candidate_id} "
                f"skills={result['static']['skills']} "
                f"canonical={result['lifecycle']['installed']['plugin_skill_count']} "
                f"coexistence={result['lifecycle']['coexistence']['standalone_skill_count']} "
                f"byte_changes={result['static']['source_comparison']['byte_changed_file_count']} "
                "migration_residual="
                f"{result['static']['residual_migration_review_required']} "
                "plugin_sensitive="
                f"{result['static']['plugin_sensitive_reference_count']}"
            )
        isolation = verify_candidate_isolation(evaluation_root, results)
        final_protected_boundary = protected_boundary_summary(
            protected_before_all
        )
        n3 = display_led_overlay(results["N1-preserve"])
        evidence = {
            "schema": "cotend.plugin-namespace-evaluation",
            "schema_version": 1,
            "codex_version": results["N1-preserve"]["preflight"]["codex_version"],
            "source_inventory": source_inventory,
            "physical_candidates": results,
            "candidate_isolation": isolation,
            "display_led_overlay": n3,
            "not_run": list(NOT_RUN),
            "final_boundary": {
                "independent_candidate_roots": isolation[
                    "candidate_roots_disjoint"
                ],
                "protected_product_state": final_protected_boundary,
                "source_and_locks_unchanged": base.source_state_snapshot()
                == source_before,
                "production_plugin_created": False,
            },
        }
        if not evidence["final_boundary"]["source_and_locks_unchanged"]:
            raise NamespaceEvaluationError("final source boundary changed")
        write_evidence(args.evidence, evaluation_root, evidence)
        print(
            "PLUGIN_NAMESPACE_EVALUATION_OK "
            "physical_candidates=2 display_overlays=1 "
            f"not_run={len(NOT_RUN)}"
        )
    except (
        NamespaceEvaluationError,
        base.PluginFixtureError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
        yaml.YAMLError,
    ) as exc:
        print("PLUGIN_NAMESPACE_EVALUATION_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
