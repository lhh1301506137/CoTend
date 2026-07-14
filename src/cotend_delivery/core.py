from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import uuid
from dataclasses import dataclass, replace
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
FIRST_PARTY_SKILLS = EXPECTED_SKILLS[:5]
SHAREABLE_COMPANION_SKILLS = EXPECTED_SKILLS[5:]
EXPECTED_FILE_COUNT = 30
RECEIPT_SCHEMA = "cotend.delivery-receipt"
CHECKPOINT_SCHEMA = "cotend.delivery-checkpoint"
TARGET_LOCK_SCHEMA = "cotend.target-artifact-lock"
MUTATION_LOCK_SCHEMA = "cotend.delivery-mutation-lock"
RECOVERY_LOCK_SCHEMA = "cotend.delivery-recovery-lock"
TARGET_LOCK_SCHEMA_VERSION = 1
MUTATION_LOCK_SCHEMA_VERSION = 1
RECOVERY_LOCK_SCHEMA_VERSION = 1
RECEIPT_SCHEMA_VERSION = 2
USER_RECEIPT_SCHEMA_VERSION = 3
PRODUCTION_USER_RECEIPT_SCHEMA_VERSION = 4
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
    "recover",
}
MUTATION_OPERATIONS = OPERATIONS - {"inspect", "recover"}
MUTATION_PHASES = {
    "planning",
    "checkpointing",
    "mutating",
    "verifying",
    "committing",
    "rolled_back",
    "completed",
    "recovery_required",
}
INTERRUPTED_MUTATION_PHASES = {
    "checkpointing",
    "mutating",
    "verifying",
    "committing",
    "recovery_required",
}
RECOVERY_PHASES = {
    "planning",
    "recovering",
    "verifying",
    "completed",
    "recovery_required",
}
RECOVERY_BRANCHES = {
    "release_abandoned_lock",
    "rollback_interrupted_transition",
}
INSTALLATION_ID_PATTERN = re.compile(r"^cotend-user-[0-9a-f]{24}$")
LAYOUT_FINGERPRINT_PATTERN = re.compile(r"^cotend-layout-[0-9a-f]{24}$")


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


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
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


def _process_liveness(process_id: int) -> str:
    """Return best-effort local evidence without treating PID state as authority."""
    if process_id == os.getpid():
        return "alive"
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            process_query_limited_information = 0x1000
            error_invalid_parameter = 87
            still_active = 259
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.GetExitCodeProcess.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(wintypes.DWORD),
            ]
            kernel32.GetExitCodeProcess.restype = wintypes.BOOL
            kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel32.CloseHandle.restype = wintypes.BOOL
            handle = kernel32.OpenProcess(
                process_query_limited_information,
                False,
                process_id,
            )
            if not handle:
                return (
                    "not_alive"
                    if ctypes.get_last_error() == error_invalid_parameter
                    else "unknown"
                )
            exit_code = wintypes.DWORD()
            queried = kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
            kernel32.CloseHandle(handle)
            if not queried:
                return "unknown"
            return "alive" if exit_code.value == still_active else "not_alive"
        except (AttributeError, OSError, ValueError):
            return "unknown"
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return "not_alive"
    except (PermissionError, OSError):
        return "unknown"
    return "alive"


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


