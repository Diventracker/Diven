from fastapi import Request
from fastapi.templating import Jinja2Templates
from ventas.crud import VentaCRUD
from ventas.repositorio import VentaRepositorio
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, HTMLResponse


templates = Jinja2Templates(directory=["templates", "ventas/templates"])

class VentaControlador:
    def __init__(self, db: Session):
        self.crud = VentaCRUD(VentaRepositorio(db))

    def vista_ventas(self, request: Request) -> HTMLResponse:
        rol = request.cookies.get("rol")
        return templates.TemplateResponse("ventas2.html", {
            "request": request,
            "rol": rol
        })

    def detalle_venta(self, id_venta: int):
        datos = self.crud.obtener_detalle_venta(id_venta)
        return JSONResponse(content=datos)

