from typing import Optional
from pydantic import BaseModel, field_validator
from fastapi import Form

class ProveedorSchema(BaseModel):
    id_proveedor: Optional[int] = None  # Opcional para creación
    nit: str
    nombre_proveedor: str
    representante_ventas: str
    telefono_representante_ventas: str
    direccion_proveedor: str

    @field_validator("nombre_proveedor", "representante_ventas", mode="before")
    @classmethod
    def validar_nombre(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("Este campo no debe contener números")
        return v

    @field_validator("telefono_representante_ventas", mode="before")
    @classmethod
    def validar_telefono(cls, v):
        if not v.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        return v
    
    @field_validator("nit")
    @classmethod
    def sin_espacios_en_nit(cls, v):
        if " " in v:
            raise ValueError("El NIT no debe contener espacios")
        return v

    @classmethod
    def as_form(
        cls,
        id_proveedor: Optional[int] = Form(None),  # Ahora es opcional
        nit: str = Form(...),
        nombre_proveedor: str = Form(...),
        representante_ventas: str = Form(...),
        telefono_representante_ventas: str = Form(...),
        direccion_proveedor: str = Form(...),
    ):
        return cls(
            id_proveedor=id_proveedor,
            nit=nit,
            nombre_proveedor=nombre_proveedor,
            representante_ventas=representante_ventas,
            telefono_representante_ventas=telefono_representante_ventas,
            direccion_proveedor=direccion_proveedor,
        )

    class Config:
        orm_mode = True
