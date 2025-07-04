from clientes.schema import ClienteBase
from clientes.model import Cliente
from clientes.repositorio import ClienteRepositorio

class ClienteCRUD:
    def __init__(self, repo: ClienteRepositorio):
        self.repo = repo

    def listar(self) -> list[Cliente]:
        return self.repo.obtener_todos()


    def buscar_por_documento(self, documento: str) -> Cliente:
        cliente = self.repo.obtener_por_documento(documento)
        if not cliente:
            raise ValueError("Cliente no encontrado")
        return cliente


    def crear(self, datos: ClienteBase) -> Cliente:
        if self.repo.obtener_por_documento(datos.numero_documento):
            raise ValueError("Ya existe un cliente con ese documento.")
        if self.repo.obtener_por_correo(datos.email_cliente):
            raise ValueError("Ya existe un cliente con ese correo.")

        nuevo = Cliente(**datos.model_dump())
        self.repo.db.add(nuevo)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo)
        return nuevo

    def editar(self, id_cliente: int, datos: ClienteBase) -> Cliente:
        cliente = self.repo.obtener_por_id(id_cliente)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        # Validar duplicados solo si se modifican
        otro = self.repo.obtener_por_documento(datos.numero_documento)
        if otro and otro.id_cliente != id_cliente:
            raise ValueError("Otro cliente ya tiene ese documento")

        otro_correo = self.repo.obtener_por_correo(datos.email_cliente)
        if otro_correo and otro_correo.id_cliente != id_cliente:
            raise ValueError("Otro cliente ya tiene ese correo")

        cliente.nombre_cliente = datos.nombre_cliente
        cliente.tipo_documento = datos.tipo_documento
        cliente.numero_documento = datos.numero_documento
        cliente.telefono_cliente = datos.telefono_cliente
        cliente.direccion_cliente = datos.direccion_cliente
        cliente.email_cliente = datos.email_cliente

        self.repo.db.commit()
        return
    
    def eliminar(self, id_cliente: int):
        cliente = self.repo.obtener_por_id(id_cliente)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        self.repo.db.delete(cliente)
        self.repo.db.commit()

    def filtrar_por_texto(self, texto: str):
        return self.repo.buscar_por_nombre_o_documento(texto)
