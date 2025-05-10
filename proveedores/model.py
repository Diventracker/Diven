from sqlalchemy import Column, Integer, String, Date, DECIMAL, Text, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship

class Proveedor(Base):
    __tablename__ = "Proveedor"

    id_proveedor = Column(Integer, primary_key=True, index=True)
    nit = Column(String(20), nullable=False)
    nombre_proveedor = Column(String(100), nullable=False)
    representante_ventas = Column(String(100), nullable=False)
    telefono_representante_ventas = Column(String(20), nullable=False)
    direccion_proveedor = Column(String(255), nullable=False)

    productos = relationship("Producto", back_populates="proveedor")