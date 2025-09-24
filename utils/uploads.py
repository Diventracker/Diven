import os
from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile

# Detectar si existe el volumen en /data (Railway)
EN_HOST = Path("/data").exists()

# Definir rutas base
BASE_PATH = Path("/data") if EN_HOST else Path("static")


def guardar_imagen(file: UploadFile, servicio_id: int, carpeta: str = "img/servicios") -> str:
    # Validar extensión
    ext = Path(file.filename).suffix.lower().strip(".")
    if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
        raise ValueError("Tipo de archivo no soportado")

    # Generar nombre único
    nombre_archivo = f"{uuid4().hex}.{ext}"

    # Carpeta física
    ruta_carpeta = BASE_PATH / carpeta / str(servicio_id)
    ruta_carpeta.mkdir(parents=True, exist_ok=True)

    # Ruta final donde se guarda
    ruta_final = ruta_carpeta / nombre_archivo
    with open(ruta_final, "wb") as f:
        f.write(file.file.read())

    # Devolver URL accesible según entorno
    if EN_HOST:
        # En Railway servimos desde /media
        return f"/media/{carpeta}/{servicio_id}/{nombre_archivo}"
    else:
        # En local usamos /static
        return f"/static/{carpeta}/{servicio_id}/{nombre_archivo}"
