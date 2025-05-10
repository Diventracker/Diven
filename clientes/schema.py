from pydantic import BaseModel, EmailStr

class ClienteBase(BaseModel):
    nombre_cliente: str
    cedula: str
    direccion_cliente: str
    telefono_cliente: str
    email_cliente: EmailStr

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id_cliente: int

    class Config:
        orm_mode = True
