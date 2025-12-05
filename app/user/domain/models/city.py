from pydantic import BaseModel
from typing import Optional

class City(BaseModel):
  """
  Modelo de dominio para Ciudad.
  Representa una ciudad en el sistema sin depender de la base de datos.
  """
  codCiudad: int  # Código único de la ciudad (PK)
  codCiudadDane: str  # Código DANE de la ciudad
  codDepto: int  # Código del departamento
  nomCiudad: str  # Nombre de la ciudad
  
  class Config:
      # Permite que el modelo funcione con ORMs
      from_attributes = True