from app.domain.ports.db_port import UserRepositoryPort
from app.domain.models.user import User, AuthData
from app.adapters.persistence.user_entity import User as UserEntity, AuthData as AuthDataEntity
from app.infrastructure.db import SessionLocal
from sqlalchemy.orm import Session

class UserRepositorySQL(UserRepositoryPort):
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_by_email(self, email: str) -> User | None:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if not user_entity:
            return None
        return self._user_entity_to_domain(user_entity)

    def get_by_document(self, document: str) -> User | None:
        user_entity = self.db.query(UserEntity).filter(UserEntity.document == document).first()
        if not user_entity:
            return None
        return self._user_entity_to_domain(user_entity)

    def save(self, user: User) -> User:
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
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)
        return self._user_entity_to_domain(user_entity)

    def save_auth_data(self, auth_data: AuthData) -> AuthData:
        auth_entity = AuthDataEntity(
            user_id=auth_data.user_id,
            password=auth_data.password
        )
        self.db.add(auth_entity)
        self.db.commit()
        self.db.refresh(auth_entity)
        return self._auth_entity_to_domain(auth_entity)

    def get_auth_data_by_user_id(self, user_id: int) -> AuthData | None:
        auth_entity = self.db.query(AuthDataEntity).filter(AuthDataEntity.user_id == user_id).first()
        if not auth_entity:
            return None
        return self._auth_entity_to_domain(auth_entity)

    def _user_entity_to_domain(self, user_entity: UserEntity) -> User:
        """
        Mapper: Convierte una entidad User de base de datos a modelo de dominio User.
        Args:
          user_entity (UserEntity): Entidad de la base de datos
        Returns:
          User: Modelo de dominio
        """
        return User(
            id=user_entity.id,
            document=user_entity.document,
            name=user_entity.name,
            lastname=user_entity.lastname,
            phone=user_entity.phone,
            email=user_entity.email,
            created_at=user_entity.created_at,
            is_active=user_entity.is_active,
            role=user_entity.role
        )

    def _auth_entity_to_domain(self, auth_entity: AuthDataEntity) -> AuthData:
        """
        Mapper: Convierte una entidad AuthData de base de datos a modelo de dominio AuthData.
        Args:
          auth_entity (AuthDataEntity): Entidad de la base de datos
        Returns:
          AuthData: Modelo de dominio
        """
        return AuthData(
            id=auth_entity.id,
            user_id=auth_entity.user_id,
            password=auth_entity.password
        )
