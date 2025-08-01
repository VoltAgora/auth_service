from app.domain.ports.db_port import UserRepositoryPort
from app.domain.models.user import User
from app.adapters.persistence.user_entity import UserEntity
from app.infrastructure.db import SessionLocal
from sqlalchemy.orm import Session

class UserRepositorySQL(UserRepositoryPort):
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_by_email(self, email: str) -> User | None:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if not user_entity:
            return None
        return self._map_to_domain(user_entity)

    def save(self, user: User) -> User:
        user_entity = UserEntity(
            name=user.name,
            lastname=user.lastname,
            phone=user.phone,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            role=user.role
        )
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)
        return self._map_to_domain(user_entity)

    def _map_to_domain(self, user_entity: UserEntity) -> User:
        return User(
            id=user_entity.id,
            name=user_entity.name,
            lastname=user_entity.lastname,
            phone=user_entity.phone,
            email=user_entity.email,
            hashed_password=user_entity.hashed_password,
            is_active=user_entity.is_active,
            role=user_entity.role
        )
