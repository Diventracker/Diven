from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from productos.model import Producto

class ProductoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id_producto: int) -> Producto | None:
        return self.db.query(Producto).filter_by(id_producto=id_producto).first()
    
    def buscar_por_nombre(self, termino: str) -> Producto | None:
        return self.db.query(Producto).filter(
            Producto.nombre_producto.ilike(f"%{termino}%")
        ).first()

    def obtener_por_nombre_modelo(self, nombre: str, modelo: str):
        return self.db.query(Producto).filter(
            Producto.nombre_producto == nombre,
            Producto.modelo == modelo
        ).first()
    
    #Filtra con stock y busqueda
    def buscar_productos(self, search: str = "", con_stock: bool = True) -> list[Producto]:
        query = self.db.query(Producto).join(Producto.proveedor)
        if search:
            query = query.filter(
                (Producto.nombre_producto.ilike(f"%{search}%")) |
                (Producto.id_producto.ilike(f"%{search}%"))
            )
        if con_stock:
            query = query.filter(Producto.stock > 0)

        return query.all()
    
    def productos_con_bajo_stock(self) -> list[Producto]:
        return self.db.query(Producto).filter(Producto.stock < 10).all()
    
    #Retorna todos los productos en /data
    def obtener_todos(self):
        return (self.db.query(Producto).options(joinedload(Producto.proveedor)).order_by(desc(Producto.fecha_compra)).all())
