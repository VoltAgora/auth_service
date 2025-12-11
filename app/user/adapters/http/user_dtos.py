from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class RegisterUserInCommunityRequest(BaseModel):
    """
    DTO para registrar un usuario en una comunidad.
    """
    user_id: int
    community_id: int
    role: str  # 'producer', 'consumer', 'prosumer'
    pde_share: Optional[Decimal] = None  # 0-1
    installed_capacity: Optional[Decimal] = None  # kW

class UserEnergyBalanceRequest(BaseModel):
    """
    DTO para solicitar balance energético de un usuario.
    """
    user_id: int
    period: str  # 'YYYY-MM'
