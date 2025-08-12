from datetime import date
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from fastapi.responses import FileResponse
from clientes.crud import ClienteCRUD
from clientes.repositorio import ClienteRepositorio
from garantias.model import GarantiaServicio
from productos.model import Producto
from proveedores.repositorio import ProveedorRepositorio
from servicios.model import ServicioTecnico
from servicios.repositorio import ServicioRepositorio
from usuarios.repositorio import UsuarioRepositorio
from utils.report_generator import generar_pdf_informe
from ventas.model import Venta
from ventas.repositorio import VentaRepositorio


class InformeControlador:
    def __init__(self, db: Session):
        self.db = db
        self.repo_clientes = ClienteRepositorio(db)
        self.cliente_crud = ClienteCRUD(self.repo_clientes)
        self.repo_ventas = VentaRepositorio(db)
        self.repo_usuarios = UsuarioRepositorio(db)
        self.repo_proveedores = ProveedorRepositorio(db)
        self.repo_servicios = ServicioRepositorio(db)

    def generar_informe_por_cliente(self, identificador: str) -> FileResponse:
        # Primero, probar como ID numérico exacto
        cliente = None
        if identificador.isdigit():
            cliente = self.cliente_crud.buscar_por_documento(identificador)
        if not cliente:
            resultados = self.cliente_crud.filtrar_por_texto(identificador)
            cliente = resultados[0] if resultados else None

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")

        ventas = (
            self.db.query(Venta)
            .filter(Venta.id_cliente == cliente.id_cliente)
            .order_by(Venta.fecha_venta.desc())
            .all()
        )

        columnas = ["ID Venta", "Fecha", "Total", "Cliente"]
        datos = [{
            "ID Venta": v.id_venta,
            "Fecha": v.fecha_venta.strftime("%d/%m/%Y"),
            "Total": f"${float(v.total_venta):,.2f}",
            "Cliente": cliente.nombre_cliente
        } for v in ventas]

        if not datos:
            datos = [{"ID Venta": "-", "Fecha": "-", "Total": "Sin ventas registradas", "Cliente": cliente.nombre_cliente}]

        path = generar_pdf_informe(
            tipo="cliente",
            fecha_inicio="N/A",
            fecha_fin="N/A",
            datos=datos,
            columnas=columnas,
            titulo_customizado=f"Informe de ventas - Cliente: {cliente.nombre_cliente} ({cliente.numero_documento})"
        )

        return FileResponse(path, filename=f"informe_cliente_{cliente.id_cliente}.pdf", media_type="application/pdf")
    
    def generar_informe(self, tipo: str, fecha_inicio: date, fecha_fin: date):
        match tipo:
            case "producto":
                productos = self.db.query(Producto).filter(
                    Producto.fecha_compra != None,
                    Producto.fecha_compra >= fecha_inicio,
                    Producto.fecha_compra <= fecha_fin
                ).all()
                columnas = ["ID", "Nombre", "Modelo", "Stock", "Precio"]
                datos = [{
                    "ID": p.id_producto,
                    "Nombre": p.nombre_producto,
                    "Modelo": p.modelo,
                    "Stock": p.stock,
                    "Precio": f"${p.precio_venta:.2f}" if p.precio_venta else "-"
                } for p in productos]

            case "clientes":
                clientes = self.repo_clientes.obtener_todos()
                columnas = ["ID", "Nombre", "Cédula", "Teléfono", "Email"]
                datos = [{
                    "ID": c.id_cliente,
                    "Nombre": c.nombre_cliente,
                    "Cédula": c.numero_documento,
                    "Teléfono": c.telefono_cliente,
                    "Email": c.email_cliente
                } for c in clientes]

            case "usuarios":
                usuarios = self.repo_usuarios.listar_todos()
                columnas = ["ID", "Nombre", "Correo", "Rol"]
                datos = [{
                    "ID": u.id_usuario,
                    "Nombre": u.nombre_usuario,
                    "Correo": u.correo,
                    "Rol": u.rol
                } for u in usuarios]

            case "proveedores":
                proveedores = self.repo_proveedores.obtener_todos()
                columnas = ["ID", "Nombre", "NIT", "Representante", "Teléfono"]
                datos = [{
                    "ID": p.id_proveedor,
                    "Nombre": p.nombre_proveedor,
                    "NIT": p.nit,
                    "Representante": p.representante_ventas,
                    "Teléfono": p.telefono_representante_ventas
                } for p in proveedores]

            case "servicios":
                servicios = self.repo_servicios.filtrar_por_fecha(fecha_inicio, fecha_fin)
                columnas = ["ID", "Equipo", "Marca", "Cliente", "Estado", "Recepción"]
                datos = [{
                    "ID": s.id_servicio,
                    "Equipo": s.tipo_equipo,
                    "Marca": s.modelo_equipo,
                    "Cliente": s.id_cliente,
                    "Estado": s.estado_servicio,
                    "Recepción": s.fecha_recepcion.strftime("%d/%m/%Y")
                } for s in servicios]

            case "garantias":
                garantias = (
                    self.db.query(GarantiaServicio)
                    .join(GarantiaServicio.servicio)  # Relación con ServicioTecnico
                    .join(ServicioTecnico.cliente)    # Relación con Cliente
                    .options(
                        joinedload(GarantiaServicio.servicio).joinedload(ServicioTecnico.cliente)
                    )
                    .filter(GarantiaServicio.fecha_inicio.between(fecha_inicio, fecha_fin))
                    .all()
                )

                columnas = ["ID Garantía", "Cliente", "Tipo de Equipo", "Inicio", "Fin"]
                datos = [{
                    "ID Garantía": g.id_garantia,
                    "Cliente": g.servicio.cliente.nombre_cliente if g.servicio and g.servicio.cliente else "Desconocido",
                    "Tipo de Equipo": g.servicio.tipo_equipo if g.servicio else "N/A",
                    "Inicio": g.fecha_inicio.strftime("%d/%m/%Y"),
                    "Fin": g.fecha_fin.strftime("%d/%m/%Y")
                } for g in garantias]

            case "ventas":
                ventas = self.repo_ventas.filtrar_por_rango(fecha_inicio, fecha_fin)
                columnas = ["ID Venta", "Fecha de venta", "Cliente", "Total"]
                datos = [{
                    "ID Venta": v.id_venta,
                    "Fecha de venta": v.fecha_venta.strftime("%d/%m/%Y"),
                    "Cliente": v.cliente.nombre_cliente if v.cliente else "Desconocido",
                    "Total": f"${float(v.total_venta):,.2f}"
                } for v in ventas]

            case _:
                raise ValueError("Tipo de informe no soportado aún.")

        return columnas, datos
