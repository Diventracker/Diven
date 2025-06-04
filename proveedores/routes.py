from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError #para manejo de errores
from database.database import get_db
from proveedores.model import Proveedor
from proveedores.schema import ProveedorSchema
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="proveedores/templates")  # Ruta donde están las vistas

#Ruta principal para mostrar tabla Proveedores
@router.get("/proveedores", response_class=HTMLResponse, tags=["Proveedores"])
def listar_proveedores(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 9,
    search: str = ""
):
    query = db.query(Proveedor)

    if search:
        query = query.filter(
            (Proveedor.nombre_proveedor.ilike(f"%{search}%")) |
            (Proveedor.nit.ilike(f"%{search}%"))
        )

    total = query.count()
    offset = (page - 1) * limit
    proveedores = query.offset(offset).limit(limit).all()

    total_pages = (total + limit - 1) // limit

    return templates.TemplateResponse("proveedores.html", {
        "request": request,
        "proveedores": proveedores,
        "page": page,
        "total_pages": total_pages,
        "search": search,
        "ruta_base": "/proveedores" 
    })

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