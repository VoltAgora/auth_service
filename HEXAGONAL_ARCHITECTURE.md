# 🏗️ Arquitectura Hexagonal - Guía Completa

## 📋 Índice
- [¿Qué es la Arquitectura Hexagonal?](#qué-es-la-arquitectura-hexagonal)
- [Principios Fundamentales](#principios-fundamentales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Flujo de Datos](#flujo-de-datos)
- [Capas y Responsabilidades](#capas-y-responsabilidades)
- [Ventajas y Beneficios](#ventajas-y-beneficios)
- [Patrones Implementados](#patrones-implementados)

## ¿Qué es la Arquitectura Hexagonal?

La **Arquitectura Hexagonal** (también conocida como **Puertos y Adaptadores**) es un patrón arquitectónico que busca **aislar la lógica de negocio** del mundo exterior.

### 🎯 Objetivo Principal
Crear un sistema donde la lógica de negocio sea **independiente** de:
- Framework web (FastAPI, Flask, Django)
- Base de datos (MySQL, PostgreSQL, MongoDB)
- APIs externas
- Interfaces de usuario
- Protocolos de comunicación

## Principios Fundamentales

### 1. 🏛️ **Inversión de Dependencias**
```
❌ Tradicional: Domain → Infrastructure
✅ Hexagonal:  Domain ← Infrastructure
```

El dominio define **QUÉ necesita** (interfaces), la infraestructura implementa **CÓMO lo hace**.

### 2. 🔌 **Puertos (Ports)**
Son **interfaces/contratos** que definen:
- Qué operaciones necesita el dominio
- Qué servicios ofrece el dominio

### 3. 🔧 **Adaptadores (Adapters)**
Son **implementaciones concretas** que:
- Conectan el dominio con el mundo exterior
- Traducen entre formatos internos y externos

## Estructura del Proyecto

```
app/
├── domain/                    # 🏛️ NÚCLEO - Lógica de negocio
│   ├── models/               # Entidades de dominio
│   ├── services/             # Casos de uso
│   └── ports/               # Interfaces/Contratos
│
├── adapters/                 # 🔧 ADAPTADORES
│   ├── http/                # Adaptadores de entrada (API REST)
│   └── persistence/         # Adaptadores de salida (Base de datos)
│
└── infrastructure/          # 🛠️ INFRAESTRUCTURA
    ├── db.py               # Configuración de base de datos
    └── response.py         # Utilidades de respuesta
```

## Flujo de Datos

### 📥 **Flujo de Entrada** (Inbound)
```
🌐 HTTP Request
    ↓
🚪 HTTP Adapter (routes.py)
    ↓
🏢 Domain Service (business logic)
    ↓
🔌 Repository Port (interface)
    ↓
🗄️ Repository Adapter (SQL implementation)
    ↓
📊 Database
```

### 📤 **Flujo de Salida** (Outbound)
```
📊 Database
    ↓
🗄️ Repository Adapter (convierte Entity → Domain Model)
    ↓
🔌 Repository Port
    ↓
🏢 Domain Service (aplica lógica de negocio)
    ↓
🚪 HTTP Adapter (convierte Domain → JSON)
    ↓
🌐 HTTP Response
```

## Capas y Responsabilidades

### 🏛️ **DOMAIN (Centro del Hexágono)**

#### 📦 **Models** (`domain/models/`)
```python
# Ejemplo: User.py
class User(BaseModel):
    id: int
    email: str
    # Solo datos y validaciones de dominio
    # NO conoce HTTP, DB, o tecnologías específicas
```

#### 🎯 **Services** (`domain/services/`)
```python
# Ejemplo: AuthService.py
class AuthService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository
    
    def register(self, user: User) -> User:
        # Lógica de negocio pura
        # Validaciones de dominio
        # Reglas de negocio
```

#### 🔌 **Ports** (`domain/ports/`)
```python
# Ejemplo: db_port.py
class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    # Define QUÉ necesita, no CÓMO se implementa
```

### 🔧 **ADAPTERS**

#### 📥 **HTTP Adapters** (`adapters/http/`)
```python
# routes.py - Adaptador de ENTRADA
@router.post("/register")
def register(user: User = Body(...)):
    # 1. Recibe HTTP request
    # 2. Convierte a modelo de dominio
    # 3. Llama al servicio de dominio
    # 4. Convierte respuesta a HTTP
    result = auth_service.register(user)
    return ResultHandler.created(data=result)
```

#### 📤 **Persistence Adapters** (`adapters/persistence/`)
```python
# user_repository.py - Adaptador de SALIDA
class UserRepositorySQL(UserRepositoryPort):
    def save(self, user: User) -> User:
        # 1. Convierte Domain Model → Entity (ORM)
        # 2. Ejecuta operación en DB
        # 3. Convierte Entity → Domain Model
        # 4. Retorna al dominio
```

### 🛠️ **INFRASTRUCTURE**

#### ⚙️ **Configuración y Utilidades**
- `db.py`: Configuración de base de datos
- `response.py`: Formateo de respuestas HTTP
- Logging, autenticación, etc.

## Ventajas y Beneficios

### ✅ **1. Testabilidad**
```python
# Test unitario fácil - Mock del puerto
mock_repo = Mock(spec=UserRepositoryPort)
auth_service = AuthService(mock_repo)
# Test aislado de DB, HTTP, etc.
```

### ✅ **2. Flexibilidad Tecnológica**
```python
# Cambiar de MySQL a PostgreSQL:
# Solo crear nuevo adaptador, dominio intacto
user_repo = PostgreSQLRepository()  # Nuevo adaptador
auth_service = AuthService(user_repo)  # Mismo servicio
```

### ✅ **3. Separación de Responsabilidades**
- **Dominio**: Solo lógica de negocio
- **Adaptadores**: Solo conversión de formatos
- **Infraestructura**: Solo configuración técnica

### ✅ **4. Escalabilidad**
- Agregar nuevos adaptadores (GraphQL, gRPC)
- Múltiples bases de datos simultáneas
- Microservicios independientes

### ✅ **5. Mantenibilidad**
- Cambios en tecnología no afectan lógica de negocio
- Código más limpio y organizado
- Facilita refactoring

## Patrones Implementados

### 🏭 **Dependency Injection**
```python
# En routes.py
user_repo = UserRepositorySQL()      # Dependencia concreta
auth_service = AuthService(user_repo)  # Inyección
```

### 🔄 **Repository Pattern**
```python
# Puerto define el contrato
class UserRepositoryPort(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

# Adaptador implementa el contrato
class UserRepositorySQL(UserRepositoryPort):
    def get_by_email(self, email: str) -> User:
        # Implementación específica para SQL
```

### 🎭 **Adapter Pattern**
```python
# HTTP Adapter traduce entre HTTP y Dominio
def register_user(user_data: dict):
    domain_user = User(**user_data)      # HTTP → Domain
    result = auth_service.register(domain_user)
    return {"user": result.dict()}       # Domain → HTTP
```

### 🏗️ **Factory Pattern** (implícito)
```python
# Crear servicios con sus dependencias
def create_auth_service():
    repo = UserRepositorySQL()
    return AuthService(repo)
```

## 🚀 **Resultado Final**

Con esta arquitectura obtienes:

1. **Lógica de negocio protegida** y aislada
2. **Tests rápidos** y confiables
3. **Flexibilidad tecnológica** total
4. **Código mantenible** y escalable
5. **Separación clara** de responsabilidades

### 🎯 **Regla de Oro**
> **El dominio no debe conocer nada del mundo exterior.**  
> **El mundo exterior debe adaptarse al dominio.**

---

*Esta arquitectura hexagonal garantiza que tu aplicación sea **robusta**, **testeable** y **evolutiva**, permitiendo cambios tecnológicos sin afectar la lógica de negocio central.*