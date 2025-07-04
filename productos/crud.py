from productos.repositorio import ProductoRepositorio
from productos.model import Producto
from productos.schema import ProductoCreate, ProductoUpdate  # Asegúrate que exista
from sqlalchemy.exc import IntegrityError

class ProductoCRUD:
    def __init__(self, db):
        self.repo = ProductoRepositorio(db)

    def crear(self, datos: ProductoCreate) -> Producto:
        # Validar duplicado por nombre + modelo
        if self.repo.obtener_por_nombre_modelo(datos.nombre_producto, datos.modelo):
            raise ValueError("Ya existe un producto con ese nombre y modelo.")

        nuevo = Producto(**datos.model_dump())
        self.repo.db.add(nuevo)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo)
        return nuevo
    
    def listar_productos(self):
        return self.repo.obtener_todos()
    
    def editar(self, producto_id: int, datos: ProductoUpdate) -> dict:
        producto = self.repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")

        for campo, valor in datos.model_dump(exclude_none=True).items():
            setattr(producto, campo, valor)

        self.repo.db.commit()
        return {"success": True}
    
    def eliminar(self, id_producto: int):
        producto = self.repo.obtener_por_id(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")

        try:
            self.repo.db.delete(producto)
            self.repo.db.commit()
        except IntegrityError:
            self.repo.db.rollback()
            raise ValueError("No se puede eliminar el producto por restricciones de integridad")