from sqlalchemy import Column, Integer, String
from database.database import Base  # Asegúrate de importar Base de tu configuración
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    direccion_cliente = Column(String(255), nullable=False)
    telefono_cliente = Column(String(20), nullable=False)
    email_cliente = Column(String(100), unique=True, nullable=False)

    ventas = relationship("Venta", back_populates="cliente")