from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse 
from sqlalchemy.orm import Session
from database.database import get_db
from servicios.controller import ServicioControlador
from servicios.schema import EstadoServicioInput, ServicioCreate, ServicioRevisionSchema, ServicioUpdate  

router = APIRouter()

#Ruta muestra el html de los servicios
@router.get("/servicios", tags=["servicio_tecnico"])
def listar_servicios(request: Request, db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.vista_principal(request)

#Ruta que envia todos los servicios json
@router.get("/servicios/data", tags=["servicio_tecnico"])
def obtener_servicios_data(db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.obtener_datos()

#Ruta para crear un nuevo servicio tecnico
@router.post("/servicio/crear", tags=["servicio_tecnico"])
def crear_servicio(
    request: Request,
    datos: ServicioCreate = Depends(ServicioCreate.as_form),
    db: Session = Depends(get_db)
):
    controlador = ServicioControlador(db)
    return controlador.crear(request, datos)


#Ruta para eliminar un servicio Tecnico
@router.delete("/servicio/eliminar/{service_id}", tags=["servicio_tecnico"])
def eliminar_servicio(service_id: int, db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.eliminar(service_id)

#Ruta para actualizar los servicios
@router.put("/servicio/editar/{id_servicio}", tags=["servicio_tecnico"])
def actualizar_servicio(
    request: Request,
    id_servicio: int,
    datos: ServicioUpdate,
    db: Session = Depends(get_db)
):
    controlador = ServicioControlador(db)
    try:
        usuario_id = request.state.usuario["usuario_id"]
    except:
        return JSONResponse(content={"success": False, "error": "Usuario inválido"}, status_code=400)

    return controlador.actualizar(id_servicio, datos, usuario_id)


#Ruta para mandar el request de la revision al administradr
@router.post("/servicio/revision", tags=["servicio_tecnico"])
async def registrar_revision(
    request: Request,
    data: ServicioRevisionSchema = Depends(ServicioRevisionSchema.as_form),
    db: Session = Depends(get_db)
):
    controlador = ServicioControlador(db)
    try:
        usuario_id = request.state.usuario["usuario_id"]
    except:
        return JSONResponse(content={"success": False, "error": "ID de usuario inválido"}, status_code=400)

    return controlador.registrar_revision(data, usuario_id)
    
    
#Ruta que retorna los servicios con revision pendiente
@router.get("/api/servicios-en-revision", tags=["servicio_tecnico"])
def servicios_en_revision(db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.listar_servicios_en_revision()


#Mostar los detalles del servicio segun su estado, tendra diferentes campos
@router.get("/servicios/comprobante/{id_servicio}", tags=["servicio_tecnico"])
def ver_comprobante(id_servicio: int, request: Request, db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.ver_comprobante(id_servicio, request)


#Ruta para obtener los detalles del servicio
@router.get("/api/servicio/{id_servicio}/detalles", tags=["servicio_tecnico"])
def obtener_detalles_servicio(id_servicio: int, db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.obtener_detalles(id_servicio)


#Funcion para aprobar el estado del servicio 
@router.put("/servicios/{servicio_id}/estado", tags=["servicio_tecnico"])
def cambiar_estado_servicio(
    servicio_id: int,
    datos: EstadoServicioInput,
    db: Session = Depends(get_db)
):
    controlador = ServicioControlador(db)
    return controlador.actualizar_estado(servicio_id, datos)