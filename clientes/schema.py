from pydantic import BaseModel, EmailStr
from fastapi import Form

class ClienteBase(BaseModel):
    nombre_cliente: str
    tipo_documento : str 
    numero_documento : str
    direccion_cliente: str
    telefono_cliente: str
    email_cliente: EmailStr    

    @classmethod
    def as_form(
        cls,
        nombre_cliente: str = Form(...),
        tipo_documento: str = Form(...),
        numero_documento: str = Form(...),
        direccion_cliente: str = Form(...),
        telefono_cliente: str = Form(...),
        email_cliente: EmailStr = Form(...)
    ):
        return cls(
            nombre_cliente=nombre_cliente,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            direccion_cliente=direccion_cliente,
            telefono_cliente=telefono_cliente,
            email_cliente=email_cliente
        )


class ClienteRead(ClienteBase):
    id_cliente: int

    class Config:
        orm_mode = True
