from sqlalchemy import Column, Integer, String, Date, DECIMAL, Text, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Date, ForeignKey
from database.database import Base

class Garantia(Base):
    __tablename__ = "garantia_servicio"

    id_garantia = Column(Integer, primary_key=True, index=True)
    id_servicio = Column(Integer, ForeignKey("servicio_tecnico.id_servicio"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    # Relación
    servicio = relationship("ServicioTecnico", back_populates="garantias")
