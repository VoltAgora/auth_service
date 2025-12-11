from typing import List, Optional
from sqlalchemy.orm import Session
from app.user.domain.ports.pde_allocation_repository_port import PDEAllocationRepositoryPort
from app.user.domain.models.pde_allocation import PDEAllocation
from app.user.adapters.persistence.pde_allocation_entity import PDEAllocationEntity
from app.shared.infrastructure.db import get_db


class PDEAllocationRepositorySQL(PDEAllocationRepositoryPort):
    """
    Implementación SQL del repositorio de asignaciones PDE.
    Usa las queries exactas especificadas en la arquitectura.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: PDEAllocationEntity) -> PDEAllocation:
        """Convierte entidad ORM a modelo de dominio"""
        return PDEAllocation(
            id=entity.id,
            user_id=entity.user_id,
            community_id=entity.community_id,
            allocation_period=entity.allocation_period,
            allocated_kwh=entity.allocated_kwh,
            share_percentage=entity.share_percentage,
            created_at=entity.created_at
        )

    def get_by_user_and_period(self, user_id: int, allocation_period: str) -> Optional[PDEAllocation]:
        """
        Query especificada:
        SELECT * FROM pde_allocations WHERE user_id = ? AND allocation_period = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(PDEAllocationEntity).filter(
                PDEAllocationEntity.user_id == user_id,
                PDEAllocationEntity.allocation_period == allocation_period
            ).first()

            if entity is None:
                return None

            return self._entity_to_domain(entity)
        except Exception as e:
            raise Exception(f"Error al obtener asignación PDE: {str(e)}")
        finally:
            db.close()

    def get_by_user_id(self, user_id: int) -> List[PDEAllocation]:
        """
        Obtiene todas las asignaciones históricas de un usuario.
        Query: SELECT * FROM pde_allocations WHERE user_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(PDEAllocationEntity).filter(
                PDEAllocationEntity.user_id == user_id
            ).order_by(PDEAllocationEntity.allocation_period.desc()).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener asignaciones de usuario: {str(e)}")
        finally:
            db.close()

    def get_by_community_and_period(self, community_id: int, allocation_period: str) -> List[PDEAllocation]:
        """
        Obtiene todas las asignaciones de una comunidad en un periodo.
        Query: SELECT * FROM pde_allocations WHERE community_id = ? AND allocation_period = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(PDEAllocationEntity).filter(
                PDEAllocationEntity.community_id == community_id,
                PDEAllocationEntity.allocation_period == allocation_period
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener asignaciones de comunidad: {str(e)}")
        finally:
            db.close()

    def save(self, allocation: PDEAllocation) -> PDEAllocation:
        """
        Guarda una nueva asignación PDE.
        Query: INSERT INTO pde_allocations (...)
        """
        db = self._get_db_session()
        try:
            allocation_entity = PDEAllocationEntity(
                user_id=allocation.user_id,
                community_id=allocation.community_id,
                allocation_period=allocation.allocation_period,
                allocated_kwh=allocation.allocated_kwh,
                share_percentage=allocation.share_percentage,
                created_at=allocation.created_at
            )

            db.add(allocation_entity)
            db.commit()
            db.refresh(allocation_entity)

            return self._entity_to_domain(allocation_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar asignación PDE: {str(e)}")
        finally:
            db.close()
