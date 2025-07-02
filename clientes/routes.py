from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session
from clientes.controller import ClienteControlador
from database.database import get_db
from clientes.model import Cliente
from clientes.schema import ClienteBase
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory=["templates", "clientes/templates"])


#Ruta principal para mostrar tabla clientes
@router.get("/clientes", tags=["Clientes"])
def listar_clientes(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 9,
    search: str = ""
):
    rol = request.cookies.get("rol")

    query = db.query(Cliente).order_by(desc(Cliente.id_cliente))

    if search:
        query = query.filter(
            (Cliente.nombre_cliente.ilike(f"%{search}%")) |
            (Cliente.numero_documento.ilike(f"%{search}%"))
        )

    total = query.count()
    offset = (page - 1) * limit
    clientes = query.offset(offset).limit(limit).all()

    total_pages = (total + limit - 1) // limit

    return templates.TemplateResponse("clientes2.html", {
        "request": request,
        "clientes": clientes,
        "page": page,
        "total_pages": total_pages,
        "search": search,
        "ruta_base": "/clientes",  
        "rol": rol
    })

@router.get("/clientes/data")
async def obtener_datos_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).order_by(desc(Cliente.id_cliente))
    # Serializamos manualmente si cliente.fecha_registro es datetime
    return JSONResponse([
        {
            "id_cliente": c.id_cliente,
            "fecha_registro": c.fecha_registro.strftime("%Y-%m-%d"),
            "nombre_cliente": c.nombre_cliente,
            "tipo_documento": c.tipo_documento,
            "numero_documento": c.numero_documento,
            "direccion_cliente": c.direccion_cliente,
            "telefono_cliente": c.telefono_cliente,
            "email_cliente": c.email_cliente
        }
        for c in clientes
    ])

#Registrar nuevo cliente
@router.post("/clientes/crear", tags=["Clientes"])
def crear_cliente_endpoint(
    datos: ClienteBase = Depends(ClienteBase.as_form),
    lugar: str = Form(...),
    db: Session = Depends(get_db)
):
    controlador = ClienteControlador(db)
    return controlador.registrar(datos, lugar)


#Editar Cliente
@router.put("/cliente/editar/{id_cliente}", tags=["Clientes"])
def editar_cliente_endpoint(
    id_cliente: int,
    datos: ClienteBase = Depends(ClienteBase.as_form),
    db: Session = Depends(get_db)
):
    controlador = ClienteControlador(db)
    return controlador.editar(id_cliente, datos)


#Eliminar Cliente...
@router.delete("/cliente/eliminar/{id_cliente}", tags=["Clientes"])
def eliminar_cliente_endpoint(
    id_cliente: int,
    db: Session = Depends(get_db)
):
    controlador = ClienteControlador(db)
    return controlador.eliminar(id_cliente)


    
#Ruta para obtener el cliente
@router.get("/clientes/buscar/{documento}", response_class=JSONResponse, tags=["Clientes"])
def buscar_cliente_por_documento(documento: str, db: Session = Depends(get_db)):
    controlador = ClienteControlador(db)
    return controlador.buscar_por_documento(documento)
