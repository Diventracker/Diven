from sqlalchemy import Column, DateTime, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    telefono_usuario = Column(String(20), nullable=False)
    clave = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)

    token_recuperacion = Column(String(6), nullable=True)  # Token de 6 dígitos
    token_expiracion = Column(DateTime, nullable=True)    # Fecha de expiración del token

    ventas = relationship("Venta", back_populates="usuario")
    detalles_realizados = relationship('DetalleServicio', back_populates='usuario', passive_deletes=True)
