from sqlalchemy import Column, Integer, String, TIMESTAMP
from database.database import Base  # Asegúrate de importar Base de tu configuración
from sqlalchemy.orm import relationship
from datetime import datetime

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String(100), nullable=False)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento= Column(String(20), unique=True, nullable=False)
    direccion_cliente = Column(String(255), nullable=False)
    telefono_cliente = Column(String(20), nullable=False)
    email_cliente = Column(String(100), unique=True, nullable=False)
    fecha_registro = Column (TIMESTAMP, nullable=False, default=datetime.now)



    ventas = relationship("Venta", back_populates="cliente")    