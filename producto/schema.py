from typing import Optional
from pydantic import BaseModel
from datetime import date

class ProductoCreate(BaseModel):
    nombre_producto: str
    modelo: str
    descripcion: str
    precio: int
    precio_venta: int
    stock: int
    id_proveedor: int
    meses_garantia: int | None = None  # Si se puede omitir

class ProductoUpdate(BaseModel):
    nombre_producto: str
    modelo: str
    descripcion: str
    precio: int
    precio_venta: int
    id_proveedor: int
    meses_garantia: int | None = None

#Para las consultas de las facturas
class ProductoOut(BaseModel):
    codigo: str         # equivale a Producto.id_producto
    nombre: str
    descripcion: str    # equivale a Producto.nombre_producto
    modelo: Optional[str] = None         # Producto.modelo
    precio: int
    stock: int
    proveedor: Optional[str] = None

class StockUpdate(BaseModel):
    cantidad: int  # cantidad a sumar
    