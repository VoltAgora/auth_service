from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    """
    DTO para la solicitud de registro de usuario.
    Incluye todos los datos necesarios para crear una cuenta.
    """
    document: str
    name: str
    lastname: str
    phone: Optional[str] = None
    email: EmailStr
    password: str  # Contraseña en texto plano (será hasheada)
    role: int = 1  # TinyInt 0-99: 0=admin, 1=user, 2=moderator, etc.

class LoginRequest(BaseModel):
    """
    DTO para la solicitud de login.
    Solo requiere email y contraseña.
    """
    email: EmailStr
    password: str

class TokenVerifyRequest(BaseModel):
    """
    DTO para la verificación de token.
    """
    token: str

class AuthResponse(BaseModel):
    """
    DTO para respuestas de autenticación exitosas.
    """
    user_id: int
    email: str
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """
    DTO para respuestas que incluyen información del usuario.
    No incluye información sensible como contraseñas.
    """
    id: int
    document: str
    name: str
    lastname: str
    phone: Optional[str]
    email: str
    role: int  # TinyInt 0-99 para tabla pivote de roles
    is_active: bool