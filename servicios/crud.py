from servicios.model import ServicioTecnico

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
