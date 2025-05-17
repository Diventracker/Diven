from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from garantias.model import Garantia
from servicios.model import ServicioTecnico
from clientes.model import Cliente

router = APIRouter()
templates = Jinja2Templates(directory="garantias/templates")



@router.get("/garantias", response_class=HTMLResponse, tags=["garantias"])
def obtener_garantias(request: Request, search: str = "", db: Session = Depends(get_db)):
    if search:
        garantias = db.query(Garantia).join(Garantia.servicio).filter(
            (Garantia.id_garantia.ilike(f"%{search}%")) |
            (ServicioTecnico.tipo_equipo.ilike(f"%{search}%"))
        ).all()
    else:
        garantias = db.query(Garantia).join(Garantia.servicio).all()
    
    return templates.TemplateResponse("garantias.html", {
        "request": request,
        "garantias": garantias
    })