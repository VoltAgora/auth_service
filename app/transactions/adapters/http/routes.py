from fastapi import APIRouter
from app.transactions.domain.services.transaction_service import TransactionService
from app.transactions.adapters.persistence.transaction_repository import TransactionRepositorySQL

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions Service"]
)

# Inyección de dependencias - Configuración de servicios
transaction_repo = TransactionRepositorySQL()
transaction_service = TransactionService(transaction_repo)


@router.get("/")
def get_transactions():
    """Obtiene todas las transacciones"""
    result = transaction_service.get_all_transactions()
    return result

@router.get("/ping")
def ping():
    """Health check para el servicio de transacciones"""
    from app.shared.infrastructure.response import ResultHandler
    return ResultHandler.success(message="pong desde transactions")
