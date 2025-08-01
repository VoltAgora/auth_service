from fastapi import APIRouter, Body
from app.domain.services.auth_service import AuthService
from app.adapters.persistence.user_repository import UserRepositorySQL
from app.infrastructure.response import ResultHandler
from app.domain.models.user import User


router = APIRouter(
  prefix="/auth",
  tags=["Auth Service"]
)

# Crear el repositorio y el manager
repo = UserRepositorySQL()
auth_manager = AuthService(repo)

@router.get("/ping")
def ping():
  return ResultHandler.success(message="pong desde auth")

@router.post("/register")
def register(user: User = Body(...)):
    result = auth_manager.register(user)
    return ResultHandler.created(data={"id": result.id, "email": result.email})

@router.post("/login")
def login_user():
  return ResultHandler.success(message="Inicio de sesión exitoso (mock)")

@router.get("/verify-token")
def verify_token():
  return ResultHandler.success(message="Token válido (mock)")
