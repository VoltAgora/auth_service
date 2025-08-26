from fastapi import FastAPI
from app.adapters.http.routes import router as auth_router

app = FastAPI(title="Auth Service")
# Hola mundo

# Registrar las rutas del microservicio
app.include_router(auth_router, prefix="/auth")
