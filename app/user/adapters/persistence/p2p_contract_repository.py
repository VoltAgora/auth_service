from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.user.domain.ports.p2p_contract_repository_port import P2PContractRepositoryPort
from app.user.domain.models.p2p_contract import P2PContract
from app.user.adapters.persistence.p2p_contract_entity import P2PContractEntity
from app.shared.infrastructure.db import get_db


class P2PContractRepositorySQL(P2PContractRepositoryPort):
    """
    Implementación SQL del repositorio de contratos P2P.
    Usa las queries exactas especificadas en la arquitectura.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: P2PContractEntity) -> P2PContract:
        """Convierte entidad ORM a modelo de dominio"""
        return P2PContract(
            id=entity.id,
            seller_id=entity.seller_id,
            buyer_id=entity.buyer_id,
            energy_kwh=entity.energy_kwh,
            price_per_kwh=entity.price_per_kwh,
            contract_period=entity.contract_period,
            status=entity.status,
            created_at=entity.created_at
        )

    def get_by_user_id(self, user_id: int) -> List[P2PContract]:
        """
        Query especificada: SELECT * FROM p2p_contracts WHERE seller_id = ? OR buyer_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(P2PContractEntity).filter(
                or_(
                    P2PContractEntity.seller_id == user_id,
                    P2PContractEntity.buyer_id == user_id
                )
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener contratos de usuario {user_id}: {str(e)}")
        finally:
            db.close()

    def get_active_by_user_id(self, user_id: int) -> List[P2PContract]:
        """
        Obtiene solo contratos activos de un usuario.
        Query: SELECT * FROM p2p_contracts WHERE (seller_id = ? OR buyer_id = ?) AND status = 'active'
        """
        db = self._get_db_session()
        try:
            entities = db.query(P2PContractEntity).filter(
                or_(
                    P2PContractEntity.seller_id == user_id,
                    P2PContractEntity.buyer_id == user_id
                ),
                P2PContractEntity.status == 'active'
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener contratos activos: {str(e)}")
        finally:
            db.close()

    def get_by_seller_id(self, seller_id: int) -> List[P2PContract]:
        """
        Query: SELECT * FROM p2p_contracts WHERE seller_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(P2PContractEntity).filter(
                P2PContractEntity.seller_id == seller_id
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener contratos como vendedor: {str(e)}")
        finally:
            db.close()

    def get_by_buyer_id(self, buyer_id: int) -> List[P2PContract]:
        """
        Query: SELECT * FROM p2p_contracts WHERE buyer_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(P2PContractEntity).filter(
                P2PContractEntity.buyer_id == buyer_id
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener contratos como comprador: {str(e)}")
        finally:
            db.close()

    def save(self, contract: P2PContract) -> P2PContract:
        """
        Guarda un nuevo contrato P2P.
        Query: INSERT INTO p2p_contracts (...)
        """
        db = self._get_db_session()
        try:
            contract_entity = P2PContractEntity(
                seller_id=contract.seller_id,
                buyer_id=contract.buyer_id,
                energy_kwh=contract.energy_kwh,
                price_per_kwh=contract.price_per_kwh,
                contract_period=contract.contract_period,
                status=contract.status,
                created_at=contract.created_at
            )

            db.add(contract_entity)
            db.commit()
            db.refresh(contract_entity)

            return self._entity_to_domain(contract_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar contrato P2P: {str(e)}")
        finally:
            db.close()

    def update_status(self, contract_id: int, status: str) -> P2PContract:
        """
        Actualiza el estado de un contrato.
        Query: UPDATE p2p_contracts SET status = ? WHERE id = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(P2PContractEntity).filter(
                P2PContractEntity.id == contract_id
            ).first()

            if not entity:
                raise ValueError(f"Contrato {contract_id} no encontrado")

            entity.status = status
            db.commit()
            db.refresh(entity)

            return self._entity_to_domain(entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al actualizar estado del contrato: {str(e)}")
        finally:
            db.close()
