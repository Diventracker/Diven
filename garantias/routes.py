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


#Ruta que muestra todas las garantias en ventas
@router.get("/garantias", response_class=HTMLResponse, tags=["garantias"])
def obtener_garantias(
    request: Request,
    search: str = "",
    page: int = 1,
    limit: int = 9,
    db: Session = Depends(get_db)
):
    query = db.query(Garantia).join(Garantia.servicio)

    if search:
        query = query.filter(
            (Garantia.id_garantia.ilike(f"%{search}%")) |
            (ServicioTecnico.tipo_equipo.ilike(f"%{search}%"))
        )

    total = query.count()
    offset = (page - 1) * limit

    garantias = (
        query.order_by(Garantia.id_garantia.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return templates.TemplateResponse("garantias.html", {
        "request": request,
        "garantias": garantias,
        "search": search,
        "page": page,
        "total_pages": total_pages,
        "ruta_base": "/garantias"
    })