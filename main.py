from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from homepage import routes as homepage_router
from login import routes as login_router
from access import routes as access_router
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

app = FastAPI()


app.middleware("http")(middleware_general)


# Montamos la carpeta 'static'
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