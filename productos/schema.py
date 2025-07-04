from typing import Optional
from fastapi import Form
from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre_producto: str
    modelo: str
    descripcion: str
    precio: int
    stock: int
    id_proveedor: int
    precio_venta: Optional[int] = None
    meses_garantia: Optional[int] = None

    @classmethod
    def as_form(cls, 
        nombre_producto: str = Form(...),
        modelo: str = Form(...),
        descripcion: str = Form(...),
        precio: int = Form(...),
        stock: int = Form(...),
        id_proveedor: int = Form(...),
        precio_venta: int = Form(None),
        meses_garantia: int = Form(None)
    ):
        return cls(
            nombre_producto=nombre_producto,
            modelo=modelo,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            id_proveedor=id_proveedor,
            precio_venta=precio_venta,
            meses_garantia=meses_garantia
        )

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
    