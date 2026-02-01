"""
Script para crear la tabla energy_readings en la base de datos.
Ejecutar con: python create_energy_table.py
"""
from app.shared.infrastructure.db import engine, Base
from app.energy.adapters.persistence.energy_record_entity import EnergyReadingEntity

def create_tables():
    """Crea la tabla energy_readings si no existe"""
    try:
        # Crear solo la tabla de energy_readings
        EnergyReadingEntity.__table__.create(engine, checkfirst=True)
        print("✅ Tabla 'energy_readings' creada exitosamente (o ya existía)")
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")

if __name__ == "__main__":
    create_tables()
