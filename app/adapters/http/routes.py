from fastapi import APIRouter, Body, Header
from app.domain.services.auth_service import AuthService
from app.domain.services.city_service import CityService
from app.adapters.persistence.user_repository import UserRepositorySQL
from app.adapters.persistence.city_repository import CityRepositorySQL
from app.infrastructure.response import ResultHandler
from app.adapters.http.auth_dtos import RegisterRequest, LoginRequest

router = APIRouter(
  prefix="/auth",
  tags=["Auth Service"]
)

# Inyección de dependencias - Configuración de servicios
user_repo = UserRepositorySQL()
auth_manager = AuthService(user_repo)

city_repo = CityRepositorySQL()
city_service = CityService(city_repo)


@router.get("/ping")
def ping():
    return ResultHandler.success(message="pong desde auth")

@router.post("/sign-up")
def sign_up(request: RegisterRequest = Body(...)):
    result = auth_manager.register(request)
    return result

@router.post("/log-in")
def log_in(request: LoginRequest = Body(...)):
    result = auth_manager.login(request)
    return result

@router.get("/verify-token")
def verify_token(authorization: str = Header(...)):
    result = auth_manager.verify_token(authorization)
    return result

@router.get("/cities")
def get_cities():
    result = city_service.get_all_cities()
    return result 

@router.get('/cities-with-departments')
def get_cities_with_departments():
    result = city_service.get_cities_with_departments()
    return result
