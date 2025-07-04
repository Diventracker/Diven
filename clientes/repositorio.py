from sqlalchemy import desc
from sqlalchemy.orm import Session
from clientes.model import Cliente

class ClienteRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_documento(self, documento: str):
        return self.db.query(Cliente).filter(Cliente.numero_documento == documento).first()

    def obtener_por_correo(self, correo: str):
        return self.db.query(Cliente).filter(Cliente.email_cliente == correo).first()
    
    def obtener_por_id(self, id_cliente: int):
        return self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    
    def obtener_todos(self) -> list[Cliente]:
        return self.db.query(Cliente).order_by(desc(Cliente.id_cliente)).all()

    def buscar_por_nombre_o_documento(self, texto: str) -> list[Cliente]:
        return self.db.query(Cliente).filter(
            (Cliente.nombre_cliente.ilike(f"%{texto}%")) |
            (Cliente.numero_documento.ilike(f"%{texto}%"))
        ).all()
