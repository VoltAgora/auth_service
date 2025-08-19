from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """
    DTO for User entity.
    Used to validate and transfer user data across the system.
    """
    id: Optional[int] = None
    document: str
    name: str
    lastname: str
    phone: Optional[str] = None
    email: EmailStr   # Validates proper email format
    created_at: Optional[datetime] = None
    is_active: bool = True
    role: int = 1  # TinyInt 0-99: 0=admin, 1=user, 2=moderator, etc.

    class Config:
        from_attributes = True  # allows ORM objects → Pydantic

class AuthData(BaseModel):
    """
    DTO for authentication data.
    Stores sensitive authentication information.
    """
    id: Optional[int] = None
    user_id: int
    password: str  # hashed password only!

    class Config:
        from_attributes = True

