from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import home_ctr, login_ctr, admin_ctr
from controllers.Madmin import clientes_ctr, servicios_ctr, producto_ctr, proveedores_ctr

app = FastAPI()

# Montamos la carpeta 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar rutas
app.include_router(home_ctr.router)
app.include_router(login_ctr.router)
app.include_router(admin_ctr.router)
app.include_router(clientes_ctr.router)
app.include_router(servicios_ctr.router)
app.include_router(producto_ctr.router)
app.include_router(proveedores_ctr.router)