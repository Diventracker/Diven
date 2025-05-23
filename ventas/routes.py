from datetime import date, datetime, timezone
from fastapi import APIRouter, HTTPException, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from inventario.model import Producto
from usuarios.model import Usuario
from ventas.model import DetalleVenta, Venta


router = APIRouter()
templates = Jinja2Templates(directory="ventas/templates")


#Ruta para la lista de las ventas
@router.get("/ventas", response_class=HTMLResponse, tags=["gestionventas"])
def gestionventas_get(request: Request):
    return templates.TemplateResponse("ventas.html", {"request": request})


@router.get("/crear_venta", response_class=HTMLResponse, tags=["ventas"])
def Ventas_get(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.cookies.get("usuario_id")
    
    if not usuario_id:
        return RedirectResponse(url="/login?error=2", status_code=303)

    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        return RedirectResponse(url="/login?error=2", status_code=303)

    fecha_actual = date.today().strftime("%Y-%m-%d")  # Formato para el input type="date"

    return templates.TemplateResponse("crear.html", {
        "request": request,
        "fecha_actual": fecha_actual,
        "nombre_usuario": usuario.nombre_usuario,
        "id_usuario": usuario_id
    })

#Funcion para registrar las ventas
@router.post("/ventas/generar")
def generar_venta(data: dict, db: Session = Depends(get_db)):
    id_cliente = data["id_cliente"]
    id_usuario = data["id_usuario"]
    productos = data["productos"]  # Lista dicts con id_producto, cantidad, precio_unitario (del front)

    total_venta = 0
    detalles = []

    for item in productos:
        id_producto = item["id_producto"]
        cantidad = item["cantidad"]

        producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()

        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {id_producto} no encontrado")

        if producto.stock < cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre_producto}")

        # Precio real desde la BD
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
    db.flush()  # Para obtener id_venta

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