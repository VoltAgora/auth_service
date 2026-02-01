from datetime import datetime
from typing import Dict, Any
from app.energy.domain.models.energy_record import EnergyRecord, MeterReadings, ReadingData, VoltageData, CurrentData, PowerData, EnergyData
from app.energy.domain.ports.energy_repository_port import EnergyRepositoryPort
from app.shared.infrastructure.response import ResultHandler
from zoneinfo import ZoneInfo


bogota_tz = ZoneInfo("America/Bogota")


class EnergyService:
    """
    Servicio de energía que maneja el almacenamiento de registros de lecturas.

    Responsabilidades:
    - Procesar y validar lecturas de medidores
    - Almacenar registros de energía
    - Transformar datos de entrada a modelos de dominio
    """

    def __init__(self, energy_repository: EnergyRepositoryPort):
        self.energy_repository = energy_repository

    def save_record(self, request_data: Dict[str, Any]):
        """
        Caso de uso: Guardar un nuevo registro de lecturas de energía.

        Lógica de negocio:
        1. Valida la estructura de los datos recibidos
        2. Transforma el diccionario de medidores en lista de MeterReadings
        3. Crea el registro en el sistema
        4. Por ahora solo simula el guardado (sin persistencia real)

        Args:
            request_data (Dict[str, Any]): Datos del registro de energía

        Returns:
            HTTP Response: Respuesta estructurada con ResultHandler
        """
        try:
            # Validar campos obligatorios
            if "operation" not in request_data:
                return ResultHandler.bad_request(message="Campo 'operation' es requerido")

            if "subject" not in request_data:
                return ResultHandler.bad_request(message="Campo 'subject' es requerido")

            if "meter" not in request_data:
                return ResultHandler.bad_request(message="Campo 'meter' es requerido")

            # Transformar el diccionario de meter a lista de MeterReadings
            meter_readings_list = []
            meter_dict = request_data.get("meter", {})

            for meter_id, readings_data in meter_dict.items():
                # Convertir cada reading al modelo ReadingData
                readings = []
                for reading_item in readings_data:
                    reading = ReadingData(
                        ts=reading_item.get("ts"),
                        flag=reading_item.get("flag"),
                        voltage=VoltageData(**reading_item.get("voltage", {})),
                        current=CurrentData(**reading_item.get("current", {})),
                        power=PowerData(**reading_item.get("power", {})),
                        energy=EnergyData(**reading_item.get("energy", {}))
                    )
                    readings.append(reading)

                meter_reading = MeterReadings(
                    meter_id=meter_id,
                    readings=readings
                )
                meter_readings_list.append(meter_reading)

            # Crear objeto EnergyRecord del dominio
            energy_record = EnergyRecord(
                operation=request_data.get("operation"),
                subject=request_data.get("subject"),
                meter_readings=meter_readings_list,
                created_at=datetime.now(bogota_tz)
            )

            # TODO: Implementar persistencia en base de datos
            # Descomentar las siguientes líneas cuando la tabla energy_readings esté creada:
            #
            # saved_record = self.energy_repository.save(energy_record)
            #
            # El repositorio descompondrá el registro en lecturas individuales
            # y las guardará en la tabla energy_readings

            # Preparar datos de respuesta
            response_data = {
                "operation": energy_record.operation,
                "subject": energy_record.subject,
                "meters_count": len(energy_record.meter_readings),
                "total_readings": sum(len(mr.readings) for mr in energy_record.meter_readings),
                "timestamp": energy_record.created_at.isoformat() if energy_record.created_at else None
            }

            return ResultHandler.success(
                data=response_data,
                message="El record ha sido almacenado correctamente"
            )

        except ValueError as e:
            # Error de validación de negocio
            return ResultHandler.bad_request(message=str(e))
        except Exception as e:
            # Error técnico (DB, conexión, etc.)
            print(f"Error al procesar registro de energía: {e}")
            return ResultHandler.internal_error(
                message="Error interno del servidor al procesar registro de energía"
            )
