from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from productos.controller import ProductoControlador
from productos.schema import ProductoCreate, ProductoOut, ProductoUpdate, StockUpdate
from proveedores.model import Proveedor
from productos.model import Producto


router = APIRouter()


# Vista principal que muestra el html de productos
@router.get("/productos", response_class=HTMLResponse, tags=["Productos"])
def vista_producto(request: Request, db: Session = Depends(get_db)):
    controlador = ProductoControlador(db)
    return controlador.mostrar_vista(request)



#Obetener los proveedores para agregarlos al Select
@router.get("/producto/proveedores", response_class=JSONResponse, tags=["Productos"])
def filtrar_proveedores(search: str = "", db: Session = Depends(get_db)):
    proveedores = db.query(Proveedor).filter(
        (Proveedor.nombre_proveedor.ilike(f"%{search}%")) |
        (Proveedor.nit.ilike(f"%{search}%"))
    ).all()

    return [{"id": p.id_proveedor, "nombre": p.nombre_proveedor, "nit": p.nit} for p in proveedores]


# Ruta que recibe el formulario de agregar Porducto
@router.post("/producto/crear", tags=["Productos"])
def crear_producto(
    datos: ProductoCreate = Depends(ProductoCreate.as_form),
    db: Session = Depends(get_db)
):
    controlador = ProductoControlador(db)
    return controlador.crear(datos)



#Ruta que recibe el fetch de js para editar producto
@router.put("/producto/editar/{productoId}", tags=["Productos"])
def editar_producto(
    productoId: int,
    nombre_producto: str = Form(...),
    modelo: str = Form(...),
    descripcion: str = Form(...),
    precio: int = Form(...),
    precio_venta: int = Form(None),
    proveedor_id: int = Form(...),
    meses_garantia: int = Form(None),
    db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(Producto.id_producto == productoId).first()
    if not producto:
        return HTMLResponse(content="Producto no encontrado", status_code=404)

    try:        
        # Validar con Pydantic
        producto_data = ProductoUpdate(
            nombre_producto=nombre_producto,
            modelo=modelo,
            descripcion=descripcion,
            precio=precio,
            precio_venta=precio_venta,
            id_proveedor=proveedor_id,
            meses_garantia=meses_garantia
        )
        for field, value in producto_data.model_dump(exclude_none=True).items():
            setattr(producto, field, value)

        
        db.commit()
        return JSONResponse(content={"message": "success"})

    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"message": "error"})


#Eliminar Producto...
@router.delete("/producto/eliminar/{id_producto}", tags=["Productos"])
def eliminar_producto(
    id_producto: int,
    db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    if not producto:
        return HTMLResponse(content="Producto no encontrado", status_code=404)
    try: 
        db.delete(producto)
        db.commit()
        return JSONResponse(content={"message": "deleted"})
    
    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"message": "error"})



#Ruta para obtener un unico producto
@router.get("/productos/buscar/{termino}", response_model=ProductoOut, tags=["Productos"])
def buscar_producto(termino: str, db: Session = Depends(get_db)):
    # Intentar buscar por ID exacto si es un número
    if termino.isdigit():
        producto = db.query(Producto).filter(Producto.id_producto == int(termino)).first()
        if producto:
            return {
                "codigo": str(producto.id_producto),
                "nombre": producto.nombre_producto,
                "descripcion": producto.descripcion,
                "precio": int(producto.precio_venta),
                "stock": int(producto.stock)
            }

    # Si no es un ID válido o no lo encontró, buscar por nombre parcial
    producto = db.query(Producto).filter(
        Producto.nombre_producto.ilike(f"%{termino}%")
    ).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "codigo": str(producto.id_producto),
        "nombre": producto.nombre_producto,
        "descripcion": producto.descripcion,
        "precio": int(producto.precio_venta),
        "stock": int(producto.stock)
    }

#Ruta para obtener los productos en el modal de ventas como json en base al stock
@router.get("/api/productos", response_model=list[ProductoOut], tags=["Productos"])
def api_productos(search: str = "", con_stock: bool = True, db: Session = Depends(get_db)):
    query = db.query(Producto).join(Producto.proveedor)
    
    if search:
        query = query.filter(
            (Producto.nombre_producto.ilike(f"%{search}%")) |
            (Producto.id_producto.ilike(f"%{search}%"))
        )
    
    if con_stock:
        query = query.filter(Producto.stock > 0)

    productos = query.all()

    return [
        ProductoOut(
            codigo=str(prod.id_producto),
            nombre=prod.nombre_producto,
            descripcion=prod.descripcion,
            modelo=prod.modelo,
            precio=prod.precio_venta,
            stock=prod.stock,
            proveedor=prod.proveedor.nombre_proveedor  # <--- aquí agregas el proveedor
        )
        for prod in productos
    ]

#Funcion para obtener los productos con stock Bajo 
@router.get("/stock/bajo", response_model=list[ProductoOut], tags=["Productos"])
def productos_bajo_stock(db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.stock < 10).all()

    return [
        ProductoOut(
            codigo=str(prod.id_producto),
            nombre=prod.nombre_producto,
            descripcion=prod.descripcion,
            modelo=prod.modelo,
            precio=prod.precio_venta,
            stock=prod.stock,
            proveedor=prod.proveedor.nombre_proveedor if prod.proveedor else None
        )
        for prod in productos
    ]

#Esta ruta Put es la que actualiza el stock, en la pestaña control Stock
@router.put("/productos/{id_producto}/stock", tags=["Productos"])
def actualizar_stock(id_producto: int, datos: StockUpdate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.stock += datos.cantidad
    db.commit()
    db.refresh(producto)

    return {"mensaje": "Stock actualizado correctamente", "stock_final": producto.stock}