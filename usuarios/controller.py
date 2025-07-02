from fastapi.responses import JSONResponse
from usuarios.repositorio import UsuarioRepositorio
from usuarios.crud import UsuarioCRUD

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
