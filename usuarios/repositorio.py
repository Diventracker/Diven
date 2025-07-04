from sqlalchemy import desc
from usuarios.model import Usuario


class UsuarioRepositorio:
    def __init__(self, db):
        self.db = db

    def listar_todos(self) -> list[Usuario]:
        return self.db.query(Usuario).order_by(desc(Usuario.id_usuario)).all()
    
    def obtener_por_id(self, id_usuario: int) -> Usuario | None:
        return self.db.query(Usuario).filter_by(id_usuario=id_usuario).first()
    
    def obtener_por_correo(self, correo: str) -> Usuario | None:
        return self.db.query(Usuario).filter_by(correo=correo).first()
