from abc import ABC, abstractmethod
from app.transactions.domain.models.transaction import Transaction
from typing import List, Optional

class TransactionRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de transacciones.
    Define el contrato que debe cumplir cualquier implementación
    de persistencia de transacciones.
    """

    @abstractmethod
    def get_all(self) -> List[Transaction]:
        """Obtiene todas las transacciones"""
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Busca una transacción por ID"""
        pass

    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        """Guarda una nueva transacción"""
        pass
