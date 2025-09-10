import os
import shutil

def setup_static_from_volume():
    # Productos
    src_prod = "/data/img/productos"
    dst_prod = "static/img/productos"
    if os.path.exists(src_prod):
        os.makedirs(dst_prod, exist_ok=True)
        for f in os.listdir(src_prod):
            shutil.copy2(os.path.join(src_prod, f), os.path.join(dst_prod, f))

    # Servicios
    src_serv = "/data/img/servicios"
    dst_serv = "static/img/servicios"
    if os.path.exists(src_serv):
        os.makedirs(dst_serv, exist_ok=True)
        for f in os.listdir(src_serv):
            shutil.copy2(os.path.join(src_serv, f), os.path.join(dst_serv, f))
