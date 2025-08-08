from typing import List
from app.domain.models.city import City
from app.domain.ports.db_port import CityRepositoryPort
from app.infrastructure.response import ResultHandler

class CityService:
  """
  Servicio de dominio para ciudades.
  Contiene la LÓGICA DE NEGOCIO relacionada con ciudades.
  
  Este servicio:
  - NO conoce nada sobre bases de datos, HTTP, o tecnologías externas
  - Recibe un puerto (interfaz) como dependencia
  - Implementa reglas de negocio puras
  - Es el CORAZÓN del hexágono
  """
    
  def __init__(self, city_repository: CityRepositoryPort):
    """
    Inyección de dependencias: recibe la INTERFAZ, no la implementación.
    
    Args:
        city_repository: Puerto que define el contrato de persistencia
    """
    self.city_repository = city_repository
    
  def get_all_cities(self):
    """
    Caso de uso: Obtener todas las ciudades del sistema.
    Lógica de negocio:
    1. Obtiene las ciudades del repositorio
    2. Aplica reglas de negocio (ej: filtros, validaciones)
    3. Maneja errores y retorna respuesta HTTP estructurada
    Returns:
        HTTP Response: Respuesta estructurada con ResultHandler
    """
    try:
      # 1. Obtener datos del repositorio (a través del puerto)
      cities = self.city_repository.get_all()
      # 2. Convertir a diccionarios para JSON serialization
      cities_dict = [city.model_dump() for city in cities]

      # 3. Retornar respuesta exitosa
      return ResultHandler.success(
        data=cities_dict,
        message=f"Se obtuvieron {len(cities)} ciudades correctamente"
      )
        
    except ValueError as e:
      # Error de validación de negocio
      return ResultHandler.bad_request(message=str(e))
        
    except Exception as e:
      # Error técnico (DB, conexión, etc.)
      print(f"Error al obtener ciudades: {e}")
      message= "Error al obtener ciudades" + " - " + str(e)
      # Retornar error interno
      return ResultHandler.internal_error(
        message=message
      )

  def get_city_by_id(self, city_id: int) -> City | None:
    """
    Caso de uso: Obtener una ciudad específica por su ID.
    
    Args:
        city_id: ID de la ciudad a buscar
        
    Returns:
        City | None: Ciudad encontrada o None si no existe
    """
    if city_id <= 0:
      # Regla de negocio: IDs deben ser positivos
      raise ValueError("El ID de la ciudad debe ser un número positivo")
    
    return self.city_repository.get_by_id(city_id)
  
  def get_cities_by_department(self, department_code: int) -> List[City]:
    """
    Caso de uso: Obtener ciudades de un departamento específico.
    
    Args:
      department_code: Código del departamento
        
    Returns:
      List[City]: Lista de ciudades del departamento
    """
    if department_code <= 0:
      raise ValueError("El código del departamento debe ser un número positivo")
    
    cities = self.city_repository.get_by_department(department_code)
    
    # Aplicar lógica de negocio específica para ciudades por departamento
    return self._apply_business_rules(cities)
  
  def _apply_business_rules(self, cities: List[City]) -> List[City]:
    """
    Aplica reglas de negocio generales a las ciudades.
    
    Ejemplos de reglas de negocio:
    - Ordenar alfabéticamente
    - Filtrar ciudades activas
    - Aplicar validaciones específicas del dominio
    
    Args:
        cities: Lista de ciudades sin procesar
        
    Returns:
        List[City]: Lista de ciudades con reglas aplicadas
    """
    # Ejemplo: ordenar por nombre
    sorted_cities = sorted(cities, key=lambda city: city.nomCiudad)
    
    # Ejemplo: filtrar ciudades con nombres válidos
    valid_cities = [city for city in sorted_cities if city.nomCiudad and city.nomCiudad.strip()]
    
    return valid_cities