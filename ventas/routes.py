from datetime import date, datetime, timezone
from fastapi import APIRouter, HTTPException, Request, Depends 
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from clientes.model import Cliente
from database.database import get_db
from inventario.model import Producto
from usuarios.model import Usuario
from ventas.model import DetalleVenta, Venta
from sqlalchemy import desc, or_

router = APIRouter()
templates = Jinja2Templates(directory="ventas/templates")

#Ruta para mostrar todas las ventas
@router.get("/ventas", response_class=HTMLResponse, tags=["Ventas"])
def gestionventas_get(
    request: Request,
    search: str = "",
    page: int = 1,
    limit: int = 9,
    db: Session = Depends(get_db)
):
    query = db.query(Venta).join(Venta.cliente).options(joinedload(Venta.cliente))

    if search:
        query = query.filter(
            or_(
                Cliente.nombre_cliente.ilike(f"%{search}%"),
                Venta.id_venta.ilike(f"%{search}%")
            )
        )

    total = query.count()
    offset = (page - 1) * limit

    ventas = (
        query.order_by(desc(Venta.fecha_venta))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return templates.TemplateResponse("ventas.html", {
        "request": request,
        "ventas": ventas,
        "search": search,
        "page": page,
        "total_pages": total_pages,
        "ruta_base": "/ventas"
    })


#Ruta para mostrar la vista de crear una nueva venta
@router.get("/crear_venta", response_class=HTMLResponse, tags=["Ventas"])
def Ventas_get(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.cookies.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(url="/login?error=2", status_code=303)

    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    if not usuario:
        return RedirectResponse(url="/login?error=2", status_code=303)

    fecha_actual = date.today().strftime("%Y-%m-%d")

    return templates.TemplateResponse("crear.html", {
        "request": request,
        "fecha_actual": fecha_actual,
        "nombre_usuario": usuario.nombre_usuario,
        "id_usuario": usuario_id
    })

#Ruta para registrar la venta del producto
@router.post("/ventas/generar", tags=["Ventas"])
def generar_venta(data: dict, db: Session = Depends(get_db)):
    id_cliente = data["id_cliente"]
    id_usuario = data["id_usuario"]
    productos = data["productos"]

    total_venta = 0
    detalles = []

    if not productos:
        raise HTTPException(status_code=400, detail="No se han agregado productos a la venta")
    
    for item in productos:
        id_producto = item["id_producto"]
        cantidad = item["cantidad"]

        producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {id_producto} no encontrado")
        if producto.stock < cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre_producto}")

        precio_real = producto.precio_venta if producto.precio_venta is not None else producto.precio
        subtotal = cantidad * float(precio_real)
        total_venta += subtotal

        detalles.append({
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio_unitario": precio_real
        })

        producto.stock -= cantidad

    nueva_venta = Venta(
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        fecha_venta=datetime.now(timezone.utc),
        total_venta=total_venta
    )
    db.add(nueva_venta)
    db.flush()

    for det in detalles:
        nuevo_detalle = DetalleVenta(
            id_venta=nueva_venta.id_venta,
            id_producto=det["id_producto"],
            cantidad=det["cantidad"],
            precio_unitario=det["precio_unitario"]
        )
        db.add(nuevo_detalle)

    db.commit()
    return {"message": "Venta registrada con éxito", "id_venta": nueva_venta.id_venta}


#Ruta para obtener venta pr id
@router.get("/ventas/detalle/{id_venta}", response_class=JSONResponse, tags=["Ventas"])
def obtener_detalle(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).options(joinedload(Venta.cliente), joinedload(Venta.usuario)).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    detalles = db.query(DetalleVenta).filter(DetalleVenta.id_venta == id_venta).all()

    resultado = {
        "cliente": venta.cliente.nombre_cliente,
        "fecha": venta.fecha_venta.strftime("%d/%m/%Y"),
        "vendedor": venta.usuario.nombre_usuario,
        "total": int(venta.total_venta),
        "detalles": []
    }

    for d in detalles:
        producto = db.query(Producto).filter(Producto.id_producto == d.id_producto).first()
        resultado["detalles"].append({
            "producto": producto.nombre_producto if producto else "¿?",
            "descripcion": producto.descripcion if producto else "¿?"
        })

    return resultado

#Mostar la venta Cuando ya este finalizada
@router.get("/ventas/comprobante/{id_venta}", response_class=HTMLResponse, tags=["Ventas"])
def ver_comprobante(id_venta: int, request: Request, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        return HTMLResponse(content="Venta no encontrada", status_code=404)
    
    cliente = db.query(Cliente).filter(Cliente.id_cliente == venta.id_cliente).first()
    detalles = (
        db.query(DetalleVenta)
        .filter(DetalleVenta.id_venta == venta.id_venta)
        .join(Producto)
        .all()
    )

    return templates.TemplateResponse("comprobante.html", {
        "request": request,
        "venta": venta,
        "cliente": cliente,
        "detalles": detalles
    })
