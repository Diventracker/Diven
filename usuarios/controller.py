from fastapi.responses import JSONResponse
from usuarios.repositorio import UsuarioRepositorio
from usuarios.crud import UsuarioCRUD
from usuarios.schema import UsuarioCreateSchema
from utils.email import enviar_correo

class UsuarioControlador:
    def __init__(self, db):
        repo = UsuarioRepositorio(db)
        self.crud = UsuarioCRUD(repo)

    def listar_todos(self):
        usuarios = self.crud.listar_todos()
        return JSONResponse([
            {
                "id_usuario": u.id_usuario,
                "nombre_usuario": u.nombre_usuario,
                "correo": u.correo,
                "telefono_usuario": u.telefono_usuario,
                "rol": u.rol
            }
            for u in usuarios
        ])

    def crear(self, datos: UsuarioCreateSchema):
        try:
            usuario, clave_plana = self.crud.crear(datos)

            enviar_correo(
                destinatario=usuario.correo,
                asunto="Tu cuenta ha sido creada",
                template_name="email_pass.html",
                nombre=usuario.nombre_usuario,
                clave=clave_plana
            )

            return JSONResponse(content={"success": True, "mensaje": "Usuario creado y correo enviado"})

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": f"Error inesperado: {str(e)}"}, status_code=500)
        
        
    def editar(self, usuario_id: int, datos: UsuarioCreateSchema):
        try:
            usuario = self.crud.actualizar(usuario_id, datos)
            return JSONResponse(content={
                "success": True,
                "mensaje": "Usuario actualizado con éxito"
            })

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
    def eliminar(self, id_usuario: int):
        try:
            self.crud.eliminar(id_usuario)
            return JSONResponse(content={"success": True, "message": "Usuario eliminado correctamente"})

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": "Error interno"}, status_code=500)

