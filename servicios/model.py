from sqlalchemy import Column, Integer, String, Date, DECIMAL, Text, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from usuarios import model
from clientes import model  # Asegúrate de importar los modelos Cliente y Usuario



class ServicioTecnico(Base):
    __tablename__= "Servicio_Tecnico"

    id_servicio = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"))
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"))
    tipo_equipo = Column(String(50), nullable=False)
    marca_equipo = Column(String(50), nullable=False)
    modelo_equipo = Column(String(50), nullable=False)
    descripcion_problema = Column(String, nullable=False)
    fecha_recepcion = Column(Date, nullable=False)
    fecha_entrega_estimada = Column(Date, nullable=False)
    estado_servicio = Column(String(50), nullable=False)

    # Relaciones opcionales si las necesitas
    cliente = relationship("Cliente")
    usuario = relationship("Usuario")