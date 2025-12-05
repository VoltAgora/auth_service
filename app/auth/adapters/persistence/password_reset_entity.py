# app/adapters/persistence/password_reset_entity.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.shared.infrastructure.db import Base
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")
def bogota_now():
    return datetime.now(bogota_tz)

class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_hash = Column(String(255), nullable=False)      # hash del OTP
    created_at = Column(DateTime(timezone=True), default=bogota_now)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)

    def __repr__(self):
        return f"<PasswordReset(user_id={self.user_id}, used={self.used})>"