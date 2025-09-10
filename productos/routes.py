from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database.database import get_db
from productos.controller import ProductoControlador
from productos.schema import ProductoCreate, ProductoUpdate, StockUpdate
from productos.model import Producto
from fastapi import UploadFile, File
from productos.schema import ProductoCreate, ProductoUpdate, StockUpdate



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
@router.post("/producto/crear")
async def crear_producto(
    datos: ProductoCreate = Depends(ProductoCreate.as_form),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return await controlador.crear(datos, imagen)

#Ruta que recibe el fetch de js para editar producto
@router.put("/producto/editar/{producto_id}", tags=["Productos"])
async def editar_producto(
    producto_id: int,
    datos: ProductoUpdate = Depends(ProductoUpdate.as_form),
    imagen: UploadFile = File(None),           
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return await controlador.editar(producto_id, datos, imagen)


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
#funcion para actualizar stock junto a la imagen
def actualizar_stock(id_producto: int, datos: StockUpdate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.stock += datos.cantidad
    db.commit()
    db.refresh(producto)

    return {"mensaje": "Stock actualizado correctamente", "stock_final": producto.stock}


def actualizar_stock_endpoint(
    id_producto: int,
    datos: StockUpdate,
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.actualizar_stock(id_producto, datos.cantidad)
