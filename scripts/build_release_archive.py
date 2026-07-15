from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402


DIST_ROOT = ROOT / "dist"
PRIVATE_BUILD_ROOT = ROOT / ".private-provenance" / "release-archive"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
RELEASE_NOTES_ROOT = ROOT / "docs" / "releases"
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
REGULAR_FILE_MODE = 0o100644


class ReleaseArchiveError(RuntimeError):
    pass


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expected_tag() -> str:
    return f"v{package.PLUGIN_VERSION}"


def archive_filename() -> str:
    return f"{package.PLUGIN_NAME}-{package.PLUGIN_VERSION}.zip"


def checksum_filename() -> str:
    return f"{archive_filename()}.sha256"


def release_notes_path() -> Path:
    return RELEASE_NOTES_ROOT / f"{expected_tag()}.md"


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseArchiveError(f"invalid {label}: {path}") from exc
    if not isinstance(value, dict):
        raise ReleaseArchiveError(f"{label} must contain a JSON object")
    return value


def validate_release_metadata(tag: str | None = None) -> dict[str, str]:
    contract = package.validate_contract()
    manifest = contract["manifest"]
    root_manifest = _load_json(ROOT / ".codex-plugin" / "plugin.json", "root manifest")
    version = package.PLUGIN_VERSION
    required_tag = expected_tag()
    if tag is not None and tag != required_tag:
        raise ReleaseArchiveError(
            f"release tag must be {required_tag}, received {tag}"
        )
    if manifest.get("version") != version or root_manifest.get("version") != version:
        raise ReleaseArchiveError("root and package manifest versions differ")
    if manifest.get("name") != package.PLUGIN_NAME:
        raise ReleaseArchiveError("package identity drifted")

    notes_path = release_notes_path()
    try:
        changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
        notes = notes_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReleaseArchiveError("release notes or changelog are missing") from exc
    if f"## [{version}]" not in changelog:
        raise ReleaseArchiveError("changelog does not contain the candidate version")
    if not notes.startswith(f"# CoTend {required_tag}\n"):
        raise ReleaseArchiveError("release notes title differs from the candidate tag")
    if "Pre-release" not in notes or "not a stable release" not in notes:
        raise ReleaseArchiveError("release notes must preserve the pre-release boundary")
    return {
        "plugin": package.PLUGIN_NAME,
        "version": version,
        "tag": required_tag,
        "release_notes": notes_path.relative_to(ROOT).as_posix(),
    }


def guarded_output_directory(path: Path) -> Path:
    raw = path.expanduser()
    if not raw.is_absolute():
        raw = ROOT / raw
    repository_root = ROOT.resolve()
    lexical = Path(os.path.abspath(raw))
    try:
        relative = lexical.relative_to(repository_root)
    except ValueError as exc:
        raise ReleaseArchiveError("release output must stay under dist/") from exc
    if not relative.parts or relative.parts[0] != "dist":
        raise ReleaseArchiveError("release output must stay under dist/")
    if any(part in {"", ".", ".."} for part in relative.parts):
        raise ReleaseArchiveError("release output path is invalid")
    cursor = repository_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and package._is_linklike(cursor):
            raise ReleaseArchiveError("release output path contains a link or junction")
    resolved = lexical.resolve(strict=False)
    try:
        resolved_relative = resolved.relative_to(repository_root)
    except ValueError as exc:
        raise ReleaseArchiveError("release output resolved outside the repository") from exc
    if not resolved_relative.parts or resolved_relative.parts[0] != "dist":
        raise ReleaseArchiveError("release output resolved outside dist/")
    return resolved


def _zip_payload(package_root: Path) -> bytes:
    package.verify_package(package_root)
    files = sorted(
        (path for path in package_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(package_root).as_posix(),
    )
    with tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024) as output:
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
            for path in files:
                relative = path.relative_to(package_root).as_posix()
                info = zipfile.ZipInfo(
                    f"{package.PLUGIN_NAME}/{relative}", date_time=FIXED_ZIP_TIMESTAMP
                )
                info.create_system = 3
                info.external_attr = REGULAR_FILE_MODE << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, path.read_bytes())
        output.seek(0)
        return output.read()


