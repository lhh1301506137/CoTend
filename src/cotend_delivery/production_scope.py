from __future__ import annotations

from pathlib import Path
from typing import Any

from .core import (
    OPERATIONS,
    PRODUCTION_USER_RECEIPT_SCHEMA_VERSION,
    USER_RECEIPT_SCHEMA_VERSION,
    Artifact,
    DeliveryError,
    DeliveryLayout,
    DeliveryManager,
)
from .production_resolver import (
    ProductionUserLayout,
    inspect_production_user_layout,
    resolve_production_user_layout,
)


class ProductionUserDeliveryBridge:
    """Read-only production facade that never constructs a delivery manager."""

    def __init__(
        self,
        *,
        home: Path | str | None = None,
        codex_home: Path | str | None = None,
    ) -> None:
        self.layout = resolve_production_user_layout(
            home=home,
            codex_home=codex_home,
        )

    def inspect(
        self,
        *,
        expected_layout_fingerprint: str | None = None,
    ) -> dict[str, Any]:
        result = inspect_production_user_layout(
            self.layout,
            expected_layout_fingerprint=expected_layout_fingerprint,
        )
        result["transaction_bridge"] = {
            "state": "hard_disabled",
            "shared_core": "DeliveryManager",
            "receipt_schema_version": PRODUCTION_USER_RECEIPT_SCHEMA_VERSION,
            "accepted_legacy_receipt_schema_versions": [
                USER_RECEIPT_SCHEMA_VERSION
            ],
            "manager_available": False,
        }
        return result

    def execute(
        self,
        operation: str = "inspect",
        *,
        apply: bool = False,
        expected_layout_fingerprint: str | None = None,
    ) -> dict[str, Any]:
        if operation not in OPERATIONS:
            raise DeliveryError(
                "operation_invalid",
                f"Unsupported delivery operation: {operation}",
            )
        if apply:
            raise DeliveryError(
                "production_apply_forbidden",
                "Production user delivery is read-only in this build",
            )
        result = self.inspect(
            expected_layout_fingerprint=expected_layout_fingerprint,
        )
        result.update(
            {
                "status": "preview",
                "operation": operation,
                "apply": False,
            }
        )
        return result


class IsolatedProductionUserSkillDeliveryManager(DeliveryManager):
    """Production-shaped delivery constrained to an explicit disposable root."""

    def __init__(
        self,
        artifact: Artifact,
        *,
        isolation_root: Path | str,
        home: Path | str,
        codex_home: Path | str,
    ) -> None:
        production_layout = resolve_production_user_layout(
            home=home,
            codex_home=codex_home,
        )
        layout = DeliveryLayout.isolated_production_user(
            isolation_root=isolation_root,
            home=production_layout.home,
            codex_home=production_layout.codex_home,
            state_root=production_layout.state_root,
            installation_id=production_layout.installation_id,
            layout_fingerprint=production_layout.layout_fingerprint,
        )
        self.production_layout: ProductionUserLayout = production_layout
        super().__init__(_layout=layout, _default_candidate=artifact)
