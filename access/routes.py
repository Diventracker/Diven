from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="access/templates")  # Ruta donde están las vistas

#Ruta para el layout
@router.get("/diventracker", tags=["admin"])
def home(request: Request):
    if not hasattr(request.state, "usuario"):
        return RedirectResponse(url="/login?error=2", status_code=303)

    usuario = request.state.usuario
    return templates.TemplateResponse("layout_admin.html", {
        "request": request,
        "rol": usuario["rol"],
        "usuario_nombre": usuario["nombre"]
    })

#Xd Ruta para cerrar sesion
@router.post("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="usuario_id")
    return response

