from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime


class VoltageData(BaseModel):
    """Modelo de dominio para datos de voltaje"""
    a: Optional[float] = None
    b: Optional[float] = None
    c: Optional[float] = None


class CurrentData(BaseModel):
    """Modelo de dominio para datos de corriente"""
    a: Optional[float] = None
    b: Optional[float] = None
    c: Optional[float] = None


class PowerData(BaseModel):
    """Modelo de dominio para datos de potencia"""
    ai: Optional[float] = None  # Active Import
    ae: Optional[float] = None  # Active Export
    ri: Optional[float] = None  # Reactive Import
    re: Optional[float] = None  # Reactive Export


class EnergyData(BaseModel):
    """Modelo de dominio para datos de energía"""
    ai: Optional[float] = None  # Active Import
    ae: Optional[float] = None  # Active Export
    ri: Optional[float] = None  # Reactive Import
    re: Optional[float] = None  # Reactive Export


class ReadingData(BaseModel):
    """Modelo de dominio para una lectura individual"""
    ts: int  # Timestamp
    flag: int
    voltage: VoltageData
    current: CurrentData
    power: PowerData
    energy: EnergyData


class MeterReadings(BaseModel):
    """Modelo de dominio para lecturas de un medidor"""
    meter_id: str
    readings: List[ReadingData]


class EnergyRecord(BaseModel):
    """
    Modelo de dominio para registro de energía.

    Representa los datos completos de lecturas de medidores
    enviados por dispositivos IoT.
    """
    id: Optional[int] = None
    operation: str
    subject: str
    meter_readings: List[MeterReadings]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
