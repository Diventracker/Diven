from servicios.model import DetalleServicio, ServicioTecnico
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
            descripcion_problema=datos.descripcion
        )

        self.repo.db.add(nuevo)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo)
        return nuevo

    def eliminar(self, id_servicio: int):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        self.repo.db.delete(servicio)
        self.repo.db.commit()

    #Funcion que actualiza el estado del servicio a en revision
    def registrar_revision(self, data: ServicioRevisionSchema, usuario_id: int):
        servicio = self.repo.obtener_por_id(data.id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        # Actualizar datos
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
                    motivo=detalle.motivo
                )
                self.repo.db.add(nuevo)

        self.repo.db.commit()

    def actualizar(self, id_servicio: int, datos: ServicioUpdate, usuario_id: int):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        # Actualiza campos básicos
        servicio.modelo_equipo = datos.modelo_equipo
        servicio.tipo_equipo = datos.tipo_equipo
        servicio.tipo_servicio = datos.tipo_servicio
        servicio.descripcion_problema = datos.descripcion
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
                    motivo=d.motivo
                )
                self.repo.db.add(detalle)

        self.repo.db.commit()

    #Retorna los servicioos con el estado en revision
    def obtener_servicios_en_revision(self):
        return self.repo.obtener_en_revision()
    
    #Obtiene la info del comprobante.html
    def obtener_comprobante_data(self, id_servicio: int):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        detalles = self.repo.obtener_detalles(id_servicio)
        return servicio, servicio.cliente, detalles
    
    #Para el modal actualizar
    def obtener_detalles_servicio(self, id_servicio: int):
        return self.repo.obtener_detalles(id_servicio)
    
    #Aprobar / rechazar el servicio
    def cambiar_estado(self, id_servicio: int, nuevo_estado: str, motivo: str | None = None):
        servicio = self.repo.obtener_por_id(id_servicio)
        if not servicio:
            raise ValueError("Servicio no encontrado")

        estado_actual = servicio.estado_servicio.lower()
        nuevo_estado = nuevo_estado.lower()

        if estado_actual == "finalizado":
            raise ValueError("El servicio ya está finalizado y no se puede modificar")

        if nuevo_estado not in {"finalizado", "rechazado"}:
            raise ValueError("Estado no válido")

        if nuevo_estado == "rechazado" and not motivo:
            raise ValueError("Debe proporcionar un motivo para el rechazo")

        servicio.estado_servicio = nuevo_estado.capitalize()
        self.repo.db.commit()

        return servicio