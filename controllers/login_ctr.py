from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import SessionLocal
from schemas.usuario import UsuarioLogin
from models.usuario import Usuario

router = APIRouter()
templates = Jinja2Templates(directory="templates")


#Ruta para la ventana del login
@router.get("/login", response_class=HTMLResponse, tags=["Login"])
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Función para obtener una sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", tags=['Login'])
async def login_post(
    response: Response,
    correo: str = Form(...),
    clave: str = Form(...),
    db: Session = Depends(get_db) #Abre conexion a bd y cierra auto
):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()

    if not usuario or usuario.clave != clave: #compara los parametros 
        return HTMLResponse(content="Correo o clave inválidos", status_code=401)

    # Verificar el rol del usuario
    if usuario.rol == "Administrador":
        response = RedirectResponse(url="/admin", status_code=302)
    elif usuario.rol == "empleado":
        response = RedirectResponse(url="/empleado", status_code=302)
    else:
        return HTMLResponse(content="Rol no autorizado", status_code=403)

    # Guardar ID del usuario en cookie
    response.set_cookie(key="usuario_id", value=str(usuario.id_usuario))
    return response