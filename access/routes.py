from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="access/templates")  # Ruta donde están las vistas

@router.get("/diventracker", tags=["admin"])
def home(request: Request):
    usuario_id = request.cookies.get("usuario_id")
    rol = request.cookies.get("rol")  # <--- Agrega esta línea  
    usuario_nombre = request.cookies.get("nombre_usuario")   

    if usuario_id:
        return templates.TemplateResponse("layout_admin.html", {"request": request, "rol": rol, "usuario_nombre": usuario_nombre})
    return RedirectResponse(url="/login?error=2", status_code=303)

#Xd Ruta para cerrar sesion
@router.post("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="usuario_id")
    return response

