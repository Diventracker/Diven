from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from garantias.controller import GarantiaControlador
from pydantic import BaseModel
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="garantias/templates")

@router.get("/garantias", tags=["Garantias"])
def obtener_garantias(request: Request, db: Session = Depends(get_db)):
    controlador = GarantiaControlador(db)
    return controlador.vista_principal(request)

@router.get("/garantias/data/ventas", tags=["Garantias"])
def garantias_ventas_data(cliente: str | None = None, db: Session = Depends(get_db)):
    controlador = GarantiaControlador(db)
    return controlador.listar_garantias_ventas(cliente)

class EstadoDTO(BaseModel):
    estado: str

@router.post("/garantias/{tipo}/{id_garantia}/estado", tags=["Garantias"])
def cambiar_estado(tipo: str, id_garantia: int, dto: EstadoDTO, db: Session = Depends(get_db)):
    return GarantiaControlador(db).actualizar_estado(tipo, id_garantia, dto.estado)


class RenovarDTO(BaseModel):
    id_producto_nuevo: int | None = None
    meses: int | None = 1
    fecha_inicio: date | None = None

@router.post("/garantias/producto/{id_garantia}/renovar", tags=["Garantias"])
def renovar_garantia_producto(id_garantia: int, dto: RenovarDTO, db: Session = Depends(get_db)):
    return GarantiaControlador(db).renovar_producto(
        id_garantia=id_garantia,
        id_producto_nuevo=dto.id_producto_nuevo,
        meses=dto.meses,
        fecha_inicio=dto.fecha_inicio
    )

@router.get("/garantias/data/servicios", tags=["Garantias"])
def garantias_servicios_data(q: str | None = None, db: Session = Depends(get_db)):
    controlador = GarantiaControlador(db)
    return controlador.listar_garantias_servicios(q)