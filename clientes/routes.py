from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError #para manejo de errores
from database.database import get_db
from clientes.model import Cliente
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="clientes/templates")  # Ruta donde están las vistas

#Ruta principal para mostrar tabla clientes
@router.get("/clientes", tags=["Clientes"])
def listar_clientes(request: Request, search: str = "", db: Session = Depends(get_db)):
    rol = request.cookies.get("rol")  # Obtener rol de la cookie

    if search:
        clientes = db.query(Cliente).filter(
            (Cliente.nombre_cliente.ilike(f"%{search}%")) |
            (Cliente.cedula.ilike(f"%{search}%"))
        ).all()
    else:
        clientes = db.query(Cliente).order_by(Cliente.id_cliente.desc()).all()

    return templates.TemplateResponse("clientes.html", {
        "request": request,
        "clientes": clientes,
        "search": search,
        "rol": rol
    })

#Registrar nuevo cliente
@router.post("/clientes/crear", tags=["Clientes"])
def crear_cliente(
    nombre_cliente: str = Form(...),
    cedula: str = Form(...),
    direccion_cliente: str = Form(...),
    telefono_cliente: str = Form(...),
    email_cliente: str = Form(...),
    lugar: str = Form(...),
    db: Session = Depends(get_db)
):
    nuevo = Cliente(
        nombre_cliente=nombre_cliente,
        cedula=cedula,
        direccion_cliente=direccion_cliente,
        telefono_cliente=telefono_cliente,
        email_cliente=email_cliente
    ) 

    try:
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)  # actualiza el objeto con el id generado

        if lugar == "ventas":
            # Devolver los datos del cliente recién creado
            return JSONResponse(content={
                "id": nuevo.id_cliente,
                "nombre_cliente": nuevo.nombre_cliente,
                "cedula": nuevo.cedula,
                "direccion_cliente": nuevo.direccion_cliente
            })

        # Si no es ventas, redirigir como antes
        return RedirectResponse(url="/clientes?create=1", status_code=303)

    except IntegrityError:
        db.rollback()
        if lugar == "ventas":
            return JSONResponse(content={"error": "Ya existe un cliente con esa cédula o Correo"}, status_code=400)
        return RedirectResponse(url="/clientes?error=1", status_code=303)


#Editar Cliente
@router.put("/cliente/editar/{id_cliente}", tags=["Clientes"])
def editar_cliente(
    id_cliente: int,
    nombre: str = Form(...),
    cedula: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        return HTMLResponse(content="Cliente no encontrado", status_code=404)

    try:        
        cliente.nombre_cliente = nombre
        cliente.cedula = cedula
        cliente.telefono_cliente = telefono
        cliente.direccion_cliente = direccion
        cliente.email_cliente = email
        db.commit()
        return JSONResponse(content={"message": "success"})

    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"message": "error"})


#Eliminar Cliente...
@router.delete("/cliente/eliminar/{id_cliente}", tags=["Clientes"])
def eliminar_cliente(
    id_cliente: int,
    db: Session = Depends(get_db)
):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        return HTMLResponse(content="Cliente no encontrado", status_code=404)
    try: 
        db.delete(cliente)
        db.commit()
        return JSONResponse(content={"message": "deleted"})
    
    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"message": "error"})

    
#Ruta para obtener el cliente
@router.get("/clientes/buscar/{cedula}", response_class=JSONResponse)
def buscar_cliente_por_cedula(cedula: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.cedula == cedula).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {
        "id": cliente.id_cliente,
        "nombre": cliente.nombre_cliente,
        "cedula": cliente.cedula,
        "direccion": cliente.direccion_cliente,
        # Agrega más campos si los tienes
    }