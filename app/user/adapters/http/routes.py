from fastapi import APIRouter
from app.user.domain.services.city_service import CityService
from app.user.adapters.persistence.city_repository import CityRepositorySQL

router = APIRouter(
    prefix="/user",
    tags=["User Service"]
)

# Inyección de dependencias - Configuración de servicios
city_repo = CityRepositorySQL()
city_service = CityService(city_repo)


@router.get("/cities")
def get_cities():
    result = city_service.get_all_cities()
    return result

@router.get('/cities-with-departments')
def get_cities_with_departments():
    result = city_service.get_cities_with_departments()
    return result
