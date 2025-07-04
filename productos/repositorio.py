from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from productos.model import Producto

class ProductoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id_producto: int) -> Producto | None:
        return self.db.query(Producto).filter_by(id_producto=id_producto).first()

    def obtener_por_nombre_modelo(self, nombre: str, modelo: str):
        return self.db.query(Producto).filter(
            Producto.nombre_producto == nombre,
            Producto.modelo == modelo
        ).first()
    
    #Retorna todos los productos en /data
    def obtener_todos(self):
        return (self.db.query(Producto).options(joinedload(Producto.proveedor)).order_by(desc(Producto.fecha_compra)).all())
