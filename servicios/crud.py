import os
import shutil
from datetime import date, timedelta
from fastapi import UploadFile

from servicios.model import (
    DetalleServicio,
    ImagenServicio,
    ServicioTecnico,
)
from garantias.model import GarantiaServicio  # <- aquí está la clase correcta
from servicios.schema import ServicioRevisionSchema, ServicioUpdate


class ServicioCRUD:
    def __init__(self, repo):
        self.repo = repo

    def obtener_todos(self):
        return self.repo.listar_todos()

    def crear(self, datos, usuario_id: int) -> ServicioTecnico:
        nuevo = ServicioTecnico(
            id_cliente=datos.cliente_id,
            id_usuario=usuario_id,
            modelo_equipo=datos.modelo_equipo,
            tipo_equipo=datos.tipo_equipo,
            tipo_servicio=datos.tipo_servicio,
            precio_servicio=datos.precio_servicio,
            descripcion_problema=datos.descripcion,
        )
        self.repo.db.add(nuevo)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo)
        return nuevo

    # --- LISTADOS / FILTROS -------------------------------------------------

    def filtrar_finalizados(self):
        return self.repo.listar_finalizados()

    # --- IMÁGENES -----------------------------------------------------------

    def guardar_imagenes(self, imagenes: list[UploadFile], servicio_id: int) -> None:
        from utils.uploads import guardar_imagen  # evitar ciclos

        for img in imagenes:
            ruta = guardar_imagen(img, servicio_id)
            imagen = ImagenServicio(id_servicio=servicio_id, ruta_archivo=ruta)
            self.repo.db.add(imagen)

        self.repo.db.commit()

    # --- ELIMINAR SERVICIO (y carpeta de imágenes) --------------------------

    def eliminar(self, id_servicio: int):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        # Eliminar carpeta de imágenes (si existe)
        ruta_carpeta = os.path.join("static", "img", "servicios", str(id_servicio))
        if os.path.exists(ruta_carpeta):
            shutil.rmtree(ruta_carpeta)

        # Eliminar el registro del servicio SIEMPRE
        self.repo.db.delete(servicio)
        self.repo.db.commit()

    # --- REVISIÓN -----------------------------------------------------------

    def registrar_revision(self, data: ServicioRevisionSchema, usuario_id: int):
        servicio = self.repo.obtener_por_id(data.id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        # Actualizar datos principales
        servicio.meses_garantia = data.meses_garantia
        servicio.descripcion_trabajo = data.descripcion
        servicio.estado_servicio = "En Revisión"
        self.repo.db.add(servicio)

        # Insertar detalles adicionales
        for detalle in data.detalles:
            if detalle.valor_adicional > 0 and detalle.motivo.strip():
                nuevo = DetalleServicio(
                    id_servicio=data.id_servicio,
                    id_usuario=usuario_id,
                    valor_adicional=detalle.valor_adicional,
                    motivo=detalle.motivo,
                )
                self.repo.db.add(nuevo)

        self.repo.db.commit()

    # --- ACTUALIZAR ---------------------------------------------------------

    def actualizar(self, id_servicio: int, datos: ServicioUpdate, usuario_id: int):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        # Actualiza campos básicos
        servicio.modelo_equipo = datos.modelo_equipo
        servicio.tipo_equipo = datos.tipo_equipo
        servicio.tipo_servicio = datos.tipo_servicio
        servicio.descripcion_problema = datos.descripcion
        servicio.precio_servicio = datos.precio_servicio

        if datos.descripcion_trabajo is not None:
            servicio.descripcion_trabajo = datos.descripcion_trabajo
        if datos.meses_garantia is not None:
            servicio.meses_garantia = datos.meses_garantia

        # Reemplaza detalles si vienen
        if datos.detalles:
            self.repo.eliminar_detalles(id_servicio)
            for d in datos.detalles:
                detalle = DetalleServicio(
                    id_servicio=id_servicio,
                    id_usuario=usuario_id,
                    valor_adicional=d.valor_adicional,
                    motivo=d.motivo,
                )
                self.repo.db.add(detalle)

        self.repo.db.commit()

    # --- CONSULTAS PARA VISTAS ---------------------------------------------

    def obtener_servicios_en_revision(self):
        return self.repo.obtener_en_revision()

    def obtener_comprobante_data(self, id_servicio: int):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")
        detalles = self.repo.obtener_detalles(id_servicio)
        return servicio, servicio.cliente, detalles

    def obtener_detalles_servicio(self, id_servicio: int):
        return self.repo.obtener_detalles(id_servicio)

    # --- APROBAR / RECHAZAR / FINALIZAR (CREA GARANTÍA) --------------------

    def cambiar_estado(self, id_servicio: int, nuevo_estado: str, motivo: str | None = None):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        estado_actual = (servicio.estado_servicio or "").lower()
        nuevo_estado = (nuevo_estado or "").lower()

        if estado_actual == "finalizado":
            raise ValueError("El servicio ya está finalizado y no se puede modificar")

        if nuevo_estado not in {"finalizado", "rechazado"}:
            raise ValueError("Estado no válido")

        if nuevo_estado == "rechazado" and not motivo:
            raise ValueError("Debe proporcionar un motivo para el rechazo")

        # Actualiza estado
        servicio.estado_servicio = nuevo_estado.capitalize()

        # Si finaliza: setea fecha_entrega y crea garantía (idempotente)
        if nuevo_estado == "finalizado":
            if not servicio.fecha_entrega:
                servicio.fecha_entrega = date.today()

            # ¿Ya existe una garantía para este servicio?
            existente = (
                self.repo.db.query(GarantiaServicio)
                .filter(GarantiaServicio.id_servicio == id_servicio)
                .first()
            )

            if not existente:
                # Si meses_garantia viene 0/None, asumimos al menos 1 mes
                meses = servicio.meses_garantia if servicio.meses_garantia and servicio.meses_garantia > 0 else 1
                dias = meses * 30
                g = GarantiaServicio(
                    id_servicio=id_servicio,
                    fecha_inicio=date.today(),
                    fecha_fin=date.today() + timedelta(days=dias),
                    estado="activa",
                )
                self.repo.db.add(g)

        self.repo.db.commit()
        self.repo.db.refresh(servicio)
        return servicio

    # --- DASHBOARD / TOTALES / IMÁGENES ------------------------------------

    def obtener_conteo_por_equipo(self):
        return self.repo.contar_por_tipo_equipo()

    def obtener_datos_para_totales(self, id_servicio: int):
        return self.repo.obtener_datos_base(id_servicio)

    def obtener_imagenes_por_servicio(self, id_servicio: int):
        return self.repo.listar_imagenes_por_servicio(id_servicio)

    def obtener_imagen_por_id(self, id_imagen: int):
        return self.repo.buscar_imagen_por_id(id_imagen)

    def eliminar_imagen(self, id_imagen: int):
        imagen = self.repo.buscar_imagen_por_id(id_imagen)
        if not imagen:
            return False, "Imagen no encontrada"

        # Eliminar archivo físico
        ruta_fisica = os.path.join(os.getcwd(), imagen.ruta_archivo.lstrip("/"))
        if os.path.exists(ruta_fisica):
            os.remove(ruta_fisica)

        # Eliminar de la BD
        self.repo.db.delete(imagen)
        self.repo.db.commit()

        return True, "Imagen eliminada correctamente"
    
    #guardar total en la base de datos
    def guardar_total(self, id_servicio: int, total: int):
            servicio = self.repo.obtener_por_id(id_servicio)
            if not servicio:
                raise ValueError("Servicio no encontrado")

            nuevo_estado = "facturado"

            servicio.estado_servicio = nuevo_estado
            servicio.total_servicio = total
            self.repo.db.commit()

            return servicio