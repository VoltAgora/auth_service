from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class CommunityMemberEntity(Base):
    """
    Entidad de base de datos para miembros de comunidad.
    Mapea la tabla 'community_members' en MySQL.
    """
    __tablename__ = "community_members"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'producer', 'consumer', 'prosumer'
    pde_share = Column(DECIMAL(5, 4), nullable=True)  # 0.0000 - 1.0000
    installed_capacity = Column(DECIMAL(10, 2), nullable=True)  # kW
    joined_at = Column(DateTime(timezone=True), default=bogota_now)

    def __repr__(self):
        return f"<CommunityMemberEntity(user_id={self.user_id}, community_id={self.community_id})>"
