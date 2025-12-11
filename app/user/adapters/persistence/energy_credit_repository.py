from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from app.user.domain.ports.energy_credit_repository_port import EnergyCreditRepositoryPort
from app.user.domain.models.energy_credit import EnergyCredit
from app.user.adapters.persistence.energy_credit_entity import EnergyCreditEntity
from app.shared.infrastructure.db import get_db


class EnergyCreditRepositorySQL(EnergyCreditRepositoryPort):
    """
    Implementación SQL del repositorio de créditos energéticos.
    Usa las queries exactas especificadas en la arquitectura.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: EnergyCreditEntity) -> EnergyCredit:
        """Convierte entidad ORM a modelo de dominio"""
        return EnergyCredit(
            id=entity.id,
            user_id=entity.user_id,
            credit_kwh=entity.credit_kwh,
            expiration_date=entity.expiration_date,
            created_at=entity.created_at,
            used_kwh=entity.used_kwh
        )

    def get_by_user_id(self, user_id: int) -> List[EnergyCredit]:
        """
        Query especificada: SELECT * FROM energy_credits WHERE user_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(EnergyCreditEntity).filter(
                EnergyCreditEntity.user_id == user_id
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener créditos de usuario {user_id}: {str(e)}")
        finally:
            db.close()

    def get_active_by_user_id(self, user_id: int) -> List[EnergyCredit]:
        """
        Obtiene solo créditos vigentes (no vencidos ni agotados).
        Query: SELECT * FROM energy_credits WHERE user_id = ?
               AND (expiration_date IS NULL OR expiration_date > NOW())
               AND used_kwh < credit_kwh
        """
        db = self._get_db_session()
        try:
            now = datetime.now()

            entities = db.query(EnergyCreditEntity).filter(
                EnergyCreditEntity.user_id == user_id,
                (EnergyCreditEntity.expiration_date.is_(None)) |
                (EnergyCreditEntity.expiration_date > now),
                EnergyCreditEntity.used_kwh < EnergyCreditEntity.credit_kwh
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener créditos activos: {str(e)}")
        finally:
            db.close()

    def save(self, credit: EnergyCredit) -> EnergyCredit:
        """
        Guarda un nuevo crédito energético.
        Query: INSERT INTO energy_credits (...)
        """
        db = self._get_db_session()
        try:
            credit_entity = EnergyCreditEntity(
                user_id=credit.user_id,
                credit_kwh=credit.credit_kwh,
                expiration_date=credit.expiration_date,
                created_at=credit.created_at,
                used_kwh=credit.used_kwh
            )

            db.add(credit_entity)
            db.commit()
            db.refresh(credit_entity)

            return self._entity_to_domain(credit_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar crédito energético: {str(e)}")
        finally:
            db.close()

    def update_used_kwh(self, credit_id: int, used_kwh: float) -> EnergyCredit:
        """
        Actualiza los kWh utilizados de un crédito.
        Query: UPDATE energy_credits SET used_kwh = ? WHERE id = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(EnergyCreditEntity).filter(
                EnergyCreditEntity.id == credit_id
            ).first()

            if not entity:
                raise ValueError(f"Crédito {credit_id} no encontrado")

            entity.used_kwh = used_kwh
            db.commit()
            db.refresh(entity)

            return self._entity_to_domain(entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al actualizar crédito: {str(e)}")
        finally:
            db.close()
