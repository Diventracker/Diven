from datetime import date
from sqlalchemy import desc, extract, func
from sqlalchemy.orm import Session, joinedload
from productos.model import Producto
from usuarios.model import Usuario
from ventas.model import Venta, DetalleVenta

class VentaRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_venta_con_relaciones(self, id_venta: int):
        return self.db.query(Venta)\
            .options(joinedload(Venta.cliente), joinedload(Venta.usuario))\
            .filter(Venta.id_venta == id_venta)\
            .first()

    def obtener_detalles_por_venta(self, id_venta: int):
        return self.db.query(DetalleVenta).filter(DetalleVenta.id_venta == id_venta).all()
    
    def obtener_por_id(self, id_venta: int) -> Venta | None:
        return self.db.query(Venta).filter(Venta.id_venta == id_venta).first()

    def listar_todas(self) -> list[Venta]:
        return (
            self.db.query(Venta)
            .options(
                joinedload(Venta.cliente),
                joinedload(Venta.detalles)
            )
            .order_by(desc(Venta.id_venta))
            .all()
        )
    
    #Total de ventas por mes
    def obtener_totales_por_mes(self):
        return self.db.query(
            extract('month', Venta.fecha_venta).label("mes"),
            func.sum(Venta.total_venta).label("total")
        ).group_by("mes").order_by("mes").all()

    #Porductos mas vendidos
    def obtener_productos_mas_vendidos(self, limite: int = 8):
        return (
            self.db.query(
                Producto.nombre_producto,
                func.sum(DetalleVenta.cantidad).label("total_vendido")
            )
            .join(Producto, DetalleVenta.id_producto == Producto.id_producto)
            .group_by(Producto.nombre_producto)
            .order_by(desc("total_vendido"))
            .limit(limite)
            .all()
        )
    
    #Ventas Por Vendedor o Tecnico en este caso
    def obtener_ventas_por_vendedor(self, limite: int = 6):
        return (
            self.db.query(
                Usuario.nombre_usuario.label("vendedor"),
                func.coalesce(func.sum(Venta.total_venta), 0).label("total")
            )
            .outerjoin(Venta, Usuario.id_usuario == Venta.id_usuario)
            .group_by(Usuario.nombre_usuario)
            .order_by(desc("total"))
            .limit(limite)
            .all()
        )
    
    #Filtrar las ventas segun un rango de fechas
    def filtrar_por_rango(self, inicio: date, fin: date) -> list[Venta]:
        return self.db.query(Venta)\
            .filter(Venta.fecha_venta.between(inicio, fin))\
            .options(joinedload(Venta.cliente))\
            .order_by(Venta.fecha_venta.desc()).all()