from typing import List, Optional
from sqlalchemy.orm import Session
from app.user.domain.ports.energy_record_repository_port import EnergyRecordRepositoryPort
from app.user.domain.models.energy_record import EnergyRecord
from app.user.adapters.persistence.energy_record_entity import EnergyRecordEntity
from app.shared.infrastructure.db import get_db


class EnergyRecordRepositorySQL(EnergyRecordRepositoryPort):
    """
    Implementación SQL del repositorio de registros energéticos.
    Usa las queries exactas especificadas en la arquitectura.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: EnergyRecordEntity) -> EnergyRecord:
        """Convierte entidad ORM a modelo de dominio"""
        return EnergyRecord(
            id=entity.id,
            user_id=entity.user_id,
            community_id=entity.community_id,
            period=entity.period,
            generated_kwh=entity.generated_kwh,
            consumed_kwh=entity.consumed_kwh,
            exported_kwh=entity.exported_kwh,
            imported_kwh=entity.imported_kwh,
            timestamp=entity.timestamp
        )

    def get_by_user_and_period(self, user_id: int, period: str) -> Optional[EnergyRecord]:
        """
        Query especificada: SELECT * FROM energy_records WHERE user_id = ? AND period = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(EnergyRecordEntity).filter(
                EnergyRecordEntity.user_id == user_id,
                EnergyRecordEntity.period == period
            ).first()

            if entity is None:
                return None

            return self._entity_to_domain(entity)
        except Exception as e:
            raise Exception(f"Error al obtener registro energético: {str(e)}")
        finally:
            db.close()

    def get_by_community_and_period(self, community_id: int, period: str) -> List[EnergyRecord]:
        """
        Query especificada: SELECT * FROM energy_records WHERE community_id = ? AND period = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(EnergyRecordEntity).filter(
                EnergyRecordEntity.community_id == community_id,
                EnergyRecordEntity.period == period
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener registros de comunidad: {str(e)}")
        finally:
            db.close()

    def get_by_user_id(self, user_id: int) -> List[EnergyRecord]:
        """
        Obtiene todos los registros históricos de un usuario.
        Query: SELECT * FROM energy_records WHERE user_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(EnergyRecordEntity).filter(
                EnergyRecordEntity.user_id == user_id
            ).order_by(EnergyRecordEntity.period.desc()).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener registros de usuario: {str(e)}")
        finally:
            db.close()

    def save(self, record: EnergyRecord) -> EnergyRecord:
        """
        Guarda un nuevo registro energético.
        Query: INSERT INTO energy_records (...)
        """
        db = self._get_db_session()
        try:
            record_entity = EnergyRecordEntity(
                user_id=record.user_id,
                community_id=record.community_id,
                period=record.period,
                generated_kwh=record.generated_kwh,
                consumed_kwh=record.consumed_kwh,
                exported_kwh=record.exported_kwh,
                imported_kwh=record.imported_kwh,
                timestamp=record.timestamp
            )

            db.add(record_entity)
            db.commit()
            db.refresh(record_entity)

            return self._entity_to_domain(record_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar registro energético: {str(e)}")
        finally:
            db.close()
