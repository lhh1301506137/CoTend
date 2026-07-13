"""CoTend project and user-scope delivery lifecycle contracts."""

from .core import Artifact, DeliveryError, DeliveryLayout, DeliveryManager
from .production_resolver import (
    ProductionUserLayout,
    inspect_production_user_layout,
    resolve_production_user_layout,
)
from .production_scope import (
    IsolatedProductionUserSkillDeliveryManager,
    ProductionUserDeliveryBridge,
)
from .user_scope import IsolatedUserSkillDeliveryManager

__all__ = [
    "Artifact",
    "DeliveryError",
    "DeliveryLayout",
    "DeliveryManager",
    "IsolatedUserSkillDeliveryManager",
    "IsolatedProductionUserSkillDeliveryManager",
    "ProductionUserDeliveryBridge",
    "ProductionUserLayout",
    "inspect_production_user_layout",
    "resolve_production_user_layout",
]
