from pydantic import BaseModel, EmailStr, constr, field_validator
from fastapi import Form
from typing import Optional


class UsuarioCreateSchema(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    telefono_usuario: str
    rol: Optional[str] = None

    @field_validator("nombre_usuario", mode="before")
    @classmethod
    def validar_nombre(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("Nombre")
        return v

    @classmethod
    def as_form(
        cls,
        nombre_usuario: str = Form(...),
        correo: EmailStr = Form(...),
        telefono_usuario: str = Form(...),
        rol: Optional[str] = Form(None),
    ):
        return cls(
            nombre_usuario=nombre_usuario,
            correo=correo,
            telefono_usuario=telefono_usuario,
            rol=rol,
        )

class SolicitudRecuperacion(BaseModel):
    correo: EmailStr


class TokenValidacionSchema(BaseModel):
    correo: EmailStr
    token: constr(min_length=6, max_length=6)  # type: ignore # Token de 6 dígitos

    class Config:
        schema_extra = {
            "example": {
                "correo": "usuario@ejemplo.com",
                "token": "123456"
            }
        }

class CambiarClaveSchema(BaseModel):
    correo: Optional[EmailStr] = None
    token: Optional[constr(min_length=6, max_length=6)] = None # type: ignore
    clave_actual: Optional[str] = None
    nueva_clave: str
    confirmar_clave: str 

    @staticmethod
    def validar_campos(schema):
        if schema.nueva_clave != schema.confirmar_clave:
            raise ValueError("Las contraseñas no coinciden")

        if not schema.token and not schema.clave_actual:
            raise ValueError("Debe proporcionar el token o la clave actual")

        return schema