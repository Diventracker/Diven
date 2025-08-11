import os
from datetime import datetime
from fastapi import UploadFile

async def guardar_imagen(imagen: UploadFile, carpeta: str = "static/img/productos") -> str:
        """
        Guarda una imagen en la carpeta especificada y devuelve la ruta relativa.
        """
        if not imagen:
            return None

        os.makedirs(carpeta, exist_ok=True)

        nombre_unico = f"{datetime.now().timestamp()}_{imagen.filename}"
        ruta_fisica = os.path.join(carpeta, nombre_unico)

        contenido = await imagen.read()
        with open(ruta_fisica, "wb") as f:
            f.write(contenido)

        # Ruta relativa para guardar en DB
        return f"/static/img/productos/{nombre_unico}"