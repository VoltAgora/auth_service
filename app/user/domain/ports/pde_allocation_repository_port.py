from abc import ABC, abstractmethod
from app.user.domain.models.pde_allocation import PDEAllocation
from typing import Optional, List

class PDEAllocationRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de asignaciones PDE.
    Define el contrato para operaciones de distribución de excedentes.
    """

    @abstractmethod
    def get_by_user_and_period(self, user_id: int, allocation_period: str) -> Optional[PDEAllocation]:
        """
        Obtiene la asignación PDE de un usuario en un periodo.
        Query: SELECT * FROM pde_allocations WHERE user_id = ? AND allocation_period = ?
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[PDEAllocation]:
        """Obtiene todas las asignaciones históricas de un usuario"""
        pass

    @abstractmethod
    def get_by_community_and_period(self, community_id: int, allocation_period: str) -> List[PDEAllocation]:
        """Obtiene todas las asignaciones de una comunidad en un periodo"""
        pass

    @abstractmethod
    def save(self, allocation: PDEAllocation) -> PDEAllocation:
        """Guarda una nueva asignación PDE"""
        pass
