from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from usuarios.controller import UsuarioControlador
from usuarios.schema import UsuarioCreateSchema

router = APIRouter()

#Ruta principal para mostrar tabla usuarios
@router.get("/usuarios", tags=["Usuarios"])
def listar_usuarios(request: Request, db: Session = Depends(get_db)):
    controlador = UsuarioControlador(db)  # No necesita DB para esta vista
    return controlador.vista_principal(request)


#Ruta que devuelve todos los datos
@router.get("/usuarios/data")
async def obtener_datos_usuarios(db: Session = Depends(get_db)):
    controlador = UsuarioControlador(db)
    return controlador.listar_todos()

#Ruta para crear un nuevo usuario
@router.post("/usuarios/crear", tags=["Usuarios"])
def crear_usuario(
    usuario: UsuarioCreateSchema = Depends(UsuarioCreateSchema.as_form),
    db: Session = Depends(get_db)
):
    controlador = UsuarioControlador(db)
    return controlador.crear(usuario)


#Ruta para actualizar los datos del Usuario
@router.put("/usuario/editar/{usuario_id}", tags=["Usuarios"])
def editar_usuario(
    usuario_id: int,
    usuario_data: UsuarioCreateSchema = Depends(UsuarioCreateSchema.as_form),
    db: Session = Depends(get_db)
):
    controlador = UsuarioControlador(db)
    return controlador.editar(usuario_id, usuario_data)

 
#Eliminar usuario...
@router.delete("/usuario/eliminar/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    controlador = UsuarioControlador(db)
    return controlador.eliminar(id_usuario)
