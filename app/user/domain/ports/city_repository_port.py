from abc import ABC, abstractmethod
from app.user.domain.models.city import City
from typing import List

class CityRepositoryPort(ABC):
    """
    Puerto (interfaz) para el repositorio de ciudades.
    Define el contrato que debe cumplir cualquier implementación
    de persistencia de ciudades (SQL, NoSQL, API externa, etc.)
    """

    @abstractmethod
    def get_all(self) -> List[City]:
        """Obtiene todas las ciudades del sistema.

        Returns:
            List[City]: Lista de todas las ciudades
        """
        pass

    @abstractmethod
    def get_by_id(self, city_id: int) -> City | None:
        """
        Obtiene una ciudad por su ID.

        Args:
            city_id (int): ID de la ciudad

        Returns:
            City | None: Ciudad encontrada o None si no existe
        """
        pass

    @abstractmethod
    def get_by_department(self, depto_code: int) -> List[City]:
        """
        Obtiene todas las ciudades de un departamento.

        Args:
            depto_code (int): Código del departamento

        Returns:
            List[City]: Lista de ciudades del departamento
        """
        pass
