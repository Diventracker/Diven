from proveedores.model import Proveedor
from proveedores.schema import ProveedorSchema 

class ProveedorCRUD:
    def __init__(self, repo):
        self.repo = repo

    def listar_todos(self) -> list[Proveedor]:
        return self.repo.listar_todos()


    def crear(self, datos):
        if self.repo.obtener_por_nit(datos.nit):
            raise ValueError("Ya existe un proveedor con ese NIT.")

        nuevo = Proveedor(**datos.model_dump())
        self.repo.db.add(nuevo)
        self.repo.db.commit()
        self.repo.db.refresh(nuevo)
        return nuevo
    
    def editar(self, proveedor_id: int, datos: ProveedorSchema) -> Proveedor:
        proveedor = self.repo.obtener_por_id(proveedor_id)
        if not proveedor:
            raise ValueError("Proveedor no encontrado")

        existente = self.repo.obtener_por_nit(datos.nit)
        if existente and existente.id_proveedor != proveedor_id:
            raise ValueError("Ya existe un proveedor con ese NIT")

        for campo, valor in datos.model_dump(exclude_none=True).items():
            setattr(proveedor, campo, valor)

        self.repo.db.commit()
        self.repo.db.refresh(proveedor)
        return proveedor
    
    def eliminar(self, proveedor_id: int):
        proveedor = self.repo.obtener_por_id(proveedor_id)
        if not proveedor:
            raise ValueError("Proveedor no encontrado")

        self.repo.db.delete(proveedor)
        self.repo.db.commit()

    def filtrar(self, search: str):
        return self.repo.filtrar_por_nombre_o_nit(search)


