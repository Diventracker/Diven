from productos.repositorio import ProductoRepositorio
from productos.model import Producto
from productos.schema import ProductoCreate, ProductoUpdate  # Asegúrate que exista
from sqlalchemy.exc import IntegrityError
import os

class ProductoCRUD:
    def __init__(self, db):
        self.repo = ProductoRepositorio(db)

    def crear(self, datos: ProductoCreate, ruta_imagen: str = None) -> Producto:
        # Validar duplicado
        if self.repo.obtener_por_nombre_modelo(datos.nombre_producto, datos.modelo):
            raise ValueError("Ya existe un producto con ese nombre y modelo.")

        nuevo = Producto(**datos.model_dump(), imagen=ruta_imagen)
        self.repo.db.add(nuevo)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo)
        return nuevo
    
    def listar_productos(self):
        return self.repo.obtener_todos()
    
    def editar(self, producto_id: int, datos: ProductoUpdate, ruta_imagen: str | None = None) -> dict:
        producto = self.repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")

        # actualizar campos base
        producto.nombre_producto = datos.nombre_producto
        producto.modelo = datos.modelo
        producto.descripcion = datos.descripcion
        producto.precio = datos.precio
        producto.id_proveedor = datos.id_proveedor
        producto.precio_venta = datos.precio_venta
        producto.meses_garantia = datos.meses_garantia

        # si viene una nueva imagen, reemplazar
        if ruta_imagen:
            # eliminar archivo viejo si existe y no es la imagen por defecto
            if producto.imagen and producto.imagen.startswith("/static/img/productos/"):
                ruta_fisica = producto.imagen.lstrip("/")  # "static/img/productos/..."
                if os.path.exists(ruta_fisica):
                    try:
                        os.remove(ruta_fisica)
                    except Exception:
                        pass  # no romper si no se puede borrar

            producto.imagen = ruta_imagen

        self.repo.db.commit()
        self.repo.db.refresh(producto)
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
        
    #Funcion busca solo un producto
    def buscar(self, termino: str) -> Producto:
        if termino.isdigit():
            producto = self.repo.obtener_por_id(int(termino))
            if producto:
                return producto

        producto = self.repo.buscar_por_nombre(termino)
        if not producto:
            raise ValueError("Producto no encontrado")

        return producto
    
    def obtener_todos(self, search: str = "", con_stock: bool = True) -> list[Producto]:
        return self.repo.buscar_productos(search, con_stock)
    
    #Para las alertas de bajo stock
    def obtener_bajo_stock(self) -> list[Producto]:
        return self.repo.productos_con_bajo_stock()
    
    #Actualiza el stock del producto en control de stock
    def actualizar_stock(self, id_producto: int, cantidad: int) -> int:
        producto = self.repo.obtener_por_id(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")

        producto.stock += cantidad
        self.repo.db.commit()
        self.repo.db.refresh(producto)
        return producto.stock
    
    