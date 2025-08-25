from clientes.repositorio import ClienteRepositorio
from productos.repositorio import ProductoRepositorio
from ventas.model import DetalleVenta, Venta
from ventas.repositorio import VentaRepositorio
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from garantias.model import GarantiaProducto
from datetime import date, timedelta
try:
    from dateutil.relativedelta import relativedelta
except Exception:
    relativedelta = None


class VentaCRUD:
    def __init__(self, db: Session):
        self.ventaRepo = VentaRepositorio(db)
        self.repo = self.ventaRepo
        self.producto_repo = ProductoRepositorio(db)
        self.cliente_repo = ClienteRepositorio(db)

    # lista todas las ventas
    def listar_todas(self) -> list[Venta]:
        return self.repo.listar_todas()

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
            producto = self.producto_repo.obtener_por_id(d.id_producto)
            resultado["detalles"].append({
                "producto": producto.nombre_producto if producto else "¿?",
                "descripcion": producto.descripcion if producto else "¿?"
            })

        return resultado

    # registra la venta y crea garantías
    def generar(self, id_cliente: int, id_usuario: int, productos: list[dict]) -> int:
        if not productos:
            raise ValueError("No se han agregado productos a la venta")

        total_venta = 0
        detalles = []

        for item in productos:
            id_producto = item["id_producto"]
            cantidad = item["cantidad"]

            producto = self.producto_repo.obtener_por_id(id_producto)
            if not producto:
                raise ValueError(f"Producto {id_producto} no encontrado")
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente para {producto.nombre_producto}")

            cliente = self.cliente_repo.obtener_por_id(id_cliente)
            if not cliente:
                raise ValueError("Cliente no encontrado")

            precio_unitario = producto.precio_venta or producto.precio
            subtotal = cantidad * float(precio_unitario)
            total_venta += subtotal

            detalles.append({
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario
            })

            # descuenta stock en memoria; el commit será al final
            producto.stock -= cantidad

        try:
            # 1) crear venta
            nueva_venta = Venta(
                id_cliente=id_cliente,
                id_usuario=id_usuario,
                total_venta=total_venta
            )
            self.repo.db.add(nueva_venta)
            self.repo.db.flush()  # obtengo id_venta

            # 2) detalles
            for det in detalles:
                self.repo.db.add(DetalleVenta(
                    id_venta=nueva_venta.id_venta,
                    id_producto=det["id_producto"],
                    cantidad=det["cantidad"],
                    precio_unitario=det["precio_unitario"]
                ))

            # 3) garantías
            fecha_inicio = (nueva_venta.fecha_venta.date()
                            if hasattr(nueva_venta.fecha_venta, "date")
                            else date.today())

            fecha_fin = (fecha_inicio + relativedelta(months=1)) if relativedelta else (fecha_inicio + timedelta(days=30))

            for det in detalles:
                for _ in range(det["cantidad"]):
                    self.repo.db.add(GarantiaProducto(
                        id_producto=det["id_producto"],
                        id_venta=nueva_venta.id_venta,   # <<<<<<<<<<
                        id_cliente=id_cliente,           # <<<<<<<<<<
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        origen_garantia="venta_cliente"
                    ))

            # 4) commit final
            self.repo.db.commit()
            return nueva_venta.id_venta

        except SQLAlchemyError:
            self.repo.db.rollback()
            raise Exception("Error al registrar la venta")

    # comprobante
    def obtener_comprobante(self, id_venta: int):
        venta = self.repo.obtener_venta_con_relaciones(id_venta)
        if not venta:
            raise ValueError("Venta no encontrada")

        detalles = self.repo.obtener_detalles_por_venta(id_venta)
        return venta, venta.cliente, detalles

    def obtener_totales_por_mes(self):
        return self.repo.obtener_totales_por_mes()

    def obtener_productos_mas_vendidos(self, limite: int = 8):
        return self.repo.obtener_productos_mas_vendidos(limite)

    def obtener_ventas_por_vendedor(self, limite: int = 6):
        return self.repo.obtener_ventas_por_vendedor(limite)
