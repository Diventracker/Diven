from fastapi import Request, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException

def verificar_usuario(roles_permitidos: list[str] = None):
    def inner(request: Request):
        usuario_id = request.cookies.get("usuario_id")
        tipo_usuario = request.cookies.get("rol")

        if not usuario_id:
            # Redirigir si no está autenticado            
            raise StarletteHTTPException(status_code=303, detail="Redirección", headers={"Location": "/login?error=2"})

        if roles_permitidos and tipo_usuario not in roles_permitidos:
            # Redirigir si el rol no es válido            
            raise StarletteHTTPException(status_code=303, detail="Redirección", headers={"Location": "/login?error=3"})

        return {"usuario_id": usuario_id, "rol": tipo_usuario} #Retorna como DICT y se accede usuario["usuario_id"]

    return Depends(inner) #Ejecuta esta funcion antes de la ruta 
