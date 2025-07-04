from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from clientes.controller import ClienteControlador
from database.database import get_db
from clientes.schema import ClienteBase

router = APIRouter()


#Ruta principal vista clientes
@router.get("/clientes", tags=["Clientes"])
def listar_clientes(request: Request, db: Session = Depends(get_db)):
    controlador = ClienteControlador(db)
    return controlador.vista_clientes(request)


#Ruta manda todos los clientes de la base de datos
@router.get("/clientes/data", tags=["Clientes"])
def obtener_datos_clientes(db: Session = Depends(get_db)):
    controlador = ClienteControlador(db)
    return controlador.listar()


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
@router.get("/clientes/buscar/{documento}", tags=["Clientes"])
def buscar_cliente_por_documento(documento: str, db: Session = Depends(get_db)):
    controlador = ClienteControlador(db)
    return controlador.buscar_por_documento(documento)


#Ruta para filtrar los clientes en las busquedas
@router.get("/clientes/filtrar", tags=["Clientes"])
def filtrar_clientes(search: str = "", db: Session = Depends(get_db)):
    controlador = ClienteControlador(db)
    return controlador.filtrar_clientes(search)
