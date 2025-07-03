from servicios.model import DetalleServicio, ServicioTecnico
from sqlalchemy.orm import joinedload


class ServicioRepositorio:
    def __init__(self, db):
        self.db = db

    def obtener_por_id(self, id_servicio: int):
        return self.db.query(ServicioTecnico).filter(ServicioTecnico.id_servicio == id_servicio).first()
    
    def eliminar_detalles(self, id_servicio: int):
        self.db.query(DetalleServicio).filter_by(id_servicio=id_servicio).delete()

    def listar_todos(self):
        return self.db.query(ServicioTecnico).options(
            joinedload(ServicioTecnico.usuario)
        ).order_by(ServicioTecnico.id_servicio.desc()).all()
    
    def obtener_en_revision(self):
        return (
            self.db.query(ServicioTecnico)
            .filter(ServicioTecnico.estado_servicio == "En Revisión")
            .all()
        )
    
    def obtener_detalles(self, id_servicio: int):
        return (
            self.db.query(DetalleServicio)
            .filter(DetalleServicio.id_servicio == id_servicio)
            .order_by(DetalleServicio.id_detalle.desc())
            .all()
        )