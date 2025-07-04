from productos.repositorio import ProductoRepositorio
from productos.model import Producto
from productos.schema import ProductoCreate  # Asegúrate que exista
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
