from sqlalchemy import desc
from proveedores.model import Proveedor


class ProveedorRepositorio:
    def __init__(self, db):
        self.db = db

    def listar_todos(self) -> list[Proveedor]:
        return self.db.query(Proveedor).order_by(desc(Proveedor.id_proveedor)).all()


    def obtener_por_id(self, proveedor_id: int) -> Proveedor | None:
        return self.db.query(Proveedor).filter_by(id_proveedor=proveedor_id).first()

    def obtener_por_nit(self, nit: str) -> Proveedor | None:
        return self.db.query(Proveedor).filter_by(nit=nit).first()
    
    def filtrar_por_nombre_o_nit(self, search: str):
        return self.db.query(Proveedor).filter(
            (Proveedor.nombre_proveedor.ilike(f"%{search}%")) |
            (Proveedor.nit.ilike(f"%{search}%"))
        ).all()

