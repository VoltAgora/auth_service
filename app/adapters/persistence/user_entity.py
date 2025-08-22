from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=bogota_now)
    is_active = Column(Boolean, default=True)
    role = Column(SmallInteger, nullable=False, default=1)  # TinyInt 0-99 para tabla pivote de roles

    auth_data = relationship("AuthData", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, document='{self.document}', email='{self.email}')>"

class AuthData(Base):
    __tablename__ = "auth_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    password = Column(String(128), nullable=False)  # hash (bcrypt/argon2, etc.)

    user = relationship("User", back_populates="auth_data")

    def __repr__(self):
        return f"<AuthData(user_id={self.user_id})>"



