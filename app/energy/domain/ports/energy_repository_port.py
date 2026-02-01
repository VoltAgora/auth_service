from abc import ABC, abstractmethod
from app.energy.domain.models.energy_record import EnergyRecord
from typing import Optional


class EnergyRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de registros de energía.
    Define el contrato que debe cumplir cualquier implementación
    de persistencia de registros de energía.
    """

    @abstractmethod
    def save(self, energy_record: EnergyRecord) -> EnergyRecord:
        """
        Guarda un nuevo registro de energía.

        Args:
            energy_record (EnergyRecord): Registro de energía a guardar

        Returns:
            EnergyRecord: Registro guardado con ID asignado
        """
        pass

    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[EnergyRecord]:
        """
        Busca un registro de energía por ID.

        Args:
            record_id (int): ID del registro

        Returns:
            Optional[EnergyRecord]: Registro encontrado o None
        """
        pass
