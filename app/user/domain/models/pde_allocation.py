from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PDEAllocation(BaseModel):
    """
    Modelo de dominio para asignación de excedentes (PDE).
    Representa la distribución de excedentes comunitarios a un usuario.
    """
    id: Optional[int] = None
    user_id: int
    community_id: int
    allocation_period: str  # Formato: 'YYYY-MM'
    allocated_kwh: Decimal  # kWh asignados del pool
    share_percentage: Decimal  # Porcentaje de participación
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def get_share_as_decimal(self) -> Decimal:
        """Convierte porcentaje a decimal (0-1)"""
        return self.share_percentage / Decimal(100)
