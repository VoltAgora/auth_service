from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class EnergyCreditEntity(Base):
    """
    Entidad de base de datos para créditos energéticos.
    Mapea la tabla 'energy_credits' en MySQL.
    """
    __tablename__ = "energy_credits"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    credit_kwh = Column(DECIMAL(10, 2), nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=bogota_now)
    used_kwh = Column(DECIMAL(10, 2), nullable=False, default=0)

    def __repr__(self):
        return f"<EnergyCreditEntity(user_id={self.user_id}, credit_kwh={self.credit_kwh})>"
