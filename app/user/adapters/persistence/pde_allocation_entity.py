from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class PDEAllocationEntity(Base):
    """
    Entidad de base de datos para asignaciones PDE.
    Mapea la tabla 'pde_allocations' en MySQL.
    """
    __tablename__ = "pde_allocations"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    allocation_period = Column(String(7), nullable=False)  # 'YYYY-MM'
    allocated_kwh = Column(DECIMAL(10, 2), nullable=False)
    share_percentage = Column(DECIMAL(5, 2), nullable=False)  # 0.00 - 100.00
    created_at = Column(DateTime(timezone=True), default=bogota_now)

    def __repr__(self):
        return f"<PDEAllocationEntity(user_id={self.user_id}, period='{self.allocation_period}')>"
