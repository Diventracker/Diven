from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from inventario.schema import ProductoCreate, ProductoOut
from proveedores.model import Proveedor
from inventario.model import Producto

from fastapi.templating import Jinja2Templates
from datetime import datetime


router = APIRouter()
templates = Jinja2Templates(directory="inventario/templates")

# Vista principal del inventario
@router.get("/inventario", response_class=HTMLResponse, tags=["Productos"])
def vista_inventario(request: Request, search: str = "", db: Session = Depends(get_db)):
   if search:
        productos = db.query(Producto).filter(
            (Producto.nombre_producto.ilike(f"%{search}%")) |
            (Producto.id_producto.ilike(f"%{search}%"))
        ).all()
   else:
        
        productos = db.query(Producto).options(joinedload(Producto.proveedor)).order_by(Producto.id_producto.desc()).all()

   return templates.TemplateResponse("inventario.html", {"request": request, "productos": productos, "search": search})


#Obetener los proveedores para agregarlos al Select
@router.get("/inventario/proveedores", response_class=JSONResponse, tags=["Productos"])
def filtrar_proveedores(q: str = "", db: Session = Depends(get_db)):
    proveedores = db.query(Proveedor).filter(
        (Proveedor.nombre_proveedor.ilike(f"%{q}%")) |
        (Proveedor.nit.ilike(f"%{q}%"))
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
    precio: float = Form(...),
    precio_venta: float = Form(None),
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
    stock: int = Form(...),
    precio: float = Form(...),
    precio_venta: float = Form(None),
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
@router.get("/productos/buscar/{termino}", response_model=ProductoOut)
def buscar_producto(termino: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(
        (Producto.id_producto.ilike(f"%{termino}%")) |
        (Producto.nombre_producto.ilike(f"%{termino}%"))
    ).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "codigo": str(producto.id_producto),
        "descripcion": producto.nombre_producto,
        "precio": float(producto.precio_venta),
        "stock": float(producto.stock)
    }

#Ruta para obtener los productos en el modal de ventas como json en base al stock
@router.get("/api/productos", response_model=list[ProductoOut])
def api_productos(search: str = "", con_stock: bool = True, db: Session = Depends(get_db)):
    query = db.query(Producto)
    
    if search:
        query = query.filter(
            (Producto.nombre_producto.ilike(f"%{search}%")) |
            (Producto.id_producto.ilike(f"%{search}%"))
        )
    
    if con_stock:
        query = query.filter(Producto.stock > 0)

    productos = query.all()

    # Mapear al schema ProductoOut
    return [
        ProductoOut(
            codigo=str(prod.id_producto),  # Lo pasa a string si no lo manda como int
            descripcion=prod.nombre_producto,
            modelo=prod.modelo,
            precio=prod.precio,
            stock=prod.stock
        )
        for prod in productos
    ]