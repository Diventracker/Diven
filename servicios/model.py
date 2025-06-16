from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER


class ServicioTecnico(Base):
    __tablename__= "servicio_tecnico"

    id_servicio = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    tipo_equipo = Column(String(50), nullable=False)
    #se elimino la columna de marca
    modelo_equipo = Column(String(50), nullable=False)
    descripcion_problema = Column(String, nullable=False)
    descripcion_trabajo = Column(String, nullable=True)
    fecha_recepcion = Column(TIMESTAMP, nullable=False, default=datetime.now)
    fecha_entrega = Column(Date, nullable=False)
    estado_servicio = Column(String(50), nullable=False, default="En Progreso")
    meses_garantia = Column(Integer, nullable=True, default=0)
    tipo_servicio = Column(String(50), nullable=False)
    precio_servicio = Column(INTEGER(unsigned=True), nullable=False) 

    # Relaciones opcionales si las necesitas
    cliente = relationship("Cliente")
    usuario = relationship("Usuario")
    garantias = relationship("Garantia", back_populates="servicio", cascade="all, delete-orphan")
    detalles = relationship('DetalleServicio', back_populates='servicio', cascade="all, delete-orphan")

class DetalleServicio(Base):
    __tablename__ = 'detalle_servicio'

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_servicio = Column(Integer, ForeignKey('servicio_tecnico.id_servicio', ondelete='CASCADE'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', ondelete='SET NULL'), nullable=True)
    valor_adicional = Column(Integer, nullable=False, default=0)
    motivo = Column(String(255), nullable=False)

    # Relaciones (opcional si deseas acceso a los objetos relacionados)
    servicio = relationship('ServicioTecnico', back_populates='detalles', passive_deletes=True)
    usuario = relationship('Usuario', back_populates='detalles_realizados', passive_deletes=True)