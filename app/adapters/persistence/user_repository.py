from typing import List
from sqlalchemy.orm import Session
from app.domain.ports.db_port import UserRepositoryPort
from app.domain.models.user import User, AuthData
from app.adapters.persistence.user_entity import User as UserEntity, AuthData as AuthDataEntity
from app.infrastructure.db import get_db
from datetime import datetime

class UserRepositorySQL(UserRepositoryPort):
  """
  Implementación concreta del UserRepositoryPort usando SQLAlchemy.
  Este es un ADAPTADOR que conecta el dominio con la base de datos.
  """
  
  def __init__(self):
    """
    Inicializa el repositorio.
    En una implementación más avanzada, podrías inyectar la sesión de DB.
    """
    pass
  
  def _get_db_session(self) -> Session:
    """
    Obtiene una sesión de base de datos.
    Helper privado para obtener la sesión de DB.
    """
    db_generator = get_db()
    return next(db_generator)
  
  def _user_entity_to_domain(self, entity: UserEntity) -> User:
    """
    Convierte una entidad User de base de datos a modelo de dominio.
    Args:
      entity (UserEntity): Entidad de la base de datos
    Returns:
      User: Modelo de dominio
    """
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
  
  def _auth_entity_to_domain(self, entity: AuthDataEntity) -> AuthData:
    """
    Convierte una entidad AuthData de base de datos a modelo de dominio.
    Args:
      entity (AuthDataEntity): Entidad de la base de datos
    Returns:
      AuthData: Modelo de dominio
    """
    return AuthData(
      id=entity.id,
      user_id=entity.user_id,
      password=entity.password
    )
  
  def get_by_email(self, email: str) -> User | None:
    """
    Implementación concreta: obtiene usuario por email desde MySQL.
    """
    db = self._get_db_session()
    try:
      entity = db.query(UserEntity).filter(UserEntity.email == email).first()
      
      if entity is None:
        return None
          
      return self._user_entity_to_domain(entity)
        
    except Exception as e:
      raise Exception(f"Error al obtener usuario por email {email}: {str(e)}")
    finally:
      db.close()
  
  def get_by_document(self, document: str) -> User | None:
    """
    Implementación concreta: obtiene usuario por documento desde MySQL.
    """
    db = self._get_db_session()
    try:
      entity = db.query(UserEntity).filter(UserEntity.document == document).first()
      
      if entity is None:
        return None
          
      return self._user_entity_to_domain(entity)
        
    except Exception as e:
      raise Exception(f"Error al obtener usuario por documento {document}: {str(e)}")
    finally:
      db.close()
  
  def get_by_id(self, user_id: int) -> User | None:
    """
    Implementación concreta: obtiene usuario por ID desde MySQL.
    """
    db = self._get_db_session()
    try:
      entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
      
      if entity is None:
        return None
          
      return self._user_entity_to_domain(entity)
        
    except Exception as e:
      raise Exception(f"Error al obtener usuario {user_id}: {str(e)}")
    finally:
      db.close()
  
  def save(self, user: User) -> User:
    """
    Implementación concreta: guarda usuario en MySQL.
    
    Flujo:
    1. Obtiene sesión de DB
    2. Crea entidad UserEntity desde modelo de dominio
    3. Persiste en base de datos
    4. Retorna modelo de dominio actualizado
    """
    db = self._get_db_session()
    try:
      # 1. Crear entidad desde modelo de dominio
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
      
      # 2. Persistir en base de datos
      db.add(user_entity)
      db.commit()
      db.refresh(user_entity)
      
      # 3. Retornar modelo de dominio
      return self._user_entity_to_domain(user_entity)
        
    except Exception as e:
      db.rollback()
      raise Exception(f"Error al guardar usuario: {str(e)}")
    finally:
      db.close()
  
  def save_auth_data(self, auth_data: AuthData) -> AuthData:
    """
    Implementación concreta: guarda datos de autenticación en MySQL.
    
    Flujo:
    1. Obtiene sesión de DB
    2. Crea entidad AuthDataEntity desde modelo de dominio
    3. Persiste en base de datos
    4. Retorna modelo de dominio actualizado
    """
    db = self._get_db_session()
    try:
      # 1. Crear entidad desde modelo de dominio
      auth_entity = AuthDataEntity(
        user_id=auth_data.user_id,
        password=auth_data.password
      )
      
      # 2. Persistir en base de datos
      db.add(auth_entity)
      db.commit()
      db.refresh(auth_entity)
      
      # 3. Retornar modelo de dominio
      return self._auth_entity_to_domain(auth_entity)
        
    except Exception as e:
      db.rollback()
      raise Exception(f"Error al guardar datos de autenticación: {str(e)}")
    finally:
      db.close()
  
  def get_auth_data_by_user_id(self, user_id: int) -> AuthData | None:
    """
    Implementación concreta: obtiene datos de autenticación por user_id desde MySQL.
    """
    db = self._get_db_session()
    try:
      entity = db.query(AuthDataEntity).filter(AuthDataEntity.user_id == user_id).first()
      
      if entity is None:
        return None
          
      return self._auth_entity_to_domain(entity)
        
    except Exception as e:
      raise Exception(f"Error al obtener datos de autenticación del usuario {user_id}: {str(e)}")
    finally:
      db.close()

  def create_password_reset(self, user_id: int, otp_hash: str, expires_at: datetime):
    db = self._get_db_session()
    try:
      from app.adapters.persistence.password_reset_entity import PasswordReset
      pr = PasswordReset(
        user_id=user_id,
        otp_hash=otp_hash,
        expires_at=expires_at
      )
      db.add(pr)
      db.commit()
      db.refresh(pr)
      return pr
    except Exception as e:
      db.rollback()
      raise Exception(f"Error al crear password reset: {str(e)}")
    finally:
      db.close()

  def get_active_password_reset(self, user_id: int):
    db = self._get_db_session()
    try:
      from app.adapters.persistence.password_reset_entity import PasswordReset
      # Retornar el más reciente que no esté usado y que no esté expirado
      now = datetime.now()
      pr = db.query(PasswordReset).filter(
          PasswordReset.user_id == user_id,
          PasswordReset.used == False,
          PasswordReset.expires_at > now
      ).order_by(PasswordReset.created_at.desc()).first()
      return pr
    except Exception as e:
      raise Exception(f"Error al obtener password reset: {str(e)}")
    finally:
      db.close()

  def increment_reset_attempts(self, reset_id: int):
    db = self._get_db_session()
    try:
      from app.adapters.persistence.password_reset_entity import PasswordReset
      pr = db.query(PasswordReset).filter(PasswordReset.id == reset_id).first()
      if not pr:
        return None
      pr.attempts = (pr.attempts or 0) + 1
      db.add(pr)
      db.commit()
      db.refresh(pr)
      return pr
    except Exception as e:
      db.rollback()
      raise Exception(f"Error al incrementar intentos: {str(e)}")
    finally:
      db.close()

  def mark_reset_used(self, reset_id: int):
    db = self._get_db_session()
    try:
      from app.adapters.persistence.password_reset_entity import PasswordReset
      pr = db.query(PasswordReset).filter(PasswordReset.id == reset_id).first()
      if not pr:
        return None
      pr.used = True
      db.add(pr)
      db.commit()
      db.refresh(pr)
      return pr
    except Exception as e:
      db.rollback()
      raise Exception(f"Error al marcar reset usado: {str(e)}")
    finally:
      db.close()

  def update_auth_password(self, user_id: int, new_hashed_password: str):
    db = self._get_db_session()
    try:
      from app.adapters.persistence.user_entity import AuthData as AuthDataEntity
      auth = db.query(AuthDataEntity).filter(AuthDataEntity.user_id == user_id).first()
      if not auth:
        # Si no existe, crear registro (por si se registro sin auth_data)
        auth = AuthDataEntity(user_id=user_id, password=new_hashed_password)
        db.add(auth)
      else:
        auth.password = new_hashed_password
        db.add(auth)
      db.commit()
      db.refresh(auth)
      return auth
    except Exception as e:
      db.rollback()
      raise Exception(f"Error al actualizar password: {str(e)}")
    finally:
      db.close()
