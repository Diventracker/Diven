from servicios.model import ServicioTecnico
from sqlalchemy.orm import joinedload


class ServicioRepositorio:
    def __init__(self, db):
        self.db = db

    def listar_todos(self):
        return self.db.query(ServicioTecnico).options(
            joinedload(ServicioTecnico.usuario)
        ).order_by(ServicioTecnico.id_servicio.desc()).all()