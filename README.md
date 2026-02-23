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

**Solo en esta PC (localhost):**
```bash
uvicorn app.main:app --reload
```

**Para que el celular o emulador en la red pueda conectarse** (usa la IP de esta PC en el .env del frontend, ej. 11.11.7.33):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
O en Windows: `.\run.ps1`

Asegúrate de que el firewall de Windows permita conexiones entrantes en el puerto 8000.

## 🐳 Docker
Próximamente se agregará soporte completo con Dockerfile y docker-compose.yml.

##📚 Documentación de API
Una vez corriendo el servicio, puedes acceder al Swagger en:
http://localhost:8000/docs


## 🧠 Organización
Este microservicio forma parte de una arquitectura distribuida basada en microservicios, desplegados como contenedores Docker y versionados de forma independiente.