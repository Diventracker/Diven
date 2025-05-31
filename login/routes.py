from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from usuarios.model import Usuario
from usuarios.schema import CambiarClaveSchema, SolicitudRecuperacion, TokenValidacionSchema
from passlib.context import CryptContext

from utils.email import enviar_correo
from utils.token import generar_token

router = APIRouter()
templates = Jinja2Templates(directory="login/templates")


#Ruta para la ventana del login
@router.get("/login", response_class=HTMLResponse, tags=["Login"])
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#Ruta para la vista de cambio de contraseña
@router.get("/cambiar-clave", response_class=HTMLResponse, tags=["Login"])
def vista_cambio_clave(request: Request):
    return templates.TemplateResponse("cambiar_clave.html", {"request": request})


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
    response.set_cookie(key="nombre_usuario", value=usuario.nombre_usuario)
    return response


#Ruta es para la generacion del token y recuperar la contraseña
@router.post("/auth/recuperar", tags=['Login'])
def solicitar_recuperacion(data: SolicitudRecuperacion, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()

    if usuario: #Si esta, asi no se muestra si existe o no el correo 
        # Generar y guardar token
        token = generar_token()
        usuario.token_recuperacion = token
        usuario.token_expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)  # Token válido por 15 minutos
        db.commit()

        # Enviar correo con el token
        enviar_correo(
            usuario.correo,
            "Código de recuperación",
            "token_recuperacion.html",
            nombre=usuario.nombre_usuario,
            token=token
        )


    return {"msg": "Código enviado al correo"}


#Ruta es para validar el Token
@router.post("/auth/validar-token")
def validar_token(data: TokenValidacionSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Correo no registrado")

    if usuario.token_recuperacion != data.token:
        raise HTTPException(status_code=400, detail="Token inválido")

    if not usuario.token_expiracion or usuario.token_expiracion.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expirado")

    return {"msg": "Token válido", "recuperacion": True, "correo": usuario.correo, "token": usuario.token_recuperacion}


@router.post("/auth/cambiar-clave")
def cambiar_clave(request: Request, data: CambiarClaveSchema, db: Session = Depends(get_db)):
    CambiarClaveSchema.validar_campos(data)  # validación manual

    if data.token:
        # Validación por recuperación
        usuario = db.query(Usuario).filter(
            Usuario.correo == data.correo,
            Usuario.token_recuperacion == data.token,
            Usuario.token_expiracion >= datetime.now(timezone.utc)
        ).first()
        if not usuario:
            raise HTTPException(status_code=400, detail="Token inválido o expirado")
    else:
        # Validación normal con clave actual
        usuario_id = request.cookies.get("usuario_id")
        usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first() # según tu lógica de sesión
        if not pwd_context.verify(data.clave_actual, usuario.clave):
            raise HTTPException(status_code=400, detail="Clave actual incorrecta")

    # Cambiar la clave
    usuario.clave = pwd_context.hash(data.nueva_clave)
    usuario.token_recuperacion = None
    usuario.token_expiracion = None
    db.commit()

    return {"msg": "Contraseña actualizada correctamente"}