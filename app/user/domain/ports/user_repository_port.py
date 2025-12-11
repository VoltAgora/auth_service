from abc import ABC, abstractmethod
from app.user.domain.models.user import User
from typing import Optional, List

class UserRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de usuarios.
    Define el contrato que debe cumplir cualquier implementación.
    """

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        """Obtiene todos los usuarios"""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda un nuevo usuario"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        pass
