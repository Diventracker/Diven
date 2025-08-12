from datetime import datetime, timedelta, timezone
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

    #para validar la session del usuario
    def autenticar(self, correo: str, clave: str) -> Usuario:
        usuario = self.repo.obtener_por_correo(correo)
        if not usuario or not pwd_context.verify(clave, usuario.clave):
            raise ValueError("Credenciales inválidas")
        return usuario
    
    #Para el token de recuperacion de cuenta
    def asignar_token_recuperacion(self, correo: str, token: str):
        usuario = self.repo.obtener_por_correo(correo)
        if not usuario:
            return  # No hacer nada si no existe

        usuario.token_recuperacion = token
        usuario.token_expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)
        self.repo.db.commit()

        return usuario
    
    def validar_token_recuperacion(self, correo: str, token: str):
        usuario = self.repo.obtener_por_correo(correo)
        if not usuario:
            raise ValueError("Correo no registrado")

        if usuario.token_recuperacion != token:
            raise ValueError("Token inválido")

        if not usuario.token_expiracion or usuario.token_expiracion.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise ValueError("Token expirado")

        return usuario
    
    def cambiar_clave(self, usuario: Usuario, nueva_clave: str):
        usuario.clave = pwd_context.hash(nueva_clave)
        usuario.token_recuperacion = None
        usuario.token_expiracion = None
        self.repo.db.commit()

    def obtener_por_token_valido(self, correo: str, token: str) -> Usuario | None:
        usuario = self.repo.obtener_por_correo(correo)
        if (
            usuario and
            usuario.token_recuperacion == token and
            usuario.token_expiracion and
            usuario.token_expiracion.replace(tzinfo=timezone.utc) >= datetime.now(timezone.utc)
        ):
            return usuario
        return None

    def verificar_clave_actual(self, usuario: Usuario, clave_actual: str) -> bool:
        return pwd_context.verify(clave_actual, usuario.clave)
