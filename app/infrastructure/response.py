from fastapi.responses import JSONResponse

class ResultHandler:
  @staticmethod
  def success(data=None, message="Operación exitosa"):
    return JSONResponse(
      status_code=200,
      content={
        "success": True,
        "message": message,
        "data": data or {}
      }
    )

  @staticmethod
  def created(data=None, message="Recurso creado exitosamente"):
    return JSONResponse(
      status_code=201,
      content={
        "success": True,
        "message": message,
        "data": data or {}
      }
    )

  @staticmethod
  def error(message="Ha ocurrido un error", status_code=400):
    return JSONResponse(
      status_code=status_code,
      content={
        "success": False,
        "message": message,
        "data": None
      }
    )
