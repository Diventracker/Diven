from datetime import datetime
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Request, UploadFile
from servicios.schema import EstadoServicioInput, ServicioCreate, ServicioRevisionSchema, ServicioUpdate
from servicios.repositorio import ServicioRepositorio
from servicios.crud import ServicioCRUD

templates = Jinja2Templates(directory=["templates", "servicios/templates"])


class ServicioControlador:
    def __init__(self, db):
        self.crud = ServicioCRUD(ServicioRepositorio(db))
        self.db = db

    def vista_principal(self, request: Request):
        usuario = request.state.usuario
        return templates.TemplateResponse("servicios.html", {
            "request": request,
            "rol": usuario["rol"]
        })
    
    #Funcion manda todos los datos en json de los servicios
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
                "precio_servicio": s.precio_servicio,
                "fecha_recepcion": s.fecha_recepcion.strftime("%Y-%m-%d") if s.fecha_recepcion else None,
                "fecha_entrega": s.fecha_entrega.strftime("%Y-%m-%d") if s.fecha_entrega else None,
                "usuario": {
                    "nombre_usuario": s.usuario.nombre_usuario if s.usuario else None
                }
            }
            for s in servicios
        ]

        return JSONResponse(content=resultado)
    
    #controlador de la ruta del js que llama solo los estados con finalizado
    def obtener_finalizados(self):
        servicios = self.crud.filtrar_finalizados()
        
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
                "precio_servicio": s.precio_servicio,
                "fecha_recepcion": s.fecha_recepcion.strftime("%Y-%m-%d") if s.fecha_recepcion else None,
                "fecha_entrega": s.fecha_entrega.strftime("%Y-%m-%d") if s.fecha_entrega else None,
                "usuario": {
                    "nombre_usuario": s.usuario.nombre_usuario if s.usuario else None
                }
            }
            for s in servicios
        ]
        
        return JSONResponse(content=resultado)

    #Funcion para registrar un nuevo servicio
    async def crear(self, request: Request, datos: ServicioCreate, imagenes: list[UploadFile]):
        try:
            usuario_id = int(request.state.usuario["usuario_id"])
            servicio = self.crud.crear(datos, usuario_id)

            if not imagenes or len(imagenes) == 0:
                return JSONResponse(status_code=400, content={"success": False, "error": "Debes subir al menos una imagen."})

            self.crud.guardar_imagenes(imagenes, servicio.id_servicio)

            return JSONResponse(content={"success": True, "mensaje": "Servicio creado correctamente", "servicio_id": servicio.id_servicio})

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"success": False, "error": "Error interno al crear servicio"}, status_code=500)

    #Funcion que elimina un servicio con todo y carpeta de imagenes
    def eliminar(self, id_servicio: int): 
        try:
            self.crud.eliminar(id_servicio)
            return JSONResponse(content={"success": True, "mensaje": "Servicio eliminado correctamente"})
        
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)
        
        except Exception:
            return JSONResponse(content={"success": False, "error": "Error al eliminar el servicio"}, status_code=500)
        
    #Controlador para mandar a revision servicio
    def registrar_revision(self, datos: ServicioRevisionSchema, usuario_id: int, imagenes: list[UploadFile]):
        try:
            self.crud.registrar_revision(datos, usuario_id)

            # Guardar imágenes si vienen
            if imagenes and len(imagenes) > 0:
                self.crud.guardar_imagenes(imagenes, datos.id_servicio)

            return JSONResponse(content={"success": True, "mensaje": "Servicio actualizado y detalles guardados."})
        
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)
        
        except Exception as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

    #Actualizar los servicios
    def actualizar(self, id_servicio: int, datos: ServicioUpdate, usuario_id: int, imagenes: list[UploadFile] = None):
        try:
            self.crud.actualizar(id_servicio, datos, usuario_id)

            # Guardar imágenes si vienen
            if imagenes and len(imagenes) > 0:
                self.crud.guardar_imagenes(imagenes, id_servicio)

            return JSONResponse(content={"success": True, "mensaje": "Servicio actualizado correctamente."})
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

    def listar_servicios_en_revision(self):
        servicios = self.crud.obtener_servicios_en_revision()
        resultado = [
            {
                "id": s.id_servicio,
                "cliente": s.cliente.nombre_cliente,
                "descripcion": f"{s.tipo_servicio} - {s.tipo_equipo}"
            }
            for s in servicios
        ]
        return JSONResponse(content=resultado)
    
    #Muestra el html del comprobante
    def ver_comprobante(self, id_servicio: int, request: Request):
        try:
            servicio, cliente, detalles = self.crud.obtener_comprobante_data(id_servicio)
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            return templates.TemplateResponse("comprobante.html", {
                "request": request,
                "servicio": servicio,
                "cliente": cliente,
                "detalles": detalles,
                "fecha_hoy": fecha_hoy
            })
        except ValueError:
            return HTMLResponse(content="Servicio no encontrado", status_code=404)
    
    #Consulta y calcula los datos de
    def calcular_totales(self, id_servicio: int):
        datos = self.crud.obtener_datos_para_totales(id_servicio)
        if not datos:
            return None

        precio_base = datos["precio_base"] or 0
        adicionales = datos["adicionales"] or 0
        subtotal = precio_base + adicionales
        iva = int(subtotal * 0.19)
        total = subtotal + iva

        return {
            "precio_base": precio_base,
            "adicionales": adicionales,
            "subtotal": subtotal,
            "iva": iva,
            "total": total
        }
        
    #Detalles para modal editar
    def obtener_detalles(self, id_servicio: int):
        detalles = self.crud.obtener_detalles_servicio(id_servicio)

        resultado = [
            {
                "id_detalle": d.id_detalle,
                "motivo": d.motivo,
                "valor_adicional": d.valor_adicional
            }
            for d in detalles
        ]
        return JSONResponse(content=resultado)
    
    #Aprobar/ rechazar el servicio
    def actualizar_estado(self, id_servicio: int, datos: EstadoServicioInput):
        try:
            servicio = self.crud.cambiar_estado(
                id_servicio=id_servicio,
                nuevo_estado=datos.nuevo_estado,
                motivo=datos.motivo
            )
            return JSONResponse(content={"success": True, "message": f"Servicio marcado como {servicio.estado_servicio}"})
        
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
        
    #graficas del dashboard
    def servicios_por_equipo(self):
        resultados = self.crud.obtener_conteo_por_equipo()
        return [{"equipo": r.equipo, "total": r.total} for r in resultados]

    #Funcion manda en json las imagenes de un servicio especifico
    def obtener_imagenes(self, id_servicio: int):
        imagenes = self.crud.obtener_imagenes_por_servicio(id_servicio)

        if not imagenes:
            return JSONResponse(content={"success": False, "error": "No se encontraron imágenes"}, status_code=404)

        resultado = [
            {
                "id_imagen": img.id_imagen,
                "ruta": img.ruta_archivo
            }
            for img in imagenes
        ]

        return JSONResponse(content=resultado)

    #Funcion para eliminar imagenes de un servicio 
    def eliminar_imagen(self, id_imagen: int):
        exito, mensaje = self.crud.eliminar_imagen(id_imagen)

        if not exito:
            return JSONResponse(content={"success": False, "error": mensaje}, status_code=404)

        return JSONResponse(content={"success": True, "message": mensaje})