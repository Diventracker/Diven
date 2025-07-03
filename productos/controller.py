from fastapi import Request
from fastapi.templating import Jinja2Templates
from productos.crud import ProductoCRUD
from productos.schema import ProductoCreate
from fastapi.responses import JSONResponse

templates = Jinja2Templates(directory=["templates", "productos/templates"])

class ProductoControlador:
    def __init__(self, db):
        self.crud = ProductoCRUD(db)

    def mostrar_vista(self, request: Request):
        rol = request.cookies.get("rol")
        return templates.TemplateResponse("productos2.html", {
            "request": request,
            "rol": rol
        })

    def crear(self, datos: ProductoCreate):
        try:
            producto = self.crud.crear(datos)
            return JSONResponse(content={
                "success": True,
                "message": "Producto creado exitosamente.",
                "id": producto.id_producto
            })
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
        except Exception as e:
            return JSONResponse(content={"success": False, "error": "Error interno al crear producto."}, status_code=500)
