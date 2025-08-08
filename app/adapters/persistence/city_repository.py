from typing import List
from sqlalchemy.orm import Session
from app.domain.ports.db_port import CityRepositoryPort
from app.domain.models.city import City
from app.adapters.persistence.city_entity import CityEntity
from app.infrastructure.db import get_db

class CityRepositorySQL(CityRepositoryPort):
  """
  Implementación concreta del CityRepositoryPort usando SQLAlchemy.
  Este es un ADAPTADOR que conecta el dominio con la base de datos.
  """
  
  def __init__(self):
    """
    Inicializa el repositorio.
    En una implementación más avanzada, podrías inyectar la sesión de DB.
    """
    pass
  
  def _get_db_session(self) -> Session:
    """
    Obtiene una sesión de base de datos.
    Helper privado para obtener la sesión de DB.
    """
    db_generator = get_db()
    return next(db_generator)
  
  def _entity_to_domain(self, entity: CityEntity) -> City:
    """
    Convierte una entidad de base de datos a modelo de dominio.
    Args:
      entity (CityEntity): Entidad de la base de datos
    Returns:
      City: Modelo de dominio
    """
    return City(
      codCiudad=entity.codCiudad,
      codCiudadDane=entity.codCiudadDane,
      codDepto=entity.codDepto,
      nomCiudad=entity.nomCiudad
    )
  
  def get_all(self) -> List[City]:
    """
    Implementación concreta: obtiene todas las ciudades desde MySQL.
    
    Flujo:
    1. Obtiene sesión de DB
    2. Consulta todas las entidades CityEntity
    3. Convierte cada entidad al modelo de dominio City
    4. Retorna lista de modelos de dominio
    """
    db = self._get_db_session()
    try:
      # 1. Consulta SQL a través del ORM
      city_entities = db.query(CityEntity).all()
      # 2. Conversión de entidades a modelos de dominio
      cities = [self._entity_to_domain(entity) for entity in city_entities]
      return cities
        
    except Exception as e:
      # En un escenario real, aquí manejarías logging y excepciones específicas
      raise Exception(f"Error al obtener ciudades: {str(e)}")
    finally:
      db.close()
  
  def get_by_id(self, city_id: int) -> City | None:
    """
    Implementación concreta: obtiene ciudad por ID desde MySQL.
    """
    db = self._get_db_session()
    try:
      entity = db.query(CityEntity).filter(CityEntity.codCiudad == city_id).first()
      
      if entity is None:
        return None
          
      return self._entity_to_domain(entity)
        
    except Exception as e:
      raise Exception(f"Error al obtener ciudad {city_id}: {str(e)}")
    finally:
      db.close()
  
  def get_by_department(self, depto_code: int) -> List[City]:
    """
    Implementación concreta: obtiene ciudades por departamento desde MySQL.
    """
    db = self._get_db_session()
    try:
      entities = db.query(CityEntity).filter(CityEntity.codDepto == depto_code).all()
      cities = [self._entity_to_domain(entity) for entity in entities]
      return cities
        
    except Exception as e:
      raise Exception(f"Error al obtener ciudades del departamento {depto_code}: {str(e)}")
    finally:
      db.close()