from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from login.controller import LoginControlador
from usuarios.schema import CambiarClaveSchema, SolicitudRecuperacion, TokenValidacionSchema

router = APIRouter()
templates = Jinja2Templates(directory="login/templates")

#Ruta para el html del login
@router.get("/login", response_class=HTMLResponse, tags=["Login"])
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


#Ruta para la vista de cambio de contraseña
@router.get("/cambiar-clave", response_class=HTMLResponse, tags=["Login"])
def vista_cambio_clave(request: Request):
    return templates.TemplateResponse("cambiar_clave.html", {"request": request})


#Ruta para validar el login
@router.post("/api/login")
def login(correo: str = Form(...), clave: str = Form(...), db: Session = Depends(get_db)):
    return LoginControlador(db).login(correo, clave)


#Ruta es para la generacion del token y recuperar la contraseña
@router.post("/auth/recuperar", tags=["Login"])
def solicitar_recuperacion(data: SolicitudRecuperacion, db: Session = Depends(get_db)):
    controlador = LoginControlador(db)
    return controlador.solicitar_recuperacion(data.correo)


#Ruta es para validar el Token
@router.post("/auth/validar-token", tags=["Login"])
def validar_token(data: TokenValidacionSchema, db: Session = Depends(get_db)):
    controlador = LoginControlador(db)
    return controlador.validar_token(data.correo, data.token)


#La que valida y cambia la contraseña
@router.post("/use/cambiar-clave", tags=["Login"])
def cambiar_clave(request: Request, data: CambiarClaveSchema, db: Session = Depends(get_db)):
    controlador = LoginControlador(db)
    return controlador.cambiar_clave(request, data)
