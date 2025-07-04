from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from proveedores.controller import ProveedorControlador
from proveedores.schema import ProveedorSchema

router = APIRouter()

#Ruta principal para mostrar tabla Proveedores
@router.get("/proveedores", tags=["Proveedores"])
def listar_proveedores(request: Request, db: Session = Depends(get_db)):
    controlador = ProveedorControlador(db)
    return controlador.mostrar_vista(request)

#Ruta manda los datos de la base de datos en proveedores
@router.get("/proveedores/data")
async def obtener_datos_proveedores(db: Session = Depends(get_db)):
    controlador = ProveedorControlador(db)
    return controlador.listar_todos()


#Ruta para Crear un nuevo Proveedor
@router.post("/proveedores/crear", tags=["Proveedores"])
def crear_proveedor(
    proveedor: ProveedorSchema = Depends(ProveedorSchema.as_form),
    db: Session = Depends(get_db)
):
    controlador = ProveedorControlador(db)
    return controlador.crear(proveedor)
    

#Ruta para actualizar los datos del proveedor
@router.put("/proveedor/editar/{proveedor_id}", tags=["Proveedores"])
def editar_proveedor(
    proveedor_id: int,
    proveedor_data: ProveedorSchema = Depends(ProveedorSchema.as_form),
    db: Session = Depends(get_db)
):
    controlador = ProveedorControlador(db)
    return controlador.editar(proveedor_id, proveedor_data)

    
#Eliminar Proveedor...
@router.delete("/proveedor/eliminar/{id_proveedor}", tags=["Proveedores"])
def eliminar_proveedor(
    id_proveedor: int,
    db: Session = Depends(get_db)
):
    controlador = ProveedorControlador(db)
    return controlador.eliminar(id_proveedor)

#Ruta filtra los proveedores por ni o nombre y los manda al select2
@router.get("/proveedores/filtrar", tags=["Proveedores"])
def filtrar_proveedores(search: str = "", db: Session = Depends(get_db)):
    return ProveedorControlador(db).filtrar_proveedores(search)