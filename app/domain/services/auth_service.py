import random
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.domain.models.user import User, AuthData
from app.domain.ports.db_port import UserRepositoryPort
from app.adapters.http.auth_dtos import RegisterRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.infrastructure.response import ResultHandler
import os # Para manejar variables de entorno
from dotenv import load_dotenv # Para cargar variables de entorno desde un archivo .env
from zoneinfo import ZoneInfo
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import BackgroundTasks
from pydantic import EmailStr


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
    self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    self.mail_conf = ConnectionConfig(
        MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
        MAIL_FROM = os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME")),
        MAIL_PORT = int(os.getenv("MAIL_PORT", 587)),
        MAIL_SERVER = os.getenv("MAIL_SERVER"),
        MAIL_STARTTLS = os.getenv("MAIL_STARTTLS", "True").lower() in ("1","true","yes"),
        MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS", "False").lower() in ("1","true","yes"),
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = os.getenv("MAIL_VALIDATE_CERTS", "true").lower() in ("1","true","yes")
    )



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
        role=request.role if request.role is not None else 1
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

  # helper: generar OTP 6 dígitos como string
  def _generate_otp(self) -> str:
    return f"{random.randint(0, 999999):06d}"

  # helper: enviar correo (si no config, hace log)
  async def send_otp_email_async(self, to_email: str, otp: str) -> bool:
    """
    Envía OTP usando FastMail y la configuración self.mail_conf (pydantic v2 compatible).
    Retorna True si el envío se realizó (o si estamos en modo dev y no hay MAIL_SERVER).
    """
    mail_server = os.getenv("MAIL_SERVER")
    # Si no hay servidor, fallback: log (modo desarrollo)
    if not mail_server:
      print(f"[DEV-OTP] to={to_email} otp={otp}")
      return True

    message = MessageSchema(
      subject="Recuperación de contraseña - OTP",
      recipients=[to_email],
      body=f"Tu código OTP para recuperar contraseña es: {otp}. Válido por {os.getenv('OTP_EXPIRE_MINUTES','30')} minutos.",
      subtype="plain"
    )

    try:
      fm = FastMail(self.mail_conf)
      await fm.send_message(message)
      print(f"[OTP-SENT] to={to_email}")
      return True
    except Exception as e:
      print(f"Error al enviar email OTP con FastMail: {e}")
      return False

  # Endpoint handler: solicitar OTP
  def forgot_password(self, request: ForgotPasswordRequest):
    try:
      user = self.user_repository.get_by_document(request.document)
      if not user:
        return ResultHandler.bad_request(message="Usuario no encontrado con ese documento")

      # Generar OTP
      otp = self._generate_otp()
      otp_hash = self._hash_password(otp)   # usar hash de passlib
      expire_minutes = int(os.getenv("OTP_EXPIRE_MINUTES", 30))
      expires_at = datetime.now(bogota_tz) + timedelta(minutes=expire_minutes)

      # Guardar registro de password reset
      pr = self.user_repository.create_password_reset(user.id, otp_hash, expires_at)

      # Enviar OTP por correo (si hay email)
      if not user.email:
        return ResultHandler.internal_error(message="Usuario no tiene correo registrado")
      sent = self._send_otp_email(user.email, otp)
      if not sent:
        # opcional: borrar el registro o dejarlo para reintentos
        return ResultHandler.internal_error(message="No se pudo enviar el correo con el OTP")
      # Respuesta: -> no incluir el OTP en producción (pero en dev puede mostrarlo)
      # Vamos a no devolver OTP salvo en mode=dev; si quieres ver OTP en logs.
      return ResultHandler.success(message="OTP enviado al correo registrado")
    except Exception as e:
      print("Error forgot_password:", e)
      return ResultHandler.internal_error(message="Error interno al solicitar recuperación")
    
  def generate_and_store_otp(self, document: str):
    user = self.user_repository.get_by_document(document)
    if not user:
      raise ValueError("Usuario no encontrado con ese documento")

    otp = self._generate_otp()
    otp_hash = self._hash_password(otp)
    expire_minutes = int(os.getenv("OTP_EXPIRE_MINUTES", 30))
    expires_at = datetime.now(bogota_tz) + timedelta(minutes=expire_minutes)

    pr = self.user_repository.create_password_reset(user.id, otp_hash, expires_at)
    # Retornamos email + otp para que la ruta pueda programar el envío (en dev es útil)
    return {"email": user.email, "otp": otp, "reset_id": pr.id}

  # Endpoint handler: verificar OTP y cambiar password
  def reset_password(self, request: ResetPasswordRequest):
    try:
      user = self.user_repository.get_by_document(request.document)
      if not user:
        return ResultHandler.bad_request(message="Usuario no encontrado")

      pr = self.user_repository.get_active_password_reset(user.id)
      if not pr:
        return ResultHandler.bad_request(message="No existe un código OTP activo. Solicite uno nuevo.")

      # Si está usado o expirado
      now = datetime.now(bogota_tz)
      pr_expires = pr.expires_at
      if pr_expires is None:
        return ResultHandler.bad_request(message="No hay fecha de expiración para el OTP.")
      
      if pr_expires.tzinfo is None:
        pr_expires = pr_expires.replace(tzinfo=bogota_tz)
      else:
        # convertir a la misma zona para comparar de forma consistente
         pr_expires = pr_expires.astimezone(bogota_tz)

      if pr.used or pr_expires < now:
        return ResultHandler.bad_request(message="El OTP ya expiró o fue utilizado. Solicite uno nuevo.")

      # Limitar intentos
      max_attempts = int(os.getenv("OTP_MAX_ATTEMPTS", 5))
      if pr.attempts and pr.attempts >= max_attempts:
        return ResultHandler.bad_request(message="Se excedió el número máximo de intentos para este OTP.")

      # Verificar OTP (comparar plain con hash guardado)
      if not self._verify_password(request.otp, pr.otp_hash):
        # incrementar intentos
        self.user_repository.increment_reset_attempts(pr.id)
        return ResultHandler.unauthorized(message="OTP inválido")
      
      # OK: actualizar password (hash)
      new_hashed = self._hash_password(request.new_password)
      self.user_repository.update_auth_password(user.id, new_hashed)

      # marcar reset como usado
      self.user_repository.mark_reset_used(pr.id)

      # notificar cambio por correo (opcional)
      try:
        # notificar al usuario que su contraseña fue cambiada
        if user.email:
          self._send_otp_email(user.email, f"Tu contraseña fue actualizada correctamente. Si no hiciste esto, contacta soporte.")
      except:
        pass

      return ResultHandler.success(message="Contraseña actualizada correctamente")
    except Exception as e:
      print("Error reset_password:", e)
      return ResultHandler.internal_error(message="Error interno al restablecer contraseña")