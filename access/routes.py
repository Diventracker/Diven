from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="access/templates")  # Ruta donde están las vistas

@router.get("/admin", tags=["admin"])
def home(request: Request):
    usuario_id = request.cookies.get("usuario_id")
    if usuario_id:
        return templates.TemplateResponse("layout_admin.html", {"request": request})
    return RedirectResponse(url="/login?error=2", status_code=303)

#Xd Ruta para cerrar sesion
@router.post("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="usuario_id")
    return response

#ruta intermedia para cerrar session
@router.get("/cerrando_sesion")
def cerrando_sesion(request: Request):
    return templates.TemplateResponse("cerrar-sesion.html", {"request": request})
