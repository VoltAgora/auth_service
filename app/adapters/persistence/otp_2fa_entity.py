# app/adapters/persistence/otp_2fa_entity.py
"""HU-06: Entidad para sesiones OTP de autenticación de dos factores."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.infrastructure.db import Base


class Otp2FA(Base):
    __tablename__ = "otp_2fa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_hash = Column(String(255), nullable=False)
    temp_token = Column(String(64), nullable=False, unique=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)

    def __repr__(self):
        return f"<Otp2FA(user_id={self.user_id}, used={self.used})>"
