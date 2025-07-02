from sqlalchemy import Column, Integer, String, TIMESTAMP
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Proveedor(Base):
    __tablename__ = "proveedor"

    id_proveedor = Column(Integer, primary_key=True, index=True)
    nit = Column(String(20), nullable=False)
    nombre_proveedor = Column(String(100), nullable=False)
    representante_ventas = Column(String(100), nullable=False)
    telefono_representante_ventas = Column(String(20), nullable=False)
    direccion_proveedor = Column(String(255), nullable=False)
    fecha_registro = Column (TIMESTAMP, nullable=False, default=datetime.now)

    productos = relationship("Producto", back_populates="proveedor")