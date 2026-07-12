from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_SKILLS = (
    "cotend-collaboration",
    "cotend-diagnose-only",
    "cotend-init",
    "cotend-model-upgrade",
    "cotend-project-init",
    "grill-me",
    "karpathy-guidelines",
)
EXPECTED_FILE_COUNT = 30
RECEIPT_SCHEMA = "cotend.delivery-receipt"
CHECKPOINT_SCHEMA = "cotend.delivery-checkpoint"
TARGET_LOCK_SCHEMA = "cotend.target-artifact-lock"
TARGET_LOCK_SCHEMA_VERSION = 1
RECEIPT_SCHEMA_VERSION = 2
CHECKPOINT_SCHEMA_VERSION = 2
LEGACY_SCHEMA_VERSION = 1
TARGET_PLATFORM = "Codex"
TARGET_LINEAGE = "cotend-codex"
OPERATIONS = {
    "inspect",
    "install",
    "update",
    "repair",
    "migrate_identity",
    "enable",
    "disable",
    "uninstall",
    "rollback",
}


class DeliveryError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = details or {}

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "blocked",
            "error": self.code,
            "message": str(self),
            "details": self.details,
        }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest_digest(files: dict[str, str]) -> str:
    encoded = json.dumps(
        files,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _target_artifact_id(lineage: str, revision: int) -> str:
    return f"{lineage}-r{revision:06d}"


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _is_linklike(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def _validate_relative_file(value: str, skills: set[str]) -> None:
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or len(relative.parts) < 2:
        raise DeliveryError("invalid_manifest_path", f"Unsafe artifact path: {value}")
    if relative.parts[0] not in skills:
        raise DeliveryError(
            "invalid_manifest_path",
            f"Artifact path is outside its declared skills: {value}",
        )


def _assert_no_symlinks(root: Path, *, label: str) -> None:
    if _is_linklike(root):
        raise DeliveryError("symlink_boundary", f"{label} cannot be a symlink")
    if not root.exists():
        return
    for path in root.rglob("*"):
        if _is_linklike(path):
            raise DeliveryError(
                "symlink_boundary",
                f"{label} contains a symlink: {path.relative_to(root).as_posix()}",
            )


def _directory_manifest(root: Path, skills: tuple[str, ...]) -> dict[str, str]:
    manifest: dict[str, str] = {}
    for skill in skills:
        skill_root = root / skill
        if _is_linklike(skill_root):
            raise DeliveryError(
                "symlink_boundary",
                f"Managed Skill path cannot be a symlink: {skill}",
            )
        if not skill_root.exists():
            continue
        if not skill_root.is_dir():
            raise DeliveryError(
                "invalid_payload",
                f"Managed Skill path is not a normal directory: {skill}",
            )
        for path in sorted(skill_root.rglob("*")):
            if _is_linklike(path):
                raise DeliveryError(
                    "symlink_boundary",
                    f"Managed Skill contains a symlink: {path}",
                )
            if path.is_file():
                manifest[path.relative_to(root).as_posix()] = _sha256(path)
    return manifest


@dataclass(frozen=True)
class LegacyReceiptMapping:
    receipt_schema_version: int
    artifact_id: str
    protocol: str
    manifest_sha256: str
    target_artifact_id: str
    target_revision: int

    def matches(self, receipt: dict[str, Any]) -> bool:
        return (
            receipt.get("schema_version") == self.receipt_schema_version
            and receipt.get("artifact_id") == self.artifact_id
            and receipt.get("protocol") == self.protocol
            and receipt.get("manifest_sha256") == self.manifest_sha256
        )


@dataclass(frozen=True)
class Artifact:
    source_release_id: str
    platform: str
    lineage: str
    artifact_id: str
    revision: int
    protocol: str
    root: Path
    skills: tuple[str, ...]
    files: dict[str, str]
    manifest_sha256: str
    legacy_receipt_mappings: tuple[LegacyReceiptMapping, ...]

    @classmethod
    def from_directory(
        cls,
        root: Path | str,
        *,
        source_release_id: str,
        artifact_id: str,
        revision: int,
        protocol: str,
        platform: str = TARGET_PLATFORM,
        lineage: str = TARGET_LINEAGE,
        legacy_receipt_mappings: tuple[LegacyReceiptMapping, ...] = (),
    ) -> "Artifact":
        string_identity = (
            source_release_id,
            platform,
            lineage,
            artifact_id,
            protocol,
        )
        if not all(isinstance(value, str) and value.strip() for value in string_identity):
            raise DeliveryError(
                "artifact_identity_invalid",
                "Artifact source, target identity, and protocol must be non-empty",
            )
        if platform != TARGET_PLATFORM or lineage != TARGET_LINEAGE:
            raise DeliveryError(
                "artifact_identity_invalid",
                "Artifact platform or lineage is not supported",
            )
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
            raise DeliveryError(
                "artifact_identity_invalid",
                "Artifact revision must be a positive integer",
            )
        if artifact_id != _target_artifact_id(lineage, revision):
            raise DeliveryError(
                "artifact_identity_invalid",
                "Artifact ID does not match its lineage and revision",
            )
        source = Path(root)
        if _is_linklike(source):
            raise DeliveryError("symlink_boundary", "Artifact root cannot be a symlink")
        source = source.resolve()
        if not source.is_dir():
            raise DeliveryError("artifact_missing", f"Artifact root is missing: {source}")
        _assert_no_symlinks(source, label="Artifact")

        entries = {path.name for path in source.iterdir()}
        expected = set(EXPECTED_SKILLS)
        if entries != expected:
            raise DeliveryError(
                "artifact_skill_inventory",
                "Artifact Skill inventory does not match the adopted CoTend set",
                details={
                    "missing": sorted(expected - entries),
                    "unexpected": sorted(entries - expected),
                },
            )
        for skill in EXPECTED_SKILLS:
            if not (source / skill / "SKILL.md").is_file():
                raise DeliveryError(
                    "artifact_skill_invalid",
                    f"Artifact Skill is missing SKILL.md: {skill}",
                )

        files = _directory_manifest(source, EXPECTED_SKILLS)
        if len(files) != EXPECTED_FILE_COUNT:
            raise DeliveryError(
                "artifact_file_inventory",
                f"Expected {EXPECTED_FILE_COUNT} artifact files, found {len(files)}",
            )
        manifest_sha256 = _manifest_digest(files)
        legacy_keys: set[tuple[int, str, str, str]] = set()
        for mapping in legacy_receipt_mappings:
            if not isinstance(mapping, LegacyReceiptMapping):
                raise DeliveryError(
                    "artifact_identity_invalid",
                    "Legacy receipt mapping has an invalid type",
                )
            key = (
                mapping.receipt_schema_version,
                mapping.artifact_id,
                mapping.protocol,
                mapping.manifest_sha256,
            )
            if (
                mapping.receipt_schema_version != LEGACY_SCHEMA_VERSION
                or not mapping.artifact_id
                or not mapping.protocol
                or not _is_sha256(mapping.manifest_sha256)
                or mapping.target_artifact_id != artifact_id
                or mapping.target_revision != revision
                or mapping.protocol != protocol
                or mapping.manifest_sha256 != manifest_sha256
                or key in legacy_keys
            ):
                raise DeliveryError(
                    "artifact_identity_invalid",
                    "Legacy receipt mapping does not match the target artifact",
                )
            legacy_keys.add(key)
        return cls(
            source_release_id=source_release_id,
            platform=platform,
            lineage=lineage,
            artifact_id=artifact_id,
            revision=revision,
            protocol=protocol,
            root=source,
            skills=EXPECTED_SKILLS,
            files=files,
            manifest_sha256=manifest_sha256,
            legacy_receipt_mappings=legacy_receipt_mappings,
        )

    @classmethod
    def from_repository(cls, repository: Path | str) -> "Artifact":
        root = Path(repository).resolve()
        lock_path = root / "upstream" / "framework.lock.json"
        target_lock_path = root / "delivery" / "codex-artifact.lock.json"
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            target_lock = json.loads(target_lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DeliveryError(
                "framework_lock_invalid",
                "Cannot read the adopted framework lock and target artifact lock",
            ) from exc
        if (
            lock.get("schema") != "cotend.framework-lock"
            or lock.get("schema_version") != 1
            or lock.get("status") != "adopted_verified"
            or lock.get("target_platform") != "Codex"
        ):
            raise DeliveryError(
                "framework_lock_untrusted",
                "Framework lock identity or adoption status is not trusted",
            )
        if (
            not isinstance(target_lock, dict)
            or target_lock.get("schema") != TARGET_LOCK_SCHEMA
            or target_lock.get("schema_version") != TARGET_LOCK_SCHEMA_VERSION
            or target_lock.get("status") != "verified"
        ):
            raise DeliveryError(
                "target_lock_untrusted",
                "Target artifact lock identity or status is not trusted",
            )
        carrier = PurePosixPath(str(lock.get("source_carrier", "")))
        if (
            carrier != PurePosixPath("codex-skills")
            or carrier.is_absolute()
            or ".." in carrier.parts
        ):
            raise DeliveryError("framework_lock_invalid", "Unsafe source carrier path")
        source_identity = target_lock.get("source")
        target_identity = target_lock.get("target")
        product_identity = target_lock.get("product")
        if not all(
            isinstance(value, dict)
            for value in (source_identity, target_identity, product_identity)
        ):
            raise DeliveryError("target_lock_invalid", "Target lock sections are invalid")
        assert isinstance(source_identity, dict)
        assert isinstance(target_identity, dict)
        assert isinstance(product_identity, dict)
        if source_identity != {
            "framework_lock": "upstream/framework.lock.json",
            "release_id": lock.get("release_id"),
            "carrier": lock.get("source_carrier"),
            "framework_protocol": lock.get("framework_protocol"),
        }:
            raise DeliveryError(
                "target_lock_mismatch",
                "Target artifact source identity differs from the adopted framework lock",
            )
        if product_identity != {"version": None}:
            raise DeliveryError(
                "target_lock_invalid",
                "Target lock product version must remain undecided",
            )
        mappings_value = target_lock.get("legacy_receipt_mappings")
        if not isinstance(mappings_value, list):
            raise DeliveryError(
                "target_lock_invalid",
                "Legacy receipt mappings are not a list",
            )
        mappings: list[LegacyReceiptMapping] = []
        for value in mappings_value:
            if not isinstance(value, dict):
                raise DeliveryError(
                    "target_lock_invalid",
                    "Legacy receipt mapping is not an object",
                )
            try:
                mappings.append(
                    LegacyReceiptMapping(
                        receipt_schema_version=value["receipt_schema_version"],
                        artifact_id=value["artifact_id"],
                        protocol=value["protocol"],
                        manifest_sha256=value["manifest_sha256"],
                        target_artifact_id=value["target_artifact_id"],
                        target_revision=value["target_revision"],
                    )
                )
            except KeyError as exc:
                raise DeliveryError(
                    "target_lock_invalid",
                    "Legacy receipt mapping is missing an identity field",
                ) from exc
        artifact = cls.from_directory(
            root.joinpath(*carrier.parts),
            source_release_id=str(source_identity.get("release_id", "")),
            platform=str(target_identity.get("platform", "")),
            lineage=str(target_identity.get("lineage", "")),
            artifact_id=str(target_identity.get("artifact_id", "")),
            revision=target_identity.get("revision"),
            protocol=str(lock.get("framework_protocol", "")),
            legacy_receipt_mappings=tuple(mappings),
        )
        if lock.get("skill_count") != len(artifact.skills):
            raise DeliveryError("framework_lock_mismatch", "Skill count differs from lock")
        if lock.get("skill_file_count") != len(artifact.files):
            raise DeliveryError("framework_lock_mismatch", "File count differs from lock")
        if (
            target_lock.get("skill_count") != len(artifact.skills)
            or target_lock.get("skill_file_count") != len(artifact.files)
            or target_identity.get("manifest_sha256") != artifact.manifest_sha256
            or lock.get("target_platform") != artifact.platform
        ):
            raise DeliveryError(
                "target_lock_mismatch",
                "Target artifact inventory or manifest differs from the repository carrier",
            )
        mapping = lock.get("skill_mapping", [])
        if not isinstance(mapping, list):
            raise DeliveryError("framework_lock_mismatch", "Skill mapping is not a list")
        mapped = {
            item.get("target")
            for item in mapping
            if isinstance(item, dict)
        }
        if len(mapping) != len(artifact.skills) or mapped != set(artifact.skills):
            raise DeliveryError(
                "framework_lock_mismatch",
                "Target Skill mapping differs from artifact",
            )
        return artifact


class DeliveryManager:
    def __init__(self, project: Path | str) -> None:
        raw = Path(project)
        if _is_linklike(raw):
            raise DeliveryError("symlink_boundary", "Project root cannot be a symlink")
        self.project = raw.resolve()
        if not self.project.is_dir():
            raise DeliveryError(
                "project_missing",
                f"Target project directory is missing: {self.project}",
            )
        self.agents_root = self.project / ".agents"
        self.enabled_root = self.agents_root / "skills"
        self.state_root = self.agents_root / ".cotend-delivery"
        self.disabled_root = self.state_root / "disabled-skills"
        self.receipt_path = self.state_root / "receipt.json"
        self.receipt_temp_path = self.state_root / "receipt.json.tmp"
        self.rollback_path = self.state_root / "rollback"
        self.rollback_new_path = self.state_root / "rollback.new"
        self.previous_rollback_path = self.state_root / "rollback.previous"
        self.staging_path = self.state_root / "staging"
        self._assert_target_boundaries()

    def _assert_target_boundaries(self) -> None:
        for path, label in (
            (self.agents_root, ".agents"),
            (self.enabled_root, "Skill carrier"),
            (self.state_root, "delivery state"),
            (self.disabled_root, "disabled Skill carrier"),
            (self.rollback_path, "rollback checkpoint"),
            (self.previous_rollback_path, "previous rollback checkpoint"),
            (self.rollback_new_path, "new rollback checkpoint"),
            (self.staging_path, "staging area"),
        ):
            if _is_linklike(path):
                raise DeliveryError("symlink_boundary", f"{label} cannot be a symlink")
            if path.exists() and not path.is_dir():
                raise DeliveryError(
                    "invalid_boundary",
                    f"{label} must be a directory when present",
                )
        if _is_linklike(self.receipt_temp_path):
            raise DeliveryError(
                "symlink_boundary",
                "Receipt temporary path cannot be a symlink",
            )
        if self.receipt_temp_path.exists() and not self.receipt_temp_path.is_file():
            raise DeliveryError(
                "invalid_boundary",
                "Receipt temporary path must be a file when present",
            )

    def _receipt_payload(self, artifact: Artifact, *, enabled: bool) -> dict[str, Any]:
        now = _utc_now()
        previous = self._load_receipt(required=False)
        installed_at = previous.get("installed_at", now) if previous else now
        return {
            "schema": RECEIPT_SCHEMA,
            "schema_version": RECEIPT_SCHEMA_VERSION,
            "platform": artifact.platform,
            "scope": "project",
            "source_release_id": artifact.source_release_id,
            "artifact_lineage": artifact.lineage,
            "artifact_id": artifact.artifact_id,
            "target_revision": artifact.revision,
            "protocol": artifact.protocol,
            "manifest_sha256": artifact.manifest_sha256,
            "skills": list(artifact.skills),
            "files": artifact.files,
            "enabled": enabled,
            "installed_at": installed_at,
            "updated_at": now,
        }

    def _validate_receipt(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise DeliveryError("receipt_invalid", "Delivery receipt is not an object")
        schema_version = value.get("schema_version")
        if (
            value.get("schema") != RECEIPT_SCHEMA
            or schema_version not in {LEGACY_SCHEMA_VERSION, RECEIPT_SCHEMA_VERSION}
        ):
            raise DeliveryError("receipt_invalid", "Unsupported delivery receipt schema")
        if value.get("platform") != TARGET_PLATFORM or value.get("scope") != "project":
            raise DeliveryError("receipt_invalid", "Receipt target boundary is invalid")
        skills = value.get("skills")
        files = value.get("files")
        if not isinstance(skills, list) or skills != list(EXPECTED_SKILLS):
            raise DeliveryError("receipt_invalid", "Receipt Skill inventory is invalid")
        if not isinstance(files, dict) or len(files) != EXPECTED_FILE_COUNT:
            raise DeliveryError("receipt_invalid", "Receipt file inventory is invalid")
        skill_set = set(skills)
        for path, digest in files.items():
            if not isinstance(path, str) or not isinstance(digest, str):
                raise DeliveryError("receipt_invalid", "Receipt file entry is invalid")
            _validate_relative_file(path, skill_set)
            if not _is_sha256(digest):
                raise DeliveryError("receipt_invalid", "Receipt file hash is invalid")
        if value.get("manifest_sha256") != _manifest_digest(files):
            raise DeliveryError("receipt_invalid", "Receipt manifest digest is invalid")
        if not all(f"{skill}/SKILL.md" in files for skill in EXPECTED_SKILLS):
            raise DeliveryError("receipt_invalid", "Receipt is missing a Skill entry point")
        if not isinstance(value.get("artifact_id"), str) or not value["artifact_id"]:
            raise DeliveryError("receipt_invalid", "Receipt artifact identity is missing")
        if not isinstance(value.get("protocol"), str) or not value["protocol"]:
            raise DeliveryError("receipt_invalid", "Receipt protocol is missing")
        if schema_version == LEGACY_SCHEMA_VERSION and any(
            key in value
            for key in ("source_release_id", "artifact_lineage", "target_revision")
        ):
            raise DeliveryError(
                "receipt_invalid",
                "Legacy receipt contains schema v2 identity fields",
            )
        if schema_version == RECEIPT_SCHEMA_VERSION:
            revision = value.get("target_revision")
            lineage = value.get("artifact_lineage")
            if (
                not isinstance(value.get("source_release_id"), str)
                or not value["source_release_id"]
                or lineage != TARGET_LINEAGE
                or isinstance(revision, bool)
                or not isinstance(revision, int)
                or revision < 1
                or value["artifact_id"] != _target_artifact_id(lineage, revision)
            ):
                raise DeliveryError(
                    "receipt_invalid",
                    "Receipt source or target revision identity is invalid",
                )
        if not isinstance(value.get("enabled"), bool):
            raise DeliveryError("receipt_invalid", "Receipt enablement is invalid")
        if not all(
            isinstance(value.get(key), str) and value[key]
            for key in ("installed_at", "updated_at")
        ):
            raise DeliveryError("receipt_invalid", "Receipt timestamps are invalid")
        return value

    def _load_receipt(self, *, required: bool) -> dict[str, Any] | None:
        if not self.receipt_path.exists():
            if required:
                raise DeliveryError("receipt_missing", "Delivery receipt is missing")
            return None
        if _is_linklike(self.receipt_path) or not self.receipt_path.is_file():
            raise DeliveryError("receipt_invalid", "Delivery receipt is not a normal file")
        try:
            value = json.loads(self.receipt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DeliveryError("receipt_invalid", "Delivery receipt cannot be parsed") from exc
        return self._validate_receipt(value)

    @staticmethod
    def _legacy_mapping(
        receipt: dict[str, Any],
        candidate: Artifact,
    ) -> LegacyReceiptMapping | None:
        return next(
            (
                mapping
                for mapping in candidate.legacy_receipt_mappings
                if mapping.matches(receipt)
            ),
            None,
        )

    def _candidate_relation(
        self,
        receipt: dict[str, Any],
        candidate: Artifact | None,
    ) -> tuple[str, list[str]]:
        if candidate is None:
            return "none", []
        if receipt["schema_version"] == LEGACY_SCHEMA_VERSION:
            if (
                self._legacy_mapping(receipt, candidate) is not None
                and receipt["files"] == candidate.files
            ):
                return "identity_migration_available", []
            return "incompatible", ["legacy_identity_unmapped"]

        exact_identity = (
            receipt["platform"] == candidate.platform
            and receipt["source_release_id"] == candidate.source_release_id
            and receipt["artifact_lineage"] == candidate.lineage
            and receipt["artifact_id"] == candidate.artifact_id
            and receipt["target_revision"] == candidate.revision
            and receipt["protocol"] == candidate.protocol
            and receipt["manifest_sha256"] == candidate.manifest_sha256
        )
        if exact_identity:
            return "same_as_current", []
        if (
            receipt["platform"] != candidate.platform
            or receipt["artifact_lineage"] != candidate.lineage
        ):
            return "incompatible", ["artifact_lineage_conflict"]
        if receipt["protocol"] != candidate.protocol:
            return "incompatible", ["protocol_incompatible"]
        if receipt["target_revision"] == candidate.revision:
            return "incompatible", ["artifact_identity_conflict"]
        if candidate.revision > receipt["target_revision"]:
            return "update_available", []
        return "downgrade_candidate", ["downgrade_requires_explicit_operation"]

    def _collision_paths_without_receipt(self) -> list[str]:
        collisions: list[str] = []
        for root in (self.enabled_root, self.disabled_root):
            for skill in EXPECTED_SKILLS:
                path = root / skill
                if path.exists() or _is_linklike(path):
                    collisions.append(path.relative_to(self.project).as_posix())
        return sorted(collisions)

    def _state_residue_without_receipt(
        self,
        *,
        include_previous_rollback: bool,
    ) -> list[str]:
        if not self.state_root.is_dir():
            return []
        allowed = {self.rollback_path}
        if not include_previous_rollback:
            allowed.add(self.previous_rollback_path)
        return sorted(
            path.relative_to(self.project).as_posix()
            for path in self.state_root.iterdir()
            if path not in allowed
        )

    def _shadow_payload_paths(self, *, enabled: bool) -> list[str]:
        opposite_root = self.disabled_root if enabled else self.enabled_root
        return sorted(
            path.relative_to(self.project).as_posix()
            for skill in EXPECTED_SKILLS
            if (path := opposite_root / skill).exists() or _is_linklike(path)
        )

    def _transition_artifacts(self, *, include_previous_rollback: bool) -> list[str]:
        paths = [self.staging_path, self.rollback_new_path, self.receipt_temp_path]
        if include_previous_rollback:
            paths.append(self.previous_rollback_path)
        return [path.name for path in paths if path.exists() or _is_linklike(path)]

    def inspect(self, candidate: Artifact | None = None) -> dict[str, Any]:
        return self._inspect(candidate, include_previous_rollback=True)

    def _inspect(
        self,
        candidate: Artifact | None,
        *,
        include_previous_rollback: bool,
    ) -> dict[str, Any]:
        self._assert_target_boundaries()
        rollback_available = self.rollback_path.is_dir()
        transition_artifacts = self._transition_artifacts(
            include_previous_rollback=include_previous_rollback
        )
        try:
            receipt = self._load_receipt(required=False)
        except DeliveryError as exc:
            return {
                "schema": "cotend.delivery-state",
                "project": str(self.project),
                "receipt_valid": False,
                "acquisition": "not_required",
                "installation": "unknown",
                "enablement": "unknown",
                "invocation": "unavailable",
                "candidate_relation": "unknown",
                "transition": "recovery_required",
                "artifact_id": None,
                "candidate_id": candidate.artifact_id if candidate else None,
                "missing": [],
                "modified": [],
                "unexpected": [],
                "transition_artifacts": transition_artifacts,
                "rollback_available": rollback_available,
                "recommended_operation": "manual_resolution",
                "diagnostics": [exc.code],
            }

        if receipt is None:
            collisions = self._collision_paths_without_receipt()
            state_residue = self._state_residue_without_receipt(
                include_previous_rollback=include_previous_rollback
            )
            if collisions or state_residue or transition_artifacts:
                diagnostics = []
                if collisions:
                    diagnostics.append("unowned_collision")
                if state_residue:
                    diagnostics.append("unowned_delivery_state")
                return {
                    "schema": "cotend.delivery-state",
                    "project": str(self.project),
                    "receipt_valid": False,
                    "acquisition": "not_required",
                    "installation": "unknown",
                    "enablement": "unknown",
                    "invocation": "unavailable",
                    "candidate_relation": "unknown",
                    "transition": "recovery_required",
                    "artifact_id": None,
                    "candidate_id": candidate.artifact_id if candidate else None,
                    "missing": [],
                    "modified": [],
                    "unexpected": sorted(collisions + state_residue),
                    "transition_artifacts": transition_artifacts,
                    "rollback_available": rollback_available,
                    "recommended_operation": "manual_resolution",
                    "diagnostics": diagnostics,
                }
            return {
                "schema": "cotend.delivery-state",
                "project": str(self.project),
                "receipt_valid": True,
                "acquisition": "not_started" if candidate else "not_required",
                "installation": "absent",
                "enablement": "not_applicable",
                "invocation": "unavailable",
                "candidate_relation": "install_candidate" if candidate else "none",
                "transition": "stable",
                "artifact_id": None,
                "candidate_id": candidate.artifact_id if candidate else None,
                "missing": [],
                "modified": [],
                "unexpected": [],
                "transition_artifacts": [],
                "rollback_available": rollback_available,
                "recommended_operation": "rollback" if rollback_available else "install",
                "diagnostics": [],
            }

        payload_root = self.enabled_root if receipt["enabled"] else self.disabled_root
        try:
            actual = _directory_manifest(payload_root, tuple(receipt["skills"]))
        except DeliveryError as exc:
            return {
                "schema": "cotend.delivery-state",
                "project": str(self.project),
                "receipt_valid": True,
                "acquisition": "not_required",
                "installation": "unknown",
                "enablement": "unknown",
                "invocation": "unavailable",
                "candidate_relation": "unknown",
                "transition": "recovery_required",
                "artifact_id": receipt["artifact_id"],
                "candidate_id": candidate.artifact_id if candidate else None,
                "missing": [],
                "modified": [],
                "unexpected": [],
                "transition_artifacts": transition_artifacts,
                "rollback_available": rollback_available,
                "recommended_operation": "manual_resolution",
                "diagnostics": [exc.code],
            }

        expected = receipt["files"]
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(
            set(actual) - set(expected)
            | set(self._shadow_payload_paths(enabled=receipt["enabled"]))
        )
        modified = sorted(
            path for path in set(expected) & set(actual) if expected[path] != actual[path]
        )
        if missing:
            installation = "partial"
        elif modified or unexpected:
            installation = "damaged"
        else:
            installation = "complete"

        relation, diagnostics = self._candidate_relation(receipt, candidate)

        complete = installation == "complete" and not transition_artifacts
        if complete:
            enablement = "enabled" if receipt["enabled"] else "disabled"
            invocation = "not_run" if receipt["enabled"] else "unavailable"
            transition = "stable"
        else:
            enablement = "failed" if receipt["enabled"] else "unknown"
            invocation = "failed" if receipt["enabled"] else "unavailable"
            transition = "recovery_required"

        if transition_artifacts or unexpected or relation in {
            "incompatible",
            "downgrade_candidate",
        }:
            recommended = "manual_resolution"
        elif installation != "complete":
            recommended = "repair"
        elif relation == "identity_migration_available":
            recommended = "migrate_identity"
        elif relation == "update_available":
            recommended = "update"
        else:
            recommended = "current_no_change"

        return {
            "schema": "cotend.delivery-state",
            "project": str(self.project),
            "receipt_valid": True,
            "acquisition": "integrity_verified" if candidate else "not_required",
            "installation": installation,
            "enablement": enablement,
            "invocation": invocation,
            "candidate_relation": relation,
            "transition": transition,
            "receipt_schema_version": receipt["schema_version"],
            "source_release_id": receipt.get("source_release_id"),
            "artifact_lineage": receipt.get("artifact_lineage"),
            "artifact_id": receipt["artifact_id"],
            "target_revision": receipt.get("target_revision"),
            "protocol": receipt["protocol"],
            "manifest_sha256": receipt["manifest_sha256"],
            "candidate_source_release_id": (
                candidate.source_release_id if candidate else None
            ),
            "candidate_lineage": candidate.lineage if candidate else None,
            "candidate_id": candidate.artifact_id if candidate else None,
            "candidate_revision": candidate.revision if candidate else None,
            "candidate_manifest_sha256": candidate.manifest_sha256 if candidate else None,
            "managed_skills": list(receipt["skills"]),
            "managed_files": len(expected),
            "missing": missing,
            "modified": modified,
            "unexpected": unexpected,
            "transition_artifacts": transition_artifacts,
            "rollback_available": rollback_available,
            "recommended_operation": recommended,
            "diagnostics": diagnostics,
        }

    def plan(
        self,
        operation: str,
        candidate: Artifact | None = None,
    ) -> dict[str, Any]:
        if operation not in OPERATIONS:
            raise DeliveryError("operation_unknown", f"Unknown operation: {operation}")
        if operation in {"install", "update", "repair", "migrate_identity"} and candidate is None:
            raise DeliveryError(
                "candidate_required",
                f"{operation} requires an exact candidate artifact",
            )

        state = self.inspect(candidate)
        if operation == "inspect":
            return {
                "operation": operation,
                "allowed": True,
                "will_mutate": False,
                "reason": "read_only_inspection",
                "state": state,
                "effects": [],
            }

        allowed = False
        will_mutate = False
        reason = "operation_not_allowed_from_current_state"
        effects: list[str] = []

        if operation == "install":
            if state["installation"] == "absent" and state["transition"] == "stable":
                allowed = will_mutate = True
                reason = "install_candidate_into_absent_project_scope"
            elif (
                state["installation"] == "complete"
                and state["candidate_relation"] == "same_as_current"
            ):
                allowed = True
                reason = "current_no_change"
        elif operation == "update":
            if (
                state["installation"] == "complete"
                and state["transition"] == "stable"
                and state["candidate_relation"] == "update_available"
            ):
                allowed = will_mutate = True
                reason = "replace_complete_managed_installation"
            elif (
                state["installation"] == "complete"
                and state["candidate_relation"] == "same_as_current"
            ):
                allowed = True
                reason = "current_no_change"
        elif operation == "repair":
            if state["unexpected"] or state["transition_artifacts"]:
                reason = "repair_refuses_unowned_or_interrupted_state"
            elif state["installation"] in {"partial", "damaged"}:
                assert candidate is not None
                relation = state["candidate_relation"]
                if relation in {"same_as_current", "identity_migration_available"}:
                    allowed = will_mutate = True
                    reason = (
                        "reconstruct_legacy_owned_files_and_migrate_identity"
                        if relation == "identity_migration_available"
                        else "reconstruct_owned_files_from_same_artifact"
                    )
                else:
                    reason = "repair_candidate_does_not_match_receipt"
            elif (
                state["installation"] == "complete"
                and state["candidate_relation"] == "same_as_current"
            ):
                allowed = True
                reason = "current_no_change"
        elif operation == "migrate_identity":
            if (
                state["installation"] == "complete"
                and state["transition"] == "stable"
                and state["candidate_relation"] == "identity_migration_available"
            ):
                allowed = will_mutate = True
                reason = "rebind_verified_legacy_receipt_to_target_identity"
        elif operation == "disable":
            if state["installation"] == "complete" and state["enablement"] == "enabled":
                allowed = will_mutate = True
                reason = "disable_complete_managed_installation"
            elif state["installation"] == "complete" and state["enablement"] == "disabled":
                allowed = True
                reason = "current_no_change"
        elif operation == "enable":
            if state["installation"] == "complete" and state["enablement"] == "disabled":
                allowed = will_mutate = True
                reason = "enable_complete_managed_installation"
            elif state["installation"] == "complete" and state["enablement"] == "enabled":
                allowed = True
                reason = "current_no_change"
        elif operation == "uninstall":
            if state["installation"] == "complete" and state["transition"] == "stable":
                allowed = will_mutate = True
                reason = "remove_exact_product_owned_installation"
        elif operation == "rollback":
            if state["unexpected"]:
                reason = "rollback_refuses_unowned_files"
            elif state["rollback_available"] and not state["transition_artifacts"]:
                self._load_checkpoint_metadata()
                allowed = will_mutate = True
                reason = "restore_latest_verified_checkpoint"

        if will_mutate:
            effects = self._effects(operation, candidate, state)
        return {
            "operation": operation,
            "allowed": allowed,
            "will_mutate": will_mutate,
            "reason": reason,
            "state": state,
            "effects": effects,
        }

    def _effects(
        self,
        operation: str,
        candidate: Artifact | None,
        state: dict[str, Any],
    ) -> list[str]:
        checkpoint = "replace the previous one-step rollback checkpoint"
        if operation in {"install", "update", "repair"}:
            assert candidate is not None
            return [
                checkpoint,
                f"write {len(candidate.skills)} managed Skill directories and {len(candidate.files)} files",
                "write the adapter-owned delivery receipt",
                f"preserve current enablement: {state.get('enablement', 'enabled')}",
            ]
        if operation == "migrate_identity":
            assert candidate is not None
            return [
                checkpoint,
                "preserve the verified managed payload without copying or replacing it",
                "rewrite only the adapter-owned receipt with schema v2 target identity",
                f"bind legacy identity to {candidate.artifact_id}",
            ]
        if operation in {"enable", "disable"}:
            return [
                checkpoint,
                f"move only the {len(EXPECTED_SKILLS)} managed Skill directories inside .agents",
                "update the adapter-owned delivery receipt",
            ]
        if operation == "uninstall":
            return [
                checkpoint,
                "remove only receipt-owned Skill directories and the active receipt",
                "preserve project files, unrelated Skills, and the rollback checkpoint",
            ]
        if operation == "rollback":
            return [
                "restore the latest checkpoint",
                "consume that one-step rollback checkpoint",
            ]
        return []

    def execute(
        self,
        operation: str,
        candidate: Artifact | None = None,
        *,
        apply: bool = False,
    ) -> dict[str, Any]:
        plan = self.plan(operation, candidate)
        if not plan["allowed"]:
            raise DeliveryError(
                "operation_blocked",
                f"{operation} is blocked: {plan['reason']}",
                details={"state": plan["state"]},
            )
        if not apply or not plan["will_mutate"]:
            return {
                "status": "planned" if plan["will_mutate"] else "current_no_change",
                "applied": False,
                "plan": plan,
                "state": plan["state"],
            }

        before = plan["state"]
        if operation == "rollback":
            restored_checkpoint, restored_receipt = self._restore_checkpoint(
                reinstate_previous=False
            )
            self._verify_rollback_postcondition(
                restored_checkpoint,
                restored_receipt,
                candidate,
            )
        else:
            self._create_checkpoint(operation)
            expected_enabled: bool | None = None
            try:
                if operation in {"install", "update", "repair"}:
                    assert candidate is not None
                    if operation == "install":
                        expected_enabled = True
                    else:
                        receipt = self._load_receipt(required=True)
                        assert receipt is not None
                        expected_enabled = receipt["enabled"]
                    self._replace_with_artifact(candidate, enabled=expected_enabled)
                elif operation == "migrate_identity":
                    assert candidate is not None
                    receipt = self._load_receipt(required=True)
                    assert receipt is not None
                    expected_enabled = receipt["enabled"]
                    self._migrate_identity(candidate, enabled=expected_enabled)
                elif operation == "disable":
                    self._move_enablement(enabled=False)
                elif operation == "enable":
                    self._move_enablement(enabled=True)
                elif operation == "uninstall":
                    self._uninstall()
                self._verify_postcondition(
                    operation,
                    candidate,
                    expected_enabled=expected_enabled,
                )
                self._commit_checkpoint()
            except Exception as exc:
                try:
                    self._restore_checkpoint(reinstate_previous=True)
                except Exception as rollback_exc:
                    raise DeliveryError(
                        "transition_and_rollback_failed",
                        f"{operation} failed and rollback also failed",
                        details={
                            "transition_error": str(exc),
                            "rollback_error": str(rollback_exc),
                        },
                    ) from rollback_exc
                raise DeliveryError(
                    "transition_failed_rolled_back",
                    f"{operation} failed; the prior checkpoint was restored",
                    details={"transition_error": str(exc)},
                ) from exc

        after = self.inspect(candidate)
        return {
            "status": "applied",
            "applied": True,
            "operation": operation,
            "plan": plan,
            "state_before": before,
            "state_after": after,
        }

    def _create_checkpoint(self, operation: str) -> None:
        self._assert_target_boundaries()
        receipt = self._load_receipt(required=False)
        payload_mode = "preserve_existing" if operation == "migrate_identity" else "snapshot"
        self.state_root.mkdir(parents=True, exist_ok=True)
        temp = self.rollback_new_path
        if temp.exists() or _is_linklike(temp):
            raise DeliveryError(
                "transition_artifact_collision",
                "New rollback checkpoint path is already occupied",
            )
        rollback_rotated = False
        try:
            temp.mkdir()
            payload_files: dict[str, str] = {}
            payload_skills: list[str] = []
            if receipt:
                shutil.copy2(self.receipt_path, temp / "receipt.json")
                source_root = (
                    self.enabled_root if receipt["enabled"] else self.disabled_root
                )
                payload_files = _directory_manifest(
                    source_root,
                    tuple(receipt["skills"]),
                )
                payload_skills = [
                    skill
                    for skill in receipt["skills"]
                    if (source_root / skill).is_dir()
                ]
                if payload_mode == "snapshot":
                    payload = temp / (
                        "enabled-skills" if receipt["enabled"] else "disabled-skills"
                    )
                    payload.mkdir()
                    for skill in payload_skills:
                        source = source_root / skill
                        shutil.copytree(source, payload / skill)
                    copied_files = _directory_manifest(
                        payload,
                        tuple(receipt["skills"]),
                    )
                    if copied_files != payload_files:
                        raise DeliveryError(
                            "checkpoint_invalid",
                            "Checkpoint copy differs from the current managed payload",
                        )
            metadata = {
                "schema": CHECKPOINT_SCHEMA,
                "schema_version": CHECKPOINT_SCHEMA_VERSION,
                "operation": operation,
                "created_at": _utc_now(),
                "receipt_present": receipt is not None,
                "payload_mode": payload_mode,
                "skills": list(receipt["skills"]) if receipt else [],
                "enabled": receipt["enabled"] if receipt else None,
                "payload_skills": payload_skills,
                "payload_files": payload_files,
                "payload_manifest_sha256": _manifest_digest(payload_files),
            }
            (temp / "checkpoint.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            if (
                self.previous_rollback_path.exists()
                or _is_linklike(self.previous_rollback_path)
            ):
                raise DeliveryError(
                    "transition_artifact_collision",
                    "Previous rollback checkpoint path is already occupied",
                )
            if self.rollback_path.exists():
                os.replace(self.rollback_path, self.previous_rollback_path)
                rollback_rotated = True
            os.replace(temp, self.rollback_path)
        except Exception:
            if rollback_rotated and not self.rollback_path.exists():
                os.replace(self.previous_rollback_path, self.rollback_path)
            if temp.exists():
                shutil.rmtree(temp)
            raise

    def _load_checkpoint_metadata(
        self,
    ) -> tuple[dict[str, Any], dict[str, Any] | None]:
        self._assert_target_boundaries()
        path = self.rollback_path / "checkpoint.json"
        if not path.is_file() or _is_linklike(path):
            raise DeliveryError("checkpoint_invalid", "Rollback checkpoint is invalid")
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DeliveryError("checkpoint_invalid", "Rollback checkpoint cannot be parsed") from exc
        schema_version = value.get("schema_version")
        payload_mode = (
            value.get("payload_mode", "snapshot")
            if schema_version == CHECKPOINT_SCHEMA_VERSION
            else "snapshot"
        )
        if (
            value.get("schema") != CHECKPOINT_SCHEMA
            or schema_version not in {LEGACY_SCHEMA_VERSION, CHECKPOINT_SCHEMA_VERSION}
            or value.get("operation") not in OPERATIONS - {"inspect", "rollback"}
            or not isinstance(value.get("created_at"), str)
            or not value["created_at"]
            or not isinstance(value.get("receipt_present"), bool)
            or not isinstance(value.get("skills"), list)
            or not isinstance(value.get("payload_skills"), list)
            or not isinstance(value.get("payload_files"), dict)
            or not isinstance(value.get("payload_manifest_sha256"), str)
            or payload_mode not in {"snapshot", "preserve_existing"}
            or (
                schema_version == CHECKPOINT_SCHEMA_VERSION
                and "payload_mode" not in value
            )
            or (
                schema_version == LEGACY_SCHEMA_VERSION
                and (
                    "payload_mode" in value
                    or value.get("operation") == "migrate_identity"
                )
            )
            or (
                payload_mode == "preserve_existing"
                and (
                    schema_version != CHECKPOINT_SCHEMA_VERSION
                    or value.get("operation") != "migrate_identity"
                    or value.get("receipt_present") is not True
                )
            )
        ):
            raise DeliveryError("checkpoint_invalid", "Rollback checkpoint metadata is invalid")
        payload_skills = value["payload_skills"]
        payload_files = value["payload_files"]
        if (
            len(payload_skills) != len(set(payload_skills))
            or not set(payload_skills).issubset(set(EXPECTED_SKILLS))
        ):
            raise DeliveryError(
                "checkpoint_invalid",
                "Checkpoint payload Skill inventory is invalid",
            )
        for relative, digest in payload_files.items():
            if not isinstance(relative, str) or not isinstance(digest, str):
                raise DeliveryError(
                    "checkpoint_invalid",
                    "Checkpoint payload file inventory is invalid",
                )
            _validate_relative_file(relative, set(EXPECTED_SKILLS))
            if not _is_sha256(digest):
                raise DeliveryError(
                    "checkpoint_invalid",
                    "Checkpoint payload file hash is invalid",
                )
        if value["payload_manifest_sha256"] != _manifest_digest(payload_files):
            raise DeliveryError(
                "checkpoint_invalid",
                "Checkpoint payload manifest digest is invalid",
            )
        expected_entries = {"checkpoint.json"}
        checkpoint_receipt: dict[str, Any] | None = None
        if value["receipt_present"]:
            receipt_path = self.rollback_path / "receipt.json"
            if not receipt_path.is_file() or _is_linklike(receipt_path):
                raise DeliveryError("checkpoint_invalid", "Checkpoint receipt is missing")
            try:
                checkpoint_receipt = self._validate_receipt(
                    json.loads(receipt_path.read_text(encoding="utf-8"))
                )
            except (OSError, json.JSONDecodeError) as exc:
                raise DeliveryError("checkpoint_invalid", "Checkpoint receipt is invalid") from exc
            if (
                value["skills"] != checkpoint_receipt["skills"]
                or value.get("enabled") != checkpoint_receipt["enabled"]
                or not set(payload_skills).issubset(set(checkpoint_receipt["skills"]))
                or not set(payload_files).issubset(set(checkpoint_receipt["files"]))
            ):
                raise DeliveryError(
                    "checkpoint_invalid",
                    "Checkpoint metadata does not match its receipt",
                )
            if payload_mode == "snapshot":
                payload_name = (
                    "enabled-skills"
                    if checkpoint_receipt["enabled"]
                    else "disabled-skills"
                )
                payload = self.rollback_path / payload_name
                if _is_linklike(payload) or not payload.is_dir():
                    raise DeliveryError(
                        "checkpoint_invalid",
                        "Checkpoint payload is missing or unsafe",
                    )
                payload_entries = {entry.name for entry in payload.iterdir()}
                if payload_entries != set(payload_skills):
                    raise DeliveryError(
                        "checkpoint_invalid",
                        "Checkpoint payload Skill inventory is invalid",
                    )
                actual = _directory_manifest(
                    payload,
                    tuple(checkpoint_receipt["skills"]),
                )
                if actual != payload_files:
                    raise DeliveryError(
                        "checkpoint_invalid",
                        "Checkpoint payload integrity verification failed",
                    )
                expected_entries.update({"receipt.json", payload_name})
            else:
                live_root = (
                    self.enabled_root
                    if checkpoint_receipt["enabled"]
                    else self.disabled_root
                )
                present_skills = {
                    skill
                    for skill in checkpoint_receipt["skills"]
                    if (live_root / skill).is_dir()
                }
                actual = _directory_manifest(
                    live_root,
                    tuple(checkpoint_receipt["skills"]),
                )
                if (
                    actual != payload_files
                    or present_skills != set(payload_skills)
                    or self._shadow_payload_paths(enabled=checkpoint_receipt["enabled"])
                ):
                    raise DeliveryError(
                        "checkpoint_invalid",
                        "Preserved checkpoint payload no longer matches the migration state",
                    )
                expected_entries.add("receipt.json")
        elif (
            value["skills"]
            or value.get("enabled") is not None
            or payload_skills
            or payload_files
        ):
            raise DeliveryError(
                "checkpoint_invalid",
                "Absent-state checkpoint metadata is inconsistent",
            )

        actual_entries = {entry.name for entry in self.rollback_path.iterdir()}
        if actual_entries != expected_entries:
            raise DeliveryError(
                "checkpoint_invalid",
                "Checkpoint contains unexpected entries",
            )
        return value, checkpoint_receipt

    def _managed_skills_for_cleanup(self, checkpoint: dict[str, Any] | None = None) -> set[str]:
        skills = set(EXPECTED_SKILLS)
        try:
            receipt = self._load_receipt(required=False)
        except DeliveryError:
            receipt = None
        if receipt:
            skills.update(receipt["skills"])
        if checkpoint:
            skills.update(checkpoint.get("skills", []))
        return skills

    def _remove_managed_payload(self, skills: set[str]) -> None:
        for root in (self.enabled_root, self.disabled_root):
            for skill in skills:
                path = root / skill
                if _is_linklike(path):
                    raise DeliveryError(
                        "symlink_boundary",
                        f"Refusing to remove symlinked managed path: {path}",
                    )
                if path.is_dir():
                    shutil.rmtree(path)
                elif path.exists():
                    raise DeliveryError(
                        "invalid_payload",
                        f"Managed path is not a directory: {path}",
                    )

    def _restore_checkpoint(
        self,
        *,
        reinstate_previous: bool,
    ) -> tuple[dict[str, Any], dict[str, Any] | None]:
        checkpoint, checkpoint_receipt = self._load_checkpoint_metadata()
        payload_mode = checkpoint.get("payload_mode", "snapshot")
        if payload_mode == "snapshot":
            self._remove_managed_payload(self._managed_skills_for_cleanup(checkpoint))
        if self.receipt_path.exists():
            if _is_linklike(self.receipt_path) or not self.receipt_path.is_file():
                raise DeliveryError("receipt_invalid", "Cannot safely replace receipt")
            self.receipt_path.unlink()

        if checkpoint["receipt_present"] and payload_mode == "snapshot":
            source_name = "enabled-skills" if checkpoint["enabled"] else "disabled-skills"
            destination = self.enabled_root if checkpoint["enabled"] else self.disabled_root
            source = self.rollback_path / source_name
            destination.mkdir(parents=True, exist_ok=True)
            for skill in checkpoint["payload_skills"]:
                skill_source = source / skill
                shutil.copytree(skill_source, destination / skill)
        if checkpoint["receipt_present"]:
            shutil.copy2(self.rollback_path / "receipt.json", self.receipt_path)

        shutil.rmtree(self.rollback_path)
        if reinstate_previous and self.previous_rollback_path.exists():
            os.replace(self.previous_rollback_path, self.rollback_path)
        elif self.previous_rollback_path.exists():
            shutil.rmtree(self.previous_rollback_path)
        self._cleanup_transition_artifacts()
        self._cleanup_empty_state()
        return checkpoint, checkpoint_receipt

    def _commit_checkpoint(self) -> None:
        if self.previous_rollback_path.exists():
            shutil.rmtree(self.previous_rollback_path)
        self._cleanup_transition_artifacts()

    def _cleanup_transition_artifacts(self) -> None:
        for path in (self.staging_path, self.rollback_new_path):
            if _is_linklike(path):
                raise DeliveryError(
                    "symlink_boundary",
                    f"Transition artifact cannot be a symlink: {path}",
                )
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                raise DeliveryError(
                    "invalid_transition_artifact",
                    f"Transition artifact is not a directory: {path}",
                )
        if self.receipt_temp_path.exists():
            if _is_linklike(self.receipt_temp_path) or not self.receipt_temp_path.is_file():
                raise DeliveryError(
                    "invalid_transition_artifact",
                    f"Receipt temporary path is invalid: {self.receipt_temp_path}",
                )
            self.receipt_temp_path.unlink()

    def _replace_with_artifact(self, artifact: Artifact, *, enabled: bool) -> None:
        if self.staging_path.exists() or _is_linklike(self.staging_path):
            raise DeliveryError(
                "transition_artifact_collision",
                "Staging path is already occupied",
            )
        staged = self.staging_path / "skills"
        staged.mkdir(parents=True)
        for skill in artifact.skills:
            shutil.copytree(artifact.root / skill, staged / skill)
        if _directory_manifest(staged, artifact.skills) != artifact.files:
            raise DeliveryError("staging_integrity", "Staged artifact integrity failed")

        self._remove_managed_payload(set(EXPECTED_SKILLS))
        destination = self.enabled_root if enabled else self.disabled_root
        destination.mkdir(parents=True, exist_ok=True)
        for skill in artifact.skills:
            os.replace(staged / skill, destination / skill)
        self._write_receipt(self._receipt_payload(artifact, enabled=enabled))
        shutil.rmtree(self.staging_path)

    def _migrate_identity(self, artifact: Artifact, *, enabled: bool) -> None:
        receipt = self._load_receipt(required=True)
        assert receipt is not None
        if (
            receipt["schema_version"] != LEGACY_SCHEMA_VERSION
            or self._legacy_mapping(receipt, artifact) is None
        ):
            raise DeliveryError(
                "identity_migration_invalid",
                "Current receipt is not an explicitly mapped legacy identity",
            )
        payload_root = self.enabled_root if enabled else self.disabled_root
        if _directory_manifest(payload_root, artifact.skills) != artifact.files:
            raise DeliveryError(
                "identity_migration_invalid",
                "Legacy payload does not exactly match the target artifact",
            )
        self._write_receipt(self._receipt_payload(artifact, enabled=enabled))

    def _write_receipt(self, receipt: dict[str, Any]) -> None:
        self.state_root.mkdir(parents=True, exist_ok=True)
        temp = self.receipt_temp_path
        if temp.exists() or _is_linklike(temp):
            raise DeliveryError(
                "transition_artifact_collision",
                "Receipt temporary path is already occupied",
            )
        temp.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temp, self.receipt_path)

    def _move_enablement(self, *, enabled: bool) -> None:
        receipt = self._load_receipt(required=True)
        assert receipt is not None
        source = self.disabled_root if enabled else self.enabled_root
        destination = self.enabled_root if enabled else self.disabled_root
        destination.mkdir(parents=True, exist_ok=True)
        for skill in receipt["skills"]:
            source_path = source / skill
            destination_path = destination / skill
            if destination_path.exists() or _is_linklike(destination_path):
                raise DeliveryError(
                    "enablement_collision",
                    f"Destination already exists: {destination_path}",
                )
            os.replace(source_path, destination_path)
        receipt = {**receipt, "enabled": enabled, "updated_at": _utc_now()}
        self._write_receipt(receipt)
        self._cleanup_empty_state()

    def _uninstall(self) -> None:
        receipt = self._load_receipt(required=True)
        assert receipt is not None
        self._remove_managed_payload(set(receipt["skills"]))
        self.receipt_path.unlink()
        self._cleanup_empty_state()

    def _verify_postcondition(
        self,
        operation: str,
        candidate: Artifact | None,
        *,
        expected_enabled: bool | None,
    ) -> None:
        after = self._inspect(candidate, include_previous_rollback=False)
        if operation in {"install", "update", "repair", "migrate_identity"}:
            if expected_enabled is None:
                raise DeliveryError(
                    "postcondition_failed",
                    f"{operation} expected enablement was not captured",
                )
            expected_enablement = "enabled" if expected_enabled else "disabled"
            if not (
                after["installation"] == "complete"
                and after["enablement"] == expected_enablement
                and after["candidate_relation"] == "same_as_current"
                and after["transition"] == "stable"
            ):
                raise DeliveryError("postcondition_failed", f"{operation} verification failed")
        elif operation == "disable":
            if after["installation"] != "complete" or after["enablement"] != "disabled":
                raise DeliveryError("postcondition_failed", "disable verification failed")
        elif operation == "enable":
            if after["installation"] != "complete" or after["enablement"] != "enabled":
                raise DeliveryError("postcondition_failed", "enable verification failed")
        elif operation == "uninstall":
            if after["installation"] != "absent":
                raise DeliveryError("postcondition_failed", "uninstall verification failed")

    def _verify_rollback_postcondition(
        self,
        expected_checkpoint: dict[str, Any],
        expected_receipt: dict[str, Any] | None,
        candidate: Artifact | None,
    ) -> None:
        after = self.inspect(candidate)
        if expected_receipt is None:
            valid = (
                after["installation"] == "absent"
                and after["enablement"] == "not_applicable"
                and after["transition"] == "stable"
            )
        else:
            payload_root = (
                self.enabled_root
                if expected_receipt["enabled"]
                else self.disabled_root
            )
            try:
                actual_payload = _directory_manifest(
                    payload_root,
                    tuple(expected_receipt["skills"]),
                )
                actual_receipt = self._load_receipt(required=True)
            except DeliveryError:
                actual_payload = {}
                actual_receipt = None
            present_skills = {
                skill
                for skill in expected_receipt["skills"]
                if (payload_root / skill).is_dir()
            }
            valid = (
                actual_receipt == expected_receipt
                and actual_payload == expected_checkpoint["payload_files"]
                and present_skills == set(expected_checkpoint["payload_skills"])
                and not self._shadow_payload_paths(enabled=expected_receipt["enabled"])
                and not after["transition_artifacts"]
                and after["rollback_available"] is False
            )
        if not valid:
            raise DeliveryError(
                "rollback_verification_failed",
                "Rollback completed but the restored state failed verification",
                details={"state": after},
            )

    def _cleanup_empty_state(self) -> None:
        for path in (self.disabled_root, self.enabled_root):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        if self.state_root.is_dir() and not any(self.state_root.iterdir()):
            self.state_root.rmdir()
        if self.agents_root.is_dir() and not any(self.agents_root.iterdir()):
            self.agents_root.rmdir()
