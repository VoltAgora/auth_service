from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    """
    DTO para la solicitud de registro de usuario.
    Incluye todos los datos necesarios para crear una cuenta.
    HU-01: nombre, apellido, teléfono, correo, contraseña, tipo de perfil.
    """
    document: Optional[str] = None  # Opcional: se genera desde email si no se envía
    name: str  # nombre
    lastname: str  # apellido
    phone: Optional[str] = None
    email: EmailStr
    password: str  # Contraseña en texto plano (será hasheada)
    role: int = 1  # 1=consumidor, 2=prosumidor, 0=admin (HU-01: tipo de perfil)

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

class ForgotPasswordRequest(BaseModel):
    """HU-05: Permite recuperar contraseña por correo electrónico."""
    document: Optional[str] = None
    email: Optional[EmailStr] = None  # Alternativa: buscar por email

class ResetPasswordRequest(BaseModel):
    document: Optional[str] = None
    email: Optional[EmailStr] = None  # Alternativa para identificar usuario
    otp: str
    new_password: str


class Verify2FARequest(BaseModel):
    """HU-06: Verificación de OTP para autenticación de dos factores."""
    temp_session: str
    otp: str


class RefreshTokenRequest(BaseModel):
    """HU-07: Renovación de token JWT. Acepta access_token o refreshToken."""
    access_token: Optional[str] = None
    refreshToken: Optional[str] = None  # Compatibilidad con frontend

    @property
    def token(self) -> Optional[str]:
        return self.access_token or self.refreshToken