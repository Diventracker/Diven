from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
from fastapi.templating import Jinja2Templates
from database.database import get_db
from utils.crud import crear_recurso
from models.usuario import Usuario
from schemas.usuario import UsuarioCreateSchema, UsuarioUpdateSchema
from controllers.email import enviar_correo

router = APIRouter()

templates = Jinja2Templates(directory="templates/admin/modulos")  # Ruta donde están las vistas

#Ruta principal para mostrar tabla usuarios
@router.get("/usuarios", tags=["Usuarios"])
def listar_usuarios(request: Request, search: str = "", db: Session = Depends(get_db)):
    if search:
        usuarios = db.query(Usuario).filter(
            (Usuario.nombre_usuario.ilike(f"%{search}%")) |
            (Usuario.correo.ilike(f"%{search}%"))
        ).all()
    else:
        usuarios = db.query(Usuario).order_by(Usuario.id_usuario.desc()).all()

    return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios, "search": search})


# Inicializamos un contexto de hash para bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Ruta para crear un nuevo usuario
@router.post("/usuario/crear", tags=["Usuarios"])
def crear_usuario(
    usuario: UsuarioCreateSchema = Depends(UsuarioCreateSchema.as_form),
    db: Session = Depends(get_db)
):
    clave_plana = secrets.token_urlsafe(10)
    clave_hash = pwd_context.hash(clave_plana)

    data = usuario.model_dump()
    data["clave"] = clave_hash

    def notificar_usuario(usuario_creado):
        enviar_correo(
            destinatario=usuario_creado.correo,
            asunto="Tu cuenta ha sido creada",
            nombre=usuario_creado.nombre_usuario,
            clave=clave_plana  # esta variable debe estar disponible en el scope
        )

    return crear_recurso(
        model_class=Usuario,
        data=data,
        db=db,
        redirect_url="/usuarios?create=1",
        error_url="/usuarios",
        on_success=notificar_usuario
    )

#Ruta para actualizar los datos del Usuario
@router.put("/usuario/editar/{usuario_id}", tags=["Usuarios"])
def editar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdateSchema = Depends(UsuarioUpdateSchema.as_form),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        return JSONResponse(content={"message": "error"})

    try:
        # Actualizar los campos dinámicamente
        for field, value in usuario_data.model_dump(exclude_none=True).items():
            setattr(usuario, field, value)

        db.commit()
        return RedirectResponse(url="/usuarios?success=1", status_code=303)

    except IntegrityError:
        db.rollback()
        return RedirectResponse(url="/usuarios?error=1", status_code=303)
    
#Eliminar usuario...
@router.delete("/usuario/eliminar/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        return JSONResponse(content={"message": "unfound"})
    try: 
        db.delete(usuario)
        db.commit()
        return JSONResponse(content={"message": "deleted"})
    
    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"message": "error"})