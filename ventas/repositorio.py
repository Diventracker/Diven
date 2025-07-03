from sqlalchemy.orm import Session, joinedload
from ventas.model import Venta, DetalleVenta
from productos.model import Producto

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

    def obtener_producto_por_id(self, id_producto: int):
        return self.db.query(Producto).filter(Producto.id_producto == id_producto).first()
