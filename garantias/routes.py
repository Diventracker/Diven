from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from garantias.controller import GarantiaControlador
from garantias.model import Garantia
from servicios.model import ServicioTecnico
from clientes.model import Cliente

router = APIRouter()
templates = Jinja2Templates(directory="garantias/templates")


#Ruta que muestra el html de garantias
@router.get("/garantias", tags=["Garantias"])
def obtener_garantias(request: Request):
    controlador = GarantiaControlador()
    return controlador.vista_principal(request)