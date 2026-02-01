from fastapi import APIRouter, Body
from app.energy.domain.services.energy_service import EnergyService
from app.energy.adapters.persistence.energy_repository import EnergyRepositorySQL
from app.shared.infrastructure.response import ResultHandler
from app.energy.adapters.http.energy_dtos import SaveRecordRequest

router = APIRouter(
    prefix="/energy",
    tags=["Energy Service"]
)

# Inyección de dependencias - Configuración de servicios
energy_repo = EnergyRepositorySQL()
energy_manager = EnergyService(energy_repo)


@router.get("/ping")
def ping():
    return ResultHandler.success(message="pong desde energy")


@router.post("/save-record")
def save_record(request: SaveRecordRequest = Body(...)):
    """
    Endpoint para guardar registros de lecturas de medidores de energía.

    Acepta datos en el formato:
    {
      "operation": "sendReadings",
      "subject": "onDemand",
      "meter": {
        "meter_id": [array de lecturas]
      }
    }

    Returns:
        JSON response con status 200 y mensaje de confirmación
    """
    # Convertir el DTO a diccionario para pasarlo al servicio
    result = energy_manager.save_record(request.model_dump())
    return result
