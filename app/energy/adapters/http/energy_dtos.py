from pydantic import BaseModel
from typing import Dict, List, Optional


class VoltageDTO(BaseModel):
    """DTO para datos de voltaje"""
    a: Optional[float] = None
    b: Optional[float] = None
    c: Optional[float] = None


class CurrentDTO(BaseModel):
    """DTO para datos de corriente"""
    a: Optional[float] = None
    b: Optional[float] = None
    c: Optional[float] = None


class PowerDTO(BaseModel):
    """DTO para datos de potencia"""
    ai: Optional[float] = None
    ae: Optional[float] = None
    ri: Optional[float] = None
    re: Optional[float] = None


class EnergyDTO(BaseModel):
    """DTO para datos de energía"""
    ai: Optional[float] = None
    ae: Optional[float] = None
    ri: Optional[float] = None
    re: Optional[float] = None


class ReadingDTO(BaseModel):
    """DTO para una lectura individual"""
    ts: int
    flag: int
    voltage: VoltageDTO
    current: CurrentDTO
    power: PowerDTO
    energy: EnergyDTO


class SaveRecordRequest(BaseModel):
    """
    DTO para la solicitud de guardar registro de energía.

    Acepta la estructura de datos de medidores IoT:
    {
      "operation": "sendReadings",
      "subject": "onDemand",
      "meter": {
        "22231127782": [
          {
            "ts": 1765918800000,
            "flag": 0,
            "voltage": {...},
            "current": {...},
            "power": {...},
            "energy": {...}
          }
        ]
      }
    }
    """
    operation: str
    subject: str
    meter: Dict[str, List[ReadingDTO]]

    class Config:
        json_schema_extra = {
            "example": {
                "operation": "sendReadings",
                "subject": "onDemand",
                "meter": {
                    "22231127782": [
                        {
                            "ts": 1765918800000,
                            "flag": 0,
                            "voltage": {"a": 121.4},
                            "current": {"a": 0.02},
                            "power": {"ai": 3, "ae": 0, "ri": 0, "re": 0},
                            "energy": {"ai": 1067, "ae": 726, "ri": 782, "re": 462}
                        }
                    ]
                }
            }
        }
