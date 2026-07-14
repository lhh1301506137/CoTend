from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = ROOT / "packaging" / "codex-plugin"
PLUGIN_TEMPLATE_ROOT = CONTRACT_ROOT / "cotend"
MANIFEST_SOURCE = PLUGIN_TEMPLATE_ROOT / ".codex-plugin" / "plugin.json"
PACKAGE_LOCK_PATH = CONTRACT_ROOT / "package.lock.json"
SOURCE_SKILLS_ROOT = ROOT / "skills"
TARGET_ARTIFACT_LOCK = ROOT / "delivery" / "codex-artifact.lock.json"
DEFAULT_OUTPUT = (
    ROOT
    / ".private-provenance"
    / "L44-codex-plugin-production-package"
    / "build"
    / "cotend"
)
PLUGIN_NAME = "cotend"
PLUGIN_VERSION = "0.1.0-rc.1"
EXPECTED_SKILLS = (
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-init",
    "cotend-model-upgrade",
    "cotend-project-init",
    "grill-me",
    "karpathy-guidelines",
)
EXPECTED_DISPLAY_NAMES = {
    "cotend-collaboration": "CoTend Collaboration",
    "cotend-diagnose-only": "CoTend Diagnose Only",
    "cotend-init": "CoTend Init",
    "cotend-model-upgrade": "CoTend Model Upgrade",
    "cotend-project-init": "CoTend Project Init",
}
PACKAGE_SUPPORT_FILES = {
    "LICENSE": ROOT / "LICENSE",
    "NOTICE": ROOT / "NOTICE",
    "THIRD-PARTY-NOTICES.md": ROOT / "THIRD-PARTY-NOTICES.md",
    "THIRD-PARTY-SOURCES.json": ROOT / "THIRD-PARTY-SOURCES.json",
    "THIRD-PARTY-LICENSES/grill-me-MIT.txt": (
        ROOT / "THIRD-PARTY-LICENSES" / "grill-me-MIT.txt"
    ),
    "THIRD-PARTY-LICENSES/karpathy-guidelines-MIT.txt": (
        ROOT / "THIRD-PARTY-LICENSES" / "karpathy-guidelines-MIT.txt"
    ),
}
PACKAGE_BRAND_ASSETS = {
    "assets/cotend-mark.svg": {
        "source": PLUGIN_TEMPLATE_ROOT / "assets" / "cotend-mark.svg",
        "role": "canonical_light_source",
    },
    "assets/cotend-mark-dark.svg": {
        "source": PLUGIN_TEMPLATE_ROOT / "assets" / "cotend-mark-dark.svg",
        "role": "canonical_dark_source",
    },
    "assets/cotend-logo.png": {
        "source": PLUGIN_TEMPLATE_ROOT / "assets" / "cotend-logo.png",
        "role": "composer_icon_and_light_logo",
    },
    "assets/cotend-logo-dark.png": {
        "source": PLUGIN_TEMPLATE_ROOT / "assets" / "cotend-logo-dark.png",
        "role": "dark_logo",
    },
}
ALLOWED_OUTPUT_ROOTS = {".private-provenance", "dist"}
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class PluginPackageError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_linklike(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def reject_link_tree(root: Path, *, label: str) -> None:
    if _is_linklike(root):
        raise PluginPackageError(f"{label} root cannot be a link or junction")
    if not root.is_dir():
        raise PluginPackageError(f"{label} root is missing")
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in (*directories, *filenames):
            path = current_path / name
            if _is_linklike(path):
                relative = path.relative_to(root).as_posix()
                raise PluginPackageError(
                    f"{label} cannot contain links or junctions: {relative}"
                )


def path_hash_manifest(root: Path) -> dict[str, str]:
    reject_link_tree(root, label="manifest source")
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def path_hash_manifest_sha256(manifest: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in sorted(manifest.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _svg_shapes(path: Path) -> list[tuple[str, tuple[tuple[str, str], ...]]]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        raise PluginPackageError(f"invalid brand SVG: {path}") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg" or root.attrib.get("viewBox") != "0 0 512 512":
        raise PluginPackageError("brand SVG viewBox drifted")
    shapes: list[tuple[str, tuple[tuple[str, str], ...]]] = []
    forbidden = {"image", "script", "foreignObject", "text", "use", "style"}
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag in forbidden:
            raise PluginPackageError(f"brand SVG contains forbidden element: {tag}")
        for key, value in element.attrib.items():
            local_key = key.rsplit("}", 1)[-1]
            if local_key == "href" or "url(" in value.lower():
                raise PluginPackageError("brand SVG contains an external reference")
        if tag in {"path", "rect", "circle"}:
            geometry = tuple(
                sorted(
                    (key, value)
                    for key, value in element.attrib.items()
                    if key not in {"fill", "stroke"}
                )
            )
            shapes.append((tag, geometry))
    if [tag for tag, _ in shapes].count("circle") != 3:
        raise PluginPackageError("brand SVG must contain exactly three endpoint circles")
    return shapes


def _validate_png(path: Path) -> None:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise PluginPackageError(f"missing brand PNG: {path}") from exc
    if len(payload) < 33 or payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise PluginPackageError("brand PNG signature drifted")
    if payload[12:16] != b"IHDR":
        raise PluginPackageError("brand PNG IHDR is missing")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", payload[16:26])
    if (width, height, bit_depth, color_type) != (1024, 1024, 8, 6):
        raise PluginPackageError("brand PNG must be 1024x1024 RGBA")


def validate_brand_assets() -> None:
    asset_root = PLUGIN_TEMPLATE_ROOT / "assets"
    reject_link_tree(asset_root, label="Plugin brand assets")
    actual = {
        path.relative_to(PLUGIN_TEMPLATE_ROOT).as_posix()
        for path in asset_root.rglob("*")
        if path.is_file()
    }
    if actual != set(PACKAGE_BRAND_ASSETS):
        raise PluginPackageError("Plugin brand asset inventory drifted")
    light_svg = PACKAGE_BRAND_ASSETS["assets/cotend-mark.svg"]["source"]
    dark_svg = PACKAGE_BRAND_ASSETS["assets/cotend-mark-dark.svg"]["source"]
    assert isinstance(light_svg, Path)
    assert isinstance(dark_svg, Path)
    if _svg_shapes(light_svg) != _svg_shapes(dark_svg):
        raise PluginPackageError("light and dark brand SVG geometry drifted")
    light_text = light_svg.read_text(encoding="utf-8")
    dark_text = dark_svg.read_text(encoding="utf-8")
    for color in ("#139C98", "#F15B50", "#67B94B"):
        if color not in light_text or color not in dark_text:
            raise PluginPackageError("brand node palette drifted")
    if "#20252B" not in light_text or "#F4F6F8" not in dark_text:
        raise PluginPackageError("brand light or dark foreground drifted")
    for relative in ("assets/cotend-logo.png", "assets/cotend-logo-dark.png"):
        source = PACKAGE_BRAND_ASSETS[relative]["source"]
        assert isinstance(source, Path)
        _validate_png(source)


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PluginPackageError(f"invalid {label}: {path}") from exc
    if not isinstance(payload, dict):
        raise PluginPackageError(f"{label} must contain a JSON object")
    return payload


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in _walk_strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in _walk_strings(child)]
    return []


def validate_manifest_contract(manifest: dict[str, Any]) -> None:
    expected_keys = {
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "skills",
        "interface",
    }
    if set(manifest) != expected_keys:
        raise PluginPackageError("Plugin manifest top-level field set drifted")
    if manifest.get("name") != PLUGIN_NAME:
        raise PluginPackageError("Plugin candidate name drifted")
    version = manifest.get("version")
    if version != PLUGIN_VERSION or not isinstance(version, str):
        raise PluginPackageError("Plugin candidate version drifted")
    if SEMVER_RE.fullmatch(version) is None:
        raise PluginPackageError("Plugin candidate version is not strict SemVer")
    if manifest.get("skills") != "./skills/":
        raise PluginPackageError("Plugin skills path must be ./skills/")
    if manifest.get("license") != "Apache-2.0":
        raise PluginPackageError("Plugin license drifted")
    if manifest.get("author") != {"name": "CoTend contributors"}:
        raise PluginPackageError("Plugin candidate author metadata drifted")
    if manifest.get("homepage") != "https://github.com/lhh1301506137/CoTend":
        raise PluginPackageError("Plugin homepage drifted")
    if manifest.get("repository") != "https://github.com/lhh1301506137/CoTend":
        raise PluginPackageError("Plugin repository URL drifted")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise PluginPackageError("Plugin interface must be an object")
    expected_interface_keys = {
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "brandColor",
        "composerIcon",
        "logo",
        "logoDark",
        "defaultPrompt",
    }
    if set(interface) != expected_interface_keys:
        raise PluginPackageError("Plugin interface field set drifted")
    if interface.get("displayName") != "CoTend":
        raise PluginPackageError("Plugin display name drifted")
    if interface.get("developerName") != "CoTend contributors":
        raise PluginPackageError("Plugin developer name drifted")
    if interface.get("category") != "Developer Tools":
        raise PluginPackageError("Plugin category drifted")
    if interface.get("capabilities") != ["Interactive", "Read", "Write"]:
        raise PluginPackageError("Plugin capability declaration drifted")
    if interface.get("brandColor") != "#139C98":
        raise PluginPackageError("Plugin brand color drifted")
    if interface.get("composerIcon") != "./assets/cotend-logo.png":
        raise PluginPackageError("Plugin composer icon path drifted")
    if interface.get("logo") != "./assets/cotend-logo.png":
        raise PluginPackageError("Plugin logo path drifted")
    if interface.get("logoDark") != "./assets/cotend-logo-dark.png":
        raise PluginPackageError("Plugin dark logo path drifted")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise PluginPackageError("Plugin defaultPrompt must contain one to three prompts")
    if not all(isinstance(prompt, str) and 0 < len(prompt) <= 128 for prompt in prompts):
        raise PluginPackageError("Plugin defaultPrompt entries must be 1-128 characters")

    windows_user_root = "c:" + "\\users\\"
    windows_user_root_slash = "c:" + "/users/"
    forbidden_fragments = (
        "[todo",
        windows_user_root,
        windows_user_root_slash,
        "/users/",
        "/home/",
    )
    for value in _walk_strings(manifest):
        lowered = value.lower()
        if any(fragment in lowered for fragment in forbidden_fragments):
            raise PluginPackageError("Plugin manifest contains placeholder or local path data")
    for forbidden in ("apps", "mcpServers", "hooks"):
        if forbidden in manifest:
            raise PluginPackageError(f"undeclared Plugin component present: {forbidden}")


def source_skill_manifest() -> dict[str, str]:
    actual_directories = tuple(
        sorted(path.name for path in SOURCE_SKILLS_ROOT.iterdir() if path.is_dir())
    )
    if actual_directories != EXPECTED_SKILLS:
        raise PluginPackageError("repository Skill directory inventory drifted")
    manifest = path_hash_manifest(SOURCE_SKILLS_ROOT)
    if len(manifest) != 30:
        raise PluginPackageError(
            f"expected 30 repository Skill files, found {len(manifest)}"
        )
    for skill in EXPECTED_SKILLS:
        if f"{skill}/SKILL.md" not in manifest:
            raise PluginPackageError(f"repository Skill is missing SKILL.md: {skill}")
    return manifest


def expected_package_manifest() -> dict[str, str]:
    validate_brand_assets()
    manifest = {
        ".codex-plugin/plugin.json": sha256_file(MANIFEST_SOURCE),
    }
    manifest.update(
        {f"skills/{relative}": digest for relative, digest in source_skill_manifest().items()}
    )
    manifest.update(
        {relative: sha256_file(source) for relative, source in PACKAGE_SUPPORT_FILES.items()}
    )
    manifest.update(
        {
            relative: sha256_file(asset["source"])
            for relative, asset in PACKAGE_BRAND_ASSETS.items()
        }
    )
    return dict(sorted(manifest.items()))


def validate_contract() -> dict[str, Any]:
    reject_link_tree(PLUGIN_TEMPLATE_ROOT, label="Plugin contract template")
    manifest = load_json_object(MANIFEST_SOURCE, "Plugin manifest")
    validate_manifest_contract(manifest)
    lock = load_json_object(PACKAGE_LOCK_PATH, "Plugin package lock")
    if lock.get("schema") != "cotend.codex-plugin-package-lock":
        raise PluginPackageError("Plugin package lock schema drifted")
    if lock.get("schema_version") != 2:
        raise PluginPackageError("Plugin package lock version drifted")
    if lock.get("status") != "production_candidate_not_published":
        raise PluginPackageError("Plugin package lock status drifted")

    plugin = lock.get("plugin")
    source = lock.get("source")
    package = lock.get("package")
    build = lock.get("build")
    authority = lock.get("authority")
    if not all(isinstance(item, dict) for item in (plugin, source, package, build, authority)):
        raise PluginPackageError("Plugin package lock sections must be objects")
    assert isinstance(plugin, dict)
    assert isinstance(source, dict)
    assert isinstance(package, dict)
    assert isinstance(build, dict)
    assert isinstance(authority, dict)
    if plugin.get("name") != PLUGIN_NAME or plugin.get("version") != PLUGIN_VERSION:
        raise PluginPackageError("Plugin package lock identity drifted")
    if plugin.get("manifest") != MANIFEST_SOURCE.relative_to(ROOT).as_posix():
        raise PluginPackageError("Plugin package lock manifest path drifted")
    if plugin.get("manifest_sha256") != sha256_file(MANIFEST_SOURCE):
        raise PluginPackageError("Plugin manifest hash differs from package lock")

    artifact_lock = load_json_object(TARGET_ARTIFACT_LOCK, "target artifact lock")
    target = artifact_lock.get("target")
    if not isinstance(target, dict):
        raise PluginPackageError("target artifact lock target is invalid")
    expected_source = {
        "carrier": "skills/",
        "artifact_lock": "delivery/codex-artifact.lock.json",
        "artifact_id": target.get("artifact_id"),
        "revision": target.get("revision"),
        "target_manifest_sha256": target.get("manifest_sha256"),
        "skill_count": len(EXPECTED_SKILLS),
        "skill_file_count": 30,
        "path_hash_manifest_sha256": path_hash_manifest_sha256(
            source_skill_manifest()
        ),
    }
    if source != expected_source:
        raise PluginPackageError("Plugin package source lock drifted")

    expected_files = expected_package_manifest()
    expected_package = {
        "output_directory_name": PLUGIN_NAME,
        "file_count": len(expected_files),
        "path_hash_manifest_sha256": path_hash_manifest_sha256(expected_files),
        "support_files": list(PACKAGE_SUPPORT_FILES),
        "brand_assets": [
            {
                "path": relative,
                "role": asset["role"],
                "sha256": sha256_file(asset["source"]),
            }
            for relative, asset in PACKAGE_BRAND_ASSETS.items()
        ],
        "forbidden_components": [
            ".app.json",
            ".mcp.json",
            ".agents",
            "hooks",
            "scripts",
        ],
    }
    if package != expected_package:
        raise PluginPackageError("Plugin package output lock drifted")
    if build != {
        "script": "scripts/build_codex_plugin.py",
        "semantic_source_count": 1,
        "network_required": False,
        "marketplace_generated": False,
        "plugin_installation_performed": False,
    }:
        raise PluginPackageError("Plugin package build boundary drifted")
    if authority != {
        "candidate_identity_only": False,
        "final_plugin_identity_confirmed": True,
        "release_or_publish_authorized": False,
    }:
        raise PluginPackageError("Plugin package authority boundary drifted")
    return {
        "manifest": manifest,
        "lock": lock,
        "source_manifest": source_skill_manifest(),
        "expected_package_manifest": expected_files,
    }


def guarded_output(path: Path) -> Path:
    raw = path.expanduser()
    if not raw.is_absolute():
        raw = ROOT / raw
    resolved = raw.resolve(strict=False)
    try:
        relative = resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise PluginPackageError("Plugin build output must stay inside the repository") from exc
    if len(relative.parts) < 2 or relative.parts[0] not in ALLOWED_OUTPUT_ROOTS:
        raise PluginPackageError(
            "Plugin build output must be under .private-provenance/ or dist/"
        )
    if resolved.name != PLUGIN_NAME:
        raise PluginPackageError(f"Plugin build output directory must be named {PLUGIN_NAME}")
    cursor = ROOT.resolve()
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and _is_linklike(cursor):
            raise PluginPackageError("Plugin build output path contains a link or junction")
    return resolved


def verify_package(package_root: Path) -> dict[str, Any]:
    package_root = guarded_output(package_root)
    contract = validate_contract()
    reject_link_tree(package_root, label="Plugin package")
    actual_manifest = path_hash_manifest(package_root)
    expected_manifest = contract["expected_package_manifest"]
    if actual_manifest != expected_manifest:
        extra = sorted(set(actual_manifest) - set(expected_manifest))
        missing = sorted(set(expected_manifest) - set(actual_manifest))
        changed = sorted(
            path
            for path in set(actual_manifest) & set(expected_manifest)
            if actual_manifest[path] != expected_manifest[path]
        )
        raise PluginPackageError(
            f"Plugin package bytes drifted; extra={extra}; missing={missing}; changed={changed}"
        )
    lock = contract["lock"]
    package_lock = lock["package"]
    if path_hash_manifest_sha256(actual_manifest) != package_lock[
        "path_hash_manifest_sha256"
    ]:
        raise PluginPackageError("Plugin package digest differs from package lock")
    for forbidden in package_lock["forbidden_components"]:
        if (package_root / forbidden).exists():
            raise PluginPackageError(f"forbidden Plugin component exists: {forbidden}")
    expected_brand_paths = set(PACKAGE_BRAND_ASSETS)
    actual_brand_paths = {
        path.relative_to(package_root).as_posix()
        for path in (package_root / "assets").rglob("*")
        if path.is_file()
    }
    if actual_brand_paths != expected_brand_paths:
        raise PluginPackageError("packaged brand asset inventory drifted")

    for skill, display_name in EXPECTED_DISPLAY_NAMES.items():
        agent = package_root / "skills" / skill / "agents" / "openai.yaml"
        if f'display_name: "{display_name}"' not in agent.read_text(encoding="utf-8"):
            raise PluginPackageError(f"N3 display metadata drifted: {skill}")
    notice_text = (package_root / "THIRD-PARTY-NOTICES.md").read_text(
        encoding="utf-8"
    )
    relative_notice_links = re.findall(r"\]\(\./([^\)#]+)(?:#[^\)]*)?\)", notice_text)
    for relative in relative_notice_links:
        if not (package_root / relative).is_file():
            raise PluginPackageError(
                f"third-party notice link is missing from package: {relative}"
            )
    return {
        "plugin_name": PLUGIN_NAME,
        "plugin_version": PLUGIN_VERSION,
        "package_files": len(actual_manifest),
        "skills": len(EXPECTED_SKILLS),
        "skill_files": len(contract["source_manifest"]),
        "friendly_display_names": len(EXPECTED_DISPLAY_NAMES),
        "relative_notice_links": len(relative_notice_links),
        "brand_assets": len(PACKAGE_BRAND_ASSETS),
        "source_bytes_identical": True,
        "source_manifest_sha256": path_hash_manifest_sha256(
            contract["source_manifest"]
        ),
        "package_manifest_sha256": path_hash_manifest_sha256(actual_manifest),
        "marketplace_files": 0,
        "undeclared_capabilities": 0,
    }


def _materialize_package(package_root: Path) -> None:
    (package_root / ".codex-plugin").mkdir(parents=True)
    shutil.copy2(MANIFEST_SOURCE, package_root / ".codex-plugin" / "plugin.json")
    shutil.copytree(SOURCE_SKILLS_ROOT, package_root / "skills")
    for relative, source in PACKAGE_SUPPORT_FILES.items():
        target = package_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for relative, asset in PACKAGE_BRAND_ASSETS.items():
        source = asset["source"]
        assert isinstance(source, Path)
        target = package_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def build_package(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    output = guarded_output(output)
    validate_contract()
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix=".cotend-build-", dir=output.parent))
    temp_package = temp_root / PLUGIN_NAME
    try:
        _materialize_package(temp_package)
        summary = verify_package(temp_package)
        if output.exists():
            try:
                verify_package(output)
            except PluginPackageError as exc:
                raise PluginPackageError(
                    "existing output is not an owned valid CoTend package; refusing replacement"
                ) from exc
            shutil.rmtree(output)
        os.replace(temp_package, output)
        summary["output"] = str(output)
        return summary
    finally:
        if temp_root.exists():
            reject_link_tree(temp_root, label="temporary Plugin build")
            shutil.rmtree(temp_root)


def run_official_validator(package_root: Path, validator: Path) -> dict[str, str]:
    package_root = guarded_output(package_root)
    validator = validator.expanduser().resolve()
    if not validator.is_file():
        raise PluginPackageError("Plugin Creator validator is unavailable")
    completed = subprocess.run(
        [sys.executable, str(validator), str(package_root)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    if completed.returncode != 0:
        raise PluginPackageError(
            "Plugin Creator validator failed: "
            + (completed.stdout + completed.stderr)[-800:]
        )
    return {
        "status": "passed",
        "validator_sha256": sha256_file(validator),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the repository-local CoTend Codex Plugin production candidate."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--official-validator", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = build_package(args.output)
        summary["official_validator"] = "not_run"
        if args.official_validator is not None:
            summary["official_validator"] = run_official_validator(
                Path(summary["output"]), args.official_validator
            )
    except PluginPackageError as exc:
        print(f"CODEX_PLUGIN_PACKAGE_FAILED {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=True, sort_keys=True))
    else:
        print(
            "CODEX_PLUGIN_PACKAGE_OK "
            f"plugin={summary['plugin_name']} version={summary['plugin_version']} "
            f"files={summary['package_files']} skills={summary['skills']} "
            f"skill_files={summary['skill_files']} "
            f"digest={summary['package_manifest_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
