from fastapi import APIRouter,HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from models.servicio import ServicioTecnico
from models.cliente import Cliente  
#from schemas import servicioSchema

router = APIRouter()
templates = Jinja2Templates(directory="templates/admin/modulos")  # Ruta donde están las vistas


@router.get("/servicios", response_class=HTMLResponse, tags=["servicio_tecnico"])
def obtener_servicios(request: Request, search: str = "", db: Session = Depends(get_db)):
    if search:
        servicios = db.query(ServicioTecnico).filter(
            (ServicioTecnico.id_servicio.ilike(f"%{search}%")) |
            (ServicioTecnico.tipo_equipo.ilike(f"%{search}%"))
        ).all()
    else:
        servicios = db.query(ServicioTecnico).all()
    return templates.TemplateResponse("servicios.html", {"request": request, "servicios": servicios})


#Obetener los clientes para agregarlos al Select
@router.get("/servicios/clientes", response_class=JSONResponse)
def filtrar_clientes(q: str = "", db: Session = Depends(get_db)):
    clientes = db.query(Cliente).filter(
        (Cliente.nombre_cliente.ilike(f"%{q}%")) |
        (Cliente.cedula.ilike(f"%{q}%"))
    ).all()

    return [{"id": c.id_cliente, "nombre": c.nombre_cliente, "cedula": c.cedula} for c in clientes]


#Ruta para crear un nuevo servicio tecnico
@router.post("/servicio/crear", tags=["servicio_tecnico"])
def crear_servicio(
    request: Request,  # Para acceder a la cookie
    cliente_id: int = Form(...),
    tipo_equipo: str = Form(...),
    marca: str = Form(...),
    modelo_equipo: str = Form(...),
    descripcion: str = Form(...),
    fecha_recepcion: str = Form(...),
    fecha_entrega: str = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    # Obtener el usuario_id desde la cookie
    usuario_id = request.cookies.get("usuario_id")

    # Convertir usuario_id a entero
    usuario_id = int(usuario_id)
    
    # Crear el nuevo servicio técnico
    nuevo = ServicioTecnico(
        id_cliente=cliente_id,
        id_usuario=usuario_id,  
        tipo_equipo=tipo_equipo,
        marca_equipo=marca,
        modelo_equipo=modelo_equipo,
        descripcion_problema=descripcion,
        fecha_recepcion=fecha_recepcion,
        fecha_entrega_estimada=fecha_entrega,
        estado_servicio=estado,
    )

    db.add(nuevo)
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
    marca: str = Form(...),
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
    servicio.marca_equipo = marca
    servicio.modelo_equipo = modelo_equipo
    servicio.descripcion_problema = descripcion
    servicio.fecha_recepcion = fecha_recepcion
    servicio.fecha_entrega_estimada = fecha_entrega
    servicio.estado_servicio = estado

    db.commit()
    db.refresh(servicio)
        
    return JSONResponse(content={"message": "success"})