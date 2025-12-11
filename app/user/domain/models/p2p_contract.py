from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class P2PContract(BaseModel):
    """
    Modelo de dominio para contrato P2P.
    Representa un acuerdo de compra-venta de energía entre usuarios.
    """
    id: Optional[int] = None
    seller_id: int
    buyer_id: int
    energy_kwh: Decimal  # kWh contratados
    price_per_kwh: Decimal  # Precio por kWh
    contract_period: str  # Formato: 'YYYY-MM'
    status: str  # 'active', 'completed', 'cancelled'
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def get_total_value(self) -> Decimal:
        """Calcula el valor total del contrato"""
        return self.energy_kwh * self.price_per_kwh

    def is_active(self) -> bool:
        """Verifica si el contrato está activo"""
        return self.status == 'active'
