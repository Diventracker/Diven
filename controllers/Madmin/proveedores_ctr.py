from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError #para manejo de errores
from database.database import get_db
from models.proveedor import Proveedor
from schemas.proveedor import ProveedorSchema
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates/admin/modulos")  # Ruta donde están las vistas

#Ruta principal para mostrar tabla Proveedores
@router.get("/proveedores", response_class=HTMLResponse, tags=["Proveedores"])
def listar_proveedores(request: Request, search: str = "", db: Session = Depends(get_db)):
    if search:
        proveedores = db.query(Proveedor).filter(
            (Proveedor.nombre_proveedor.ilike(f"%{search}%")) |
            (Proveedor.nit.ilike(f"%{search}%"))
        ).all()
    else:
        proveedores = db.query(Proveedor).order_by(Proveedor.id_proveedor.desc()).all()

    return templates.TemplateResponse("proveedores.html", {"request": request, "proveedores": proveedores, "search": search})

#Ruta para Crear un nuevo Proveedor
@router.post("/proveedores/crear", tags=["Proveedores"])
def crear_proveedor(
    proveedor: ProveedorSchema = Depends(ProveedorSchema.as_form),
    db: Session = Depends(get_db)
):
    nuevo_proveedor = Proveedor(**proveedor.model_dump())  # Mapea los datos directamente

    try:
        db.add(nuevo_proveedor)
        db.commit()
        return RedirectResponse(url="/proveedores?create=1", status_code=303)
    
    except IntegrityError:
        db.rollback()
        return RedirectResponse(url="/proveedores?error=1", status_code=303)
    

#Ruta para actualizar los datos del proveedor
@router.put("/proveedor/editar/{proveedor_id}", tags=["Proveedores"])
def editar_proveedor(
    proveedor_id: int,
    proveedor_data: ProveedorSchema = Depends(ProveedorSchema.as_form),
    db: Session = Depends(get_db)
):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == proveedor_id).first()
    if not proveedor:
        return HTMLResponse(content="Proveedor no encontrado", status_code=404)

    try:
        # Actualizar los campos dinámicamente
        for field, value in proveedor_data.model_dump(exclude_none=True).items():
            setattr(proveedor, field, value)

        db.commit()
        return RedirectResponse(url="/proveedores?success=1", status_code=303)

    except IntegrityError:
        db.rollback()
        return RedirectResponse(url="/proveedores?error=1", status_code=303)
    
#Eliminar Proveedor...
@router.delete("/proveedor/eliminar/{id_proveedor}", tags=["Proveedores"])
def eliminar_proveedor(
    id_proveedor: int,
    db: Session = Depends(get_db)
):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        return HTMLResponse(content="Proveedor no encontrado", status_code=404)
    try: 
        db.delete(proveedor)
        db.commit()
        return JSONResponse(content={"message": "deleted"})
    
    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"message": "error"})