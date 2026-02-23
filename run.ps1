# Inicia el Auth Service escuchando en todas las interfaces (0.0.0.0)
# Asi el celular/emulador en la red puede conectarse a la IP de esta PC (ej: 11.11.7.33:8000)
# Uso: .\run.ps1   o   pwsh .\run.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
