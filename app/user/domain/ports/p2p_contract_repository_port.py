from abc import ABC, abstractmethod
from app.user.domain.models.p2p_contract import P2PContract
from typing import List

class P2PContractRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de contratos P2P.
    Define el contrato para operaciones de contratos de compra-venta.
    """

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[P2PContract]:
        """
        Obtiene todos los contratos donde el usuario es comprador o vendedor.
        Query: SELECT * FROM p2p_contracts WHERE seller_id = ? OR buyer_id = ?
        """
        pass

    @abstractmethod
    def get_active_by_user_id(self, user_id: int) -> List[P2PContract]:
        """Obtiene solo los contratos activos de un usuario"""
        pass

    @abstractmethod
    def get_by_seller_id(self, seller_id: int) -> List[P2PContract]:
        """Obtiene contratos donde el usuario es vendedor"""
        pass

    @abstractmethod
    def get_by_buyer_id(self, buyer_id: int) -> List[P2PContract]:
        """Obtiene contratos donde el usuario es comprador"""
        pass

    @abstractmethod
    def save(self, contract: P2PContract) -> P2PContract:
        """Guarda un nuevo contrato P2P"""
        pass

    @abstractmethod
    def update_status(self, contract_id: int, status: str) -> P2PContract:
        """Actualiza el estado de un contrato"""
        pass
