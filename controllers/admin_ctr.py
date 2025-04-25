from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates/admin")  # Ruta donde están las vistas

@router.get("/admin", response_class=HTMLResponse, tags=["admin"])
def home(request: Request):
    usuario_id = request.cookies.get("usuario_id")
    if usuario_id:
        return templates.TemplateResponse("layout_admin.html", {"request": request})
    return HTMLResponse(content="No has iniciado sesión")

#Xd