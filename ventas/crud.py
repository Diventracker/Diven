from ventas.repositorio import VentaRepositorio
from fastapi import HTTPException

class VentaCRUD:
    def __init__(self, repo: VentaRepositorio):
        self.repo = repo

    def obtener_detalle_venta(self, id_venta: int):
        venta = self.repo.obtener_venta_con_relaciones(id_venta)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")

        detalles = self.repo.obtener_detalles_por_venta(id_venta)

        resultado = {
            "cliente": venta.cliente.nombre_cliente,
            "fecha": venta.fecha_venta.strftime("%d/%m/%Y"),
            "vendedor": venta.usuario.nombre_usuario,
            "total": int(venta.total_venta),
            "detalles": []
        }

        for d in detalles:
            producto = self.repo.obtener_producto_por_id(d.id_producto)
            resultado["detalles"].append({
                "producto": producto.nombre_producto if producto else "¿?",
                "descripcion": producto.descripcion if producto else "¿?"
            })

        return resultado
