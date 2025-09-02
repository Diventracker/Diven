from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship  # <-- añade esto

class GarantiaServicio(Base):
    __tablename__ = "garantia_servicio"
    id_garantia = Column(Integer, primary_key=True, index=True)
    id_servicio = Column(Integer, ForeignKey("servicio_tecnico.id_servicio"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    # RESTAURA ESTA LÍNEA:
    servicio = relationship("ServicioTecnico", back_populates="garantias")

class GarantiaProducto(Base):
    __tablename__ = "garantia_producto"
    id_garantia   = Column(Integer, primary_key=True, autoincrement=True)
    id_producto   = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    id_venta      = Column(Integer, ForeignKey("venta.id_venta"), nullable=True)
    id_cliente    = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=True)
    id_garantia_origen = Column(Integer, ForeignKey("garantia_producto.id_garantia"), nullable=True)  # opcional
    fecha_inicio  = Column(Date, nullable=False)
    fecha_fin     = Column(Date, nullable=False)
    origen_garantia = Column(String(20), nullable=False)  # 'venta_cliente', 'renovacion', etc.
    estado = Column(String(10), nullable=False, default="activa")  # activa/vencida/anulada/renovada