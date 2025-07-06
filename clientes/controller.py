from sqlalchemy.exc import IntegrityError
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from clientes.schema import ClienteBase
from clientes.crud import ClienteCRUD
from clientes.repositorio import ClienteRepositorio

#Ruta de las vistas html
templates = Jinja2Templates(directory=["templates", "clientes/templates"])

class ClienteControlador:
    def __init__(self, db: Session):
        repo = ClienteRepositorio(db)
        self.crud = ClienteCRUD(repo)
        

    def vista_clientes(self, request: Request) -> HTMLResponse:
        usuario = request.state.usuario
        return templates.TemplateResponse("clientes.html", {
            "request": request,
            "rol": usuario["rol"]
        })
    
    
    def listar(self):
        clientes = self.crud.listar()

        return JSONResponse(content=[
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


    def buscar_por_documento(self, documento: str):
        try:
            cliente = self.crud.buscar_por_documento(documento)

            return JSONResponse(content={"success": True,
                "data": {
                    "id": cliente.id_cliente,
                    "nombre": cliente.nombre_cliente,
                    "numero_documento": cliente.numero_documento,
                    "direccion": cliente.direccion_cliente,
                    "tipo_documento": cliente.tipo_documento,
                    "telefono": cliente.telefono_cliente,
                    "email": cliente.email_cliente
                }
            }, status_code=200)

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)


    def registrar(self, datos: ClienteBase, lugar: str):
        try:
            nuevo = self.crud.crear(datos)

            if lugar == "ventas":
                return JSONResponse(content={
                    "id": nuevo.id_cliente,
                    "nombre_cliente": nuevo.nombre_cliente,
                    "tipo_documento": nuevo.tipo_documento,
                    "numero_documento": nuevo.numero_documento,
                    "direccion_cliente": nuevo.direccion_cliente
                })

            return JSONResponse(content={"success": True, "mensaje": "Cliente creado exitosamente"}, status_code=200)

        except ValueError as e:
            if lugar == "ventas":
                return JSONResponse(content={"error": str(e)}, status_code=400)
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
        
    def editar(self, id_cliente: int, datos: ClienteBase):
        try:
            self.crud.editar(id_cliente, datos)
            return JSONResponse(content={"success": True, "mensaje": "Cliente actualizado exitosamente"}, status_code=200)

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
        
    def eliminar(self, id_cliente: int):
        try:
            self.crud.eliminar(id_cliente)
            return JSONResponse(content={"success": True, "mensaje": "Cliente eliminado exitosamente"},status_code=200)

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)},status_code=404)

        except IntegrityError as e:
            self.crud.repo.db.rollback()

            # Validar si es una violación por clave foránea
            if "foreign key constraint" in str(e).lower() or "a foreign key constraint fails" in str(e.orig).lower():
                return JSONResponse(content={"success": False, "error": "No se puede eliminar el cliente porque tiene relaciones con otros registros."}, status_code=400)

            return JSONResponse(
                content={"success": False, "error": "Error al eliminar el cliente"},
                status_code=400
            )

        except Exception as e:
            return JSONResponse(content={"success": False, "error": f"Error inesperado: {str(e)}"},status_code=500)
    
    #Funcion pasa filtra los clientes para los selects de servicios
    def filtrar_clientes(self, texto: str):
        clientes = self.crud.filtrar_por_texto(texto)
        return [
            {
                "id": c.id_cliente,
                "nombre": c.nombre_cliente,
                "documento": c.numero_documento
            } for c in clientes
        ]
        
        



