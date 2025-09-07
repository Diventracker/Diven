from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="layout/templates")  # Ruta donde están las vistas

#Ruta para el layout
@router.get("/diventracker", tags=["admin"])
def home(request: Request):
    usuario = request.state.usuario
    return templates.TemplateResponse("layout_admin.html", {
        "request": request,
        "rol": usuario["rol"],
        "usuario_nombre": usuario["nombre"]
    })



