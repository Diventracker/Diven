import os
import shutil
from datetime import datetime
from fastapi import UploadFile

VOLUMEN_PRODUCTOS = "/data/img/productos"
STATIC_PRODUCTOS = "static/img/productos"

async def guardar_imagen(imagen: UploadFile, carpeta_volumen: str = VOLUMEN_PRODUCTOS, carpeta_static: str = STATIC_PRODUCTOS) -> str:
    """
    Guarda una imagen en la carpeta del volumen persistente y copia a static.
    Devuelve la ruta relativa para usar en la base de datos.
    """
    if not imagen:
        return None

    # Asegurar que existan las carpetas
    os.makedirs(carpeta_volumen, exist_ok=True)
    os.makedirs(carpeta_static, exist_ok=True)

    # Nombre único para evitar colisiones
    nombre_unico = f"{datetime.now().timestamp()}_{imagen.filename}"
    ruta_volumen = os.path.join(carpeta_volumen, nombre_unico)
    ruta_static = os.path.join(carpeta_static, nombre_unico)

    # Guardar en volumen persistente
    contenido = await imagen.read()
    with open(ruta_volumen, "wb") as f:
        f.write(contenido)

    # Copiar a static para servirlo
    shutil.copy2(ruta_volumen, ruta_static)

    # Devolver ruta relativa para usar en la UI/DB
    return f"/static/img/productos/{nombre_unico}"
