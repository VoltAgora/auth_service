from fastapi import APIRouter, Body, Query
from app.user.domain.services.city_service import CityService
from app.user.domain.services.user_service import UserService
from app.user.adapters.persistence.city_repository import CityRepositorySQL
from app.user.adapters.persistence.user_repository import UserRepositorySQL
from app.user.adapters.persistence.community_member_repository import CommunityMemberRepositorySQL
from app.user.adapters.persistence.energy_record_repository import EnergyRecordRepositorySQL
from app.user.adapters.persistence.p2p_contract_repository import P2PContractRepositorySQL
from app.user.adapters.persistence.energy_credit_repository import EnergyCreditRepositorySQL
from app.user.adapters.persistence.pde_allocation_repository import PDEAllocationRepositorySQL
from app.user.adapters.http.user_dtos import RegisterUserInCommunityRequest
from app.shared.infrastructure.response import ResultHandler

router = APIRouter(
    prefix="/user",
    tags=["User Service"]
)

# Inyección de dependencias - Configuración de servicios
city_repo = CityRepositorySQL()
city_service = CityService(city_repo)

# Repositorios para UserService
user_repo = UserRepositorySQL()
community_member_repo = CommunityMemberRepositorySQL()
energy_record_repo = EnergyRecordRepositorySQL()
p2p_contract_repo = P2PContractRepositorySQL()
energy_credit_repo = EnergyCreditRepositorySQL()
pde_allocation_repo = PDEAllocationRepositorySQL()

user_service = UserService(
    user_repository=user_repo,
    community_member_repository=community_member_repo,
    energy_record_repository=energy_record_repo,
    p2p_contract_repository=p2p_contract_repo,
    energy_credit_repository=energy_credit_repo,
    pde_allocation_repository=pde_allocation_repo
)


@router.get("/cities")
def get_cities():
    result = city_service.get_all_cities()
    return result

@router.get('/cities-with-departments')
def get_cities_with_departments():
    result = city_service.get_cities_with_departments()
    return result


# ========== ENDPOINTS DE USUARIOS P2P ==========

@router.get("/{user_id}/complete-data")
def get_user_with_community_data(user_id: int):
    """
    Obtiene datos completos de un usuario con información energética.
    Incluye: datos básicos, membresía, energía del mes, contratos, créditos, PDE.
    """
    result = user_service.get_user_with_community_data(user_id)
    return result


@router.get("/community/{community_id}/members")
def get_community_users(community_id: int):
    """
    Obtiene lista completa de usuarios de una comunidad.
    Incluye: datos consolidados, energía, contratos, créditos, PDE.
    """
    result = user_service.get_community_users(community_id)
    return result


@router.get("/{user_id}/energy-balance")
def get_user_energy_balance(
    user_id: int,
    period: str = Query(..., description="Periodo en formato YYYY-MM")
):
    """
    Obtiene balance energético detallado de un usuario.
    Calcula: autoconsumo, excedentes, importaciones, compras/ventas P2P, balance neto.
    """
    result = user_service.get_user_energy_balance(user_id, period)
    return result


@router.post("/register-in-community")
def register_user_in_community(request: RegisterUserInCommunityRequest = Body(...)):
    """
    Registra un usuario en una comunidad energética.
    Valida: usuario activo, no duplicado, rol válido, pde_share en rango.
    """
    result = user_service.register_user_in_community(
        user_id=request.user_id,
        community_id=request.community_id,
        role=request.role,
        pde_share=request.pde_share,
        installed_capacity=request.installed_capacity
    )
    return result


@router.get("/ping")
def ping():
    """Health check para el servicio de usuarios"""
    return ResultHandler.success(message="pong desde user service")
