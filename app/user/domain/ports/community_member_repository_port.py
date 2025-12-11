from abc import ABC, abstractmethod
from app.user.domain.models.community_member import CommunityMember
from typing import Optional, List

class CommunityMemberRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de miembros de comunidad.
    Define el contrato para operaciones de persistencia.
    """

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[CommunityMember]:
        """
        Obtiene la membresía de un usuario.
        Query: SELECT * FROM community_members WHERE user_id = ?
        """
        pass

    @abstractmethod
    def get_by_community_id(self, community_id: int) -> List[CommunityMember]:
        """
        Obtiene todos los miembros de una comunidad.
        Query: SELECT * FROM community_members WHERE community_id = ?
        """
        pass

    @abstractmethod
    def save(self, member: CommunityMember) -> CommunityMember:
        """
        Registra un nuevo miembro en una comunidad.
        Query: INSERT INTO community_members (community_id, user_id, role, pde_share, installed_capacity)
               VALUES (?, ?, ?, ?, ?)
        """
        pass

    @abstractmethod
    def update(self, member: CommunityMember) -> CommunityMember:
        """Actualiza datos de un miembro"""
        pass
