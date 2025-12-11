from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class EnergyRecordEntity(Base):
    """
    Entidad de base de datos para registros energéticos.
    Mapea la tabla 'energy_records' en MySQL.
    """
    __tablename__ = "energy_records"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    period = Column(String(7), nullable=False)  # 'YYYY-MM'
    generated_kwh = Column(DECIMAL(10, 2), nullable=False, default=0)
    consumed_kwh = Column(DECIMAL(10, 2), nullable=False, default=0)
    exported_kwh = Column(DECIMAL(10, 2), nullable=False, default=0)
    imported_kwh = Column(DECIMAL(10, 2), nullable=False, default=0)
    timestamp = Column(DateTime(timezone=True), default=bogota_now)

    def __repr__(self):
        return f"<EnergyRecordEntity(user_id={self.user_id}, period='{self.period}')>"
