from sqlalchemy import Column, Integer, String, DateTime, Float
from app.shared.infrastructure.db import Base
from datetime import datetime

class TransactionEntity(Base):
    """
    Entidad de base de datos para transacciones.
    Esta clase mapea la estructura de la tabla transactions en la base de datos.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Aquí irán las columnas específicas de transacciones
    # Por ejemplo: user_id, amount, timestamp, status, etc.

    def __repr__(self):
        return f"<TransactionEntity(id={self.id})>"
