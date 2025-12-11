from typing import List, Optional
from sqlalchemy.orm import Session
from app.user.domain.ports.user_repository_port import UserRepositoryPort
from app.user.domain.models.user import User
from app.user.adapters.persistence.user_entity import UserEntity
from app.shared.infrastructure.db import get_db


class UserRepositorySQL(UserRepositoryPort):
    """
    Implementación SQL del repositorio de usuarios.
    Adaptador que conecta el dominio con MySQL.
    """

    def __init__(self):
        pass

    def _get_db_session(self) -> Session:
        """Obtiene sesión de base de datos"""
        db_generator = get_db()
        return next(db_generator)

    def _entity_to_domain(self, entity: UserEntity) -> User:
        """Convierte entidad ORM a modelo de dominio"""
        return User(
            id=entity.id,
            document=entity.document,
            name=entity.name,
            lastname=entity.lastname,
            phone=entity.phone,
            email=entity.email,
            created_at=entity.created_at,
            is_active=entity.is_active,
            role=entity.role
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene usuario por ID.
        Query: SELECT * FROM users WHERE id = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if entity is None:
                return None
            return self._entity_to_domain(entity)
        except Exception as e:
            raise Exception(f"Error al obtener usuario {user_id}: {str(e)}")
        finally:
            db.close()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene usuario por email.
        Query: SELECT * FROM users WHERE email = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(UserEntity).filter(UserEntity.email == email).first()
            if entity is None:
                return None
            return self._entity_to_domain(entity)
        except Exception as e:
            raise Exception(f"Error al obtener usuario por email {email}: {str(e)}")
        finally:
            db.close()

    def get_all(self) -> List[User]:
        """
        Obtiene todos los usuarios.
        Query: SELECT * FROM users
        """
        db = self._get_db_session()
        try:
            entities = db.query(UserEntity).all()
            return [self._entity_to_domain(entity) for entity in entities]
        except Exception as e:
            raise Exception(f"Error al obtener todos los usuarios: {str(e)}")
        finally:
            db.close()

    def save(self, user: User) -> User:
        """
        Guarda un nuevo usuario.
        Query: INSERT INTO users (document, name, lastname, phone, email, is_active, role)
               VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db = self._get_db_session()
        try:
            user_entity = UserEntity(
                document=user.document,
                name=user.name,
                lastname=user.lastname,
                phone=user.phone,
                email=user.email,
                created_at=user.created_at,
                is_active=user.is_active,
                role=user.role
            )
            db.add(user_entity)
            db.commit()
            db.refresh(user_entity)
            return self._entity_to_domain(user_entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al guardar usuario: {str(e)}")
        finally:
            db.close()

    def update(self, user: User) -> User:
        """
        Actualiza un usuario existente.
        Query: UPDATE users SET ... WHERE id = ?
        """
        db = self._get_db_session()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user.id).first()
            if not entity:
                raise ValueError(f"Usuario {user.id} no encontrado")

            entity.name = user.name
            entity.lastname = user.lastname
            entity.phone = user.phone
            entity.email = user.email
            entity.is_active = user.is_active
            entity.role = user.role

            db.commit()
            db.refresh(entity)
            return self._entity_to_domain(entity)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al actualizar usuario: {str(e)}")
        finally:
            db.close()
