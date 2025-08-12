from fastapi import Request
from fastapi.templating import Jinja2Templates
from productos.crud import ProductoCRUD
from productos.schema import ProductoCreate, ProductoUpdate
from fastapi.responses import JSONResponse
from utils.imagenes import guardar_imagen

templates = Jinja2Templates(directory=["templates", "productos/templates"])

class ProductoControlador:
    def __init__(self, db):
        self.crud = ProductoCRUD(db)

    def mostrar_vista(self, request: Request):
        usuario = request.state.usuario
        return templates.TemplateResponse("productos.html", {
            "request": request,
            "rol": usuario["rol"]
        })

    async def crear(self, datos: ProductoCreate, imagen):
        try:
            # Aquí usamos await correctamente
            ruta_imagen = await guardar_imagen(imagen)

            producto = self.crud.crear(datos, ruta_imagen)

            return JSONResponse(content={
                "success": True,
                "mensaje": "Producto creado exitosamente.",
                "id": producto.id_producto
            })

        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
        except Exception:
            return JSONResponse(content={"success": False, "error": "Error interno al crear producto."}, status_code=500)

        
    #Pasa los productos mediante /data
    def obtener_productos(self):
        productos = self.crud.listar_productos()

        datos = []
        for p in productos:
            datos.append({
                "id": p.id_producto,
                "nombre": p.nombre_producto,
                "modelo": p.modelo,
                "descripcion": p.descripcion,
                "precio": p.precio_venta if p.precio_venta is not None else p.precio,
                "stock": p.stock,
                "garantia": p.meses_garantia,
                "fecha_compra": p.fecha_compra.strftime("%Y-%m-%d"),
                "id_proveedor": p.id_proveedor,
                "proveedor": p.proveedor.nombre_proveedor if p.proveedor else "Desconocido",
                "imagen_url": p.imagen if p.imagen else "/static/img/productos/sin-imagen.png"
            })

        return JSONResponse(content=datos)
    
    async def editar(self, producto_id: int, datos: ProductoUpdate, imagen):
        try:
            ruta_imagen = None
            if imagen and getattr(imagen, "filename", None):
                ruta_imagen = await guardar_imagen(imagen)  # 👈 guarda y devuelve /static/...

            self.crud.editar(producto_id, datos, ruta_imagen)  # 👈 pásala al CRUD (puede ser None)
            return JSONResponse(content={"success": True, "mensaje": "Producto actualizado exitosamente."})
        except ValueError as e:
            return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)
        except Exception:
            return JSONResponse(content={"success": False, "error": "Error interno al editar producto."}, status_code=500)
        
    def eliminar(self, id_producto: int) -> JSONResponse:
        try:
            self.crud.eliminar(id_producto)
            return JSONResponse(content={"success": True, "mensaje": "Producto eliminado correctamente."})
        except ValueError as e:
            return JSONResponse(status_code=400, content={"success": False, "error": str(e)})
        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Ocurrió un error inesperado."})

    def buscar(self, termino: str) -> JSONResponse:
        try:
            producto = self.crud.buscar(termino)
            return JSONResponse(content={
                "codigo": str(producto.id_producto),
                "nombre": producto.nombre_producto,
                "descripcion": producto.descripcion,
                "precio": int(producto.precio_venta),
                "stock": int(producto.stock)
            })
        except ValueError as e:
            return JSONResponse(status_code=404, content={"success": False, "error": str(e)})
        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Error interno al buscar el producto."})
        
    #Lista para el modal de crear venta
    def listar_api(self, search: str = "", con_stock: bool = True) -> JSONResponse:
        try:
            productos = self.crud.obtener_todos(search, con_stock)
            return JSONResponse(content=[
                {
                    "codigo": str(prod.id_producto),
                    "nombre": prod.nombre_producto,
                    "descripcion": prod.descripcion,
                    "modelo": prod.modelo,
                    "precio": prod.precio_venta,
                    "stock": prod.stock,
                    "proveedor": prod.proveedor.nombre_proveedor
                }
                for prod in productos
            ])
        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Error al obtener productos."})
        

    def bajo_stock(self) -> JSONResponse:
        try:
            productos = self.crud.obtener_bajo_stock()
            return JSONResponse(content=[
                {
                    "codigo": str(prod.id_producto),
                    "nombre": prod.nombre_producto,
                    "descripcion": prod.descripcion,
                    "modelo": prod.modelo,
                    "precio": prod.precio_venta,
                    "stock": prod.stock,
                    "proveedor": prod.proveedor.nombre_proveedor if prod.proveedor else None
                }
                for prod in productos
            ])
        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Error al obtener productos con bajo stock."})

    #Actualizar stock de un producto 
    def actualizar_stock(self, id_producto: int, cantidad: int) -> JSONResponse:
        try:
            stock_final = self.crud.actualizar_stock(id_producto, cantidad)
            return JSONResponse(content={
                "success": True,
                "mensaje": "Stock actualizado correctamente",
                "stock_final": stock_final
            })
        except ValueError as e:
            return JSONResponse(status_code=404, content={"success": False, "error": str(e)})
        except Exception:
            return JSONResponse(status_code=500, content={"success": False, "error": "Error al actualizar el stock."})
