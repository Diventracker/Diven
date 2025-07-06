from datetime import date
from fastapi import Request
from fastapi.templating import Jinja2Templates
from usuarios.repositorio import UsuarioRepositorio
from ventas.crud import VentaCRUD
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse


templates = Jinja2Templates(directory=["templates", "ventas/templates"])


class VentaControlador:
    def __init__(self, db: Session):
        self.crud = VentaCRUD(db)
        self.usuario_repo = UsuarioRepositorio(db)

    def vista_ventas(self, request: Request) -> HTMLResponse:
        usuario = request.state.usuario
        return templates.TemplateResponse("ventas.html", {
            "request": request,
            "rol": usuario["rol"]
        })
    
    def listar_todas(self):
        ventas = self.crud.listar_todas()
        return JSONResponse([
            {
                "id_venta": v.id_venta,
                "fecha_venta": v.fecha_venta.strftime("%Y-%m-%d"),
                "nombre_cliente": v.cliente.nombre_cliente if v.cliente else "—",
                "cantidad_productos": sum(d.cantidad for d in v.detalles),
                "valor_venta": f"${v.total_venta:,.0f}",
                "nombre_usuario": v.usuario.nombre_usuario,
            }
            for v in ventas
        ])

    def detalle_venta(self, id_venta: int):
        datos = self.crud.obtener_detalle_venta(id_venta)
        return JSONResponse(content=datos)

    def vista_crear_venta(self, request: Request) -> HTMLResponse | RedirectResponse:
        usuario = request.state.usuario

        if not usuario:
            return RedirectResponse(url="/login?error=2", status_code=303)

        usuario = self.usuario_repo.obtener_por_id(int(usuario["usuario_id"]))  # usamos repositorio
        if not usuario:
            return RedirectResponse(url="/login?error=2", status_code=303)

        fecha_actual = date.today().strftime("%Y-%m-%d") #hacerlo timestamp en la bd y esto dejarlo de vista

        return templates.TemplateResponse("crear.html", {
            "request": request,
            "fecha_actual": fecha_actual,
            "nombre_usuario": usuario.nombre_usuario,
            "id_usuario": usuario.id_usuario
        })
    
    #Funcion que registra la venta
    def generar_venta(self, id_cliente: int, id_usuario: int, productos: list[dict]) -> JSONResponse:
        try:
            id_venta = self.crud.generar(id_cliente, id_usuario, productos)
            return JSONResponse(content={"success": True, "mensaje": "Venta registrada con éxito", "id_venta": id_venta})
        except ValueError as e:
            return JSONResponse(status_code=400, content={"success": False, "error": str(e)})
        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Ocurrió un error al registrar la venta."})
        
    def ver_comprobante(self, id_venta: int, request: Request) -> HTMLResponse:
        try:
            venta, cliente, detalles = self.crud.obtener_comprobante(id_venta)
            return templates.TemplateResponse("comprobante.html", {
                "request": request,
                "venta": venta,
                "cliente": cliente,
                "detalles": detalles
            })
        except ValueError as e:
            return HTMLResponse(content=str(e), status_code=404)
    
    