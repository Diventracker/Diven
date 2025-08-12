from uuid import uuid4
from typing import Optional

class SessionManager:
    def __init__(self):
        self._sesiones = {}

    def crear_sesion(self, datos_usuario: dict) -> str:
        session_id = str(uuid4())
        self._sesiones[session_id] = datos_usuario
        print("✅ Sesión guardada:", session_id, datos_usuario) #Para la session 
        return session_id

    def obtener_sesion(self, session_id: str) -> Optional[dict]:
        return self._sesiones.get(session_id)

    def eliminar_sesion(self, session_id: str):
        self._sesiones.pop(session_id, None)


# Esta es la instancia global que todos van a importar y usar
session_manager = SessionManager()
