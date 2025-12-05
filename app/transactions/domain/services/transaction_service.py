from typing import List
from app.transactions.domain.models.transaction import Transaction
from app.transactions.domain.ports.transaction_repository_port import TransactionRepositoryPort
from app.shared.infrastructure.response import ResultHandler

class TransactionService:
    """
    Servicio de dominio para transacciones.
    Contiene la lógica de negocio relacionada con transacciones P2P de energía.
    """

    def __init__(self, transaction_repository: TransactionRepositoryPort):
        """
        Inyección de dependencias: recibe la interfaz del repositorio.

        Args:
            transaction_repository: Puerto que define el contrato de persistencia
        """
        self.transaction_repository = transaction_repository

    def get_all_transactions(self):
        """
        Caso de uso: Obtener todas las transacciones del sistema.

        Returns:
            HTTP Response: Respuesta estructurada con ResultHandler
        """
        try:
            transactions = self.transaction_repository.get_all()
            transactions_dict = [transaction.model_dump() for transaction in transactions]

            return ResultHandler.success(
                data=transactions_dict,
                message=f"Se obtuvieron {len(transactions)} transacciones correctamente"
            )

        except ValueError as e:
            return ResultHandler.bad_request(message=str(e))

        except Exception as e:
            print(f"Error al obtener transacciones: {e}")
            return ResultHandler.internal_error(
                message="Error al obtener transacciones"
            )
