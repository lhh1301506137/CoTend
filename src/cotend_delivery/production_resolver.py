from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .core import DeliveryError, FIRST_PARTY_SKILLS


CONTRACT_NAME = "cotend.production-user-layout"
CONTRACT_VERSION = 1
LEGACY_USER_RECEIPT_SCHEMA_VERSION = 3
STATE_DIRECTORY_NAME = ".cotend-delivery"
LAYOUT_FINGERPRINT_PATTERN = re.compile(r"^cotend-layout-[0-9a-f]{24}$")


def _is_linklike(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def _path_identity(path: Path) -> str:
    return os.path.normcase(str(path))


def _digest_identity(domain: str, *paths: Path) -> str:
    digest = hashlib.sha256()
    digest.update(domain.encode("ascii"))
    for path in paths:
        digest.update(b"\0")
        digest.update(_path_identity(path).encode("utf-8"))
    return digest.hexdigest()[:24]


def _paths_overlap(left: Path, right: Path) -> bool:
    left_resolved = left.resolve(strict=False)
    right_resolved = right.resolve(strict=False)
    return (
        left_resolved == right_resolved
        or left_resolved.is_relative_to(right_resolved)
        or right_resolved.is_relative_to(left_resolved)
    )


def _root_from_value(
    value: Path | str | None,
    *,
    label: str,
    default: Path,
    must_exist: bool,
) -> Path:
    selected = default if value is None else value
    raw_text = os.fspath(selected)
    if not raw_text.strip():
        raise DeliveryError("production_path_invalid", f"{label} cannot be empty")
    raw = Path(raw_text).expanduser()
    if not raw.is_absolute():
        raise DeliveryError(
            "production_path_invalid",
            f"{label} must be an absolute path",
        )
    if _is_linklike(raw):
        raise DeliveryError(
            "production_path_link_forbidden",
            f"{label} cannot be a link or junction",
        )
    resolved = raw.resolve(strict=False)
    if must_exist and not resolved.is_dir():
        raise DeliveryError(
            "production_path_missing",
            f"{label} must identify an existing directory",
        )
    if resolved.exists() and not resolved.is_dir():
        raise DeliveryError(
            "production_path_invalid",
            f"{label} must identify a directory",
        )
    return resolved


def _reject_linked_delivery_roots(paths: dict[str, Path]) -> None:
    for label, path in paths.items():
        if _is_linklike(path):
            raise DeliveryError(
                "production_path_link_forbidden",
                f"{label} cannot be a link or junction",
            )


@dataclass(frozen=True)
class ProductionUserLayout:
    home: Path
    codex_home: Path
    canonical_root: Path
    compatibility_root: Path
    state_root: Path
    installation_id: str
    layout_fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract": CONTRACT_NAME,
            "contract_version": CONTRACT_VERSION,
            "paths": {
                "home": str(self.home),
                "codex_home": str(self.codex_home),
                "canonical_root": str(self.canonical_root),
                "compatibility_root": str(self.compatibility_root),
                "state_root": str(self.state_root),
            },
            "identity": {
                "installation_id": self.installation_id,
                "layout_fingerprint": self.layout_fingerprint,
            },
        }


def resolve_production_user_layout(
    *,
    home: Path | str | None = None,
    codex_home: Path | str | None = None,
) -> ProductionUserLayout:
    default_home = Path.home()
    home_root = _root_from_value(
        home,
        label="HOME",
        default=default_home,
        must_exist=True,
    )
    if codex_home is None:
        configured_codex_home = os.environ.get("CODEX_HOME")
        codex_value: Path | str | None = configured_codex_home
        codex_default = home_root / ".codex"
    else:
        codex_value = codex_home
        codex_default = home_root / ".codex"
    codex_root = _root_from_value(
        codex_value,
        label="CODEX_HOME",
        default=codex_default,
        must_exist=False,
    )

    agents_root = home_root / ".agents"
    canonical_root = agents_root / "skills"
    compatibility_root = codex_root / "skills"
    state_root = agents_root / STATE_DIRECTORY_NAME
    if agents_root.exists() and not agents_root.is_dir():
        raise DeliveryError(
            "production_path_invalid",
            "$HOME/.agents must identify a directory",
        )
    _reject_linked_delivery_roots(
        {
            "$HOME/.agents": agents_root,
            "canonical Skill root": canonical_root,
            "compatibility Skill root": compatibility_root,
            "CoTend state root": state_root,
        }
    )

    roots = {
        "canonical Skill root": canonical_root,
        "compatibility Skill root": compatibility_root,
        "CoTend state root": state_root,
    }
    labels = list(roots)
    for index, label in enumerate(labels):
        for other_label in labels[index + 1 :]:
            if _paths_overlap(roots[label], roots[other_label]):
                raise DeliveryError(
                    "production_path_overlap",
                    f"{label} overlaps {other_label}",
                )

    installation_digest = _digest_identity(
        "cotend.production-installation.v1",
        canonical_root,
    )
    layout_digest = _digest_identity(
        "cotend.production-layout.v1",
        canonical_root,
        compatibility_root,
    )
    return ProductionUserLayout(
        home=home_root,
        codex_home=codex_root,
        canonical_root=canonical_root,
        compatibility_root=compatibility_root,
        state_root=state_root,
        installation_id=f"cotend-user-{installation_digest}",
        layout_fingerprint=f"cotend-layout-{layout_digest}",
    )


