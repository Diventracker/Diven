from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from productos.controller import ProductoControlador
from productos.schema import ProductoCreate, ProductoOut, ProductoUpdate, StockUpdate
from productos.model import Producto


router = APIRouter()


# Vista principal que muestra el html de productos
@router.get("/productos", response_class=HTMLResponse, tags=["Productos"])
def vista_producto(request: Request, db: Session = Depends(get_db)):
    controlador = ProductoControlador(db)
    return controlador.mostrar_vista(request)


#Ruta que retorna todos los productos en json
@router.get("/productos/data", tags=["Productos"])
def obtener_productos(db: Session = Depends(get_db)):
    return ProductoControlador(db).obtener_productos()


# Ruta que recibe el formulario de agregar Porducto
@router.post("/producto/crear", tags=["Productos"])
def crear_producto(
    datos: ProductoCreate = Depends(ProductoCreate.as_form),
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.crear(datos)


#Ruta que recibe el fetch de js para editar producto
@router.put("/producto/editar/{producto_id}", tags=["Productos"])
def editar_producto(
    producto_id: int,
    datos: ProductoUpdate = Depends(ProductoUpdate.as_form),
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.editar_producto(producto_id, datos)


#Eliminar Producto...
@router.delete("/producto/eliminar/{id_producto}", tags=["Productos"])
def eliminar_producto_endpoint(
    id_producto: int,
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.eliminar(id_producto)



#Ruta para obtener un unico producto
@router.get("/productos/buscar/{termino}", tags=["Productos"])
def buscar_producto_endpoint(termino: str, db: Session = Depends(get_db)):
    controlador = ProductoControlador(db)
    return controlador.buscar(termino)


#Ruta para obtener los productos en el modal de ventas como json en base al stock
@router.get("/api/productos", tags=["Productos"])
def api_productos_endpoint(
    search: str = "",
    con_stock: bool = True,
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.listar_api(search, con_stock)

#Funcion para obtener los productos con stock Bajo 
@router.get("/stock/bajo", tags=["Productos"])
def productos_bajo_stock_endpoint(db: Session = Depends(get_db)):
    controlador = ProductoControlador(db)
    return controlador.bajo_stock()


#Esta ruta Put es la que actualiza el stock, en la pestaña control Stock
@router.put("/productos/{id_producto}/stock", tags=["Productos"])
def actualizar_stock_endpoint(
    id_producto: int,
    datos: StockUpdate,
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.actualizar_stock(id_producto, datos.cantidad)