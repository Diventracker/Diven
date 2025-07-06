import json
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from login.sesiones import session_manager

# Rutas completamente libres (coincidencia exacta)
rutas_libres_exacto = ["/", "/login", "/logout", "/cambiar-clave"]

# Rutas con prefijo que deben permitirse
rutas_libres_prefijo = ["/static", "/api", "/auth"]

async def middleware_general(request: Request, call_next):
    path = request.url.path

    # 1. Permitir rutas públicas (libres)
    if path in rutas_libres_exacto or any(path.startswith(pref) for pref in rutas_libres_prefijo):
        return await call_next(request)

    # 2. Excepción para /auth/cambiar-clave si trae token y correo (para recuperación)
    if path == "/use/cambiar-clave" and request.method == "POST":
        try:
            body = await request.body()
            data = json.loads(body)
            if "token" in data and "correo" in data:
                return await call_next(request)
        except json.JSONDecodeError:
            pass  # sigue al control normal

    # 3. Validar sesión
    session_id = request.cookies.get("session_id")
    datos = session_manager.obtener_sesion(session_id)

    if not datos:
        return RedirectResponse(url="/login?error=2", status_code=303)

    request.state.usuario = datos

    # 4. Continuar y evitar caché en todas las respuestas
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
