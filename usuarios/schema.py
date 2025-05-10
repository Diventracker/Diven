from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Form
from typing import Optional


class UsuarioCreateSchema(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    clave: Optional[str] = None  # Ahora es opcional
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
        clave: Optional[str] = Form(None),
        rol: Optional[str] = Form(None),
    ):
        return cls(
            nombre_usuario=nombre_usuario,
            correo=correo,
            clave=clave,
            rol=rol
        )

class UsuarioUpdateSchema(BaseModel):
    id_usuario: int
    nombre_usuario: Optional[str] = None
    correo: Optional[EmailStr] = None    
    rol: Optional[str] = None

    @field_validator("nombre_usuario", mode="before")
    @classmethod
    def validar_nombre(cls, v):
        if v is not None and any(char.isdigit() for char in v):
            raise ValueError("El nombre de usuario no debe contener números.")
        return v

    @classmethod
    def as_form(
        cls,
        id_usuario: int = Form(...),
        nombre_usuario: Optional[str] = Form(None),
        correo: Optional[EmailStr] = Form(None),        
        rol: Optional[str] = Form(None),
    ):
        return cls(
            id_usuario=id_usuario,
            nombre_usuario=nombre_usuario,
            correo=correo,            
            rol=rol,
        )


    class UsuarioOutSchema(BaseModel):
        id_usuario: int
        nombre_usuario: str
        correo: EmailStr
        rol: Optional[str] = None

        class Config:
            orm_mode = True  # Permite que Pydantic convierta objetos ORM a dicts automáticamente