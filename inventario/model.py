from sqlalchemy import Column, Integer, String, Date, DECIMAL, Text, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship

class Producto(Base):
    __tablename__ = "Producto"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre_producto = Column(String(100), nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    precio_venta = Column(DECIMAL(10, 2), nullable=True)  
    stock = Column(Integer, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("Proveedor.id_proveedor"), nullable=False)
    fecha_inicio_garantia = Column(Date, nullable=True)
    fecha_expiracion_garantia = Column(Date, nullable=True)
    fecha_compra = Column(Date, nullable=False)

    proveedor = relationship("Proveedor", back_populates="productos")
    # En Producto
    # (Si quieres que Producto conozca sus detalles de venta)
    detalles_venta = relationship("DetalleVenta", back_populates="producto")