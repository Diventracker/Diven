from clientes.repositorio import ClienteRepositorio
from productos.repositorio import ProductoRepositorio
from ventas.model import DetalleVenta, Venta
from ventas.repositorio import VentaRepositorio
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import UploadFile
from servicios.model import DetalleServicio, ImagenServicio, ServicioTecnico
from servicios.schema import ServicioRevisionSchema, ServicioUpdate

class VentaCRUD:
    def __init__(self, db: Session):
        self.ventaRepo = VentaRepositorio(db)
        self.repo = self.ventaRepo
        self.producto_repo = ProductoRepositorio(db)
        self.cliente_repo = ClienteRepositorio(db)

    #lista todas las ventas para mostrar en la tabla
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
    
    #esta es la funcion que registra la venta
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
            #Consulta si esta el cliente
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

            producto.stock -= cantidad

        try:
            nueva_venta = Venta(
                id_cliente=id_cliente,
                id_usuario=id_usuario,
                total_venta=total_venta
            )
            self.repo.db.add(nueva_venta)
            self.repo.db.flush()  # para obtener id_venta

            for det in detalles:
                detalle = DetalleVenta(
                    id_venta=nueva_venta.id_venta,
                    id_producto=det["id_producto"],
                    cantidad=det["cantidad"],
                    precio_unitario=det["precio_unitario"]
                )
                self.repo.db.add(detalle)

            self.repo.db.commit()
            return nueva_venta.id_venta

        except SQLAlchemyError:
            self.repo.db.rollback()
            raise Exception("Error al registrar la venta")
        
    #Para mostrar los datos del comprobante
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


