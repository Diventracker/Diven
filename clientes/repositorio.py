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
