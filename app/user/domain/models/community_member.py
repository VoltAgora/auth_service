from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CommunityMember(BaseModel):
    """
    Modelo de dominio para miembro de comunidad energética.
    Representa la relación entre un usuario y una comunidad.
    """
    id: Optional[int] = None
    community_id: int
    user_id: int
    role: str  # 'producer', 'consumer', 'prosumer'
    pde_share: Optional[Decimal] = None  # Participación en excedentes (0-1)
    installed_capacity: Optional[Decimal] = None  # kW instalados
    joined_at: Optional[datetime] = None

    class Config:
        from_attributes = True
