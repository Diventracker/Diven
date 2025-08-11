import os
from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile

def guardar_imagen(file: UploadFile, servicio_id: int, carpeta_base: str = "static/img/servicios") -> str:
    # Extrae extensión de forma segura
    ext = Path(file.filename).suffix.lower().strip(".")
    if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
        raise ValueError("Tipo de archivo no soportado")

    # Genera nombre único
    nombre_archivo = f"{uuid4().hex}.{ext}"

    # Ruta completa usando pathlib
    ruta_carpeta = Path(carpeta_base) / str(servicio_id)
    ruta_carpeta.mkdir(parents=True, exist_ok=True)

    ruta_final = ruta_carpeta / nombre_archivo

    # Guarda el archivo
    with open(ruta_final, "wb") as f:
        f.write(file.file.read())

    # Retorna ruta relativa desde /static
    return f"/{ruta_final.as_posix()}"
