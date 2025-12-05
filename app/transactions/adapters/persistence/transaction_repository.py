from typing import List, Optional
from sqlalchemy.orm import Session
from app.transactions.domain.ports.transaction_repository_port import TransactionRepositoryPort
from app.transactions.domain.models.transaction import Transaction
from app.transactions.adapters.persistence.transaction_entity import TransactionEntity
from app.shared.infrastructure.db import get_db

class TransactionRepositorySQL(TransactionRepositoryPort):
    """
    Implementación concreta del TransactionRepositoryPort usando SQLAlchemy.
    Este es un adaptador que conecta el dominio con la base de datos.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        """Obtiene una sesión de base de datos."""
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: TransactionEntity) -> Transaction:
        """
        Convierte una entidad de base de datos a modelo de dominio.
        """
        return Transaction(
            id=entity.id
            # Aquí mapear los demás campos
        )

    def get_all(self) -> List[Transaction]:
        """Obtiene todas las transacciones desde MySQL."""
        db = self._get_db_session()
        try:
            transaction_entities = db.query(TransactionEntity).all()
            transactions = [self._entity_to_domain(entity) for entity in transaction_entities]
            return transactions
        except Exception as e:
            raise Exception(f"Error al obtener transacciones: {str(e)}")
        finally:
            db.close()

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Obtiene transacción por ID desde MySQL."""
        db = self._get_db_session()
        try:
            entity = db.query(TransactionEntity).filter(TransactionEntity.id == transaction_id).first()
            if entity is None:
                return None
            return self._entity_to_domain(entity)
        except Exception as e:
            raise Exception(f"Error al obtener transacción {transaction_id}: {str(e)}")
        finally:
            db.close()

    def save(self, transaction: Transaction) -> Transaction:
        """Guarda transacción en MySQL."""
        db = self._get_db_session()
        try:
            transaction_entity = TransactionEntity(
                # Aquí mapear los campos del modelo al entity
            )
            db.add(transaction_entity)
            db.commit()
            db.refresh(transaction_entity)
            return self._entity_to_domain(transaction_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar transacción: {str(e)}")
        finally:
            db.close()
