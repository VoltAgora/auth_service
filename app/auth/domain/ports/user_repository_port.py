from abc import ABC, abstractmethod
from app.auth.domain.models.user import User, AuthData
from typing import Optional
from datetime import datetime

class UserRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de usuarios.
    Define el contrato que debe cumplir cualquier implementación
    de persistencia de usuarios.
    """

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email"""
        pass

    @abstractmethod
    def get_by_document(self, document: str) -> Optional[User]:
        """Busca un usuario por documento"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por ID"""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda un nuevo usuario"""
        pass

    @abstractmethod
    def save_auth_data(self, auth_data: AuthData) -> AuthData:
        """Guarda los datos de autenticación de un usuario"""
        pass

    @abstractmethod
    def get_auth_data_by_user_id(self, user_id: int) -> Optional[AuthData]:
        """Obtiene los datos de autenticación de un usuario"""
        pass

    @abstractmethod
    def create_password_reset(self, user_id: int, otp_hash: str, expires_at: datetime):
        """Crea un registro de recuperación de contraseña"""
        pass

    @abstractmethod
    def get_active_password_reset(self, user_id: int):
        """Obtiene el registro de recuperación de contraseña activo"""
        pass

    @abstractmethod
    def increment_reset_attempts(self, reset_id: int):
        """Incrementa los intentos de un registro de recuperación"""
        pass

    @abstractmethod
    def update_auth_password(self, user_id: int, new_password_hash: str):
        """Actualiza la contraseña de un usuario"""
        pass

    @abstractmethod
    def mark_reset_used(self, reset_id: int):
        """Marca un registro de recuperación como usado"""
        pass
