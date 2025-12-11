from abc import ABC, abstractmethod
from app.user.domain.models.energy_credit import EnergyCredit
from typing import List

class EnergyCreditRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de créditos energéticos.
    Define el contrato para operaciones de créditos acumulados.
    """

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[EnergyCredit]:
        """
        Obtiene todos los créditos de un usuario.
        Query: SELECT * FROM energy_credits WHERE user_id = ?
        """
        pass

    @abstractmethod
    def get_active_by_user_id(self, user_id: int) -> List[EnergyCredit]:
        """Obtiene solo los créditos vigentes (no vencidos ni agotados)"""
        pass

    @abstractmethod
    def save(self, credit: EnergyCredit) -> EnergyCredit:
        """Guarda un nuevo crédito energético"""
        pass

    @abstractmethod
    def update_used_kwh(self, credit_id: int, used_kwh: float) -> EnergyCredit:
        """Actualiza los kWh utilizados de un crédito"""
        pass
