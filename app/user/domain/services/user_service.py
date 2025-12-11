from typing import Dict, Any, List, Optional
from decimal import Decimal
from datetime import datetime
from app.user.domain.ports.user_repository_port import UserRepositoryPort
from app.user.domain.ports.community_member_repository_port import CommunityMemberRepositoryPort
from app.user.domain.ports.energy_record_repository_port import EnergyRecordRepositoryPort
from app.user.domain.ports.p2p_contract_repository_port import P2PContractRepositoryPort
from app.user.domain.ports.energy_credit_repository_port import EnergyCreditRepositoryPort
from app.user.domain.ports.pde_allocation_repository_port import PDEAllocationRepositoryPort
from app.user.domain.models.community_member import CommunityMember
from app.shared.infrastructure.response import ResultHandler


class UserService:
    """
    Servicio de dominio para gestión integral de usuarios en el sistema P2P.
    Implementa los casos de uso definidos en la arquitectura hexagonal.

    Casos de uso:
    - getUserWithCommunityData: Datos completos de usuario con info energética
    - getCommunityUsers: Lista de miembros con datos consolidados
    - getUserEnergyBalance: Balance energético detallado
    - registerUserInCommunity: Registro de usuario en comunidad
    """

    def __init__(
        self,
        user_repository: UserRepositoryPort,
        community_member_repository: CommunityMemberRepositoryPort,
        energy_record_repository: EnergyRecordRepositoryPort,
        p2p_contract_repository: P2PContractRepositoryPort,
        energy_credit_repository: EnergyCreditRepositoryPort,
        pde_allocation_repository: PDEAllocationRepositoryPort
    ):
        """Inyección de dependencias - Inversión de control"""
        self.user_repository = user_repository
        self.community_member_repository = community_member_repository
        self.energy_record_repository = energy_record_repository
        self.p2p_contract_repository = p2p_contract_repository
        self.energy_credit_repository = energy_credit_repository
        self.pde_allocation_repository = pde_allocation_repository


    def get_user_with_community_data(self, user_id: int) -> Dict[str, Any]:
        """
        Caso de uso: Obtener datos completos de un usuario.

        Retorna:
        - Datos básicos del usuario
        - Rol en la comunidad
        - Membresía (community_members)
        - Energía del mes actual (generated, consumed, exported, imported)
        - Contratos P2P activos
        - Créditos energéticos vigentes
        - Asignaciones PDE del periodo actual

        Args:
            user_id: ID del usuario

        Returns:
            HTTP Response con ResultHandler
        """
        try:
            # 1. Obtener usuario
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return ResultHandler.not_found(message=f"Usuario {user_id} no encontrado")

            # 2. Obtener membresía en comunidad
            membership = self.community_member_repository.get_by_user_id(user_id)

            # 3. Periodo actual (YYYY-MM)
            current_period = datetime.now().strftime("%Y-%m")

            # 4. Registro energético del mes
            energy_record = None
            energy_data = {}
            if membership:
                energy_record = self.energy_record_repository.get_by_user_and_period(
                    user_id, current_period
                )
                if energy_record:
                    energy_data = {
                        "generated_kwh": float(energy_record.generated_kwh),
                        "consumed_kwh": float(energy_record.consumed_kwh),
                        "exported_kwh": float(energy_record.exported_kwh),
                        "imported_kwh": float(energy_record.imported_kwh),
                        "self_consumption_kwh": float(energy_record.get_self_consumption()),
                        "surplus_kwh": float(energy_record.get_surplus()),
                        "deficit_kwh": float(energy_record.get_deficit())
                    }

            # 5. Contratos P2P activos
            contracts = self.p2p_contract_repository.get_active_by_user_id(user_id)
            contracts_data = [
                {
                    "id": c.id,
                    "seller_id": c.seller_id,
                    "buyer_id": c.buyer_id,
                    "energy_kwh": float(c.energy_kwh),
                    "price_per_kwh": float(c.price_per_kwh),
                    "total_value": float(c.get_total_value()),
                    "contract_period": c.contract_period,
                    "status": c.status,
                    "role": "seller" if c.seller_id == user_id else "buyer"
                }
                for c in contracts
            ]

            # 6. Créditos energéticos vigentes
            credits = self.energy_credit_repository.get_active_by_user_id(user_id)
            credits_data = [
                {
                    "id": c.id,
                    "credit_kwh": float(c.credit_kwh),
                    "used_kwh": float(c.used_kwh),
                    "available_kwh": float(c.get_available_credit()),
                    "expiration_date": c.expiration_date.isoformat() if c.expiration_date else None
                }
                for c in credits
            ]

            # 7. Asignaciones PDE del periodo
            pde_allocation = None
            pde_data = {}
            if membership:
                pde_allocation = self.pde_allocation_repository.get_by_user_and_period(
                    user_id, current_period
                )
                if pde_allocation:
                    pde_data = {
                        "allocated_kwh": float(pde_allocation.allocated_kwh),
                        "share_percentage": float(pde_allocation.share_percentage),
                        "period": pde_allocation.allocation_period
                    }

            # 8. Construir respuesta completa
            response_data = {
                "user": {
                    "id": user.id,
                    "document": user.document,
                    "name": user.name,
                    "lastname": user.lastname,
                    "email": user.email,
                    "phone": user.phone,
                    "is_active": user.is_active,
                    "role": user.role
                },
                "community_membership": {
                    "community_id": membership.community_id if membership else None,
                    "role": membership.role if membership else None,
                    "pde_share": float(membership.pde_share) if membership and membership.pde_share else None,
                    "installed_capacity": float(membership.installed_capacity) if membership and membership.installed_capacity else None,
                    "joined_at": membership.joined_at.isoformat() if membership and membership.joined_at else None
                } if membership else None,
                "current_month_energy": energy_data if energy_data else None,
                "active_contracts": contracts_data,
                "active_credits": credits_data,
                "pde_allocation": pde_data if pde_data else None
            }

            return ResultHandler.success(
                data=response_data,
                message="Datos de usuario obtenidos exitosamente"
            )

        except ValueError as e:
            return ResultHandler.bad_request(message=str(e))
        except Exception as e:
            print(f"Error al obtener datos de usuario: {e}")
            return ResultHandler.internal_error(
                message="Error interno al obtener datos de usuario"
            )


    def get_community_users(self, community_id: int) -> Dict[str, Any]:
        """
        Caso de uso: Obtener lista completa de usuarios de una comunidad.

        Retorna para cada miembro:
        - Datos de usuario
        - Datos energéticos consolidados
        - Contratos P2P
        - Créditos
        - Participación PDE

        Args:
            community_id: ID de la comunidad

        Returns:
            HTTP Response con ResultHandler
        """
        try:
            # 1. Obtener todos los miembros de la comunidad
            members = self.community_member_repository.get_by_community_id(community_id)

            if not members:
                return ResultHandler.success(
                    data={"members": []},
                    message="No se encontraron miembros en la comunidad"
                )

            # 2. Periodo actual
            current_period = datetime.now().strftime("%Y-%m")

            # 3. Procesar cada miembro
            members_data = []
            for member in members:
                user = self.user_repository.get_by_id(member.user_id)
                if not user:
                    continue

                # Datos energéticos
                energy_record = self.energy_record_repository.get_by_user_and_period(
                    member.user_id, current_period
                )

                # Contratos
                contracts = self.p2p_contract_repository.get_active_by_user_id(member.user_id)

                # Créditos
                credits = self.energy_credit_repository.get_active_by_user_id(member.user_id)
                total_credits = sum(float(c.get_available_credit()) for c in credits)

                # PDE
                pde = self.pde_allocation_repository.get_by_user_and_period(
                    member.user_id, current_period
                )

                member_data = {
                    "user_id": user.id,
                    "name": f"{user.name} {user.lastname}",
                    "email": user.email,
                    "role": member.role,
                    "pde_share": float(member.pde_share) if member.pde_share else 0,
                    "installed_capacity": float(member.installed_capacity) if member.installed_capacity else 0,
                    "energy_data": {
                        "generated_kwh": float(energy_record.generated_kwh) if energy_record else 0,
                        "consumed_kwh": float(energy_record.consumed_kwh) if energy_record else 0,
                        "exported_kwh": float(energy_record.exported_kwh) if energy_record else 0,
                        "imported_kwh": float(energy_record.imported_kwh) if energy_record else 0
                    },
                    "active_contracts_count": len(contracts),
                    "total_credits_kwh": total_credits,
                    "pde_allocated_kwh": float(pde.allocated_kwh) if pde else 0
                }

                members_data.append(member_data)

            return ResultHandler.success(
                data={
                    "community_id": community_id,
                    "members_count": len(members_data),
                    "members": members_data
                },
                message=f"Se obtuvieron {len(members_data)} miembros de la comunidad"
            )

        except ValueError as e:
            return ResultHandler.bad_request(message=str(e))
        except Exception as e:
            print(f"Error al obtener usuarios de comunidad: {e}")
            return ResultHandler.internal_error(
                message="Error interno al obtener usuarios de comunidad"
            )


    def get_user_energy_balance(self, user_id: int, period: str) -> Dict[str, Any]:
        """
        Caso de uso: Obtener balance energético detallado de un usuario.

        Calcula:
        - Autoconsumo
        - Excedentes
        - Importaciones
        - Compras P2P
        - Ventas P2P
        - Balance neto

        Args:
            user_id: ID del usuario
            period: Periodo en formato 'YYYY-MM'

        Returns:
            HTTP Response con ResultHandler
        """
        try:
            # 1. Validar usuario
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return ResultHandler.not_found(message=f"Usuario {user_id} no encontrado")

            # 2. Obtener registro energético del periodo
            energy_record = self.energy_record_repository.get_by_user_and_period(user_id, period)

            if not energy_record:
                return ResultHandler.not_found(
                    message=f"No hay registros energéticos para el usuario {user_id} en el periodo {period}"
                )

            # 3. Calcular métricas del dominio
            self_consumption = energy_record.get_self_consumption()
            surplus = energy_record.get_surplus()
            deficit = energy_record.get_deficit()

            # 4. Obtener contratos P2P del periodo
            all_contracts = self.p2p_contract_repository.get_by_user_id(user_id)
            period_contracts = [c for c in all_contracts if c.contract_period == period]

            # Separar ventas y compras
            sales = [c for c in period_contracts if c.seller_id == user_id]
            purchases = [c for c in period_contracts if c.buyer_id == user_id]

            total_sold_kwh = sum(float(c.energy_kwh) for c in sales)
            total_bought_kwh = sum(float(c.energy_kwh) for c in purchases)
            total_sold_value = sum(float(c.get_total_value()) for c in sales)
            total_bought_value = sum(float(c.get_total_value()) for c in purchases)

            # 5. Balance neto
            net_balance = (
                float(energy_record.generated_kwh) +
                total_bought_kwh -
                float(energy_record.consumed_kwh) -
                total_sold_kwh
            )

            # 6. Construir respuesta
            balance_data = {
                "user_id": user_id,
                "period": period,
                "generation": {
                    "total_generated_kwh": float(energy_record.generated_kwh),
                    "self_consumed_kwh": float(self_consumption),
                    "surplus_kwh": float(surplus)
                },
                "consumption": {
                    "total_consumed_kwh": float(energy_record.consumed_kwh),
                    "from_own_generation_kwh": float(self_consumption),
                    "deficit_kwh": float(deficit)
                },
                "grid_interaction": {
                    "exported_to_grid_kwh": float(energy_record.exported_kwh),
                    "imported_from_grid_kwh": float(energy_record.imported_kwh)
                },
                "p2p_transactions": {
                    "sold_kwh": total_sold_kwh,
                    "sold_value": total_sold_value,
                    "bought_kwh": total_bought_kwh,
                    "bought_value": total_bought_value,
                    "sales_count": len(sales),
                    "purchases_count": len(purchases)
                },
                "net_balance_kwh": net_balance
            }

            return ResultHandler.success(
                data=balance_data,
                message="Balance energético calculado exitosamente"
            )

        except ValueError as e:
            return ResultHandler.bad_request(message=str(e))
        except Exception as e:
            print(f"Error al calcular balance energético: {e}")
            return ResultHandler.internal_error(
                message="Error interno al calcular balance energético"
            )


    def register_user_in_community(
        self,
        user_id: int,
        community_id: int,
        role: str,
        pde_share: Optional[Decimal] = None,
        installed_capacity: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """
        Caso de uso: Registrar un usuario en una comunidad energética.

        Validaciones:
        - Usuario existe y está activo
        - No está ya registrado en la comunidad
        - Rol es válido (producer, consumer, prosumer)
        - pde_share está entre 0 y 1

        Args:
            user_id: ID del usuario
            community_id: ID de la comunidad
            role: Rol del usuario ('producer', 'consumer', 'prosumer')
            pde_share: Participación en excedentes (0-1)
            installed_capacity: Capacidad instalada en kW

        Returns:
            HTTP Response con ResultHandler
        """
        try:
            # 1. Validar usuario
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return ResultHandler.not_found(message=f"Usuario {user_id} no encontrado")

            if not user.is_active:
                return ResultHandler.bad_request(message="El usuario no está activo")

            # 2. Validar que no esté ya registrado
            existing_membership = self.community_member_repository.get_by_user_id(user_id)
            if existing_membership:
                return ResultHandler.bad_request(
                    message=f"El usuario ya está registrado en la comunidad {existing_membership.community_id}"
                )

            # 3. Validar rol
            valid_roles = ['producer', 'consumer', 'prosumer']
            if role not in valid_roles:
                return ResultHandler.bad_request(
                    message=f"Rol inválido. Debe ser uno de: {', '.join(valid_roles)}"
                )

            # 4. Validar pde_share
            if pde_share is not None:
                if pde_share < 0 or pde_share > 1:
                    return ResultHandler.bad_request(
                        message="pde_share debe estar entre 0 y 1"
                    )

            # 5. Valores por defecto
            if pde_share is None:
                pde_share = Decimal("0.1")  # 10% por defecto

            if installed_capacity is None:
                installed_capacity = Decimal("0")

            # 6. Crear membresía
            member = CommunityMember(
                community_id=community_id,
                user_id=user_id,
                role=role,
                pde_share=pde_share,
                installed_capacity=installed_capacity,
                joined_at=datetime.now()
            )

            saved_member = self.community_member_repository.save(member)

            # 7. Preparar respuesta
            response_data = {
                "membership_id": saved_member.id,
                "user_id": user_id,
                "community_id": community_id,
                "role": role,
                "pde_share": float(pde_share),
                "installed_capacity": float(installed_capacity),
                "joined_at": saved_member.joined_at.isoformat() if saved_member.joined_at else None
            }

            return ResultHandler.created(
                data=response_data,
                message="Usuario registrado exitosamente en la comunidad"
            )

        except ValueError as e:
            return ResultHandler.bad_request(message=str(e))
        except Exception as e:
            print(f"Error al registrar usuario en comunidad: {e}")
            return ResultHandler.internal_error(
                message="Error interno al registrar usuario en comunidad"
            )
