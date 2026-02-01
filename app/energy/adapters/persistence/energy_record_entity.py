from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger
from app.shared.infrastructure.db import Base
from datetime import datetime
from zoneinfo import ZoneInfo

bogota_tz = ZoneInfo("America/Bogota")


def bogota_now():
    return datetime.now(bogota_tz)


class EnergyReadingEntity(Base):
    """
    Entidad de base de datos para lecturas individuales de energía.

    Descompone el JSON de entrada y almacena cada lectura como un registro individual.
    Esto facilita consultas, análisis y reportes sobre los datos de energía.
    """
    __tablename__ = "energy_readings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Metadata del request
    operation = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    meter_id = Column(String(100), nullable=False, index=True)

    # Datos de la lectura
    timestamp = Column(BigInteger, nullable=False, index=True)  # ts en milisegundos
    flag = Column(Integer, nullable=False)

    # Voltaje (voltage)
    voltage_a = Column(Float, nullable=True)
    voltage_b = Column(Float, nullable=True)
    voltage_c = Column(Float, nullable=True)

    # Corriente (current)
    current_a = Column(Float, nullable=True)
    current_b = Column(Float, nullable=True)
    current_c = Column(Float, nullable=True)

    # Potencia (power)
    power_ai = Column(Float, nullable=True)  # Active Import
    power_ae = Column(Float, nullable=True)  # Active Export
    power_ri = Column(Float, nullable=True)  # Reactive Import
    power_re = Column(Float, nullable=True)  # Reactive Export

    # Energía (energy)
    energy_ai = Column(Float, nullable=True)  # Active Import
    energy_ae = Column(Float, nullable=True)  # Active Export
    energy_ri = Column(Float, nullable=True)  # Reactive Import
    energy_re = Column(Float, nullable=True)  # Reactive Export

    # Metadata del sistema
    created_at = Column(DateTime(timezone=True), default=bogota_now)

    def __repr__(self):
        return f"<EnergyReading(id={self.id}, meter_id='{self.meter_id}', timestamp={self.timestamp})>"
