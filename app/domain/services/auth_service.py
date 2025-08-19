from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.domain.models.user import User, AuthData
from app.domain.ports.db_port import UserRepositoryPort
from app.adapters.http.auth_dtos import RegisterRequest, LoginRequest
from app.infrastructure.response import ResultHandler
import os # Para manejar variables de entorno
from dotenv import load_dotenv # Para cargar variables de entorno desde un archivo .env
from datetime import datetime
from zoneinfo import ZoneInfo


bogota_tz = ZoneInfo("America/Bogota")

load_dotenv()

class AuthService:
  """
  Servicio de autenticación que maneja el registro, login y verificación de tokens.
  
  Responsabilidades:
  - Registro de nuevos usuarios con hash de contraseña
  - Autenticación de usuarios existentes
  - Generación y verificación de tokens JWT
  - Validación de credenciales
  """
    
  def __init__(self, user_repository: UserRepositoryPort):
    self.user_repository = user_repository
    # Configuración para hash de contraseñas con bcrypt
    self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Configuración JWT - En producción estos valores deben venir de variables de entorno
    self.SECRET_KEY = os.getenv("SECRET_KEY")
    self.ALGORITHM  = os.getenv("ALGORITHM", "HS256")
    self.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)


  def register(self, request: RegisterRequest):
    """
    Caso de uso: Registrar un nuevo usuario en el sistema.
    
    Lógica de negocio:
    1. Valida que no exista usuario con mismo email o documento
    2. Crea usuario en la base de datos
    3. Hashea y guarda la contraseña por separado
    4. Genera token JWT de acceso
    
    Args:
      request (RegisterRequest): Datos de registro del usuario
        
    Returns:
      HTTP Response: Respuesta estructurada con ResultHandler
    """
    try:
      # Verificar si el usuario ya existe por email o documento
      existing_user_email = self.user_repository.get_by_email(request.email)
      if existing_user_email:
        return ResultHandler.bad_request(message="Ya existe un usuario con este email")
            
      existing_user_document = self.user_repository.get_by_document(request.document)
      if existing_user_document:
        return ResultHandler.bad_request(message="Ya existe un usuario con este documento")
        
      # Crear objeto User del dominio
      user_data = User(
        document=request.document,
        name=request.name,
        lastname=request.lastname,
        phone=request.phone if request.phone else None,
        email=request.email,
        created_at=datetime.now(bogota_tz),
        is_active=True,
        role=request.role if request.role else 0
      )
        
      # Guardar usuario
      saved_user = self.user_repository.save(user_data)
        
      # Hash de la contraseña y guardar datos de auth
      hashed_password = self._hash_password(request.password)
      # Creo el modelo del authData
      auth_data = AuthData(
        user_id=saved_user.id,
        password=hashed_password
      )

      self.user_repository.save_auth_data(auth_data)

      # Preparar datos de respuesta
      response_data = {
        "documento": saved_user.document,
        "email": saved_user.email
      }
        
      return ResultHandler.created(
        data=response_data,
        message="Usuario registrado exitosamente"
      )
        
    except ValueError as e:
      # Error de validación de negocio
      return ResultHandler.bad_request(message=str(e))
    except Exception as e:
      # Error técnico (DB, conexión, etc.)
      print(f"Error al registrar usuario: {e}")
      return ResultHandler.internal_error(
          message="Error interno del servidor al registrar usuario"
      )


  def login(self, request: LoginRequest):
    """
    Caso de uso: Autenticar un usuario existente.
    
    Lógica de negocio:
    1. Busca usuario por email
    2. Verifica que esté activo
    3. Valida la contraseña
    4. Genera nuevo token JWT
    
    Args:
        request (LoginRequest): Datos de login del usuario
        
    Returns:
        HTTP Response: Respuesta estructurada con ResultHandler
    """
    try:
      # Buscar usuario por email
      user = self.user_repository.get_by_email(request.email)
      if not user:
          return ResultHandler.unauthorized(message="Credenciales inválidas")
        
      # Verificar que el usuario esté activo
      if not user.is_active:
          return ResultHandler.unauthorized(message="Usuario inactivo")
        
      # Obtener datos de autenticación
      auth_data = self.user_repository.get_auth_data_by_user_id(user.id)
      if not auth_data:
          return ResultHandler.unauthorized(message="Datos de autenticación no encontrados")
        
      # Verificar contraseña
      if not self._verify_password(request.password, auth_data.password):
          return ResultHandler.unauthorized(message="Credenciales inválidas")
        
      # Generar token de acceso
      access_token = self._create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
      })
        
      # Preparar datos de respuesta
      response_data = {
        "user_id": user.id,
        "email": user.email,
        "access_token": access_token
      }
        
      return ResultHandler.success(
        data=response_data,
        message="Log-in exitoso"
      )
        
    except ValueError as e:
      # Error de validación de negocio
      return ResultHandler.unauthorized(message=str(e))
    except Exception as e:
      # Error técnico (DB, conexión, etc.)
      print(f"Error al hacer login: {e}")
      return ResultHandler.internal_error(
          message="Error interno del servidor al hacer login"
      )


  def verify_token(self, authorization_header: str):
    """
    Caso de uso: Verificar la validez de un token JWT.
    
    Lógica de negocio:
    1. Extrae token del header Authorization
    2. Decodifica y valida el JWT
    3. Verifica que el usuario esté activo
    4. Retorna información del usuario
    
    Args:
        authorization_header (str): Header Authorization completo
        
    Returns:
        HTTP Response: Respuesta estructurada con ResultHandler
    """
    try:
      # Extraer token del header "Bearer <token>"
      if not authorization_header.startswith("Bearer "):
          return ResultHandler.unauthorized(message="Formato de token inválido")
        
      token = authorization_header.split(" ")[1]
        
      # Decodificar token
      payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
      user_id: str = payload.get("sub")
        
      if user_id is None:
          return ResultHandler.unauthorized(message="Token inválido")
            
      # Buscar usuario por ID
      user = self.user_repository.get_by_id(int(user_id))
      if user is None:
          return ResultHandler.unauthorized(message="Usuario no encontrado")
          
      if not user.is_active:
          return ResultHandler.unauthorized(message="Usuario inactivo")
            
      # Preparar datos de respuesta
      user_data = {
        "id": user.id,
        "document": user.document,
        "name": user.name,
        "lastname": user.lastname,
        "phone": user.phone,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
      }
        
      return ResultHandler.success(
        data=user_data,
        message="Token válido"
      )
          
    except JWTError:
      return ResultHandler.unauthorized(message="Token inválido o expirado")
    except ValueError as e:
      # Error de validación de negocio
      return ResultHandler.unauthorized(message=str(e))
    except Exception as e:
      # Error técnico (DB, conexión, etc.)
      print(f"Error al verificar token: {e}")
      return ResultHandler.internal_error(
          message="Error interno del servidor al verificar token"
      )


  def _hash_password(self, password: str) -> str:
    """
    Genera hash de la contraseña usando bcrypt.
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
    """
    return self.pwd_context.hash(password)


  def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        plain_password (str): Contraseña en texto plano
        hashed_password (str): Hash de la contraseña
        
    Returns:
        bool: True si coinciden, False en caso contrario
    """
    return self.pwd_context.verify(plain_password, hashed_password)


  def _create_access_token(self, data: dict) -> str:
    """
    Crea un token JWT de acceso.
    
    Args:
        data (dict): Datos a incluir en el token
        
    Returns:
        str: Token JWT firmado
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    return encoded_jwt
