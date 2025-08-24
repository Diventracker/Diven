from datetime import date
from sqlalchemy import func
from servicios.model import DetalleServicio, ImagenServicio, ServicioTecnico
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
    
    #Contar Servicios segun el tipo de equipo
    def contar_por_tipo_equipo(self):
        return (
            self.db.query(
                ServicioTecnico.tipo_equipo.label("equipo"),
                func.count().label("total")
            )
            .group_by(ServicioTecnico.tipo_equipo)
            .order_by(func.count().desc())
            .all()
        )
    
    #Filtrar servicios rango de fechas
    def filtrar_por_rango(self, inicio: date, fin: date) -> list[ServicioTecnico]:
        return self.db.query(ServicioTecnico)\
            .filter(ServicioTecnico.fecha_recepcion.between(inicio, fin))\
            .options(joinedload(ServicioTecnico.cliente))\
            .order_by(ServicioTecnico.fecha_recepcion.desc()).all()

    #Para listar todas las imagenes de un servicio
    def listar_imagenes_por_servicio(self, id_servicio: int):
        return (
            self.db.query(ImagenServicio)
            .filter(ImagenServicio.id_servicio == id_servicio)
            .all()
        )
    
    #Obtener la imagen por id
    def buscar_imagen_por_id(self, id_imagen: int):
        return self.db.query(ImagenServicio).filter(ImagenServicio.id_imagen == id_imagen).first()