from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.adapters.http.routes import router as auth_router

app = FastAPI(title="Auth Service")
# Hola mundo

# Registrar las rutas del microservicio
app.include_router(auth_router, prefix="/auth")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Microservicio de autenticación con JWT",
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