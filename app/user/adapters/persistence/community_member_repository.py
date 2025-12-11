from typing import List, Optional
from sqlalchemy.orm import Session
from app.user.domain.ports.community_member_repository_port import CommunityMemberRepositoryPort
from app.user.domain.models.community_member import CommunityMember
from app.user.adapters.persistence.community_member_entity import CommunityMemberEntity
from app.shared.infrastructure.db import get_db


class CommunityMemberRepositorySQL(CommunityMemberRepositoryPort):
    """
    Implementación SQL del repositorio de miembros de comunidad.
    Usa las queries exactas especificadas en la arquitectura.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: CommunityMemberEntity) -> CommunityMember:
        """Convierte entidad ORM a modelo de dominio"""
        return CommunityMember(
            id=entity.id,
            community_id=entity.community_id,
            user_id=entity.user_id,
            role=entity.role,
            pde_share=entity.pde_share,
            installed_capacity=entity.installed_capacity,
            joined_at=entity.joined_at
        )

    def get_by_user_id(self, user_id: int) -> Optional[CommunityMember]:
        """
        Query especificada: SELECT * FROM community_members WHERE user_id = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(CommunityMemberEntity).filter(
                CommunityMemberEntity.user_id == user_id
            ).first()

            if entity is None:
                return None

            return self._entity_to_domain(entity)
        except Exception as e:
            raise Exception(f"Error al obtener miembro por user_id {user_id}: {str(e)}")
        finally:
            db.close()

    def get_by_community_id(self, community_id: int) -> List[CommunityMember]:
        """
        Query especificada: SELECT * FROM community_members WHERE community_id = ?
        """
        db = self._get_db_session()
        try:
            entities = db.query(CommunityMemberEntity).filter(
                CommunityMemberEntity.community_id == community_id
            ).all()

            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener miembros de comunidad {community_id}: {str(e)}")
        finally:
            db.close()

    def save(self, member: CommunityMember) -> CommunityMember:
        """
        Query especificada:
        INSERT INTO community_members (community_id, user_id, role, pde_share, installed_capacity)
        VALUES (?, ?, ?, ?, ?)
        """
        db = self._get_db_session()
        try:
            member_entity = CommunityMemberEntity(
                community_id=member.community_id,
                user_id=member.user_id,
                role=member.role,
                pde_share=member.pde_share,
                installed_capacity=member.installed_capacity,
                joined_at=member.joined_at
            )

            db.add(member_entity)
            db.commit()
            db.refresh(member_entity)

            return self._entity_to_domain(member_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar miembro de comunidad: {str(e)}")
        finally:
            db.close()

    def update(self, member: CommunityMember) -> CommunityMember:
        """Actualiza datos de un miembro"""
        db = self._get_db_session()
        try:
            entity = db.query(CommunityMemberEntity).filter(
                CommunityMemberEntity.id == member.id
            ).first()

            if not entity:
                raise ValueError(f"Miembro {member.id} no encontrado")

            entity.role = member.role
            entity.pde_share = member.pde_share
            entity.installed_capacity = member.installed_capacity

            db.commit()
            db.refresh(entity)

            return self._entity_to_domain(entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al actualizar miembro: {str(e)}")
        finally:
            db.close()
