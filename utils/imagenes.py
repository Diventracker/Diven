import os
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile

# Detectar si estamos en Railway (con /data montado) o en local
EN_HOST = Path("/data").exists()

# Base según entorno
BASE_PATH = Path("/data") if EN_HOST else Path("static")


async def guardar_imagen(imagen: UploadFile, carpeta: str = "img/productos") -> str:
    if not imagen:
        return None

    # Crear carpeta si no existe
    ruta_carpeta = BASE_PATH / carpeta
    ruta_carpeta.mkdir(parents=True, exist_ok=True)

    # Nombre único
    nombre_unico = f"{datetime.now().timestamp()}_{imagen.filename}"
    ruta_final = ruta_carpeta / nombre_unico

    # Guardar archivo
    contenido = await imagen.read()
    with open(ruta_final, "wb") as f:
        f.write(contenido)

    # Retornar la ruta accesible desde /static
    return f"/static/{carpeta}/{nombre_unico}"
