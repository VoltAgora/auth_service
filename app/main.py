from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.auth.adapters.http.routes import router as auth_router
from app.user.adapters.http.routes import router as user_router
from app.transactions.adapters.http.routes import router as transactions_router
from app.energy.adapters.http.routes import router as energy_router

app = FastAPI(title="Volt Platform Services")

# Registrar las rutas de los microservicios
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(transactions_router)
app.include_router(energy_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Plataforma Volt - Servicios de Autenticación, Usuarios, Transacciones P2P y Energía",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Sobrescribir la documentación por defecto
app.openapi = custom_openapi