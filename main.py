from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from homepage import routes as homepage_router
from login import routes as login_router
from layout import routes as access_router
from middleware import middleware_general
from usuarios import routes as usuarios_router
from clientes import routes as clientes_router
from servicios import routes as servicios_router
from productos import routes as producto_router
from proveedores import routes as proveedores_router
from ventas import routes as ventas_router
from garantias import routes as garantias_router
from dashboard import routes as dashboard_router
from informes import routes as informes_router
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback


app = FastAPI()


@app.exception_handler(Exception)
async def _debug_ex_handler(request: Request, exc: Exception):
    print("=== EXCEPTION on", request.method, request.url.path, "===")
    traceback.print_exc()
    return JSONResponse({"detail": "internal error"}, status_code=500)

app.middleware("http")(middleware_general)


# Montar directamente desde /data en Railway
if Path("/data").exists():
    app.mount("/static/img/servicios", StaticFiles(directory="/data/img/servicios"), name="servicios")
    app.mount("/static/img/productos", StaticFiles(directory="/data/img/productos"), name="productos")
else:
    # En local usamos la carpeta estática normal
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar rutas
app.include_router(homepage_router.router)
app.include_router(login_router.router)

# Rutas/layout segun el Rol
app.include_router(access_router.router)

# Rutas modulos internos
app.include_router(usuarios_router.router)
app.include_router(clientes_router.router)
app.include_router(servicios_router.router)
app.include_router(producto_router.router)
app.include_router(proveedores_router.router)
app.include_router(ventas_router.router)
app.include_router(garantias_router.router)
app.include_router(dashboard_router.router)
app.include_router(informes_router.router)