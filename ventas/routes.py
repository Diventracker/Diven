from fastapi import APIRouter, Request, Depends 
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database.database import get_db
from ventas.controller import VentaControlador
from servicios.controller import ServicioControlador
from servicios.schema import EstadoServicioInput, ServicioCreate, ServicioRevisionSchema, ServicioUpdate 

router = APIRouter()

#Ruta para mostrar el html de ventas
@router.get("/ventas", tags=["Ventas"])
def gestionventas_get(request: Request, db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.vista_ventas(request)


#Ruta que retorna todas la ventas en json
@router.get("/ventas/data")
async def obtener_datos_ventas(db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.listar_todas()


#Ruta para mostrar la vista de crear una nueva venta
@router.get("/crear_venta", response_class=HTMLResponse, tags=["Ventas"])
def ventas_get_endpoint(request: Request, db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.vista_crear_venta(request)


#Ruta para registrar la venta del producto
@router.post("/ventas/generar", tags=["Ventas"])
def generar_venta_endpoint(data: dict, db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.generar_venta(
        id_cliente=data["id_cliente"],
        id_usuario=data["id_usuario"],
        productos=data["productos"]
    )


#Ruta para obtener venta por id
@router.get("/ventas/detalle/{id_venta}", tags=["Ventas"])
def obtener_detalle(id_venta: int, db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.detalle_venta(id_venta)

#Mostar la venta Cuando ya este finalizada
@router.get("/ventas/comprobante/{id_venta}", tags=["Ventas"])
def ver_comprobante_endpoint(id_venta: int, request: Request, db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.ver_comprobante(id_venta, request)

#Ruta para ventas por mes
@router.post("/ventas/data/mes")
def get_ventas_por_mes(db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.obtener_datos_grafico_mensual()

#Productos mas vendidos
@router.get("/ventas/productos-mas-vendidos", tags=["Ventas"])
def productos_mas_vendidos(db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.productos_mas_vendidos()

#Ventas Por vendedor
@router.get("/ventas/ventas-vendedor", tags=["Ventas"])
def ventas_por_vendedor(db: Session = Depends(get_db)):
    controlador = VentaControlador(db)
    return controlador.ventas_por_vendedor()


#fragmento para mostrar los productos que estan en finalizado
@router.get("/servicios/finalizado", tags=["servicio_tecnico"])
def listar_estado_finalizado(db: Session = Depends(get_db)):
    controlador = ServicioControlador(db)
    return controlador.obtener_finalizados()