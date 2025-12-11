from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class EnergyCredit(BaseModel):
    """
    Modelo de dominio para créditos energéticos.
    Representa créditos acumulados por excedentes exportados.
    """
    id: Optional[int] = None
    user_id: int
    credit_kwh: Decimal  # kWh en crédito
    expiration_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    used_kwh: Decimal = Decimal(0)  # kWh ya utilizados

    class Config:
        from_attributes = True

    def get_available_credit(self) -> Decimal:
        """Calcula crédito disponible"""
        return self.credit_kwh - self.used_kwh

    def is_expired(self, current_date: datetime) -> bool:
        """Verifica si el crédito está vencido"""
        if self.expiration_date is None:
            return False
        return current_date > self.expiration_date

    def is_fully_used(self) -> bool:
        """Verifica si el crédito está completamente utilizado"""
        return self.used_kwh >= self.credit_kwh
