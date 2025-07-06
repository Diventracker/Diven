from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dashboard.controller import DashboardControlador
from database.database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="dashboard/templates")

#Ruta del html del dashboard
@router.get("/dashboard", tags=["dashboard"])
def dashboard_get(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request,})


# Ruta para obtener las estadisticas del dashboard
@router.get("/api/dashboard/stats/{periodo}", tags=["Dashboard"])
def get_dashboard_stats(
    periodo: str,
    fecha_inicio: str = Query(None),
    fecha_fin: str = Query(None),
    db: Session = Depends(get_db)
):
    controlador = DashboardControlador(db)
    return controlador.obtener_estadisticas(periodo, fecha_inicio, fecha_fin)