def verify_release_archive(
    archive_path: Path, checksum_path: Path | None = None
) -> dict[str, Any]:
    metadata = validate_release_metadata()
    expected_manifest = package.validate_contract()["expected_package_manifest"]
    try:
        archive_bytes = archive_path.read_bytes()
    except OSError as exc:
        raise ReleaseArchiveError("release archive is missing") from exc
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            members = archive.infolist()
            actual_names = [member.filename for member in members]
            expected_names = [
                f"{package.PLUGIN_NAME}/{relative}"
                for relative in sorted(expected_manifest)
            ]
            if actual_names != expected_names:
                raise ReleaseArchiveError("release archive file inventory drifted")
            for member in members:
                relative = member.filename.removeprefix(f"{package.PLUGIN_NAME}/")
                if (
                    member.is_dir()
                    or member.date_time != FIXED_ZIP_TIMESTAMP
                    or member.compress_type != zipfile.ZIP_STORED
                    or (member.external_attr >> 16) != REGULAR_FILE_MODE
                ):
                    raise ReleaseArchiveError("release archive metadata drifted")
                if sha256_bytes(archive.read(member)) != expected_manifest[relative]:
                    raise ReleaseArchiveError(
                        f"release archive content drifted: {relative}"
                    )
    except (OSError, zipfile.BadZipFile) as exc:
        raise ReleaseArchiveError("release archive is not a valid ZIP file") from exc

    archive_sha256 = sha256_bytes(archive_bytes)
    if checksum_path is not None:
        try:
            checksum = checksum_path.read_text(encoding="ascii")
        except OSError as exc:
            raise ReleaseArchiveError("release checksum file is missing") from exc
        expected_line = f"{archive_sha256}  {archive_path.name}\n"
        if checksum != expected_line:
            raise ReleaseArchiveError("release checksum file drifted")
    return {
        **metadata,
        "archive": archive_path.name,
        "archive_sha256": archive_sha256,
        "package_files": len(expected_manifest),
        "package_manifest_sha256": package.path_hash_manifest_sha256(
            expected_manifest
        ),
    }


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_release_archive(
    output_directory: Path = DIST_ROOT, *, tag: str | None = None
) -> dict[str, Any]:
    validate_release_metadata(tag)
    output_directory = guarded_output_directory(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    PRIVATE_BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(prefix=".build-", dir=PRIVATE_BUILD_ROOT)
    )
    package_root = temporary_root / package.PLUGIN_NAME
    archive_path = output_directory / archive_filename()
    checksum_path = output_directory / checksum_filename()
    try:
        package.build_package(package_root)
        archive_payload = _zip_payload(package_root)
        _atomic_write(archive_path, archive_payload)
        archive_sha256 = sha256_bytes(archive_payload)
        _atomic_write(
            checksum_path,
            f"{archive_sha256}  {archive_path.name}\n".encode("ascii"),
        )
        result = verify_release_archive(archive_path, checksum_path)
        result["archive_path"] = str(archive_path)
        result["checksum_path"] = str(checksum_path)
        return result
    finally:
        if temporary_root.exists():
            package.reject_link_tree(temporary_root, label="temporary release build")
            shutil.rmtree(temporary_root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a deterministic CoTend pre-release ZIP and SHA-256 file."
    )
    parser.add_argument("--output-directory", type=Path, default=DIST_ROOT)
    parser.add_argument("--check-tag")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = build_release_archive(
            args.output_directory, tag=args.check_tag
        )
    except (ReleaseArchiveError, package.PluginPackageError) as exc:
        print(f"RELEASE_ARCHIVE_FAILED reason={exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
    else:
        print(
            "RELEASE_ARCHIVE_OK "
            f"tag={result['tag']} files={result['package_files']} "
            f"archive={result['archive']} sha256={result['archive_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
