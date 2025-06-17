from fastapi import APIRouter, Request, Form, Depends, Response, HTTPException , Query
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from utils.report_generator import generar_pdf_informe
from producto.model import Producto
from clientes.model import Cliente
from usuarios.model import Usuario
from proveedores.model import Proveedor
from servicios.model import  ServicioTecnico
from garantias.model import Garantia
from datetime import datetime 
from ventas.model import Venta
from producto.model import Producto
from producto.schema import ProductoOut
from sqlalchemy import text , extract, func

router = APIRouter()

templates = Jinja2Templates(directory="dashboard/templates")


#Ruta para la ventana del dashboard/y mostrar la informacion de ventas y servicios

@router.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
def dashboard_get(request: Request, db: Session = Depends(get_db)):
    ultimas_ventas = db.query(Venta).order_by(Venta.fecha_venta.desc()).limit(5).all()
    ultimos_servicios = db.query(ServicioTecnico).order_by(ServicioTecnico.fecha_recepcion.desc()).limit(5).all()
    alertas_producto = db.query(Producto).filter(Producto.stock < 10).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "ultimas_ventas": ultimas_ventas,
        "ultimos_servicios": ultimos_servicios,
        "alertas_producto": alertas_producto
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
        Producto.fecha_compra != None,
        Producto.fecha_compra >= fecha_inicio,
        Producto.fecha_compra <= fecha_fin
        ).all()
        columnas = ["ID", "Nombre", "Modelo", "Stock", "Precio"]
        datos = [{
            "ID": p.id_producto,
            "Nombre": p.nombre_producto,
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
        resultados = db.execute(text("""
            SELECT 
                gs.id_garantia, 
                gs.fecha_inicio, 
                gs.fecha_fin,
                c.nombre_cliente,
                st.tipo_equipo
            FROM garantia_servicio gs
            JOIN servicio_tecnico st ON gs.id_servicio = st.id_servicio
            JOIN cliente c ON st.id_cliente = c.id_cliente
            WHERE gs.fecha_inicio BETWEEN :inicio AND :fin
        """), {"inicio": fecha_inicio, "fin": fecha_fin}).fetchall()

        columnas = ["ID Garantía", "Cliente", "Tipo de Equipo", "Inicio", "Fin"]
        datos = [{
            "ID Garantía": r[0],
            "Cliente": r[3],
            "Tipo de Equipo": r[4],
            "Inicio": r[1].strftime("%d/%m/%Y"),
            "Fin": r[2].strftime("%d/%m/%Y")
        } for r in resultados]


    elif tipo == "ventas":
        ventas = db.query(Venta).filter(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta <= fecha_fin
        ).all()
        columnas = ["ID Venta", "Fecha de venta", "Cliente", "Total"]
        datos = [{
            "ID Venta": v.id_venta,
            "Fecha de venta": v.fecha_venta.strftime("%d/%m/%y"),
            "Cliente": v.cliente.nombre_cliente if v.cliente else "Desconocido",
            "Total": f"${v.total_venta:.2f}"
        } for v in ventas]
    

    else:
        return {"error": "Tipo de informe no soportado aún."}

    path = generar_pdf_informe(tipo, fecha_inicio_str, fecha_fin_str, datos, columnas)
    return FileResponse(path, filename=f"informe_{tipo}.pdf", media_type="application/pdf")


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


#ruta de fecha personalizada
@router.get("/api/dashboard/stats")
def get_stats_personalizado(
    fecha_inicio: str = Query(...),
    fecha_fin: str = Query(...),
    db=Depends(get_db)
):
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (debe ser AAAA-MM-DD)")

    if inicio > fin:
        raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser mayor que la fecha final")

    filtro = f"DATE(fecha_venta) BETWEEN '{inicio}' AND '{fin}'"

    ventas_totales = db.execute(text(f"""
        SELECT COALESCE(SUM(total_venta), 0)
        FROM venta
        WHERE {filtro}
    """)).scalar()

    numero_ventas = db.execute(text(f"""
        SELECT COUNT(*) 
        FROM venta
        WHERE {filtro}
    """)).scalar()

    nuevos_clientes = db.execute(text(f"""
        SELECT COUNT(DISTINCT id_cliente)
        FROM venta
        WHERE {filtro}
    """)).scalar()

    return {
        "fecha_inicio": str(inicio),
        "fecha_fin": str(fin),
        "ventas_totales": ventas_totales,
        "numero_ventas": numero_ventas,
        "nuevos_clientes": nuevos_clientes
    }


# Ruta para obtener las estadisticas del dashboard
@router.get("/api/dashboard/stats/{periodo}")
def get_dashboard_stats(periodo: str, db=Depends(get_db)):
    print("🧠 Periodo recibido:", periodo)
    if periodo == "hoy":
        filtro_actual = "DATE(fecha_venta) = CURDATE()"
        filtro_anterior = "DATE(fecha_venta) = CURDATE() - INTERVAL 1 DAY"
    elif periodo == "semana":
        filtro_actual = "YEARWEEK(fecha_venta, 1) = YEARWEEK(CURDATE(), 1)"
        filtro_anterior = "YEARWEEK(fecha_venta, 1) = YEARWEEK(CURDATE() - INTERVAL 1 WEEK, 1)"
    elif periodo == "mes":
        filtro_actual = "MONTH(fecha_venta) = MONTH(CURDATE()) AND YEAR(fecha_venta) = YEAR(CURDATE())"
        filtro_anterior = "MONTH(fecha_venta) = MONTH(CURDATE() - INTERVAL 1 MONTH) AND YEAR(fecha_venta) = YEAR(CURDATE() - INTERVAL 1 MONTH)"
    elif periodo == "anio":
        filtro_actual = "YEAR(fecha_venta) = YEAR(CURDATE())"
        filtro_anterior = "YEAR(fecha_venta) = YEAR(CURDATE() - INTERVAL 1 YEAR)"
    else:
        raise HTTPException(status_code=400, detail="Periodo inválido")

    # Valores actuales
    total_actual = db.execute(text(f"""
        SELECT COALESCE(SUM(total_venta), 0)
        FROM venta WHERE {filtro_actual}
    """)).scalar()

    ventas_actual = db.execute(text(f"""
        SELECT COUNT(*) FROM venta WHERE {filtro_actual}
    """)).scalar()

    clientes_actual = db.execute(text(f"""
        SELECT COUNT(DISTINCT id_cliente) FROM venta WHERE {filtro_actual}
    """)).scalar()

    # Valores anteriores
    total_anterior = db.execute(text(f"""
        SELECT COALESCE(SUM(total_venta), 0)
        FROM venta WHERE {filtro_anterior}
    """)).scalar()

    ventas_anterior = db.execute(text(f"""
        SELECT COUNT(*) FROM venta WHERE {filtro_anterior}
    """)).scalar()

    clientes_anterior = db.execute(text(f"""
        SELECT COUNT(DISTINCT id_cliente) FROM venta WHERE {filtro_anterior}
    """)).scalar()
    #calcular la variacion porcentual
    def calcular_variacion(actual, anterior):
        if anterior == 0:
            return 100 if actual > 0 else 0
        return round(((actual - anterior) / anterior) * 100, 1)

    return {
        "periodo": periodo,
        "ventas_totales": total_actual,
        "numero_ventas": ventas_actual,
        "nuevos_clientes": clientes_actual,
        "var_ventas_totales": calcular_variacion(total_actual, total_anterior),
        "var_numero_ventas": calcular_variacion(ventas_actual, ventas_anterior),
        "var_nuevos_clientes": calcular_variacion(clientes_actual, clientes_anterior)
    }



#ruta para la informacion de cards en el periodo seleccionado
@router.get("/api/dashboard/stats/{periodo}")
def get_dashboard_stats(periodo: str, db=Depends(get_db)):
    if periodo == "hoy":
        filtro = "DATE(fecha_venta) = CURDATE()"
    elif periodo == "semana":
        filtro = "YEARWEEK(fecha_venta, 1) = YEARWEEK(CURDATE(), 1)"
    elif periodo == "mes":
        filtro = "MONTH(fecha_venta) = MONTH(CURDATE()) AND YEAR(fecha_venta) = YEAR(CURDATE())"
    elif periodo == "anio":
        filtro = "YEAR(fecha_venta) = YEAR(CURDATE())"
    else:
        raise HTTPException(status_code=400, detail="Periodo inválido")

    ventas_totales = db.execute(text(f"""
        SELECT COALESCE(SUM(total_venta), 0)
        FROM venta
        WHERE {filtro}
    """)).scalar()

    numero_ventas = db.execute(text(f"""
        SELECT COUNT(*) 
        FROM venta
        WHERE {filtro}
    """)).scalar()

    nuevos_clientes = db.execute(text(f"""
        SELECT COUNT(DISTINCT id_cliente)
        FROM venta
        WHERE {filtro}
    """)).scalar()

    return {
        "ventas_totales": ventas_totales,
        "numero_ventas": numero_ventas,
        "nuevos_clientes": nuevos_clientes
    }

#llamada de datos para la grafica 1
@router.post("/api/datos")
def get_ventas_por_mes(db: Session = Depends(get_db)):
    resultados = db.query(
        extract('month', Venta.fecha_venta).label("mes"),
        func.sum(Venta.total_venta).label("total")
    ).group_by("mes").order_by("mes").all()

    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    datos_por_mes = {mes: total for mes, total in resultados}

    labels = meses_nombres
    datos = [datos_por_mes.get(i + 1, 0) for i in range(12)]

    return {
        "labels": labels,
        "datasets": [{
            "label": "Total Ventas por Mes",
            "data": datos,
            "backgroundColor": '#5e9188',
            "borderColor": '#5e9188',
            "borderWidth": 2
        }]
    }


    
#ruta para obtener el producto menos vendido
@router.get("/api/dashboard/productos-mas-vendidos")
def productos_mas_vendidos(db=Depends(get_db)):
    query = text("""
        SELECT p.nombre_producto, SUM(dv.cantidad) AS total_vendido
        FROM detalle_venta dv
        JOIN producto p ON dv.id_producto = p.id_producto
        GROUP BY p.nombre_producto
        ORDER BY total_vendido DESC
        LIMIT 6
    """)
    resultados = db.execute(query).fetchall()
    return [{"producto": r[0], "cantidad": r[1]} for r in resultados]

# Ruta para obtener las ventas por vendedor
@router.get("/api/dashboard/ventas-vendedor")
def ventas_por_vendedor(db: Session = Depends(get_db)):
    query = text("""
        SELECT u.nombre_usuario, COALESCE(SUM(v.total_venta), 0) AS total_vendido
        FROM usuario u
        LEFT JOIN venta v ON u.id_usuario = v.id_usuario
        WHERE u.rol = 'vendedor'
        GROUP BY u.nombre_usuario
        ORDER BY total_vendido DESC
    """)
    resultados = db.execute(query).fetchall()

    return [{"vendedor": r[0], "total": r[1]} for r in resultados]

# tipo de equipo mas recibido
@router.get("/api/dashboard/servicios-por-equipo")
def servicios_por_equipo(db: Session = Depends(get_db)):
    query = text("""
        SELECT tipo_equipo, COUNT(*) AS total
        FROM servicio_tecnico
        GROUP BY tipo_equipo
        ORDER BY total DESC
    """)
    resultados = db.execute(query).fetchall()
    return [{"equipo": r[0], "total": r[1]} for r in resultados]
