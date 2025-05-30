from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from utils.report_generator import generar_pdf_informe
from inventario.model import Producto
from clientes.model import Cliente
from usuarios.model import Usuario
from proveedores.model import Proveedor
from servicios.model import  ServicioTecnico
from garantias.model import Garantia
from datetime import datetime
from ventas.model import Venta
from servicios.model import ServicioTecnico  # Asegúrate de importar tu modelo

router = APIRouter()

templates = Jinja2Templates(directory="dashboard/templates")


#Ruta para la ventana del dashboard/y mostrar la informacion de ventas y servicios
@router.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
def dashboard_get(request: Request, db: Session = Depends(get_db)):
    ultimas_ventas = db.query(Venta).order_by(Venta.fecha_venta.desc()).limit(5).all()
    ultimos_servicios = db.query(ServicioTecnico).order_by(ServicioTecnico.fecha_recepcion.desc()).limit(5).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "ultimas_ventas": ultimas_ventas,
        "ultimos_servicios": ultimos_servicios
    })


@router.post("/api/generar-informe")
async def generar_informe(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    tipo = data["tipo"]
    fecha_inicio_str = data["fecha_inicio"]
    fecha_fin_str = data["fecha_fin"]

    # Convertir fechas a tipo date (requerido para comparaciones)
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Formato de fecha inválido"}

    if tipo == "inventario":
        productos = db.query(Producto).filter(
            Producto.fecha_compra >= fecha_inicio,
            Producto.fecha_compra <= fecha_fin
        ).all()
        columnas = ["ID", "Nombre", "Marca", "Modelo", "Stock", "Precio"]
        datos = [{
            "ID": p.id_producto,
            "Nombre": p.nombre_producto,
            "Marca": p.marca,
            "Modelo": p.modelo,
            "Stock": p.stock,
            "Precio": f"${p.precio_venta:.2f}" if p.precio_venta else "-"
        } for p in productos]

    elif tipo == "clientes":
        clientes = db.query(Cliente).all()  # No tiene fecha para filtrar
        columnas = ["ID", "Nombre", "Cédula", "Teléfono", "Email"]
        datos = [{
            "ID": c.id_cliente,
            "Nombre": c.nombre_cliente,
            "Cédula": c.cedula,
            "Teléfono": c.telefono_cliente,
            "Email": c.email_cliente
        } for c in clientes]

    elif tipo == "usuarios":
        usuarios = db.query(Usuario).all()  # No tiene fecha para filtrar
        columnas = ["ID", "Nombre", "Correo", "Rol"]
        datos = [{
            "ID": u.id_usuario,
            "Nombre": u.nombre_usuario,
            "Correo": u.correo,
            "Rol": u.rol
        } for u in usuarios]

    elif tipo == "proveedores":
        proveedores = db.query(Proveedor).all()  # No tiene fecha para filtrar
        columnas = ["ID", "Nombre", "NIT", "Representante", "Teléfono"]
        datos = [{
            "ID": p.id_proveedor,
            "Nombre": p.nombre_proveedor,
            "NIT": p.nit,
            "Representante": p.representante_ventas,
            "Teléfono": p.telefono_representante_ventas
        } for p in proveedores]

    elif tipo == "servicios":
        servicios = db.query(ServicioTecnico).filter(
            ServicioTecnico.fecha_recepcion >= fecha_inicio,
            ServicioTecnico.fecha_recepcion <= fecha_fin
        ).all()
        columnas = ["ID", "Equipo", "Marca", "Cliente", "Estado", "Recepción"]
        datos = [{
            "ID": s.id_servicio,
            "Equipo": s.tipo_equipo,
            "Marca": s.marca_equipo,
            "Cliente": s.id_cliente,
            "Estado": s.estado_servicio,
            "Recepción": s.fecha_recepcion.strftime("%d/%m/%Y")
        } for s in servicios]

    elif tipo == "garantias":
        garantias = db.query(Garantia).filter(
            Garantia.fecha_inicio >= fecha_inicio,
            Garantia.fecha_inicio <= fecha_fin
        ).all()
        columnas = ["ID Garantía", "Servicio", "Inicio", "Fin"]
        datos = [{
            "ID Garantía": g.id_garantia,
            "Servicio": g.id_servicio,
            "Inicio": g.fecha_inicio.strftime("%d/%m/%Y"),
            "Fin": g.fecha_fin.strftime("%d/%m/%Y")
        } for g in garantias]

    else:
        return {"error": "Tipo de informe no soportado aún."}

    path = generar_pdf_informe(tipo, fecha_inicio_str, fecha_fin_str, datos, columnas)
    return FileResponse(path, filename=f"informe_{tipo}.pdf", media_type="application/pdf")




