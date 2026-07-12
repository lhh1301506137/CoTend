from __future__ import annotations

from pathlib import Path

from .core import Artifact, DeliveryLayout, DeliveryManager


class IsolatedUserSkillDeliveryManager(DeliveryManager):
    """User-scope delivery constrained to an explicit disposable root."""

    def __init__(
        self,
        artifact: Artifact,
        *,
        isolation_root: Path | str,
        home: Path | str,
        codex_home: Path | str,
        state_root: Path | str,
    ) -> None:
        layout = DeliveryLayout.isolated_user(
            isolation_root=isolation_root,
            home=home,
            codex_home=codex_home,
            state_root=state_root,
        )
        super().__init__(_layout=layout, _default_candidate=artifact)