def _carrier_observation(root: Path) -> tuple[dict[str, Any], list[str]]:
    blockers: list[str] = []
    if _is_linklike(root):
        return {"status": "unsafe_link", "first_party_present": []}, [
            "carrier_root_unsafe"
        ]
    if not root.exists():
        return {"status": "absent", "first_party_present": []}, blockers
    if not root.is_dir():
        return {"status": "unsafe_non_directory", "first_party_present": []}, [
            "carrier_root_unsafe"
        ]
    present = [
        skill
        for skill in FIRST_PARTY_SKILLS
        if _is_linklike(root / skill) or (root / skill).exists()
    ]
    return {"status": "directory", "first_party_present": present}, blockers


def _state_observation(state_root: Path) -> tuple[dict[str, Any], list[str]]:
    if _is_linklike(state_root):
        return {
            "status": "unknown_state",
            "receipt_status": "unsafe_link",
            "entry_count": None,
        }, ["unknown_state"]
    if not state_root.exists():
        return {
            "status": "absent",
            "receipt_status": "absent",
            "entry_count": 0,
        }, []
    if not state_root.is_dir():
        return {
            "status": "unknown_state",
            "receipt_status": "state_root_not_directory",
            "entry_count": None,
        }, ["unknown_state"]
    try:
        entry_count = sum(1 for _ in os.scandir(state_root))
    except OSError:
        return {
            "status": "unknown_state",
            "receipt_status": "state_root_unreadable",
            "entry_count": None,
        }, ["unknown_state"]

    receipt_path = state_root / "receipt.json"
    if _is_linklike(receipt_path) or not receipt_path.is_file():
        return {
            "status": "unknown_state",
            "receipt_status": "missing_or_unsafe",
            "entry_count": entry_count,
        }, ["unknown_state"]
    try:
        if receipt_path.stat().st_size > 1024 * 1024:
            raise ValueError("receipt too large")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return {
            "status": "unknown_state",
            "receipt_status": "unreadable_or_invalid",
            "entry_count": entry_count,
        }, ["unknown_state"]
    if (
        isinstance(receipt, dict)
        and receipt.get("schema") == "cotend.delivery-receipt"
        and receipt.get("schema_version") == LEGACY_USER_RECEIPT_SCHEMA_VERSION
        and receipt.get("scope") == "user"
    ):
        return {
            "status": "legacy_user_receipt",
            "receipt_status": "explicit_receipt_migration_required",
            "receipt_schema_version": LEGACY_USER_RECEIPT_SCHEMA_VERSION,
            "entry_count": entry_count,
        }, ["explicit_receipt_migration_required"]
    return {
        "status": "unknown_state",
        "receipt_status": "unsupported_envelope",
        "entry_count": entry_count,
    }, ["unknown_state"]


def inspect_production_user_layout(
    layout: ProductionUserLayout,
    *,
    expected_layout_fingerprint: str | None = None,
) -> dict[str, Any]:
    if expected_layout_fingerprint is not None and not LAYOUT_FINGERPRINT_PATTERN.fullmatch(
        expected_layout_fingerprint
    ):
        raise DeliveryError(
            "production_layout_fingerprint_invalid",
            "Expected layout fingerprint is invalid",
        )
    canonical, canonical_blockers = _carrier_observation(layout.canonical_root)
    compatibility, compatibility_blockers = _carrier_observation(
        layout.compatibility_root
    )
    state, state_blockers = _state_observation(layout.state_root)
    blockers = canonical_blockers + compatibility_blockers + state_blockers

    if canonical["first_party_present"] and state["status"] != "legacy_user_receipt":
        blockers.append("first_party_canonical_residue")
    if compatibility["first_party_present"]:
        blockers.append("first_party_compatibility_residue")
    if (
        expected_layout_fingerprint is not None
        and expected_layout_fingerprint != layout.layout_fingerprint
    ):
        blockers.append("layout_context_changed")
    blockers = list(dict.fromkeys(blockers))

    if "explicit_receipt_migration_required" in blockers:
        migration_status = "explicit_receipt_migration_required"
    elif "unknown_state" in blockers:
        migration_status = "blocked_unknown_state"
    elif "layout_context_changed" in blockers:
        migration_status = "explicit_layout_context_migration_required"
    elif any(code.startswith("first_party_") for code in blockers):
        migration_status = "explicit_first_party_migration_required"
    else:
        migration_status = "none"

    result = layout.as_dict()
    result.update(
        {
            "mode": "read_only",
            "state": state,
            "carriers": {
                "canonical": canonical,
                "compatibility": compatibility,
            },
            "migration_status": migration_status,
            "blockers": blockers,
            "layout_context": {
                "status": (
                    "unbound"
                    if expected_layout_fingerprint is None
                    else (
                        "current"
                        if expected_layout_fingerprint == layout.layout_fingerprint
                        else "changed"
                    )
                ),
                "expected_layout_fingerprint": expected_layout_fingerprint,
            },
            "production_apply": {
                "available": False,
                "reason": "production_apply_forbidden",
            },
        }
    )
    return result
