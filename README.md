# Auth Service - Microservicio de Autenticación

Este repositorio contiene el microservicio `auth_service` desarrollado en **Python con FastAPI** y estructurado según la **arquitectura hexagonal**, como parte de un ecosistema de microservicios para la plataforma P2P de energía.

## 🧱 Arquitectura

El proyecto sigue el enfoque de **puertos y adaptadores (Hexagonal)**, dividiendo claramente las siguientes capas:

- `domain/`: lógica de negocio y modelos puros
- `services/`: managers que orquestan los casos de uso
- `ports/`: interfaces que definen contratos para persistencia
- `adapters/`: implementación concreta de puertos (ej. SQLAlchemy)
- `infrastructure/`: conexión con el exterior (DB, HTTP, etc.)
- `main.py`: punto de entrada y configuración de FastAPI

## 🚀 Tecnologías

- Python 3.12
- FastAPI
- SQLAlchemy
- Uvicorn
- dotenv
- Docker

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/volt-uao/auth_service.git
cd auth_service

# Crear entorno virtual
python -m venv venv
source venv/Scripts/activate  # En Windows

# Instalar dependencias
pip install -r requirements.txt

## 🧪 Ejecutar el servicio
uvicorn app.main:app --reload

## 🐳 Docker
Próximamente se agregará soporte completo con Dockerfile y docker-compose.yml.

##📚 Documentación de API
Una vez corriendo el servicio, puedes acceder al Swagger en:
http://localhost:8000/docs


## 🧠 Organización
Este microservicio forma parte de una arquitectura distribuida basada en microservicios, desplegados como contenedores Docker y versionados de forma independiente.