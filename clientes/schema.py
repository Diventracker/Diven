from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClienteBase(BaseModel):
    nombre_cliente: str
    tipo_documento : str 
    numero_documento : str
    direccion_cliente: str
    telefono_cliente: str
    email_cliente: EmailStr
    fecha_registro: datetime

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id_cliente: int

    class Config:
        orm_mode = True
