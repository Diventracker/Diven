from pydantic import BaseModel
from datetime import date

class ProductoCreate(BaseModel):
    nombre_producto: str
    marca: str
    modelo: str
    descripcion: str
    precio: float
    stock: int
    id_proveedor: int
    fecha_inicio_garantia: date | None = None
    fecha_expiracion_garantia: date | None = None
    fecha_compra: date
    precio_venta: float | None = None