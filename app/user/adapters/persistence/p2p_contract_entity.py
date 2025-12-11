from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class P2PContractEntity(Base):
    """
    Entidad de base de datos para contratos P2P.
    Mapea la tabla 'p2p_contracts' en MySQL.
    """
    __tablename__ = "p2p_contracts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    energy_kwh = Column(DECIMAL(10, 2), nullable=False)
    price_per_kwh = Column(DECIMAL(10, 2), nullable=False)
    contract_period = Column(String(7), nullable=False)  # 'YYYY-MM'
    status = Column(String(20), nullable=False, default='active')  # 'active', 'completed', 'cancelled'
    created_at = Column(DateTime(timezone=True), default=bogota_now)

    def __repr__(self):
        return f"<P2PContractEntity(id={self.id}, seller={self.seller_id}, buyer={self.buyer_id})>"
