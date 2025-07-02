from sqlalchemy import desc
from usuarios.model import Usuario


class UsuarioRepositorio:
    def __init__(self, db):
        self.db = db

    def listar_todos(self) -> list[Usuario]:
        return self.db.query(Usuario).order_by(desc(Usuario.id_usuario)).all()
