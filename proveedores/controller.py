from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from proveedores.schema import ProveedorSchema
from proveedores.repositorio import ProveedorRepositorio
from proveedores.crud import ProveedorCRUD


templates = Jinja2Templates(directory=["templates", "proveedores/templates"])

class ProveedorControlador:
    def __init__(self, db):
        repo = ProveedorRepositorio(db)
        self.crud = ProveedorCRUD(repo)

    def mostrar_vista(self, request: Request):
        usuario = request.state.usuario
        return templates.TemplateResponse("proveedores.html", {"request": request, "rol": usuario["rol"]})
    
    def listar_todos(self):
        proveedores = self.crud.listar_todos()
        return JSONResponse([
            {
                "id_proveedor": p.id_proveedor,
                "nit": p.nit,
                "fecha_registro": p.fecha_registro.strftime("%Y-%m-%d"),
                "nombre_proveedor": p.nombre_proveedor,
                "representante_ventas": p.representante_ventas,
                "telefono_representante_ventas": p.telefono_representante_ventas,
                "direccion_proveedor": p.direccion_proveedor
            }
            for p in proveedores
        ])

    def crear(self, datos: ProveedorSchema):
        try:
            proveedor = self.crud.crear(datos)
            return JSONResponse(content={"success": True, "mensaje": "Proveedor registrado correctamente", "id": proveedor.id_proveedor})

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": f"Error inesperado: {str(e)}"}, status_code=500)
        
    def editar(self, proveedor_id: int, datos: ProveedorSchema):
        try:
            proveedor = self.crud.editar(proveedor_id, datos)
            return JSONResponse(content={"success": True, "mensaje": "Proveedor actualizado correctamente"})
        
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": f"Error inesperado: {str(e)}"}, status_code=500)
        
    def eliminar(self, proveedor_id: int):
        try:
            self.crud.eliminar(proveedor_id)
            return JSONResponse(content={"success": True, "mensaje": "Proveedor eliminado correctamente"})

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)

        except IntegrityError:
            self.crud.repo.db.rollback()
            return JSONResponse(content={"success": False, "error": "No se puede eliminar el proveedor (relaciones existentes)"}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": f"Error inesperado: {str(e)}"}, status_code=500)
        
    def filtrar_proveedores(self, search: str = ""):
        proveedores = self.crud.filtrar(search)
        return JSONResponse(content=[
            {
                "id": p.id_proveedor,
                "nombre": p.nombre_proveedor,
                "nit": p.nit
            } for p in proveedores
        ])

