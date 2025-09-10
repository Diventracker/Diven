import os
import shutil
from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile

VOLUMEN_SERVICIOS = "/data/img/servicios"
STATIC_SERVICIOS = "static/img/servicios"

def guardar_imagen(file: UploadFile, servicio_id: int,
                   carpeta_volumen: str = VOLUMEN_SERVICIOS,
                   carpeta_static: str = STATIC_SERVICIOS) -> str:
    # Extrae extensión de forma segura
    ext = Path(file.filename).suffix.lower().strip(".")
    if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
        raise ValueError("Tipo de archivo no soportado")

    # Genera nombre único
    nombre_archivo = f"{uuid4().hex}.{ext}"

    # Rutas completas
    ruta_carpeta_volumen = Path(carpeta_volumen) / str(servicio_id)
    ruta_carpeta_static = Path(carpeta_static) / str(servicio_id)
    ruta_carpeta_volumen.mkdir(parents=True, exist_ok=True)
    ruta_carpeta_static.mkdir(parents=True, exist_ok=True)

    ruta_final_volumen = ruta_carpeta_volumen / nombre_archivo
    ruta_final_static = ruta_carpeta_static / nombre_archivo

    # Guarda en volumen persistente
    with open(ruta_final_volumen, "wb") as f:
        f.write(file.file.read())

    # Copia a static para que FastAPI pueda servirlo
    shutil.copy2(ruta_final_volumen, ruta_final_static)

    # Retorna ruta relativa desde /static
    return f"/static/img/servicios/{servicio_id}/{nombre_archivo}"
