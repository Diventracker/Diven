import secrets
from usuarios.model import Usuario
from usuarios.schema import UsuarioCreateSchema
from utils.hash import pwd_context #contexto del hash


class UsuarioCRUD:
    def __init__(self, repo):
        self.repo = repo

    def listar_todos(self) -> list[Usuario]:
        return self.repo.listar_todos()

    def crear(self, datos):
        if self.repo.obtener_por_correo(datos.correo):
            raise ValueError("Ya existe un usuario con ese correo")

        clave_plana = secrets.token_urlsafe(10)
        clave_hash = pwd_context.hash(clave_plana)

        nuevo_usuario = Usuario(**datos.model_dump(), clave=clave_hash)
        self.repo.db.add(nuevo_usuario)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo_usuario)

        return nuevo_usuario, clave_plana
    
    def actualizar(self, usuario_id: int, datos: UsuarioCreateSchema) -> Usuario:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # Validar que el nuevo correo no sea de otro usuario
        existente = self.repo.obtener_por_correo(datos.correo)
        if existente and existente.id_usuario != usuario_id:
            raise ValueError("Ya existe otro usuario con ese correo")

        for campo, valor in datos.model_dump(exclude_none=True).items():
            setattr(usuario, campo, valor)

        self.repo.db.commit()
        self.repo.db.refresh(usuario)
        return usuario
    
    def eliminar(self, id_usuario: int):
        usuario = self.repo.obtener_por_id(id_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        self.repo.db.delete(usuario)
        self.repo.db.commit()
