from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    """
    Modelo de dominio para Transaction.
    Representa una transacción en el sistema P2P de energía.
    """
    id: Optional[int] = None
    # Aquí irán los campos específicos de transacciones
    # Por ejemplo: user_id, amount, timestamp, status, etc.

    class Config:
        from_attributes = True
