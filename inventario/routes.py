from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from inventario.schema import ProductoCreate, ProductoOut, ProductoUpdate, StockUpdate
from proveedores.model import Proveedor
from inventario.model import Producto

from fastapi.templating import Jinja2Templates
from datetime import datetime


router = APIRouter()
templates = Jinja2Templates(directory="inventario/templates")

# Vista principal del inventario
@router.get("/inventario", response_class=HTMLResponse, tags=["Productos"])
def vista_inventario(
    request: Request,
    search: str = "",
    page: int = 1,
    limit: int = 9,
    db: Session = Depends(get_db)
):
    rol = request.cookies.get("rol")  # Obtener rol desde cookies

    query = db.query(Producto).options(joinedload(Producto.proveedor))

    if search:
        query = query.filter(
            (Producto.nombre_producto.ilike(f"%{search}%")) |
            (Producto.id_producto.ilike(f"%{search}%"))
        )

    total = query.count()
    offset = (page - 1) * limit

    productos = (
        query.order_by(Producto.id_producto.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return templates.TemplateResponse("inventario.html", {
        "request": request,
        "productos": productos,
        "search": search,
        "rol": rol,
        "page": page,
        "total_pages": total_pages,
        "ruta_base": "/inventario"
    })



#Obetener los proveedores para agregarlos al Select
@router.get("/inventario/proveedores", response_class=JSONResponse, tags=["Productos"])
def filtrar_proveedores(search: str = "", db: Session = Depends(get_db)):
    proveedores = db.query(Proveedor).filter(
        (Proveedor.nombre_proveedor.ilike(f"%{search}%")) |
        (Proveedor.nit.ilike(f"%{search}%"))
    ).all()

    return [{"id": p.id_proveedor, "nombre": p.nombre_proveedor, "nit": p.nit} for p in proveedores]



# Agregar producto formulario
@router.post("/inventario/crear", tags=["Productos"])
def crear_producto(
    nombre_producto: str = Form(...),
    marca: str = Form(...),
    modelo: str = Form(...),
    descripcion: str = Form(...),
    stock: int = Form(...),
    precio: int = Form(...),
    precio_venta: int = Form(None),
    proveedor_id: int = Form(...),
    fecha_inicio_garantia: str = Form(None),
    fecha_expiracion_garantia: str = Form(None),
    fecha_compra: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Convertir las fechas a formato datetime
        inicio = datetime.strptime(fecha_inicio_garantia, "%Y-%m-%d").date() if fecha_inicio_garantia else None
        fin = datetime.strptime(fecha_expiracion_garantia, "%Y-%m-%d").date() if fecha_expiracion_garantia else None
        compra = datetime.strptime(fecha_compra, "%Y-%m-%d").date()

        # Validar con Pydantic
        producto_data = ProductoCreate(
            nombre_producto=nombre_producto,
            marca=marca,
            modelo=modelo,
            descripcion=descripcion,
            precio=precio,
            precio_venta=precio_venta,
            stock=stock,
            id_proveedor=proveedor_id,
            fecha_inicio_garantia=inicio,
            fecha_expiracion_garantia=fin,
            fecha_compra=compra
        )
        
        nuevo_producto = Producto(**producto_data.model_dump())
        db.add(nuevo_producto)
        db.commit()      

        return RedirectResponse(url="/inventario?create=1", status_code=303)  # Redirección con éxito

    except IntegrityError:
        db.rollback()
        return RedirectResponse(url="/inventario?error=1", status_code=303)  # Redirección con error algun duplicado

    except Exception as e:
        return RedirectResponse(url="/inventario?error=2", status_code=303)  # Redirección con error al crear


#Ruta que recibe el fetch de js para editar producto
@router.put("/producto/editar/{productoId}", tags=["Productos"])
def editar_producto(
    productoId: int,
    nombre_producto: str = Form(...),
    marca: str = Form(...),
    modelo: str = Form(...),
    descripcion: str = Form(...),
    precio: int = Form(...),
    precio_venta: int = Form(None),
    proveedor_id: int = Form(...),
    fecha_inicio_garantia: str = Form(None),
    fecha_expiracion_garantia: str = Form(None),
    fecha_compra: str = Form(...),
    db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(Producto.id_producto == productoId).first()
    if not producto:
        return HTMLResponse(content="Producto no encontrado", status_code=404)

    try:        
        # Convertir las fechas a formato datetime
        inicio = datetime.strptime(fecha_inicio_garantia, "%Y-%m-%d").date() if fecha_inicio_garantia else None
        fin = datetime.strptime(fecha_expiracion_garantia, "%Y-%m-%d").date() if fecha_expiracion_garantia else None
        compra = datetime.strptime(fecha_compra, "%Y-%m-%d").date()

        # Validar con Pydantic
        producto_data = ProductoUpdate(
            nombre_producto=nombre_producto,
            marca=marca,
            modelo=modelo,
            descripcion=descripcion,
            precio=precio,
            precio_venta=precio_venta,
            id_proveedor=proveedor_id,
            fecha_inicio_garantia=inicio,
            fecha_expiracion_garantia=fin,
            fecha_compra=compra
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