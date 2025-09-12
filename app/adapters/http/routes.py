from fastapi import APIRouter, Body, Header, BackgroundTasks
from app.domain.services.auth_service import AuthService
from app.domain.services.city_service import CityService
from app.adapters.persistence.user_repository import UserRepositorySQL
from app.adapters.persistence.city_repository import CityRepositorySQL
from app.infrastructure.response import ResultHandler
from app.adapters.http.auth_dtos import RegisterRequest, LoginRequest, TokenVerifyRequest, ForgotPasswordRequest, ResetPasswordRequest

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

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks):
    try:
        res = auth_manager.generate_and_store_otp(request.document)
    except ValueError as e:
        return ResultHandler.bad_request(message=str(e))
    except Exception as e:
        print("Error en generate_and_store_otp route:", e)
        return ResultHandler.internal_error(message="Error interno al solicitar OTP")

    # Programar envío asíncrono
    background_tasks.add_task(auth_manager.send_otp_email_async, res["email"], res["otp"])
    # Nota: en producción NO incluyas OTP en la respuesta. Aquí devolvemos mensaje genérico.
    return ResultHandler.success(message="Si existe una cuenta con ese documento, se ha enviado un OTP al correo registrado.")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    result = auth_manager.reset_password(request)
    return result

@router.get("/verify-token")
def verify_token(authorization: str = Header(...)):
    result = auth_manager.verify_token(authorization)
    return result

@router.get("/cities")
def get_cities():
    result = city_service.get_all_cities()
    return result 
