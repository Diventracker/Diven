from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime, timezone

class Venta(Base):
    __tablename__ = 'venta'

    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('Cliente.id_cliente'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('Usuario.id_usuario'), nullable=False)
    fecha_venta = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    total_venta = Column(DECIMAL(10, 2), nullable=False)

    cliente = relationship("Cliente", back_populates="ventas")
    usuario = relationship("Usuario", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey('venta.id_venta'), nullable=False)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")