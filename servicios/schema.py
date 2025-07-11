from pydantic import BaseModel, Field
from fastapi import Form
from typing import List, Optional

class ServicioCreate(BaseModel):
    cliente_id: int
    modelo_equipo: str = Field(..., max_length=20)
    tipo_equipo: str
    tipo_servicio: str
    precio_servicio: int
    descripcion: str = Field(..., max_length=100)

    @classmethod
    def as_form(
        cls,
        cliente_id: int = Form(...),
        modelo_equipo: str = Form(...),
        tipo_equipo: str = Form(...),
        tipo_servicio: str = Form(...),
        precio_servicio: int = Form(...),
        descripcion: str = Form(...),
    ):
        return cls(
            cliente_id=cliente_id,
            modelo_equipo=modelo_equipo,
            tipo_equipo=tipo_equipo,
            tipo_servicio=tipo_servicio,
            precio_servicio=precio_servicio,
            descripcion=descripcion
        )

class DetalleGasto(BaseModel):
    valor_adicional: int
    motivo: str

class ServicioRevisionSchema(BaseModel):
    id_servicio: int
    meses_garantia: int
    descripcion: str
    detalles: List[DetalleGasto] = []

    @classmethod
    def as_form(
        cls,
        id_servicio: int = Form(...),
        meses_garantia: int = Form(...),
        descripcion: str = Form(...),
        detalles: str = Form(None)  # puede venir None
    ):
        import json
        detalles_list = json.loads(detalles) if detalles else []
        return cls(
            id_servicio=id_servicio,
            meses_garantia=meses_garantia,
            descripcion=descripcion,
            detalles=[DetalleGasto(**d) for d in detalles_list]
        )
    
class ServicioUpdate(BaseModel):
    modelo_equipo: str
    tipo_equipo: str
    tipo_servicio: str
    descripcion: str
    descripcion_trabajo: Optional[str] = None
    meses_garantia: Optional[int] = None
    detalles: Optional[List[DetalleGasto]] = []

class EstadoServicioInput(BaseModel):
    nuevo_estado: str
    motivo: str | None = None  # Solo requerido si el estado es "rechazado"