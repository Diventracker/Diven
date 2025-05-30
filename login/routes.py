from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from usuarios.model import Usuario
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="login/templates")


#Ruta para la ventana del login
@router.get("/login", response_class=HTMLResponse, tags=["Login"])
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


#Contexto para verificar la cntraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Ruta para validar el login
@router.post("/login", tags=['Login'])
async def login_post(
    response: Response,
    correo: str = Form(...),
    clave: str = Form(...),
    db: Session = Depends(get_db) #Abre conexion a bd y cierra auto
):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()

    def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool: #booleano
        return pwd_context.verify(contraseña_plana, contraseña_hash) #Verfiica la contra almacena y devuelva true o false
    

    if not usuario or not verificar_contraseña(clave, usuario.clave):
        return RedirectResponse(url="/login?error=1", status_code=303)

    # Verificar el rol del usuario
    if usuario.rol == "Administrador":
        response = RedirectResponse(url="/diventracker", status_code=302)
    elif usuario.rol == "Tecnico":
        response = RedirectResponse(url="/diventracker", status_code=302)
    else:
        return HTMLResponse(content="Rol no autorizado", status_code=403)

    # Guardar ID del usuario en cookie
    response.set_cookie(key="usuario_id", value=str(usuario.id_usuario))
    response.set_cookie(key="rol", value=usuario.rol)  # <- Aquí agregas el rol
    return response