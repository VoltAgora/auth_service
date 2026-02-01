from typing import Optional, List
from sqlalchemy.orm import Session
from app.energy.domain.ports.energy_repository_port import EnergyRepositoryPort
from app.energy.domain.models.energy_record import EnergyRecord
from app.energy.adapters.persistence.energy_record_entity import EnergyReadingEntity
from app.shared.infrastructure.db import get_db


class EnergyRepositorySQL(EnergyRepositoryPort):
    """
    Implementación concreta del EnergyRepositoryPort usando SQLAlchemy.
    Este es un ADAPTADOR que conecta el dominio con la base de datos.

    Descompone el EnergyRecord en lecturas individuales para almacenarlas
    de forma normalizada en la base de datos.
    """

    def __init__(self):
        """
        Inicializa el repositorio.
        """
        pass

    def _get_db_session(self) -> Session:
        """
        Obtiene una sesión de base de datos.
        Helper privado para obtener la sesión de DB.
        """
        db_generator = get_db()
        return next(db_generator)

    def _create_reading_entity(self, operation: str, subject: str, meter_id: str, reading_data) -> EnergyReadingEntity:
        """
        Crea una entidad EnergyReadingEntity desde los datos de una lectura.

        Args:
            operation (str): Tipo de operación
            subject (str): Sujeto de la operación
            meter_id (str): ID del medidor
            reading_data: Datos de la lectura individual

        Returns:
            EnergyReadingEntity: Entidad lista para persistir
        """
        return EnergyReadingEntity(
            operation=operation,
            subject=subject,
            meter_id=meter_id,
            timestamp=reading_data.ts,
            flag=reading_data.flag,
            # Voltaje
            voltage_a=reading_data.voltage.a,
            voltage_b=reading_data.voltage.b,
            voltage_c=reading_data.voltage.c,
            # Corriente
            current_a=reading_data.current.a,
            current_b=reading_data.current.b,
            current_c=reading_data.current.c,
            # Potencia
            power_ai=reading_data.power.ai,
            power_ae=reading_data.power.ae,
            power_ri=reading_data.power.ri,
            power_re=reading_data.power.re,
            # Energía
            energy_ai=reading_data.energy.ai,
            energy_ae=reading_data.energy.ae,
            energy_ri=reading_data.energy.ri,
            energy_re=reading_data.energy.re
        )

    def save(self, energy_record: EnergyRecord) -> EnergyRecord:
        """
        Implementación concreta: guarda registro de energía en MySQL.

        Descompone el EnergyRecord en lecturas individuales y las persiste
        de forma normalizada en la tabla energy_readings.

        Flujo:
        1. Obtiene sesión de DB
        2. Itera sobre cada medidor y sus lecturas
        3. Crea una entidad EnergyReadingEntity por cada lectura
        4. Persiste todas las lecturas en batch
        5. Retorna el modelo de dominio original

        Args:
            energy_record (EnergyRecord): Registro de energía a guardar

        Returns:
            EnergyRecord: Registro original con metadata actualizada
        """
        db = self._get_db_session()
        try:
            entities_to_save = []

            # Descomponer el registro en lecturas individuales
            for meter_reading in energy_record.meter_readings:
                meter_id = meter_reading.meter_id

                # Crear una entidad por cada lectura individual
                for reading in meter_reading.readings:
                    entity = self._create_reading_entity(
                        operation=energy_record.operation,
                        subject=energy_record.subject,
                        meter_id=meter_id,
                        reading_data=reading
                    )
                    entities_to_save.append(entity)

            # Persistir todas las entidades en batch
            if entities_to_save:
                db.bulk_save_objects(entities_to_save)
                db.commit()

            return energy_record

        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar registros de energía: {str(e)}")
        finally:
            db.close()

    def get_by_id(self, record_id: int) -> Optional[EnergyRecord]:
        """
        Implementación concreta: obtiene registro de energía por ID desde MySQL.

        Args:
            record_id (int): ID del registro de lectura individual

        Returns:
            Optional[EnergyRecord]: Registro encontrado o None
        """
        db = self._get_db_session()
        try:
            entity = db.query(EnergyReadingEntity).filter(EnergyReadingEntity.id == record_id).first()

            if entity is None:
                return None

            # Reconstruir el modelo de dominio desde una sola lectura
            from app.energy.domain.models.energy_record import (
                MeterReadings, ReadingData, VoltageData, CurrentData, PowerData, EnergyData
            )

            reading = ReadingData(
                ts=entity.timestamp,
                flag=entity.flag,
                voltage=VoltageData(a=entity.voltage_a, b=entity.voltage_b, c=entity.voltage_c),
                current=CurrentData(a=entity.current_a, b=entity.current_b, c=entity.current_c),
                power=PowerData(ai=entity.power_ai, ae=entity.power_ae, ri=entity.power_ri, re=entity.power_re),
                energy=EnergyData(ai=entity.energy_ai, ae=entity.energy_ae, ri=entity.energy_ri, re=entity.energy_re)
            )

            meter_reading = MeterReadings(meter_id=entity.meter_id, readings=[reading])

            return EnergyRecord(
                id=entity.id,
                operation=entity.operation,
                subject=entity.subject,
                meter_readings=[meter_reading],
                created_at=entity.created_at
            )

        except Exception as e:
            raise Exception(f"Error al obtener registro de energía {record_id}: {str(e)}")
        finally:
            db.close()
