import os # Para manejar variables de entorno
import logging # Para logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv # Para cargar variables de entorno desde un archivo .env
from urllib.parse import quote_plus # Para codificar la contraseña en URL

# Configuración de logging
logging.basicConfig(level=logging.INFO) # Nivel de logging
logger = logging.getLogger(__name__) # Logger para este módulo

load_dotenv()

# Variables de conexión
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Base para modelos ORM
# ORM es Object-Relational Mapping
# Permite mapear tablas de la base de datos a clases de Python
Base = declarative_base()

# Validación de configuración
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
  # Si falta alguna variable, loguear error y no crear engine
  logger.warning("Faltan variables de conexión en el archivo .env")
  engine = None
else:

  # Construcción segura de la URL (usa pymysql como driver)
  # Codificar la contraseña para manejar caracteres especiales como @
  DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
  try:
    # Crear el engine de SQLAlchemy con pool_pre_ping para evitar conexiones muertas
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    # Probar la conexión
    with engine.connect() as conn:
      logger.info("Conexión OK a la base de datos")
  except Exception as e:
    logger.error(f"No se pudo conectar a la base de datos → {e}")
    engine = None

# SessionLocal solo si hay engine válido es decir si pudo conectar a la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

# Dependencia para obtener la sesión
def get_db():
  """
  Generador que proporciona una sesión de base de datos.
  Cierra la sesión automáticamente al finalizar.
  """
  if SessionLocal is None:
    raise RuntimeError("La base de datos no está configurada correctamente.")
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
