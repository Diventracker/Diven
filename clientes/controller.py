from sqlite3 import IntegrityError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from clientes.schema import ClienteBase
from clientes.CRUD import ClienteCRUD
from clientes.repositorio import ClienteRepositorio

class ClienteControlador:
    def __init__(self, db: Session):
        repo = ClienteRepositorio(db)
        self.crud = ClienteCRUD(repo)

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
            return JSONResponse(content={"success": True, "mensaje": "Cliente eliminado exitosamente"}, status_code=200)

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)

        except IntegrityError:
            self.crud.repo.db.rollback()
            return JSONResponse(content={"success": False, "error": "Error al eliminar el cliente"}, status_code=400)



