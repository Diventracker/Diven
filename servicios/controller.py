from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import Request
from servicios.schema import ServicioCreate
from servicios.repositorio import ServicioRepositorio
from servicios.crud import ServicioCRUD

templates = Jinja2Templates(directory=["templates", "servicios/templates"])


class ServicioControlador:
    def __init__(self, db):
        self.crud = ServicioCRUD(ServicioRepositorio(db))
        self.db = db

    def vista_principal(self, request: Request):
        rol = request.cookies.get("rol")
        return templates.TemplateResponse("servicios2.html", {
            "request": request,
            "rol": rol
        })
    
    def obtener_datos(self):
        servicios = self.crud.obtener_todos()

        resultado = [
            {
                "id_servicio": s.id_servicio,
                "estado_servicio": s.estado_servicio,
                "modelo_equipo": s.modelo_equipo,
                "tipo_equipo": s.tipo_equipo,
                "tipo_servicio": s.tipo_servicio,
                "descripcion_problema": s.descripcion_problema,
                "descripcion_trabajo": s.descripcion_trabajo,
                "meses_garantia": s.meses_garantia,
                "fecha_recepcion": s.fecha_recepcion.strftime("%Y-%m-%d") if s.fecha_recepcion else None,
                "fecha_entrega": s.fecha_entrega.strftime("%Y-%m-%d") if s.fecha_entrega else None,
                "usuario": {
                    "nombre_usuario": s.usuario.nombre_usuario if s.usuario else None
                }
            }
            for s in servicios
        ]

        return JSONResponse(content=resultado)


    def crear(self, request: Request, datos: ServicioCreate):
        try:
            usuario_id = request.cookies.get("usuario_id")
            if not usuario_id:
                raise ValueError("Usuario no autenticado")
            
            usuario_id = int(usuario_id)
            servicio = self.crud.crear(datos, usuario_id)

            return JSONResponse(content={"success": True, "message": "Servicio creado correctamente", "servicio_id": servicio.id_servicio})

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": "Error interno al crear servicio"}, status_code=500)

