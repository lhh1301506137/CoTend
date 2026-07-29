from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in os.sys.path:
    os.sys.path.insert(0, str(SRC))

from cotend_delivery import Artifact, DeliveryError  # noqa: E402


FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
LOCK_PATHS = (
    PurePosixPath("delivery/codex-artifact.lock.json"),
    PurePosixPath("upstream/framework.lock.json"),
)


class LocalArtifactBuildError(RuntimeError):
    pass


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expected_entries(repository: Path, artifact: Artifact) -> dict[str, bytes]:
    prefix = PurePosixPath(artifact.artifact_id)
    entries: dict[str, bytes] = {}
    for relative, expected_digest in sorted(artifact.files.items()):
        relative_path = PurePosixPath(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise LocalArtifactBuildError(f"unsafe Skill path: {relative}")
        payload = artifact.root.joinpath(*relative_path.parts).read_bytes()
        if sha256_bytes(payload) != expected_digest:
            raise LocalArtifactBuildError(f"Skill changed during build: {relative}")
        entries[(prefix / "skills" / relative_path).as_posix()] = payload
    for relative_path in LOCK_PATHS:
        source = repository.joinpath(*relative_path.parts)
        if not source.is_file() or source.is_symlink():
            raise LocalArtifactBuildError(f"required lock is missing: {relative_path}")
        entries[(prefix / relative_path).as_posix()] = source.read_bytes()
    return dict(sorted(entries.items()))


def archive_bytes(repository: Path | str = ROOT) -> tuple[Artifact, bytes]:
    repository_path = Path(repository).resolve()
    try:
        artifact = Artifact.from_repository(repository_path)
    except DeliveryError as exc:
        raise LocalArtifactBuildError(
            f"repository artifact is not trusted: {exc}"
        ) from exc
    entries = expected_entries(repository_path, artifact)
    if len(entries) != len(artifact.files) + len(LOCK_PATHS):
        raise LocalArtifactBuildError("local archive entry inventory drifted")

    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for name, payload in entries.items():
            info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(
                info,
                payload,
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    payload = buffer.getvalue()
    verify_archive_bytes(repository_path, artifact, payload)
    return artifact, payload


def verify_archive_bytes(
    repository: Path,
    artifact: Artifact,
    payload: bytes,
) -> None:
    expected = expected_entries(repository, artifact)
    try:
        with zipfile.ZipFile(io.BytesIO(payload), mode="r") as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if names != sorted(expected) or len(names) != len(set(names)):
                raise LocalArtifactBuildError("local archive path inventory drifted")
            for info in infos:
                if (
                    info.date_time != FIXED_TIMESTAMP
                    or info.compress_type != zipfile.ZIP_DEFLATED
                    or (info.external_attr >> 16) != 0o100644
                    or info.is_dir()
                ):
                    raise LocalArtifactBuildError(
                        f"local archive metadata drifted: {info.filename}"
                    )
                if archive.read(info) != expected[info.filename]:
                    raise LocalArtifactBuildError(
                        f"local archive payload drifted: {info.filename}"
                    )
            if archive.testzip() is not None:
                raise LocalArtifactBuildError("local archive CRC verification failed")
    except zipfile.BadZipFile as exc:
        raise LocalArtifactBuildError("local artifact is not a valid ZIP") from exc


def output_name(artifact: Artifact) -> str:
    return f"{artifact.artifact_id}-local-" f"{artifact.manifest_sha256[:12]}.zip"


def build_local_artifact(
    repository: Path | str = ROOT,
    output_dir: Path | str | None = None,
) -> dict[str, Any]:
    repository_path = Path(repository).resolve()
    artifact, first = archive_bytes(repository_path)
    repeated_artifact, second = archive_bytes(repository_path)
    if repeated_artifact != artifact or second != first:
        raise LocalArtifactBuildError(
            "two local artifact builds are not byte-identical"
        )

    destination_root = (
        repository_path / "dist" / "local"
        if output_dir is None
        else Path(output_dir).resolve()
    )
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / output_name(artifact)
    if destination.exists():
        if not destination.is_file() or destination.is_symlink():
            raise LocalArtifactBuildError(
                "local artifact destination is not a normal file"
            )
        if destination.read_bytes() != first:
            raise LocalArtifactBuildError(
                "refusing to replace a different existing local artifact"
            )
    else:
        handle, temporary_name = tempfile.mkstemp(
            prefix=f".{artifact.artifact_id}-",
            suffix=".zip.tmp",
            dir=destination_root,
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(handle, "wb") as stream:
                stream.write(first)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        finally:
            if temporary.exists():
                temporary.unlink()

    return {
        "status": "built_verified_local",
        "artifact_id": artifact.artifact_id,
        "revision": artifact.revision,
        "framework_protocol": artifact.protocol,
        "skill_count": len(artifact.skills),
        "skill_file_count": len(artifact.files),
        "archive_entry_count": len(artifact.files) + len(LOCK_PATHS),
        "manifest_sha256": artifact.manifest_sha256,
        "archive_sha256": sha256_bytes(first),
        "reproducible_builds": 2,
        "output": str(destination),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the deterministic, local-only CoTend Codex artifact."
    )
    parser.add_argument("--repository", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = build_local_artifact(args.repository, args.output_dir)
    except (OSError, LocalArtifactBuildError) as exc:
        print(f"LOCAL_CODEX_ARTIFACT_BUILD_FAILED reason={exc}")
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(
            "LOCAL_CODEX_ARTIFACT_BUILD_OK "
            f"artifact={result['artifact_id']} "
            f"skills={result['skill_count']} "
            f"files={result['skill_file_count']} "
            f"entries={result['archive_entry_count']} "
            f"sha256={result['archive_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
