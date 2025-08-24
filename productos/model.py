from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Date, Text, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre_producto = Column(String(100), nullable=False)
    modelo = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=False)
    precio = Column(INTEGER(unsigned=True), nullable=False) 
    precio_venta = Column(INTEGER(unsigned=True), nullable=True) 
    stock = Column(Integer, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id_proveedor"), nullable=False)
    meses_garantia = Column(Integer, nullable=True)
    fecha_compra = Column(TIMESTAMP, nullable=False, default=datetime.now)
    imagen = Column(String(255), nullable=True)

    proveedor = relationship("Proveedor", back_populates="productos")
    # En Producto
    # (Si quieres que Producto conozca sus detalles de venta)
    detalles_venta = relationship("DetalleVenta", back_populates="producto")