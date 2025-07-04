from sqlalchemy.orm import Session
from productos.model import Producto

class ProductoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_nombre_modelo(self, nombre: str, modelo: str):
        return self.db.query(Producto).filter(
            Producto.nombre_producto == nombre,
            Producto.modelo == modelo
        ).first()