def _portable_text_digest(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DeliveryError(
            "portable_compatibility_unsupported",
            f"Portable compatibility requires UTF-8 text: {path.name}",
        ) from exc
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


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
class DeliveryLayout:
    scope: str
    anchor_root: Path
    agents_root: Path
    enabled_root: Path
    state_root: Path
    skill_roots: tuple[tuple[str, Path], ...]
    default_owned_skills: tuple[str, ...]
    receipt_schema_version: int
    legacy_receipt_schema_versions: tuple[int, ...]
    installation_id: str | None
    layout_fingerprint: str | None
    isolated: bool

    @classmethod
    def project(cls, project: Path | str) -> "DeliveryLayout":
        raw = Path(project)
        if _is_linklike(raw):
            raise DeliveryError("symlink_boundary", "Project root cannot be a symlink")
        root = raw.resolve()
        if not root.is_dir():
            raise DeliveryError(
                "project_missing",
                f"Target project directory is missing: {root}",
            )
        agents_root = root / ".agents"
        enabled_root = agents_root / "skills"
        return cls(
            scope="project",
            anchor_root=root,
            agents_root=agents_root,
            enabled_root=enabled_root,
            state_root=agents_root / ".cotend-delivery",
            skill_roots=(("project", enabled_root),),
            default_owned_skills=EXPECTED_SKILLS,
            receipt_schema_version=RECEIPT_SCHEMA_VERSION,
            legacy_receipt_schema_versions=(LEGACY_SCHEMA_VERSION,),
            installation_id=None,
            layout_fingerprint=None,
            isolated=False,
        )

    @classmethod
    def isolated_user(
        cls,
        *,
        isolation_root: Path | str,
        home: Path | str,
        codex_home: Path | str,
        state_root: Path | str,
    ) -> "DeliveryLayout":
        raw_isolation = Path(isolation_root)
        raw_home = Path(home)
        raw_codex_home = Path(codex_home)
        raw_state_root = Path(state_root)
        if any(
            _is_linklike(path)
            for path in (raw_isolation, raw_home, raw_codex_home, raw_state_root)
        ):
            raise DeliveryError(
                "symlink_boundary",
                "User delivery roots cannot be links",
            )
        anchor = raw_isolation.resolve()
        home_root = raw_home.resolve()
        codex_root = raw_codex_home.resolve()
        delivery_state = raw_state_root.resolve()
        if not anchor.is_dir() or not home_root.is_dir() or not codex_root.is_dir():
            raise DeliveryError(
                "user_scope_missing",
                "Isolated user delivery roots must exist before planning",
            )
        live_home = Path.home().resolve()
        live_codex = Path(os.environ.get("CODEX_HOME", live_home / ".codex")).resolve()
        if home_root == live_home or codex_root == live_codex:
            raise DeliveryError(
                "live_user_scope_forbidden",
                "This adapter accepts isolated user roots only",
            )
        guarded = {
            "home": home_root,
            "codex_home": codex_root,
            "state_root": delivery_state,
        }
        for label, path in guarded.items():
            if not path.is_relative_to(anchor):
                raise DeliveryError(
                    "user_scope_escape",
                    f"{label} is outside the explicit isolation root",
                )
        agents_root = home_root / ".agents"
        enabled_root = agents_root / "skills"
        roots: list[tuple[str, Path]] = [("canonical", enabled_root)]
        compatibility_root = codex_root / "skills"
        if compatibility_root != enabled_root:
            roots.append(("compatibility", compatibility_root))
        for index, (label, root) in enumerate(roots):
            if (
                delivery_state == root
                or delivery_state.is_relative_to(root)
                or root.is_relative_to(delivery_state)
            ):
                raise DeliveryError(
                    "user_scope_overlap",
                    f"Delivery state overlaps the {label} Skill root",
                )
            for other_label, other_root in roots[index + 1 :]:
                if root.is_relative_to(other_root) or other_root.is_relative_to(root):
                    raise DeliveryError(
                        "user_scope_overlap",
                        f"{label} and {other_label} Skill roots overlap",
                    )
        return cls(
            scope="user",
            anchor_root=anchor,
            agents_root=agents_root,
            enabled_root=enabled_root,
            state_root=delivery_state,
            skill_roots=tuple(roots),
            default_owned_skills=FIRST_PARTY_SKILLS,
            receipt_schema_version=USER_RECEIPT_SCHEMA_VERSION,
            legacy_receipt_schema_versions=(),
            installation_id=None,
            layout_fingerprint=None,
            isolated=True,
        )

    @classmethod
    def isolated_production_user(
        cls,
        *,
        isolation_root: Path | str,
        home: Path | str,
        codex_home: Path | str,
        state_root: Path | str,
        installation_id: str,
        layout_fingerprint: str,
    ) -> "DeliveryLayout":
        if not INSTALLATION_ID_PATTERN.fullmatch(installation_id):
            raise DeliveryError(
                "production_installation_identity_invalid",
                "Production installation identity is invalid",
            )
        if not LAYOUT_FINGERPRINT_PATTERN.fullmatch(layout_fingerprint):
            raise DeliveryError(
                "production_layout_fingerprint_invalid",
                "Production layout fingerprint is invalid",
            )
        layout = cls.isolated_user(
            isolation_root=isolation_root,
            home=home,
            codex_home=codex_home,
            state_root=state_root,
        )
        return replace(
            layout,
            receipt_schema_version=PRODUCTION_USER_RECEIPT_SCHEMA_VERSION,
            legacy_receipt_schema_versions=(USER_RECEIPT_SCHEMA_VERSION,),
            installation_id=installation_id,
            layout_fingerprint=layout_fingerprint,
        )


@dataclass(frozen=True)
class _ComponentPlan:
    owned_skills: tuple[str, ...]
    owned_files: dict[str, str]
    components: dict[str, dict[str, Any]]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class _MutationLease:
    owner_token: str
    operation: str


@dataclass(frozen=True)
class _RecoveryLease:
    owner_token: str
    recovery_plan_id: str
    branch: str


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
            carrier != PurePosixPath("skills")
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
    def __init__(
        self,
        project: Path | str | None = None,
        *,
        _layout: DeliveryLayout | None = None,
        _default_candidate: Artifact | None = None,
    ) -> None:
        if _layout is None:
            if project is None:
                raise DeliveryError("project_missing", "Target project is required")
            layout = DeliveryLayout.project(project)
        else:
            if project is not None:
                raise DeliveryError(
                    "layout_invalid",
                    "A delivery layout cannot be combined with a project argument",
                )
            layout = _layout
        self.layout = layout
        self.scope = layout.scope
        self.project = layout.anchor_root
        self.agents_root = layout.agents_root
        self.enabled_root = layout.enabled_root
        self.state_root = layout.state_root
        self.skill_roots = layout.skill_roots
        self._default_candidate = _default_candidate
        self._active_owned_skills: set[str] = set()
        self.disabled_root = self.state_root / "disabled-skills"
        self.receipt_path = self.state_root / "receipt.json"
        self.receipt_temp_path = self.state_root / "receipt.json.tmp"
        self.rollback_path = self.state_root / "rollback"
        self.rollback_new_path = self.state_root / "rollback.new"
        self.previous_rollback_path = self.state_root / "rollback.previous"
        self.staging_path = self.state_root / "staging"
        self.mutation_lock_path = self.state_root / "mutation.lock"
        self.mutation_owner_path = self.mutation_lock_path / "owner.json"
        self.mutation_owner_temp_path = self.mutation_lock_path / "owner.json.tmp"
        self.recovery_lock_path = self.state_root / "recovery.lock"
        self.recovery_owner_path = self.recovery_lock_path / "owner.json"
        self.recovery_owner_temp_path = self.recovery_lock_path / "owner.json.tmp"
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

        for label, root in self.skill_roots:
            if _is_linklike(root):
                raise DeliveryError(
                    "symlink_boundary",
                    f"{label} Skill root cannot be a symlink",
                )
            if root.exists() and not root.is_dir():
                raise DeliveryError(
                    "invalid_boundary",
                    f"{label} Skill root must be a directory when present",
                )

    def _display_path(self, path: Path) -> str:
        try:
            return path.relative_to(self.project).as_posix()
        except ValueError:
            return str(path)

    def _effective_candidate(self, candidate: Artifact | None) -> Artifact | None:
        return candidate if candidate is not None else self._default_candidate

    @staticmethod
    def _files_for_skills(
        files: dict[str, str],
        skills: tuple[str, ...],
    ) -> dict[str, str]:
        prefixes = tuple(f"{skill}/" for skill in skills)
        return {
            relative: digest
            for relative, digest in files.items()
            if relative.startswith(prefixes)
        }

    @staticmethod
    def _receipt_owned_skills(receipt: dict[str, Any]) -> tuple[str, ...]:
        if receipt.get("scope") == "user":
            return tuple(receipt["owned_skills"])
        return tuple(receipt["skills"])

    @staticmethod
    def _receipt_owned_files(receipt: dict[str, Any]) -> dict[str, str]:
        if receipt.get("scope") == "user":
            return receipt["owned_files"]
        return receipt["files"]

    def _portable_candidate_digest(self, artifact: Artifact, skill: str) -> str:
        skill_files = sorted(
            relative
            for relative in artifact.files
            if relative.startswith(f"{skill}/")
        )
        if skill_files != [f"{skill}/SKILL.md"]:
            raise DeliveryError(
                "portable_compatibility_unsupported",
                f"Portable companion compatibility is unsupported for {skill}",
            )
        return _portable_text_digest(artifact.root / skill / "SKILL.md")

    def _portable_root_digest(
        self,
        root: Path,
        skill: str,
        *,
        label: str,
    ) -> str | None:
        skill_root = root / skill
        if _is_linklike(skill_root):
            raise DeliveryError(
                "symlink_boundary",
                f"{label} companion path cannot be a link: {skill}",
            )
        if not skill_root.exists():
            return None
        if not skill_root.is_dir():
            raise DeliveryError(
                "invalid_payload",
                f"{label} companion path is not a directory: {skill}",
            )
        _assert_no_symlinks(skill_root, label=f"{label} companion {skill}")
        files = [
            path.relative_to(skill_root).as_posix()
            for path in sorted(skill_root.rglob("*"))
            if path.is_file()
        ]
        if files != ["SKILL.md"]:
            raise DeliveryError(
                "companion_inventory_incompatible",
                f"{label} companion has unsupported files: {skill}",
                details={"root": label, "skill": skill, "files": files},
            )
        return _portable_text_digest(skill_root / "SKILL.md")

    def _scan_companion(
        self,
        skill: str,
        expected_digest: str,
    ) -> tuple[list[str], list[str]]:
        locations: list[str] = []
        for label, root in self.skill_roots:
            actual = self._portable_root_digest(root, skill, label=label)
            if actual is None:
                continue
            if actual != expected_digest:
                raise DeliveryError(
                    "companion_content_incompatible",
                    f"Existing companion is incompatible: {skill}",
                    details={"root": label, "skill": skill},
                )
            locations.append(label)
        warnings = (
            [f"compatible_duplicate:{skill}"] if len(locations) > 1 else []
        )
        return locations, warnings

    def _component_plan_for_install(self, artifact: Artifact) -> _ComponentPlan:
        if self.scope == "project":
            components = {
                skill: {"disposition": "owned"} for skill in artifact.skills
            }
            return _ComponentPlan(
                owned_skills=artifact.skills,
                owned_files=artifact.files,
                components=components,
                warnings=(),
            )

        collisions: list[str] = []
        for skill in FIRST_PARTY_SKILLS:
            for label, root in self.skill_roots:
                path = root / skill
                if path.exists() or _is_linklike(path):
                    collisions.append(f"{label}:{skill}")
        if collisions:
            raise DeliveryError(
                "unowned_collision",
                "CoTend-owned Skill names already exist in user scope",
                details={"paths": sorted(collisions)},
            )

        owned = list(FIRST_PARTY_SKILLS)
        components: dict[str, dict[str, Any]] = {
            skill: {"disposition": "owned"} for skill in FIRST_PARTY_SKILLS
        }
        warnings: list[str] = []
        for skill in SHAREABLE_COMPANION_SKILLS:
            portable_digest = self._portable_candidate_digest(artifact, skill)
            locations, duplicate_warnings = self._scan_companion(
                skill,
                portable_digest,
            )
            warnings.extend(duplicate_warnings)
            if locations:
                components[skill] = {
                    "disposition": "external_shared",
                    "portable_manifest_sha256": portable_digest,
                    "observed_roots": locations,
                }
            else:
                owned.append(skill)
                components[skill] = {"disposition": "owned"}
        owned_skills = tuple(skill for skill in EXPECTED_SKILLS if skill in owned)
        return _ComponentPlan(
            owned_skills=owned_skills,
            owned_files=self._files_for_skills(artifact.files, owned_skills),
            components=components,
            warnings=tuple(sorted(warnings)),
        )

    def _component_plan_from_receipt(self, receipt: dict[str, Any]) -> _ComponentPlan:
        owned_skills = self._receipt_owned_skills(receipt)
        components = receipt.get("components") or {
            skill: {"disposition": "owned"} for skill in receipt["skills"]
        }
        return _ComponentPlan(
            owned_skills=owned_skills,
            owned_files=self._receipt_owned_files(receipt),
            components=components,
            warnings=(),
        )

    def _user_component_state(
        self,
        receipt: dict[str, Any],
    ) -> tuple[list[str], list[str], dict[str, dict[str, Any]]]:
        if self.scope != "user":
            return [], [], {}
        issues: list[str] = []
        warnings: list[str] = []
        current: dict[str, dict[str, Any]] = {}
        for skill in EXPECTED_SKILLS:
            component = receipt["components"][skill]
            disposition = component["disposition"]
            if disposition == "owned":
                collisions = []
                for label, root in self.skill_roots:
                    if label == "canonical":
                        continue
                    path = root / skill
                    if path.exists() or _is_linklike(path):
                        collisions.append(label)
                if collisions:
                    issues.append(f"owned_duplicate:{skill}")
                current[skill] = {
                    "disposition": "owned",
                    "unexpected_roots": collisions,
                }
                continue

            expected_digest = component["portable_manifest_sha256"]
            try:
                locations, duplicate_warnings = self._scan_companion(
                    skill,
                    expected_digest,
                )
            except DeliveryError as exc:
                issues.append(f"{exc.code}:{skill}")
                locations = []
                duplicate_warnings = []
            if not locations:
                issues.append(f"external_shared_missing:{skill}")
            warnings.extend(duplicate_warnings)
            current[skill] = {
                "disposition": "external_shared",
                "roots": locations,
                "portable_manifest_sha256": expected_digest,
            }
        return sorted(set(issues)), sorted(set(warnings)), current

    @staticmethod
    def _no_mutation_lock() -> dict[str, Any]:
        return {
            "present": False,
            "state": "none",
            "interrupted": False,
            "metadata_residue": False,
            "diagnostics": [],
            "metadata": None,
        }

    @staticmethod
    def _validate_mutation_metadata(value: Any) -> dict[str, Any]:
        expected_keys = {
            "schema",
            "schema_version",
            "owner_token",
            "operation",
            "process_id",
            "created_at",
            "updated_at",
            "phase",
        }
        if not isinstance(value, dict) or set(value) != expected_keys:
            raise DeliveryError(
                "mutation_lock_invalid",
                "Mutation lock metadata shape is invalid",
            )
        token = value.get("owner_token")
        process_id = value.get("process_id")
        if (
            value.get("schema") != MUTATION_LOCK_SCHEMA
            or value.get("schema_version") != MUTATION_LOCK_SCHEMA_VERSION
            or not isinstance(token, str)
            or len(token) != 32
            or any(char not in "0123456789abcdef" for char in token)
            or value.get("operation") not in MUTATION_OPERATIONS
            or isinstance(process_id, bool)
            or not isinstance(process_id, int)
            or process_id < 1
            or not isinstance(value.get("created_at"), str)
            or not value["created_at"]
            or not isinstance(value.get("updated_at"), str)
            or not value["updated_at"]
            or value.get("phase") not in MUTATION_PHASES
        ):
            raise DeliveryError(
                "mutation_lock_invalid",
                "Mutation lock metadata is invalid",
            )
        return value

    def _load_mutation_metadata_strict(self) -> dict[str, Any]:
        if _is_linklike(self.mutation_lock_path) or not self.mutation_lock_path.is_dir():
            raise DeliveryError(
                "mutation_lock_invalid",
                "Mutation lock is not a normal directory",
            )
        if _is_linklike(self.mutation_owner_path) or not self.mutation_owner_path.is_file():
            raise DeliveryError(
                "mutation_lock_invalid",
                "Mutation lock owner metadata is missing or unsafe",
            )
        try:
            value = json.loads(self.mutation_owner_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DeliveryError(
                "mutation_lock_invalid",
                "Mutation lock owner metadata cannot be parsed",
            ) from exc
        return self._validate_mutation_metadata(value)

    def _read_mutation_lock(self) -> dict[str, Any]:
        if not self.mutation_lock_path.exists() and not _is_linklike(
            self.mutation_lock_path
        ):
            return self._no_mutation_lock()
        invalid = {
            "present": True,
            "state": "stale_or_unverifiable",
            "interrupted": False,
            "metadata_residue": False,
            "diagnostics": ["mutation_lock_unverifiable"],
            "metadata": None,
        }
        if _is_linklike(self.mutation_lock_path) or not self.mutation_lock_path.is_dir():
            return invalid
        try:
            entries = {entry.name for entry in self.mutation_lock_path.iterdir()}
        except OSError:
            return invalid
        metadata_residue = "owner.json.tmp" in entries
        unexpected = entries - {"owner.json", "owner.json.tmp"}
        if unexpected:
            return {
                **invalid,
                "metadata_residue": metadata_residue,
                "diagnostics": [
                    "mutation_lock_unverifiable",
                    "mutation_lock_unexpected_entries",
                ],
            }
        try:
            metadata = self._load_mutation_metadata_strict()
        except DeliveryError:
            return {
                **invalid,
                "metadata_residue": metadata_residue,
                "diagnostics": [
                    "mutation_lock_unverifiable",
                    *(
                        ["mutation_lock_metadata_residue"]
                        if metadata_residue
                        else []
                    ),
                ],
            }

        liveness = _process_liveness(metadata["process_id"])
        interrupted = metadata["phase"] in INTERRUPTED_MUTATION_PHASES
        if metadata["phase"] == "recovery_required" or (
            interrupted and liveness != "alive"
        ):
            state = "recovery_required"
            diagnostic = "mutation_transition_interrupted"
        elif liveness == "alive":
            state = "active"
            diagnostic = "mutation_lock_active"
        else:
            state = "stale_or_unverifiable"
            diagnostic = "mutation_lock_stale_or_unverifiable"
        diagnostics = [diagnostic]
        if metadata_residue:
            diagnostics.append("mutation_lock_metadata_residue")
        return {
            "present": True,
            "state": state,
            "interrupted": interrupted,
            "metadata_residue": metadata_residue,
            "diagnostics": diagnostics,
            "metadata": {**metadata, "process_liveness": liveness},
        }

    @staticmethod
    def _public_mutation_lock(lock: dict[str, Any]) -> dict[str, Any]:
        metadata = lock["metadata"]
        owner = None
        if metadata is not None:
            owner = {
                "owner_id": metadata["owner_token"][:12],
                "operation": metadata["operation"],
                "process_id": metadata["process_id"],
                "process_liveness": metadata["process_liveness"],
                "phase": metadata["phase"],
                "created_at": metadata["created_at"],
                "updated_at": metadata["updated_at"],
            }
        return {
            "present": lock["present"],
            "state": lock["state"],
            "interrupted": lock["interrupted"],
            "metadata_residue": lock["metadata_residue"],
            "owner": owner,
        }

    @staticmethod
    def _no_recovery_lock() -> dict[str, Any]:
        return {
            "present": False,
            "state": "none",
            "metadata_residue": False,
            "diagnostics": [],
            "metadata": None,
        }

    @staticmethod
    def _validate_recovery_metadata(value: Any) -> dict[str, Any]:
        expected_keys = {
            "schema",
            "schema_version",
            "owner_token",
            "process_id",
            "created_at",
            "updated_at",
            "phase",
            "recovery_plan_id",
            "branch",
        }
        if not isinstance(value, dict) or set(value) != expected_keys:
            raise DeliveryError(
                "recovery_lock_invalid",
                "Recovery lock metadata shape is invalid",
            )
        token = value.get("owner_token")
        process_id = value.get("process_id")
        if (
            value.get("schema") != RECOVERY_LOCK_SCHEMA
            or value.get("schema_version") != RECOVERY_LOCK_SCHEMA_VERSION
            or not isinstance(token, str)
            or len(token) != 32
            or any(char not in "0123456789abcdef" for char in token)
            or isinstance(process_id, bool)
            or not isinstance(process_id, int)
            or process_id < 1
            or not isinstance(value.get("created_at"), str)
            or not value["created_at"]
            or not isinstance(value.get("updated_at"), str)
            or not value["updated_at"]
            or value.get("phase") not in RECOVERY_PHASES
            or not _is_sha256(value.get("recovery_plan_id"))
            or value.get("branch") not in RECOVERY_BRANCHES
        ):
            raise DeliveryError(
                "recovery_lock_invalid",
                "Recovery lock metadata is invalid",
            )
        return value

    def _load_recovery_metadata_strict(self) -> dict[str, Any]:
        if _is_linklike(self.recovery_lock_path) or not self.recovery_lock_path.is_dir():
            raise DeliveryError(
                "recovery_lock_invalid",
                "Recovery lock is not a normal directory",
            )
        if _is_linklike(self.recovery_owner_path) or not self.recovery_owner_path.is_file():
            raise DeliveryError(
                "recovery_lock_invalid",
                "Recovery lock owner metadata is missing or unsafe",
            )
        try:
            value = json.loads(self.recovery_owner_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DeliveryError(
                "recovery_lock_invalid",
                "Recovery lock owner metadata cannot be parsed",
            ) from exc
        return self._validate_recovery_metadata(value)

    def _read_recovery_lock(self) -> dict[str, Any]:
        if not self.recovery_lock_path.exists() and not _is_linklike(
            self.recovery_lock_path
        ):
            return self._no_recovery_lock()
        invalid = {
            "present": True,
            "state": "stale_or_unverifiable",
            "metadata_residue": False,
            "diagnostics": ["recovery_lock_unverifiable"],
            "metadata": None,
        }
        if _is_linklike(self.recovery_lock_path) or not self.recovery_lock_path.is_dir():
            return invalid
        try:
            entries = {entry.name for entry in self.recovery_lock_path.iterdir()}
        except OSError:
            return invalid
        metadata_residue = "owner.json.tmp" in entries
        unexpected = entries - {"owner.json", "owner.json.tmp"}
        if unexpected:
            return {
                **invalid,
                "metadata_residue": metadata_residue,
                "diagnostics": [
                    "recovery_lock_unverifiable",
                    "recovery_lock_unexpected_entries",
                ],
            }
        try:
            metadata = self._load_recovery_metadata_strict()
        except DeliveryError:
            return {
                **invalid,
                "metadata_residue": metadata_residue,
                "diagnostics": [
                    "recovery_lock_unverifiable",
                    *(
                        ["recovery_lock_metadata_residue"]
                        if metadata_residue
                        else []
                    ),
                ],
            }
        liveness = _process_liveness(metadata["process_id"])
        if metadata["phase"] == "recovery_required":
            state = "recovery_required"
            diagnostic = "recovery_execution_failed"
        elif liveness == "alive":
            state = "active"
            diagnostic = "recovery_lock_active"
        else:
            state = "recovery_required"
            diagnostic = "recovery_lock_stale_or_unverifiable"
        diagnostics = [diagnostic]
        if metadata_residue:
            diagnostics.append("recovery_lock_metadata_residue")
        return {
            "present": True,
            "state": state,
            "metadata_residue": metadata_residue,
            "diagnostics": diagnostics,
            "metadata": {**metadata, "process_liveness": liveness},
        }

    @staticmethod
    def _public_recovery_lock(lock: dict[str, Any]) -> dict[str, Any]:
        metadata = lock["metadata"]
        owner = None
        if metadata is not None:
            owner = {
                "owner_id": metadata["owner_token"][:12],
                "process_id": metadata["process_id"],
                "process_liveness": metadata["process_liveness"],
                "phase": metadata["phase"],
                "branch": metadata["branch"],
                "recovery_plan_id": metadata["recovery_plan_id"],
                "created_at": metadata["created_at"],
                "updated_at": metadata["updated_at"],
            }
        return {
            "present": lock["present"],
            "state": lock["state"],
            "metadata_residue": lock["metadata_residue"],
            "owner": owner,
        }

    def _apply_recovery_lock_state(
        self,
        state: dict[str, Any],
        lock: dict[str, Any],
        *,
        owner_token: str | None,
    ) -> dict[str, Any]:
        metadata = lock["metadata"]
        owned = (
            metadata is not None
            and owner_token is not None
            and metadata["owner_token"] == owner_token
        )
        if owned:
            state["recovery_lock"] = self._public_recovery_lock(
                self._no_recovery_lock()
            )
            return state
        state["recovery_lock"] = self._public_recovery_lock(lock)
        if not lock["present"]:
            return state
        state["diagnostics"] = list(
            dict.fromkeys([*state.get("diagnostics", []), *lock["diagnostics"]])
        )
        state["transition"] = (
            "staged" if lock["state"] == "active" else "recovery_required"
        )
        state["recommended_operation"] = (
            "wait_for_active_recovery"
            if lock["state"] == "active"
            else "manual_recovery_required"
        )
        state["recovery_guidance"] = (
            "Wait for the reported recovery owner to finish, then inspect again."
            if lock["state"] == "active"
            else "Preserve both recovery and mutation evidence for manual resolution."
        )
        return state

    def _apply_mutation_lock_state(
        self,
        state: dict[str, Any],
        lock: dict[str, Any],
        *,
        owner_token: str | None,
    ) -> dict[str, Any]:
        metadata = lock["metadata"]
        owned = (
            metadata is not None
            and owner_token is not None
            and metadata["owner_token"] == owner_token
        )
        if owned:
            state["mutation_lock"] = self._public_mutation_lock(
                self._no_mutation_lock()
            )
            return state

        state["mutation_lock"] = self._public_mutation_lock(lock)
        if not lock["present"]:
            return state
        state["diagnostics"] = list(
            dict.fromkeys([*state.get("diagnostics", []), *lock["diagnostics"]])
        )
        if lock["state"] == "active":
            state["transition"] = "staged"
            state["recommended_operation"] = "wait_for_active_mutation"
            state["recovery_guidance"] = (
                "Wait for the reported owner to finish, then inspect again."
            )
        else:
            state["transition"] = "recovery_required"
            state["recommended_operation"] = "manual_recovery_required"
            state["recovery_guidance"] = (
                "Preserve the lock and transition evidence; verify ownership before "
                "an explicit recovery or lock-removal procedure."
            )
        return state

    def _write_mutation_metadata(self, metadata: dict[str, Any]) -> None:
        self._validate_mutation_metadata(metadata)
        if self.mutation_owner_temp_path.exists() or _is_linklike(
            self.mutation_owner_temp_path
        ):
            raise DeliveryError(
                "mutation_lock_invalid",
                "Mutation lock metadata temporary path is occupied",
            )
        self.mutation_owner_temp_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(self.mutation_owner_temp_path, self.mutation_owner_path)

    def _acquire_mutation_lock(self, operation: str) -> _MutationLease:
        self._assert_target_boundaries()
        self.state_root.mkdir(parents=True, exist_ok=True)
        try:
            os.mkdir(self.mutation_lock_path)
        except FileExistsError as exc:
            lock = self._read_mutation_lock()
            raise DeliveryError(
                "mutation_locked",
                "Another mutation owns or left an unverifiable project delivery lock",
                details={"mutation_lock": self._public_mutation_lock(lock)},
            ) from exc

        lease = _MutationLease(owner_token=uuid.uuid4().hex, operation=operation)
        now = _utc_now()
        metadata = {
            "schema": MUTATION_LOCK_SCHEMA,
            "schema_version": MUTATION_LOCK_SCHEMA_VERSION,
            "owner_token": lease.owner_token,
            "operation": operation,
            "process_id": os.getpid(),
            "created_at": now,
            "updated_at": now,
            "phase": "planning",
        }
        try:
            self._write_mutation_metadata(metadata)
        except Exception:
            for path in (self.mutation_owner_temp_path, self.mutation_owner_path):
                if path.is_file() and not _is_linklike(path):
                    path.unlink()
            try:
                self.mutation_lock_path.rmdir()
            except OSError:
                pass
            self._cleanup_empty_lock_parents()
            raise
        return lease

    def _update_mutation_phase(self, lease: _MutationLease, phase: str) -> None:
        if phase not in MUTATION_PHASES:
            raise DeliveryError("mutation_phase_invalid", f"Unknown mutation phase: {phase}")
        metadata = self._load_mutation_metadata_strict()
        if metadata["owner_token"] != lease.owner_token:
            raise DeliveryError(
                "mutation_lock_owner_mismatch",
                "Mutation lock ownership changed during the operation",
            )
        self._write_mutation_metadata(
            {**metadata, "phase": phase, "updated_at": _utc_now()}
        )

    def _mark_mutation_recovery_required(self, lease: _MutationLease) -> None:
        try:
            self._update_mutation_phase(lease, "recovery_required")
        except (DeliveryError, OSError):
            pass

    def _release_mutation_lock(self, lease: _MutationLease) -> None:
        metadata = self._load_mutation_metadata_strict()
        if metadata["owner_token"] != lease.owner_token:
            raise DeliveryError(
                "mutation_lock_owner_mismatch",
                "Refusing to release a mutation lock owned by another process",
            )
        entries = {entry.name for entry in self.mutation_lock_path.iterdir()}
        unexpected = entries - {"owner.json", "owner.json.tmp"}
        if unexpected:
            raise DeliveryError(
                "mutation_lock_invalid",
                "Refusing to release a mutation lock with unexpected entries",
            )
        if self.mutation_owner_temp_path.exists():
            if _is_linklike(self.mutation_owner_temp_path) or not (
                self.mutation_owner_temp_path.is_file()
            ):
                raise DeliveryError(
                    "mutation_lock_invalid",
                    "Mutation lock metadata residue is unsafe",
                )
            self.mutation_owner_temp_path.unlink()
        self.mutation_owner_path.unlink()
        self.mutation_lock_path.rmdir()
        self._cleanup_empty_lock_parents()

    def _cleanup_empty_lock_parents(self) -> None:
        for path in (self.state_root, self.agents_root):
            try:
                path.rmdir()
            except (FileNotFoundError, OSError):
                pass

    def _release_terminal_mutation_lock(
        self,
        lease: _MutationLease,
        *,
        prior_error: Exception | None = None,
    ) -> None:
        try:
            self._release_mutation_lock(lease)
        except Exception as release_error:
            self._mark_mutation_recovery_required(lease)
            raise DeliveryError(
                "mutation_lock_release_failed",
                "The delivery transition reached a terminal state but its lock could not be released",
                details={
                    "operation": lease.operation,
                    "prior_error": str(prior_error) if prior_error else None,
                    "release_error": str(release_error),
                },
            ) from release_error

    def _write_recovery_metadata(self, metadata: dict[str, Any]) -> None:
        self._validate_recovery_metadata(metadata)
        if self.recovery_owner_temp_path.exists() or _is_linklike(
            self.recovery_owner_temp_path
        ):
            raise DeliveryError(
                "recovery_lock_invalid",
                "Recovery lock metadata temporary path is occupied",
            )
        self.recovery_owner_temp_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(self.recovery_owner_temp_path, self.recovery_owner_path)

    def _acquire_recovery_lock(self, plan: dict[str, Any]) -> _RecoveryLease:
        recovery = plan["recovery"]
        self._assert_target_boundaries()
        self.state_root.mkdir(parents=True, exist_ok=True)
        try:
            os.mkdir(self.recovery_lock_path)
        except FileExistsError as exc:
            lock = self._read_recovery_lock()
            raise DeliveryError(
                "recovery_locked",
                "Another recovery owns or left an unverifiable project recovery lock",
                details={"recovery_lock": self._public_recovery_lock(lock)},
            ) from exc

        lease = _RecoveryLease(
            owner_token=uuid.uuid4().hex,
            recovery_plan_id=recovery["recovery_plan_id"],
            branch=recovery["branch"],
        )
        now = _utc_now()
        metadata = {
            "schema": RECOVERY_LOCK_SCHEMA,
            "schema_version": RECOVERY_LOCK_SCHEMA_VERSION,
            "owner_token": lease.owner_token,
            "process_id": os.getpid(),
            "created_at": now,
            "updated_at": now,
            "phase": "planning",
            "recovery_plan_id": lease.recovery_plan_id,
            "branch": lease.branch,
        }
        try:
            self._write_recovery_metadata(metadata)
        except Exception:
            for path in (self.recovery_owner_temp_path, self.recovery_owner_path):
                if path.is_file() and not _is_linklike(path):
                    path.unlink()
            try:
                self.recovery_lock_path.rmdir()
            except OSError:
                pass
            self._cleanup_empty_lock_parents()
            raise
        return lease

    def _update_recovery_phase(self, lease: _RecoveryLease, phase: str) -> None:
        if phase not in RECOVERY_PHASES:
            raise DeliveryError("recovery_phase_invalid", f"Unknown recovery phase: {phase}")
        metadata = self._load_recovery_metadata_strict()
        if metadata["owner_token"] != lease.owner_token:
            raise DeliveryError(
                "recovery_lock_owner_mismatch",
                "Recovery lock ownership changed during the operation",
            )
        self._write_recovery_metadata(
            {**metadata, "phase": phase, "updated_at": _utc_now()}
        )

    def _mark_recovery_required(self, lease: _RecoveryLease) -> None:
        try:
            self._update_recovery_phase(lease, "recovery_required")
        except (DeliveryError, OSError):
            pass

    def _release_recovery_lock(self, lease: _RecoveryLease) -> None:
        metadata = self._load_recovery_metadata_strict()
        if metadata["owner_token"] != lease.owner_token:
            raise DeliveryError(
                "recovery_lock_owner_mismatch",
                "Refusing to release a recovery lock owned by another process",
            )
        entries = {entry.name for entry in self.recovery_lock_path.iterdir()}
        unexpected = entries - {"owner.json", "owner.json.tmp"}
        if unexpected:
            raise DeliveryError(
                "recovery_lock_invalid",
                "Refusing to release a recovery lock with unexpected entries",
            )
        if self.recovery_owner_temp_path.exists():
            if _is_linklike(self.recovery_owner_temp_path) or not (
                self.recovery_owner_temp_path.is_file()
            ):
                raise DeliveryError(
                    "recovery_lock_invalid",
                    "Recovery lock metadata residue is unsafe",
                )
            self.recovery_owner_temp_path.unlink()
        self.recovery_owner_path.unlink()
        self.recovery_lock_path.rmdir()
        self._cleanup_empty_lock_parents()

    def _release_terminal_recovery_lock(
        self,
        lease: _RecoveryLease,
        *,
        prior_error: Exception | None = None,
    ) -> None:
        try:
            self._release_recovery_lock(lease)
        except Exception as release_error:
            self._mark_recovery_required(lease)
            raise DeliveryError(
                "recovery_lock_release_failed",
                "Recovery reached a terminal state but its lock could not be released",
                details={
                    "recovery_plan_id": lease.recovery_plan_id,
                    "prior_error": str(prior_error) if prior_error else None,
                    "release_error": str(release_error),
                },
            ) from release_error

    def _receipt_payload(
        self,
        artifact: Artifact,
        *,
        enabled: bool,
        component_plan: _ComponentPlan | None = None,
    ) -> dict[str, Any]:
        now = _utc_now()
        previous = self._load_receipt(required=False)
        installed_at = previous.get("installed_at", now) if previous else now
        payload = {
            "schema": RECEIPT_SCHEMA,
            "schema_version": self.layout.receipt_schema_version,
            "platform": artifact.platform,
            "scope": self.scope,
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
        if self.scope == "user":
            plan = component_plan
            if plan is None:
                plan = (
                    self._component_plan_from_receipt(previous)
                    if previous
                    else self._component_plan_for_install(artifact)
                )
            payload.update(
                {
                    "owned_skills": list(plan.owned_skills),
                    "owned_files": plan.owned_files,
                    "components": plan.components,
                }
            )
        if self.layout.receipt_schema_version == PRODUCTION_USER_RECEIPT_SCHEMA_VERSION:
            if self.layout.installation_id is None or self.layout.layout_fingerprint is None:
                raise DeliveryError(
                    "production_layout_identity_missing",
                    "Production delivery layout identity is missing",
                )
            payload.update(
                {
                    "installation_id": self.layout.installation_id,
                    "layout_fingerprint": self.layout.layout_fingerprint,
                }
            )
        return payload

    def _validate_receipt(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise DeliveryError("receipt_invalid", "Delivery receipt is not an object")
        schema_version = value.get("schema_version")
        scope = value.get("scope")
        if value.get("schema") != RECEIPT_SCHEMA:
            raise DeliveryError("receipt_invalid", "Unsupported delivery receipt schema")
        valid_versions = {
            self.layout.receipt_schema_version,
            *self.layout.legacy_receipt_schema_versions,
        }
        if schema_version not in valid_versions or scope != self.scope:
            raise DeliveryError("receipt_invalid", "Unsupported delivery receipt schema")
        if value.get("platform") != TARGET_PLATFORM:
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
        if schema_version != LEGACY_SCHEMA_VERSION:
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
        production_identity_fields = {"installation_id", "layout_fingerprint"}
        if schema_version != PRODUCTION_USER_RECEIPT_SCHEMA_VERSION and any(
            key in value for key in production_identity_fields
        ):
            raise DeliveryError(
                "receipt_invalid",
                "Legacy receipt contains production identity fields",
            )
        if schema_version == PRODUCTION_USER_RECEIPT_SCHEMA_VERSION:
            installation_id = value.get("installation_id")
            layout_fingerprint = value.get("layout_fingerprint")
            if (
                not isinstance(installation_id, str)
                or not INSTALLATION_ID_PATTERN.fullmatch(installation_id)
                or not isinstance(layout_fingerprint, str)
                or not LAYOUT_FINGERPRINT_PATTERN.fullmatch(layout_fingerprint)
            ):
                raise DeliveryError(
                    "receipt_invalid",
                    "Production receipt identity is invalid",
                )
            if installation_id != self.layout.installation_id:
                raise DeliveryError(
                    "receipt_installation_identity_mismatch",
                    "Production receipt belongs to a different installation",
                )
        if scope == "user":
            owned_skills = value.get("owned_skills")
            owned_files = value.get("owned_files")
            components = value.get("components")
            if (
                not isinstance(owned_skills, list)
                or len(owned_skills) != len(set(owned_skills))
                or any(skill not in EXPECTED_SKILLS for skill in owned_skills)
                or not set(FIRST_PARTY_SKILLS).issubset(set(owned_skills))
                or owned_skills
                != [skill for skill in EXPECTED_SKILLS if skill in set(owned_skills)]
            ):
                raise DeliveryError(
                    "receipt_invalid",
                    "User receipt owned Skill inventory is invalid",
                )
            expected_owned_files = self._files_for_skills(files, tuple(owned_skills))
            if owned_files != expected_owned_files:
                raise DeliveryError(
                    "receipt_invalid",
                    "User receipt owned file inventory is invalid",
                )
            if not isinstance(components, dict) or set(components) != set(EXPECTED_SKILLS):
                raise DeliveryError(
                    "receipt_invalid",
                    "User receipt component inventory is invalid",
                )
            component_owned: list[str] = []
            root_labels = {label for label, _ in self.skill_roots}
            for skill in EXPECTED_SKILLS:
                component = components[skill]
                if not isinstance(component, dict):
                    raise DeliveryError(
                        "receipt_invalid",
                        f"User receipt component is invalid: {skill}",
                    )
                disposition = component.get("disposition")
                if disposition == "owned":
                    if set(component) != {"disposition"}:
                        raise DeliveryError(
                            "receipt_invalid",
                            f"Owned component metadata is invalid: {skill}",
                        )
                    component_owned.append(skill)
                elif disposition == "external_shared":
                    roots = component.get("observed_roots")
                    if (
                        skill not in SHAREABLE_COMPANION_SKILLS
                        or not _is_sha256(component.get("portable_manifest_sha256"))
                        or not isinstance(roots, list)
                        or not roots
                        or len(roots) != len(set(roots))
                        or not set(roots).issubset(root_labels)
                        or set(component)
                        != {
                            "disposition",
                            "portable_manifest_sha256",
                            "observed_roots",
                        }
                    ):
                        raise DeliveryError(
                            "receipt_invalid",
                            f"External component metadata is invalid: {skill}",
                        )
                else:
                    raise DeliveryError(
                        "receipt_invalid",
                        f"Unknown component disposition: {skill}",
                    )
            if component_owned != owned_skills:
                raise DeliveryError(
                    "receipt_invalid",
                    "User receipt ownership fields disagree",
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

        if self.scope == "user":
            for skill in SHAREABLE_COMPANION_SKILLS:
                component = receipt["components"][skill]
                if component["disposition"] != "external_shared":
                    continue
                try:
                    candidate_digest = self._portable_candidate_digest(candidate, skill)
                except DeliveryError as exc:
                    return "incompatible", [exc.code]
                if candidate_digest != component["portable_manifest_sha256"]:
                    return "incompatible", [
                        f"external_shared_candidate_incompatible:{skill}"
                    ]

        exact_identity = (
            receipt["platform"] == candidate.platform
            and receipt["source_release_id"] == candidate.source_release_id
            and receipt["artifact_lineage"] == candidate.lineage
            and receipt["artifact_id"] == candidate.artifact_id
            and receipt["target_revision"] == candidate.revision
            and receipt["protocol"] == candidate.protocol
            and receipt["manifest_sha256"] == candidate.manifest_sha256
        )
        if (
            self.scope == "user"
            and self.layout.receipt_schema_version
            == PRODUCTION_USER_RECEIPT_SCHEMA_VERSION
        ):
            if receipt["schema_version"] == USER_RECEIPT_SCHEMA_VERSION:
                if exact_identity:
                    return "identity_migration_available", [
                        "production_receipt_binding_required"
                    ]
                return "incompatible", [
                    "production_receipt_binding_requires_current_artifact"
                ]
            if receipt["layout_fingerprint"] != self.layout.layout_fingerprint:
                if exact_identity:
                    return "identity_migration_available", [
                        "layout_context_changed"
                    ]
                return "incompatible", [
                    "layout_context_migration_required_before_artifact_change"
                ]
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

    def _identity_migration_kind(self, receipt: dict[str, Any]) -> str | None:
        if receipt["schema_version"] == LEGACY_SCHEMA_VERSION:
            return "project_target_identity"
        if (
            self.scope == "user"
            and self.layout.receipt_schema_version
            == PRODUCTION_USER_RECEIPT_SCHEMA_VERSION
        ):
            if receipt["schema_version"] == USER_RECEIPT_SCHEMA_VERSION:
                return "production_receipt_binding"
            if receipt["layout_fingerprint"] != self.layout.layout_fingerprint:
                return "layout_context_rebind"
        return None

    def _collision_paths_without_receipt(
        self,
        candidate: Artifact | None,
    ) -> tuple[list[str], _ComponentPlan | None, list[str]]:
        if self.scope == "user":
            if candidate is None:
                return ["candidate_required_for_user_preflight"], None, [
                    "candidate_required"
                ]
            try:
                component_plan = self._component_plan_for_install(candidate)
            except DeliveryError as exc:
                paths = exc.details.get("paths")
                collisions = (
                    [str(path) for path in paths]
                    if isinstance(paths, list) and paths
                    else [exc.code]
                )
                return collisions, None, [exc.code]
            return [], component_plan, []

        collisions: list[str] = []
        for root in (self.enabled_root, self.disabled_root):
            for skill in EXPECTED_SKILLS:
                path = root / skill
                if path.exists() or _is_linklike(path):
                    collisions.append(self._display_path(path))
        return sorted(collisions), None, []

    def _state_residue_without_receipt(
        self,
        *,
        include_previous_rollback: bool,
    ) -> list[str]:
        if not self.state_root.is_dir():
            return []
        allowed = {
            self.rollback_path,
            self.mutation_lock_path,
            self.recovery_lock_path,
        }
        if not include_previous_rollback:
            allowed.add(self.previous_rollback_path)
        return sorted(
            self._display_path(path)
            for path in self.state_root.iterdir()
            if path not in allowed
        )

    def _shadow_payload_paths(
        self,
        *,
        enabled: bool,
        skills: tuple[str, ...] | None = None,
    ) -> list[str]:
        opposite_root = self.disabled_root if enabled else self.enabled_root
        managed_skills = skills or self.layout.default_owned_skills
        return sorted(
            self._display_path(path)
            for skill in managed_skills
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
        owner_token: str | None = None,
        recovery_owner_token: str | None = None,
    ) -> dict[str, Any]:
        candidate = self._effective_candidate(candidate)
        self._assert_target_boundaries()
        mutation_lock = self._read_mutation_lock()
        recovery_lock = self._read_recovery_lock()

        def finalize(state: dict[str, Any]) -> dict[str, Any]:
            if self.scope == "user":
                state.pop("project", None)
                state.update(
                    {
                        "scope": "user",
                        "target_root": str(self.enabled_root),
                    }
                )
            state = self._apply_mutation_lock_state(
                state,
                mutation_lock,
                owner_token=owner_token,
            )
            return self._apply_recovery_lock_state(
                state,
                recovery_lock,
                owner_token=recovery_owner_token,
            )

        rollback_available = self.rollback_path.is_dir()
        transition_artifacts = self._transition_artifacts(
            include_previous_rollback=include_previous_rollback
        )
        try:
            receipt = self._load_receipt(required=False)
        except DeliveryError as exc:
            return finalize({
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
            })

        if receipt is None:
            collisions, component_plan, preflight_diagnostics = (
                self._collision_paths_without_receipt(candidate)
            )
            state_residue = self._state_residue_without_receipt(
                include_previous_rollback=include_previous_rollback
            )
            if collisions or state_residue or transition_artifacts:
                diagnostics = list(preflight_diagnostics)
                if collisions:
                    diagnostics.append("unowned_collision")
                if state_residue:
                    diagnostics.append("unowned_delivery_state")
                return finalize({
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
                })
            absent_state = {
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
            if component_plan is not None:
                absent_state["components"] = component_plan.components
                absent_state["warnings"] = list(component_plan.warnings)
            return finalize(absent_state)

        payload_root = self.enabled_root if receipt["enabled"] else self.disabled_root
        owned_skills = self._receipt_owned_skills(receipt)
        owned_files = self._receipt_owned_files(receipt)
        try:
            actual = _directory_manifest(payload_root, owned_skills)
        except DeliveryError as exc:
            return finalize({
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
            })

        expected = owned_files
        component_issues, component_warnings, component_state = (
            self._user_component_state(receipt)
        )
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(
            set(actual) - set(expected)
            | set(
                self._shadow_payload_paths(
                    enabled=receipt["enabled"],
                    skills=owned_skills,
                )
            )
            | set(component_issues)
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
        identity_migration_kind = (
            self._identity_migration_kind(receipt)
            if relation == "identity_migration_available"
            else None
        )

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

        complete_state = {
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
            "installation_id": receipt.get("installation_id"),
            "receipt_layout_fingerprint": receipt.get("layout_fingerprint"),
            "current_layout_fingerprint": self.layout.layout_fingerprint,
            "identity_migration_kind": identity_migration_kind,
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
            "managed_skills": list(owned_skills),
            "managed_files": len(expected),
            "missing": missing,
            "modified": modified,
            "unexpected": unexpected,
            "transition_artifacts": transition_artifacts,
            "rollback_available": rollback_available,
            "recommended_operation": recommended,
            "diagnostics": diagnostics,
        }
        if self.scope == "user":
            complete_state["components"] = component_state
            complete_state["warnings"] = component_warnings
        return finalize(complete_state)

    def _snapshot_owned_path(
        self,
        path: Path,
        label: str,
        entries: dict[str, dict[str, str]],
    ) -> None:
        if _is_linklike(path):
            entries[label] = {"kind": "link"}
            return
        if not path.exists():
            entries[label] = {"kind": "missing"}
            return
        if path.is_file():
            entries[label] = {"kind": "file", "sha256": _sha256(path)}
            return
        if not path.is_dir():
            entries[label] = {"kind": "special"}
            return
        entries[label] = {"kind": "directory"}
        for child in sorted(path.iterdir(), key=lambda item: item.name):
            self._snapshot_owned_path(child, f"{label}/{child.name}", entries)

    def _recovery_snapshot(self) -> dict[str, Any]:
        entries: dict[str, dict[str, str]] = {}
        owned_paths = (
            (self.mutation_lock_path, "mutation.lock"),
            (self.receipt_path, "receipt.json"),
            (self.receipt_temp_path, "receipt.json.tmp"),
            (self.rollback_path, "rollback"),
            (self.rollback_new_path, "rollback.new"),
            (self.previous_rollback_path, "rollback.previous"),
            (self.staging_path, "staging"),
        )
        for path, label in owned_paths:
            self._snapshot_owned_path(path, label, entries)
        managed_skills = set(self.layout.default_owned_skills) | self._active_owned_skills
        try:
            receipt = self._load_receipt(required=False)
        except DeliveryError:
            receipt = None
        if receipt:
            managed_skills.update(self._receipt_owned_skills(receipt))
        for carrier, root in (
            ("enabled-skills", self.enabled_root),
            ("disabled-skills", self.disabled_root),
        ):
            for skill in sorted(managed_skills):
                self._snapshot_owned_path(
                    root / skill,
                    f"{carrier}/{skill}",
                    entries,
                )
        payload = {
            "schema": "cotend.delivery-recovery-snapshot",
            "schema_version": 1,
            "entries": entries,
        }
        return {**payload, "sha256": _canonical_digest(payload)}

    @staticmethod
    def _timestamp(value: str) -> datetime | None:
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None
        return parsed if parsed.tzinfo is not None else None

    def _checkpoint_relation(
        self,
        checkpoint: dict[str, Any],
        mutation: dict[str, Any],
    ) -> str:
        checkpoint_time = self._timestamp(checkpoint["created_at"])
        mutation_time = self._timestamp(mutation["created_at"])
        if checkpoint_time is None or mutation_time is None:
            return "unverifiable"
        if checkpoint_time < mutation_time:
            return "predates_mutation"
        if checkpoint["operation"] != mutation["operation"]:
            return "operation_mismatch"
        return "belongs_to_mutation"

    def _walk_recovery_managed_path(
        self,
        path: Path,
        inventory_root: Path,
        allowed_files: set[str],
        allowed_directories: set[str],
    ) -> list[str]:
        unexpected: list[str] = []

        def walk(current: Path) -> None:
            for child in sorted(current.iterdir(), key=lambda item: item.name):
                relative = child.relative_to(inventory_root).as_posix()
                display = self._display_path(child)
                if _is_linklike(child):
                    unexpected.append(display)
                elif child.is_file():
                    if relative not in allowed_files:
                        unexpected.append(display)
                elif child.is_dir():
                    if relative not in allowed_directories:
                        unexpected.append(display)
                    walk(child)
                else:
                    unexpected.append(display)

        walk(path)
        return unexpected

    def _recovery_unexpected_owned_paths(
        self,
        checkpoint_receipt: dict[str, Any] | None,
    ) -> list[str]:
        unexpected: list[str] = []
        allowed_state_entries = {
            self.disabled_root.name,
            self.receipt_path.name,
            self.receipt_temp_path.name,
            self.rollback_path.name,
            self.rollback_new_path.name,
            self.previous_rollback_path.name,
            self.staging_path.name,
            self.mutation_lock_path.name,
            self.recovery_lock_path.name,
        }
        if self.state_root.is_dir():
            unexpected.extend(
                self._display_path(entry)
                for entry in self.state_root.iterdir()
                if entry.name not in allowed_state_entries
            )
        if self.disabled_root.is_dir():
            unexpected.extend(
                self._display_path(entry)
                for entry in self.disabled_root.iterdir()
                if entry.name not in EXPECTED_SKILLS
            )

        managed_skills = (
            self._receipt_owned_skills(checkpoint_receipt)
            if checkpoint_receipt
            else self.layout.default_owned_skills
        )
        allowed_files = (
            set(self._receipt_owned_files(checkpoint_receipt))
            if checkpoint_receipt
            else set()
        )
        allowed_directories = {
            PurePosixPath(relative).parent.as_posix()
            for relative in allowed_files
        }
        allowed_directories.update(
            parent.as_posix()
            for relative in allowed_files
            for parent in PurePosixPath(relative).parents
            if parent.as_posix() != "."
        )
        for root in (self.enabled_root, self.disabled_root):
            for skill in managed_skills:
                skill_root = root / skill
                if _is_linklike(skill_root) or (
                    skill_root.exists() and not skill_root.is_dir()
                ):
                    unexpected.append(self._display_path(skill_root))
                elif skill_root.is_dir():
                    if skill not in allowed_directories:
                        unexpected.append(self._display_path(skill_root))
                    unexpected.extend(
                        self._walk_recovery_managed_path(
                            skill_root,
                            root,
                            allowed_files,
                            allowed_directories,
                        )
                    )

        if self.staging_path.exists():
            if _is_linklike(self.staging_path) or not self.staging_path.is_dir():
                unexpected.append(self._display_path(self.staging_path))
            else:
                staging_entries = {entry.name for entry in self.staging_path.iterdir()}
                staged = self.staging_path / "skills"
                if staging_entries != {"skills"} or _is_linklike(staged) or not staged.is_dir():
                    unexpected.append(self._display_path(self.staging_path))
                else:
                    unexpected.extend(
                        self._walk_recovery_managed_path(
                            staged,
                            staged,
                            allowed_files,
                            allowed_directories,
                        )
                    )
        if self.rollback_new_path.exists() or _is_linklike(self.rollback_new_path):
            unexpected.append(self._display_path(self.rollback_new_path))
        return sorted(set(unexpected))

    @staticmethod
    def _blocked_recovery_plan(
        state: dict[str, Any],
        *,
        reason: str,
        recommendation: str,
        diagnostics: list[str],
    ) -> dict[str, Any]:
        return {
            "operation": "recover",
            "allowed": False,
            "will_mutate": False,
            "reason": reason,
            "state": state,
            "effects": [],
            "recovery": {
                "status": "blocked",
                "recommendation": recommendation,
                "branch": None,
                "recovery_plan_id": None,
                "snapshot_sha256": None,
                "requires_confirmation": False,
                "diagnostics": diagnostics,
            },
        }

    def _plan_recovery(
        self,
        *,
        _recovery_owner_token: str | None = None,
    ) -> dict[str, Any]:
        visible_state = self._inspect(
            None,
            include_previous_rollback=True,
            recovery_owner_token=_recovery_owner_token,
        )
        recovery_lock = self._read_recovery_lock()
        recovery_metadata = recovery_lock["metadata"]
        recovery_owned = (
            recovery_metadata is not None
            and _recovery_owner_token is not None
            and recovery_metadata["owner_token"] == _recovery_owner_token
        )
        if recovery_lock["present"] and not recovery_owned:
            recommendation = (
                "wait_for_active_recovery"
                if recovery_lock["state"] == "active"
                else "manual_resolution"
            )
            return self._blocked_recovery_plan(
                visible_state,
                reason=f"recovery_lock_{recovery_lock['state']}",
                recommendation=recommendation,
                diagnostics=recovery_lock["diagnostics"],
            )

        mutation_lock = self._read_mutation_lock()
        mutation = mutation_lock["metadata"]
        if not mutation_lock["present"]:
            return self._blocked_recovery_plan(
                visible_state,
                reason="no_interrupted_mutation_lock",
                recommendation="inspect_or_continue_normal_delivery",
                diagnostics=[],
            )
        if mutation is None or mutation_lock["metadata_residue"]:
            return self._blocked_recovery_plan(
                visible_state,
                reason="mutation_lock_unverifiable",
                recommendation="manual_resolution",
                diagnostics=mutation_lock["diagnostics"],
            )
        if mutation["process_liveness"] == "alive":
            return self._blocked_recovery_plan(
                visible_state,
                reason="mutation_owner_active",
                recommendation="wait_for_active_owner",
                diagnostics=mutation_lock["diagnostics"],
            )
        if mutation["process_liveness"] != "not_alive":
            return self._blocked_recovery_plan(
                visible_state,
                reason="mutation_owner_liveness_unverifiable",
                recommendation="manual_resolution",
                diagnostics=mutation_lock["diagnostics"],
            )
        if mutation["operation"] == "rollback":
            return self._blocked_recovery_plan(
                visible_state,
                reason="interrupted_rollback_requires_manual_resolution",
                recommendation="manual_resolution",
                diagnostics=["rollback_checkpoint_intent_unverifiable"],
            )

        raw_state = self._inspect(
            None,
            include_previous_rollback=True,
            owner_token=mutation["owner_token"],
            recovery_owner_token=_recovery_owner_token,
        )
        stable_without_transition = (
            raw_state["transition"] == "stable"
            and not raw_state["transition_artifacts"]
            and not raw_state["unexpected"]
        )
        branch: str | None = None
        checkpoint: dict[str, Any] | None = None
        checkpoint_receipt: dict[str, Any] | None = None
        checkpoint_relation = "absent"
        checkpoint_error: str | None = None
        if self.rollback_path.exists() or _is_linklike(self.rollback_path):
            try:
                checkpoint, checkpoint_receipt = self._load_checkpoint_metadata()
                checkpoint_relation = self._checkpoint_relation(checkpoint, mutation)
            except DeliveryError as exc:
                checkpoint_error = exc.code
                checkpoint_relation = "invalid"
        if checkpoint_receipt is not None and self.scope == "user":
            component_issues, _, _ = self._user_component_state(checkpoint_receipt)
            if component_issues:
                return self._blocked_recovery_plan(
                    visible_state,
                    reason="external_shared_state_changed",
                    recommendation="explicit_repair_or_migration_decision",
                    diagnostics=["external_shared_state_changed", *component_issues],
                )

        phase = mutation["phase"]
        if phase == "planning":
            if stable_without_transition and checkpoint_relation in {
                "absent",
                "predates_mutation",
            }:
                branch = "release_abandoned_lock"
        elif phase == "completed":
            if stable_without_transition:
                branch = "release_abandoned_lock"
        elif phase == "rolled_back":
            if stable_without_transition and checkpoint_relation in {
                "absent",
                "predates_mutation",
            }:
                branch = "release_abandoned_lock"
        elif phase == "checkpointing":
            if stable_without_transition and checkpoint_relation in {
                "absent",
                "predates_mutation",
            }:
                branch = "release_abandoned_lock"
            elif checkpoint_relation == "belongs_to_mutation":
                branch = "rollback_interrupted_transition"
        elif checkpoint_relation == "belongs_to_mutation":
            branch = "rollback_interrupted_transition"

        unexpected_owned: list[str] = []
        if branch == "rollback_interrupted_transition":
            unexpected_owned = self._recovery_unexpected_owned_paths(
                checkpoint_receipt
            )
            if unexpected_owned:
                branch = None

        if branch is None:
            diagnostics = ["recovery_evidence_insufficient"]
            if checkpoint_error:
                diagnostics.append(checkpoint_error)
            if checkpoint_relation != "absent":
                diagnostics.append(f"checkpoint_{checkpoint_relation}")
            if unexpected_owned:
                diagnostics.append("unexpected_owned_content")
            blocked = self._blocked_recovery_plan(
                visible_state,
                reason="recovery_requires_manual_resolution",
                recommendation="manual_resolution",
                diagnostics=diagnostics,
            )
            blocked["recovery"]["unexpected_owned_paths"] = unexpected_owned
            return blocked

        snapshot = self._recovery_snapshot()
        plan_identity = {
            "schema": "cotend.delivery-recovery-plan-identity",
            "schema_version": 1,
            "project": str(self.project),
            "snapshot_sha256": snapshot["sha256"],
            "branch": branch,
            "mutation_owner_id": mutation["owner_token"][:12],
            "mutation_operation": mutation["operation"],
            "mutation_phase": mutation["phase"],
        }
        recovery_plan_id = _canonical_digest(plan_identity)
        if branch == "release_abandoned_lock":
            effects = [
                "create a temporary recovery.lock and retain it if recovery fails",
                "remove only the exact abandoned mutation.lock after snapshot revalidation",
                "preserve receipt, managed payload, rollback checkpoints, and transition state",
                "preserve project files and unrelated Skill directories",
            ]
            affected_paths = [
                self._display_path(self.recovery_lock_path),
                self._display_path(self.mutation_lock_path),
            ]
        else:
            recovery_skills = (
                self._receipt_owned_skills(checkpoint_receipt)
                if checkpoint_receipt
                else self.layout.default_owned_skills
            )
            effects = [
                "create a temporary recovery.lock and retain it if recovery fails",
                "restore the exact verified current checkpoint",
                "reinstate the previous one-step rollback topology when present",
                "clean only adapter-owned staging and receipt temporary residue",
                "remove the exact abandoned mutation.lock only after restored-state verification",
                "preserve project files and unrelated Skill directories",
            ]
            affected_paths = [
                self._display_path(self.recovery_lock_path),
                *(self._display_path(self.enabled_root / skill) for skill in recovery_skills),
                *(
                    self._display_path(self.disabled_root / skill)
                    for skill in recovery_skills
                ),
                self._display_path(self.receipt_path),
                self._display_path(self.rollback_path),
                self._display_path(self.rollback_new_path),
                self._display_path(self.previous_rollback_path),
                self._display_path(self.staging_path),
                self._display_path(self.receipt_temp_path),
                self._display_path(self.mutation_lock_path),
            ]
        return {
            "operation": "recover",
            "allowed": True,
            "will_mutate": True,
            "reason": f"{branch}_requires_exact_confirmation",
            "state": visible_state,
            "effects": effects,
            "recovery": {
                "status": "confirmation_required",
                "recommendation": branch,
                "branch": branch,
                "recovery_plan_id": recovery_plan_id,
                "snapshot_sha256": snapshot["sha256"],
                "requires_confirmation": True,
                "confirmation_scope": "one_exact_snapshot_bound_recovery_apply",
                "mutation_owner": {
                    "owner_id": mutation["owner_token"][:12],
                    "operation": mutation["operation"],
                    "phase": mutation["phase"],
                    "process_liveness": mutation["process_liveness"],
                },
                "checkpoint_relation": checkpoint_relation,
                "affected_paths": affected_paths,
                "unrelated_project_content": "preserved",
                "forward_finalize": "not_available_without_intended_target_evidence",
                "diagnostics": [],
            },
        }

    def plan(
        self,
        operation: str,
        candidate: Artifact | None = None,
        *,
        _owner_token: str | None = None,
    ) -> dict[str, Any]:
        if operation not in OPERATIONS:
            raise DeliveryError("operation_unknown", f"Unknown operation: {operation}")
        if operation == "recover":
            return self._plan_recovery()
        candidate = self._effective_candidate(candidate)
        if operation in {"install", "update", "repair", "migrate_identity"} and candidate is None:
            raise DeliveryError(
                "candidate_required",
                f"{operation} requires an exact candidate artifact",
            )

        state = self._inspect(
            candidate,
            include_previous_rollback=True,
            owner_token=_owner_token,
        )
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

        if state["recovery_lock"]["present"]:
            reason = f"recovery_lock_{state['recovery_lock']['state']}"
        elif state["mutation_lock"]["present"]:
            reason = f"mutation_lock_{state['mutation_lock']['state']}"
        elif operation == "install":
            if state["installation"] == "absent" and state["transition"] == "stable":
                allowed = will_mutate = True
                reason = f"install_candidate_into_absent_{self.scope}_scope"
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
                    migration_kind = state.get("identity_migration_kind")
                    if relation == "identity_migration_available" and migration_kind in {
                        "production_receipt_binding",
                        "layout_context_rebind",
                    }:
                        reason = (
                            "production_identity_migration_requires_complete_"
                            "verified_payload"
                        )
                    else:
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
                migration_kind = state.get("identity_migration_kind")
                reason = {
                    "project_target_identity": (
                        "rebind_verified_legacy_receipt_to_target_identity"
                    ),
                    "production_receipt_binding": (
                        "bind_verified_schema_v3_receipt_to_production_identity"
                    ),
                    "layout_context_rebind": (
                        "rebind_verified_receipt_to_current_layout_context"
                    ),
                }.get(migration_kind, "rebind_verified_receipt_identity")
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
            if state["installation"] == "absent":
                component_plan = self._component_plan_for_install(candidate)
            else:
                receipt = self._load_receipt(required=True)
                assert receipt is not None
                component_plan = self._component_plan_from_receipt(receipt)
            return [
                checkpoint,
                f"write {len(component_plan.owned_skills)} managed Skill directories and {len(component_plan.owned_files)} files",
                "write the adapter-owned delivery receipt",
                f"preserve current enablement: {state.get('enablement', 'enabled')}",
            ]
        if operation == "migrate_identity":
            assert candidate is not None
            target_schema = self.layout.receipt_schema_version
            return [
                checkpoint,
                "preserve the verified managed payload without copying or replacing it",
                f"rewrite only the adapter-owned receipt with schema v{target_schema} identity",
                f"bind verified identity to {candidate.artifact_id}",
            ]
        if operation in {"enable", "disable"}:
            return [
                checkpoint,
                f"move only the {len(state.get('managed_skills', []))} receipt-owned Skill directories",
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

    def _execute_recovery(
        self,
        *,
        apply: bool,
        confirm_recovery_plan_id: str | None,
    ) -> dict[str, Any]:
        plan = self._plan_recovery()
        if not plan["allowed"]:
            raise DeliveryError(
                "operation_blocked",
                f"recover is blocked: {plan['reason']}",
                details={"state": plan["state"], "recovery": plan["recovery"]},
            )
        if not apply:
            return {
                "status": "planned",
                "applied": False,
                "plan": plan,
                "state": plan["state"],
            }

        recovery_plan_id = plan["recovery"]["recovery_plan_id"]
        if confirm_recovery_plan_id is None:
            raise DeliveryError(
                "recovery_confirmation_required",
                "Recovery apply requires the exact previewed recovery_plan_id",
                details={"recovery_plan_id": recovery_plan_id, "plan": plan},
            )
        if confirm_recovery_plan_id != recovery_plan_id:
            raise DeliveryError(
                "recovery_plan_mismatch",
                "Recovery confirmation does not match the current recovery plan",
                details={"recovery_plan_id": recovery_plan_id, "plan": plan},
            )

        lease = self._acquire_recovery_lock(plan)
        try:
            locked_plan = self._plan_recovery(
                _recovery_owner_token=lease.owner_token
            )
        except Exception as exc:
            self._release_terminal_recovery_lock(lease, prior_error=exc)
            raise
        if (
            not locked_plan["allowed"]
            or locked_plan["recovery"]["recovery_plan_id"] != recovery_plan_id
        ):
            changed = DeliveryError(
                "recovery_plan_changed",
                "Recovery evidence changed before exclusive recovery ownership",
                details={"locked_plan": locked_plan},
            )
            self._release_terminal_recovery_lock(lease, prior_error=changed)
            raise changed

        try:
            mutation = self._load_mutation_metadata_strict()
        except Exception as exc:
            changed = DeliveryError(
                "recovery_plan_changed",
                "Mutation ownership changed before recovery execution",
            )
            self._release_terminal_recovery_lock(lease, prior_error=exc)
            raise changed from exc
        mutation_lease = _MutationLease(
            owner_token=mutation["owner_token"],
            operation=mutation["operation"],
        )
        branch = locked_plan["recovery"]["branch"]
        before = locked_plan["state"]
        try:
            self._update_recovery_phase(lease, "recovering")
            if (
                self._recovery_snapshot()["sha256"]
                != locked_plan["recovery"]["snapshot_sha256"]
            ):
                raise DeliveryError(
                    "recovery_snapshot_changed",
                    "Recovery evidence changed immediately before mutation",
                )
            if branch == "rollback_interrupted_transition":
                checkpoint, checkpoint_receipt = self._load_checkpoint_metadata()
                if self._checkpoint_relation(checkpoint, mutation) != "belongs_to_mutation":
                    raise DeliveryError(
                        "recovery_checkpoint_changed",
                        "The checkpoint no longer belongs to the interrupted mutation",
                    )
                if (
                    self._recovery_snapshot()["sha256"]
                    != locked_plan["recovery"]["snapshot_sha256"]
                ):
                    raise DeliveryError(
                        "recovery_snapshot_changed",
                        "Recovery evidence changed while validating the checkpoint",
                    )
                self._stage_recovery_checkpoint_restore(checkpoint)
                self._update_recovery_phase(lease, "verifying")
                self._verify_recovery_rollback_postcondition(
                    checkpoint,
                    checkpoint_receipt,
                    mutation_owner_token=mutation["owner_token"],
                    recovery_owner_token=lease.owner_token,
                )
                self._commit_recovery_checkpoint_restore()
                self._release_mutation_lock(mutation_lease)
            elif branch == "release_abandoned_lock":
                self._release_mutation_lock(mutation_lease)
                self._update_recovery_phase(lease, "verifying")
                after_release = self._inspect(
                    None,
                    include_previous_rollback=True,
                    recovery_owner_token=lease.owner_token,
                )
                if (
                    after_release["transition"] != "stable"
                    or after_release["transition_artifacts"]
                    or after_release["unexpected"]
                ):
                    raise DeliveryError(
                        "recovery_release_verification_failed",
                        "Abandoned lock release did not leave a stable delivery state",
                        details={"state": after_release},
                    )
            else:
                raise DeliveryError(
                    "recovery_branch_invalid",
                    f"Unsupported recovery branch: {branch}",
                )
            self._update_recovery_phase(lease, "completed")
        except Exception as exc:
            self._mark_recovery_required(lease)
            raise DeliveryError(
                "recovery_failed_lock_retained",
                "Recovery failed; available lock and checkpoint evidence was retained",
                details={
                    "recovery_plan_id": recovery_plan_id,
                    "branch": branch,
                    "recovery_error": str(exc),
                },
            ) from exc

        self._release_terminal_recovery_lock(lease)
        after = self.inspect(None)
        return {
            "status": "applied",
            "applied": True,
            "operation": "recover",
            "recovery_plan_id": recovery_plan_id,
            "branch": branch,
            "plan": locked_plan,
            "state_before": before,
            "state_after": after,
        }

    def execute(
        self,
        operation: str,
        candidate: Artifact | None = None,
        *,
        apply: bool = False,
        confirm_recovery_plan_id: str | None = None,
    ) -> dict[str, Any]:
        candidate = self._effective_candidate(candidate)
        if operation == "recover":
            return self._execute_recovery(
                apply=apply,
                confirm_recovery_plan_id=confirm_recovery_plan_id,
            )
        if confirm_recovery_plan_id is not None:
            raise DeliveryError(
                "recovery_confirmation_operation_invalid",
                "A recovery plan confirmation can only be used with recover",
            )
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

        lease = self._acquire_mutation_lock(operation)
        try:
            plan = self.plan(operation, candidate, _owner_token=lease.owner_token)
        except Exception as exc:
            self._release_terminal_mutation_lock(lease, prior_error=exc)
            raise
        if not plan["allowed"]:
            self._release_terminal_mutation_lock(lease)
            raise DeliveryError(
                "operation_blocked",
                f"{operation} is blocked after lock acquisition: {plan['reason']}",
                details={"state": plan["state"]},
            )
        if not plan["will_mutate"]:
            self._release_terminal_mutation_lock(lease)
            return {
                "status": "current_no_change",
                "applied": False,
                "plan": plan,
                "state": self.inspect(candidate),
            }

        before = plan["state"]
        if operation == "rollback":
            try:
                self._update_mutation_phase(lease, "mutating")
                restored_checkpoint, restored_receipt = self._restore_checkpoint(
                    reinstate_previous=False
                )
                self._update_mutation_phase(lease, "verifying")
                self._verify_rollback_postcondition(
                    restored_checkpoint,
                    restored_receipt,
                    candidate,
                    owner_token=lease.owner_token,
                )
                self._update_mutation_phase(lease, "completed")
            except Exception as exc:
                self._mark_mutation_recovery_required(lease)
                raise DeliveryError(
                    "rollback_failed_lock_retained",
                    "Rollback failed; the mutation lock and recovery evidence were retained",
                    details={"rollback_error": str(exc)},
                ) from exc
        else:
            expected_enabled: bool | None = None
            try:
                self._update_mutation_phase(lease, "checkpointing")
                self._create_checkpoint(operation)
            except Exception as exc:
                self._mark_mutation_recovery_required(lease)
                raise DeliveryError(
                    "checkpoint_failed_lock_retained",
                    f"{operation} could not establish a checkpoint; recovery evidence was retained",
                    details={"checkpoint_error": str(exc)},
                ) from exc
            try:
                self._update_mutation_phase(lease, "mutating")
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
                self._update_mutation_phase(lease, "verifying")
                self._verify_postcondition(
                    operation,
                    candidate,
                    expected_enabled=expected_enabled,
                    owner_token=lease.owner_token,
                )
                self._update_mutation_phase(lease, "committing")
                self._commit_checkpoint()
                self._update_mutation_phase(lease, "completed")
            except Exception as exc:
                try:
                    self._restore_checkpoint(reinstate_previous=True)
                except Exception as rollback_exc:
                    self._mark_mutation_recovery_required(lease)
                    raise DeliveryError(
                        "transition_and_rollback_failed",
                        f"{operation} failed and rollback also failed; the lock was retained",
                        details={
                            "transition_error": str(exc),
                            "rollback_error": str(rollback_exc),
                        },
                    ) from rollback_exc
                self._active_owned_skills.clear()
                try:
                    self._update_mutation_phase(lease, "rolled_back")
                except Exception as phase_exc:
                    self._mark_mutation_recovery_required(lease)
                    raise DeliveryError(
                        "transition_failed_rollback_restored_lock_retained",
                        f"{operation} failed and the prior checkpoint was restored, but recovery metadata could not be finalized",
                        details={
                            "transition_error": str(exc),
                            "phase_error": str(phase_exc),
                        },
                    ) from phase_exc
                self._release_terminal_mutation_lock(lease, prior_error=exc)
                raise DeliveryError(
                    "transition_failed_rolled_back",
                    f"{operation} failed; the prior checkpoint was restored",
                    details={"transition_error": str(exc)},
                ) from exc

        self._release_terminal_mutation_lock(lease)
        self._active_owned_skills.clear()
        if (
            self.scope == "user"
            and candidate is not None
            and operation in {"install", "update", "repair", "migrate_identity"}
        ):
            self._default_candidate = candidate
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
                owned_skills = self._receipt_owned_skills(receipt)
                shutil.copy2(self.receipt_path, temp / "receipt.json")
                source_root = (
                    self.enabled_root if receipt["enabled"] else self.disabled_root
                )
                payload_files = _directory_manifest(
                    source_root,
                    owned_skills,
                )
                payload_skills = [
                    skill
                    for skill in owned_skills
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
                        owned_skills,
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
                "skills": list(self._receipt_owned_skills(receipt)) if receipt else [],
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
            or value.get("operation") not in MUTATION_OPERATIONS - {"rollback"}
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
                value["skills"] != list(self._receipt_owned_skills(checkpoint_receipt))
                or value.get("enabled") != checkpoint_receipt["enabled"]
                or not set(payload_skills).issubset(
                    set(self._receipt_owned_skills(checkpoint_receipt))
                )
                or not set(payload_files).issubset(
                    set(self._receipt_owned_files(checkpoint_receipt))
                )
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
                    self._receipt_owned_skills(checkpoint_receipt),
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
                    for skill in self._receipt_owned_skills(checkpoint_receipt)
                    if (live_root / skill).is_dir()
                }
                actual = _directory_manifest(
                    live_root,
                    self._receipt_owned_skills(checkpoint_receipt),
                )
                if (
                    actual != payload_files
                    or present_skills != set(payload_skills)
                    or self._shadow_payload_paths(
                        enabled=checkpoint_receipt["enabled"],
                        skills=self._receipt_owned_skills(checkpoint_receipt),
                    )
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
        skills = set(self.layout.default_owned_skills) | self._active_owned_skills
        try:
            receipt = self._load_receipt(required=False)
        except DeliveryError:
            receipt = None
        if receipt:
            skills.update(self._receipt_owned_skills(receipt))
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

    def _restore_checkpoint_payload(self, checkpoint: dict[str, Any]) -> None:
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

    def _restore_checkpoint(
        self,
        *,
        reinstate_previous: bool,
    ) -> tuple[dict[str, Any], dict[str, Any] | None]:
        checkpoint, checkpoint_receipt = self._load_checkpoint_metadata()
        self._restore_checkpoint_payload(checkpoint)

        shutil.rmtree(self.rollback_path)
        if reinstate_previous and self.previous_rollback_path.exists():
            os.replace(self.previous_rollback_path, self.rollback_path)
        elif self.previous_rollback_path.exists():
            shutil.rmtree(self.previous_rollback_path)
        self._cleanup_transition_artifacts()
        self._cleanup_empty_state()
        return checkpoint, checkpoint_receipt

    def _stage_recovery_checkpoint_restore(
        self,
        checkpoint: dict[str, Any],
    ) -> None:
        self._restore_checkpoint_payload(checkpoint)
        self._cleanup_transition_artifacts()
        self._cleanup_empty_state()

    def _commit_recovery_checkpoint_restore(self) -> None:
        self._assert_target_boundaries()
        if self.rollback_new_path.exists() or _is_linklike(self.rollback_new_path):
            raise DeliveryError(
                "transition_artifact_collision",
                "Recovery checkpoint retirement path is occupied",
            )
        if _is_linklike(self.rollback_path) or not self.rollback_path.is_dir():
            raise DeliveryError(
                "checkpoint_invalid",
                "Recovery checkpoint disappeared before retirement",
            )
        os.replace(self.rollback_path, self.rollback_new_path)
        try:
            if self.previous_rollback_path.exists():
                os.replace(self.previous_rollback_path, self.rollback_path)
            shutil.rmtree(self.rollback_new_path)
        except Exception:
            if not self.rollback_path.exists() and self.rollback_new_path.exists():
                os.replace(self.rollback_new_path, self.rollback_path)
            raise
        self._cleanup_empty_state()

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
        previous = self._load_receipt(required=False)
        if previous:
            previous_plan = self._component_plan_from_receipt(previous)
            component_plan = _ComponentPlan(
                owned_skills=previous_plan.owned_skills,
                owned_files=self._files_for_skills(
                    artifact.files,
                    previous_plan.owned_skills,
                ),
                components=previous_plan.components,
                warnings=previous_plan.warnings,
            )
        else:
            component_plan = self._component_plan_for_install(artifact)
        if previous and self.scope == "user":
            issues, _, _ = self._user_component_state(previous)
            if issues:
                raise DeliveryError(
                    "external_shared_state_changed",
                    "External shared components changed before mutation",
                    details={"issues": issues},
                )
        self._active_owned_skills = set(component_plan.owned_skills)
        for skill in component_plan.owned_skills:
            shutil.copytree(artifact.root / skill, staged / skill)
        if (
            _directory_manifest(staged, component_plan.owned_skills)
            != component_plan.owned_files
        ):
            raise DeliveryError("staging_integrity", "Staged artifact integrity failed")

        removal_skills = (
            set(self._receipt_owned_skills(previous))
            if previous
            else set(component_plan.owned_skills)
        )
        self._remove_managed_payload(removal_skills)
        destination = self.enabled_root if enabled else self.disabled_root
        destination.mkdir(parents=True, exist_ok=True)
        for skill in component_plan.owned_skills:
            os.replace(staged / skill, destination / skill)
        self._write_receipt(
            self._receipt_payload(
                artifact,
                enabled=enabled,
                component_plan=component_plan,
            )
        )
        shutil.rmtree(self.staging_path)

    def _migrate_identity(self, artifact: Artifact, *, enabled: bool) -> None:
        receipt = self._load_receipt(required=True)
        assert receipt is not None
        relation, _ = self._candidate_relation(receipt, artifact)
        migration_kind = self._identity_migration_kind(receipt)
        if relation != "identity_migration_available" or migration_kind is None:
            raise DeliveryError(
                "identity_migration_invalid",
                "Current receipt is not eligible for explicit identity migration",
            )
        payload_root = self.enabled_root if enabled else self.disabled_root
        owned_skills = self._receipt_owned_skills(receipt)
        if (
            _directory_manifest(payload_root, owned_skills)
            != self._receipt_owned_files(receipt)
        ):
            raise DeliveryError(
                "identity_migration_invalid",
                "Legacy payload does not exactly match the target artifact",
            )
        component_plan: _ComponentPlan | None = None
        if self.scope == "user":
            component_issues, _, _ = self._user_component_state(receipt)
            if component_issues:
                raise DeliveryError(
                    "identity_migration_invalid",
                    "External shared components changed before identity migration",
                    details={"issues": component_issues},
                )
            component_plan = self._component_plan_from_receipt(receipt)
        self._write_receipt(
            self._receipt_payload(
                artifact,
                enabled=enabled,
                component_plan=component_plan,
            )
        )

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
        for skill in self._receipt_owned_skills(receipt):
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
        self._remove_managed_payload(set(self._receipt_owned_skills(receipt)))
        self.receipt_path.unlink()
        self._cleanup_empty_state()

    def _verify_postcondition(
        self,
        operation: str,
        candidate: Artifact | None,
        *,
        expected_enabled: bool | None,
        owner_token: str | None = None,
    ) -> None:
        after = self._inspect(
            candidate,
            include_previous_rollback=False,
            owner_token=owner_token,
        )
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
        *,
        owner_token: str | None = None,
    ) -> None:
        after = self._inspect(
            candidate,
            include_previous_rollback=True,
            owner_token=owner_token,
        )
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
            expected_owned_skills = self._receipt_owned_skills(expected_receipt)
            component_issues, _, _ = self._user_component_state(expected_receipt)
            try:
                actual_payload = _directory_manifest(
                    payload_root,
                    expected_owned_skills,
                )
                actual_receipt = self._load_receipt(required=True)
            except DeliveryError:
                actual_payload = {}
                actual_receipt = None
            present_skills = {
                skill
                for skill in expected_owned_skills
                if (payload_root / skill).is_dir()
            }
            valid = (
                actual_receipt == expected_receipt
                and actual_payload == expected_checkpoint["payload_files"]
                and present_skills == set(expected_checkpoint["payload_skills"])
                and not component_issues
                and not self._shadow_payload_paths(
                    enabled=expected_receipt["enabled"],
                    skills=expected_owned_skills,
                )
                and not after["transition_artifacts"]
                and after["rollback_available"] is False
            )
        if not valid:
            raise DeliveryError(
                "rollback_verification_failed",
                "Rollback completed but the restored state failed verification",
                details={"state": after},
            )

    def _verify_recovery_rollback_postcondition(
        self,
        expected_checkpoint: dict[str, Any],
        expected_receipt: dict[str, Any] | None,
        *,
        mutation_owner_token: str,
        recovery_owner_token: str,
    ) -> None:
        after = self._inspect(
            None,
            include_previous_rollback=False,
            owner_token=mutation_owner_token,
            recovery_owner_token=recovery_owner_token,
        )
        if after["transition_artifacts"]:
            valid = False
        elif expected_receipt is None:
            try:
                actual_receipt = self._load_receipt(required=False)
            except DeliveryError:
                actual_receipt = {"invalid": True}
            recovery_managed_skills = (
                set(self.layout.default_owned_skills) | self._active_owned_skills
            )
            managed_present = any(
                (root / skill).exists() or _is_linklike(root / skill)
                for root in (self.enabled_root, self.disabled_root)
                for skill in recovery_managed_skills
            )
            valid = actual_receipt is None and not managed_present
        else:
            payload_root = (
                self.enabled_root
                if expected_receipt["enabled"]
                else self.disabled_root
            )
            expected_owned_skills = self._receipt_owned_skills(expected_receipt)
            component_issues, _, _ = self._user_component_state(expected_receipt)
            try:
                actual_payload = _directory_manifest(
                    payload_root,
                    expected_owned_skills,
                )
                actual_receipt = self._load_receipt(required=True)
            except DeliveryError:
                actual_payload = {}
                actual_receipt = None
            present_skills = {
                skill
                for skill in expected_owned_skills
                if (payload_root / skill).is_dir()
            }
            valid = (
                actual_receipt == expected_receipt
                and actual_payload == expected_checkpoint["payload_files"]
                and present_skills == set(expected_checkpoint["payload_skills"])
                and not component_issues
                and not self._shadow_payload_paths(
                    enabled=expected_receipt["enabled"],
                    skills=expected_owned_skills,
                )
            )
        if not valid:
            raise DeliveryError(
                "recovery_rollback_verification_failed",
                "Recovery restored a checkpoint but the exact prior state failed verification",
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
