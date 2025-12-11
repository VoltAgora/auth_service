from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class EnergyRecord(BaseModel):
    """
    Modelo de dominio para registro energético.
    Representa la generación/consumo de un usuario en un periodo.
    """
    id: Optional[int] = None
    user_id: int
    community_id: int
    period: str  # Formato: 'YYYY-MM'
    generated_kwh: Decimal  # kWh generados
    consumed_kwh: Decimal  # kWh consumidos
    exported_kwh: Decimal  # kWh exportados a red
    imported_kwh: Decimal  # kWh importados de red
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True

    def get_self_consumption(self) -> Decimal:
        """Calcula autoconsumo: lo generado que se consumió directamente"""
        return min(self.generated_kwh, self.consumed_kwh)

    def get_surplus(self) -> Decimal:
        """Calcula excedente: lo generado que no se autoconsumió"""
        return max(Decimal(0), self.generated_kwh - self.consumed_kwh)

    def get_deficit(self) -> Decimal:
        """Calcula déficit: lo consumido que no se generó"""
        return max(Decimal(0), self.consumed_kwh - self.generated_kwh)
