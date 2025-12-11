from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """
    Modelo de dominio para Usuario.
    Representa un actor del sistema P2P de energía.
    """
    id: Optional[int] = None
    document: str
    name: str
    lastname: str
    phone: Optional[str] = None
    email: EmailStr
    created_at: Optional[datetime] = None
    is_active: bool = True
    role: int = 1  # TinyInt 0-99: 0=admin, 1=user, 2=moderator, etc.

    class Config:
        from_attributes = True
