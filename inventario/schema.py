from typing import Optional
from pydantic import BaseModel
from datetime import date

class ProductoCreate(BaseModel):
    nombre_producto: str
    marca: str
    modelo: str
    descripcion: str
    precio: int
    stock: int
    id_proveedor: int
    fecha_inicio_garantia: date | None = None
    fecha_expiracion_garantia: date | None = None
    fecha_compra: date
    precio_venta: int | None = None

#Para las consultas de las facturas
class ProductoOut(BaseModel):
    codigo: str         # equivale a Producto.id_producto
    descripcion: str    # equivale a Producto.nombre_producto
    modelo: Optional[str] = None         # Producto.modelo
    precio: int
    stock: int
    