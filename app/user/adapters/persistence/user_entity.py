from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class UserEntity(Base):
    """
    Entidad de base de datos para usuarios.
    Mapea la tabla 'users' en MySQL.
    """
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    document = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=bogota_now)
    is_active = Column(Boolean, default=True)
    role = Column(SmallInteger, nullable=False, default=1)

    def __repr__(self):
        return f"<UserEntity(id={self.id}, email='{self.email}')>"
