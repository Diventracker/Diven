from sqlalchemy import Column, Integer, String
from database.database import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    clave = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
