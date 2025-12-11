from abc import ABC, abstractmethod
from app.user.domain.models.energy_record import EnergyRecord
from typing import Optional, List

class EnergyRecordRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de registros energéticos.
    Define el contrato para consultas de generación/consumo.
    """

    @abstractmethod
    def get_by_user_and_period(self, user_id: int, period: str) -> Optional[EnergyRecord]:
        """
        Obtiene el registro energético de un usuario en un periodo.
        Query: SELECT * FROM energy_records WHERE user_id = ? AND period = ?
        """
        pass

    @abstractmethod
    def get_by_community_and_period(self, community_id: int, period: str) -> List[EnergyRecord]:
        """
        Obtiene todos los registros de una comunidad en un periodo.
        Query: SELECT * FROM energy_records WHERE community_id = ? AND period = ?
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[EnergyRecord]:
        """Obtiene todos los registros históricos de un usuario"""
        pass

    @abstractmethod
    def save(self, record: EnergyRecord) -> EnergyRecord:
        """Guarda un nuevo registro energético"""
        pass
