from fastapi import APIRouter,HTTPException, Depends, Request, Form 
from datetime import datetime
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse 
from fastapi.templating import Jinja2Templates 
from sqlalchemy.orm import Session
from database.database import get_db
from servicios.model import DetalleServicio, ServicioTecnico
from clientes.model import Cliente
from servicios.schema import ServicioCreate, ServicioRevisionSchema  

router = APIRouter()
templates = Jinja2Templates(directory="servicios/templates")  # Ruta donde están las vistas

@router.get("/servicios", response_class=HTMLResponse, tags=["servicio_tecnico"])
def listar_servicios(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 9,
    search: str = ""
):
    query = db.query(ServicioTecnico)

    rol = request.cookies.get("rol")  # Obtener rol de la cookie

    if search:
        query = query.filter(
            (ServicioTecnico.id_servicio.ilike(f"%{search}%")) |
            (ServicioTecnico.tipo_equipo.ilike(f"%{search}%"))
        )
    
    total = query.count()
    offset = (page - 1) * limit
    servicios = query.offset(offset).limit(limit).all()

    total_pages = (total + limit - 1) // limit  # Redondeo hacia arriba

    return templates.TemplateResponse("servicios.html", {
        "request": request,
        "servicios": servicios,
        "ruta_base": "/servicios",
        "page": page,
        "total_pages": total_pages,
        "search": search,
        "rol": rol  
    })


#Obetener los clientes para agregarlos al Select
@router.get("/servicios/clientes", response_class=JSONResponse)
def filtrar_clientes(search: str = "", db: Session = Depends(get_db)):
    clientes = db.query(Cliente).filter(
        (Cliente.nombre_cliente.ilike(f"%{search}%")) |
        (Cliente.numero_documento.ilike(f"%{search}%"))
    ).all()

    return [{"id": c.id_cliente, "nombre": c.nombre_cliente, "cedula": c.numero_documento} for c in clientes]


#Ruta para crear un nuevo servicio tecnico
@router.post("/servicio/crear", tags=["servicio_tecnico"])
def crear_servicio(
    request: Request,  # Para acceder a la cookie
    datos: ServicioCreate = Depends(ServicioCreate.as_form),
    db: Session = Depends(get_db)
):
    # Obtener el usuario_id desde la cookie
    usuario_id = request.cookies.get("usuario_id")

    # Convertir usuario_id a entero
    usuario_id = int(usuario_id)
    
    # Crear el nuevo servicio técnico
    nuevo_servicio = ServicioTecnico(
        id_cliente=datos.cliente_id,
        id_usuario=usuario_id,
        modelo_equipo=datos.modelo_equipo,
        tipo_equipo=datos.tipo_equipo,
        tipo_servicio=datos.tipo_servicio,
        precio_servicio=datos.precio_servicio,
        descripcion_problema=datos.descripcion
    )

    db.add(nuevo_servicio)
    db.commit()

    return RedirectResponse(url="/servicios?create=1", status_code=303)


#Ruta para eliminar un servicio Tecnico
@router.delete("/servicio/eliminar/{service_id}", response_model=dict)
def eliminar_servicio(service_id: int, db: Session = Depends(get_db)):
    # Buscar el servicio por ID
    servicio = db.query(ServicioTecnico).filter(ServicioTecnico.id_servicio == service_id).first()
    
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # Eliminar el servicio
    db.delete(servicio)
    db.commit()

    return JSONResponse(content={"message": "deleted"})



#Ruta para Editar servicio Tecnico
@router.put("/servicio/editar/{service_id}", tags=["servicio_tecnico"])
def editar_servicio(
    service_id: int,
    tipo_equipo: str = Form(...),
    #se elimino marca
    modelo_equipo: str = Form(...),
    descripcion: str = Form(...),
    fecha_recepcion: str = Form(...),
    fecha_entrega: str = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    servicio = db.query(ServicioTecnico).filter(ServicioTecnico.id_servicio == service_id).first()
    
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # Actualizar los campos
    servicio.tipo_equipo = tipo_equipo
    #se elminio marca de actualizar
    servicio.modelo_equipo = modelo_equipo
    servicio.descripcion_problema = descripcion
    servicio.fecha_recepcion = fecha_recepcion
    servicio.fecha_entrega_estimada = fecha_entrega
    servicio.estado_servicio = estado

    db.commit()
    db.refresh(servicio)
        
    return JSONResponse(content={"message": "success"})

#Ruta para mandar el request de la revision al administradr
@router.post("/api/servicio/revision")
async def registrar_revision(
    request: Request,
    data: ServicioRevisionSchema = Depends(ServicioRevisionSchema.as_form),
    db: Session = Depends(get_db)
):
    try:
        servicio = db.query(ServicioTecnico).filter_by(id_servicio=data.id_servicio).first()

        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # Actualizar campos en ServicioTecnico
        servicio.meses_garantia = data.meses_garantia
        servicio.descripcion_trabajo = data.descripcion
        servicio.estado_servicio = "En Revisión"
        db.add(servicio)

        # Obtener el usuario_id desde la cookie
        usuario_id = request.cookies.get("usuario_id")

        # Convertir usuario_id a entero
        usuario_id = int(usuario_id)

        # Insertar detalles de costos adicionales
        for detalle in data.detalles:
            if detalle.valor_adicional > 0 and detalle.motivo.strip():
                nuevo = DetalleServicio(
                    id_servicio=data.id_servicio,
                    id_usuario=usuario_id,
                    valor_adicional=detalle.valor_adicional,
                    motivo=detalle.motivo
                )
                db.add(nuevo)

        db.commit()
        return {"message": "Servicio actualizado y detalles guardados."}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")
    
#Ruta que retorna los serivicos con revision pendiente
@router.get("/api/servicios-en-revision")
def servicios_en_revision(db: Session = Depends(get_db)):
    servicios = db.query(ServicioTecnico).filter(ServicioTecnico.estado_servicio == "En Revisión").all()

    resultado = []
    for s in servicios:
        resultado.append({
            "id": s.id_servicio,
            "cliente": s.cliente.nombre_cliente,
            "descripcion": s.tipo_servicio + " - " + s.tipo_equipo,            
        })

    return resultado

#Mostar los detalles del servicio segun su estado, tendra diferentes campos
@router.get("/servicios/comprobante/{id_servicio}", response_class=HTMLResponse, tags=["servicio_tecnico"])
def ver_comprobante(id_servicio: int, request: Request, db: Session = Depends(get_db)):
    servicio = db.query(ServicioTecnico).filter(ServicioTecnico.id_servicio == id_servicio).first()
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")  # o usa datetime.today()
    if not servicio:
        return HTMLResponse(content="Venta no encontrada", status_code=404)
    
    cliente = db.query(Cliente).filter(Cliente.id_cliente == ServicioTecnico.id_cliente).first()
    detalles = (
        db.query(DetalleServicio)
        .filter(DetalleServicio.id_servicio == ServicioTecnico.id_servicio).all()
    )

    return templates.TemplateResponse("comprobante.html", {
        "request": request,
        "servicio": servicio,
        "cliente": cliente,
        "fecha_hoy": fecha_hoy,
        "detalles": detalles
    })
