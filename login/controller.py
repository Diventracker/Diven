from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from usuarios.crud import UsuarioCRUD
from usuarios.repositorio import UsuarioRepositorio
from access.sesiones import session_manager
from usuarios.schema import CambiarClaveSchema
from utils.email import enviar_correo
from utils.token import generar_token


class LoginControlador:
    def __init__(self, db: Session):
        repo = UsuarioRepositorio(db)
        self.crud = UsuarioCRUD(repo)
        self.sessions = session_manager

    def login(self, correo: str, clave: str) -> JSONResponse:
        try:
            usuario = self.crud.autenticar(correo, clave)

            if usuario.rol not in ["Administrador", "Técnico"]:
                return JSONResponse(status_code=403, content={"success": False, "error": "Rol no autorizado"})

            session_id = session_manager.crear_sesion({
                "usuario_id": usuario.id_usuario,
                "rol": usuario.rol,
                "nombre": usuario.nombre_usuario
            })

            response = JSONResponse(status_code=200, content={"success": True, "redirect": "/diventracker"})
            response.set_cookie(key="session_id", value=session_id, httponly=True, path="/")
            return response

        except ValueError:
            return JSONResponse(status_code=401, content={"success": False, "error": "Correo o contraseña incorrectos"})

        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Error interno al procesar el login"})
        

    def solicitar_recuperacion(self, correo: str) -> JSONResponse:
        try:
            token = generar_token()
            usuario = self.crud.asignar_token_recuperacion(correo, token)

            # Aunque no se sepa si el correo existe, se intenta enviar
            enviar_correo(
                correo,
                "Código de recuperación",
                "token_recuperacion.html",
                nombre=usuario.nombre_usuario,  # si no existe el usuario, nombre se pone igual
                token=token
            )

        except Exception:
            pass

        return JSONResponse(content={"msg": "Código enviado al correo"})
    
    def validar_token(self, correo: str, token: str) -> JSONResponse:
        try:
            usuario = self.crud.validar_token_recuperacion(correo, token)

            return JSONResponse(content={
                "msg": "Token válido",
                "recuperacion": True,
                "correo": usuario.correo,
                "token": usuario.token_recuperacion
            })
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Error interno al validar token")
        
       #Para cambiar la contraseña en el login 
    def cambiar_clave(self, request: Request, data: CambiarClaveSchema) -> JSONResponse:
        CambiarClaveSchema.validar_campos(data)

        usuario = None

        # Caso 1: Viene desde recuperación (token + correo)
        if data.token:
            usuario = self.crud.obtener_por_token_valido(data.correo, data.token)
            if not usuario:
                raise HTTPException(status_code=400, detail="Token inválido o expirado")

        # Caso 2: Usuario logueado (requiere sesión válida)
        elif hasattr(request.state, "usuario"):
            usuario_id = request.state.usuario.get("usuario_id")

            if not usuario_id:
                raise HTTPException(status_code=401, detail="Sesión no válida")

            usuario = self.crud.repo.obtener_por_id(int(usuario_id))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Validar la clave actual antes de cambiarla
            if not self.crud.verificar_clave_actual(usuario, data.clave_actual):
                raise HTTPException(status_code=400, detail="Clave actual incorrecta")

        else:
            # No hay ni token ni sesión válida
            raise HTTPException(status_code=403, detail="Acceso no autorizado")

        # Cambiar la contraseña
        self.crud.cambiar_clave(usuario, data.nueva_clave)

        return JSONResponse(content={"msg": "Contraseña actualizada correctamente"})