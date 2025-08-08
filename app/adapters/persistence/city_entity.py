from sqlalchemy import Column, Integer, String
from app.infrastructure.db import Base

class CityEntity(Base):
  """
  Entidad de base de datos para la tabla de ciudades.
  Esta clase mapea la estructura de la tabla ciudades en la base de datos.
  Es parte del adaptador de persistencia, NO del dominio.
  """
  __tablename__ = "ciudades"  # Nombre de la tabla en la base de datos
  # Mapeo de columnas según la estructura que proporcionaste
  codCiudad = Column(Integer, primary_key=True, autoincrement=True)
  codCiudadDane = Column(String(50), nullable=False)
  codDepto = Column(Integer, nullable=False)
  nomCiudad = Column(String(100), nullable=False)
  
  # El método __repr__ en tu CityEntity es 
  # simplemente una forma de decirle a Python 
  # cómo quieres que se vea ese objeto cuando lo 
  # imprimas o lo inspecciones en la consola o en logs.
  def __repr__(self):
    return f"<CityEntity(id={self.codCiudad}, name={self.nomCiudad})>"