from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import Request
from sqlalchemy.orm import Session
from garantias.model import GarantiaProducto, GarantiaServicio
from productos.repositorio import ProductoRepositorio
from clientes.repositorio import ClienteRepositorio
from clientes.model import Cliente
from fastapi import HTTPException
from datetime import date, timedelta
from servicios.model import ServicioTecnico
try:
    from dateutil.relativedelta import relativedelta
except Exception:
    relativedelta = None



templates = Jinja2Templates(directory=["templates", "garantias/templates"])

class GarantiaControlador:
    def __init__(self, db: Session | None = None):
        self.db = db
        self.producto_repo = ProductoRepositorio(db) if db else None
        self.cliente_repo  = ClienteRepositorio(db) if db else None

    def vista_principal(self, request: Request):
        usuario = request.state.usuario
        return templates.TemplateResponse("garantias.html", {"request": request, "rol": usuario["rol"]})

    def listar_garantias_ventas(self, cliente: str | None = None):
        q = self.db.query(GarantiaProducto)
        if cliente:
            q = q.join(Cliente, Cliente.id_cliente == GarantiaProducto.id_cliente)\
                 .filter(Cliente.nombre_cliente.ilike(f"%{cliente}%"))

        garantias = q.order_by(GarantiaProducto.id_garantia.desc()).all()

        data = []
        for g in garantias:
            prod = self.producto_repo.obtener_por_id(g.id_producto) if self.producto_repo else None
            cli  = self.cliente_repo.obtener_por_id(g.id_cliente) if (g.id_cliente and self.cliente_repo) else None
            data.append({
                "id_garantia": g.id_garantia,
                "cliente": cli.nombre_cliente if cli else "—",
                "producto": prod.nombre_producto if prod else f"ID {g.id_producto}",
                "fecha_inicio": g.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": g.fecha_fin.strftime("%Y-%m-%d"),
                "estado": g.estado,
                "descripcion": getattr(prod, "descripcion", "") if prod else ""
            })
        return JSONResponse(data)
    
    def actualizar_estado(self, tipo: str, id_garantia: int, estado: str):
        if estado not in ("activa", "vencida", "anulada"):
            raise HTTPException(400, "Estado inválido")

        if tipo == "producto":
            g = self.db.query(GarantiaProducto).get(id_garantia)
        elif tipo == "servicio":
            g = self.db.query(GarantiaServicio).get(id_garantia)
        else:
            raise HTTPException(400, "Tipo inválido")

        if not g:
            raise HTTPException(404, "Garantía no encontrada")

        g.estado = estado
        self.db.commit()
        return JSONResponse({"ok": True})
    
    def actualizar_vencidas(self):
        hoy = date.today()
        q = self.db.query(GarantiaProducto).filter(
            GarantiaProducto.estado == "activa",
            GarantiaProducto.fecha_fin < hoy
        )
        for g in q:
            g.estado = "vencida"
        self.db.commit()

    def cambiar_estado(self, tipo: str, id_garantia: int, estado: str):
        if estado not in ("activa", "vencida", "anulada"):
            raise HTTPException(400, "Estado inválido")

        if tipo == "producto":
            g = self.db.query(GarantiaProducto).get(id_garantia)
        elif tipo == "servicio":
            g = self.db.query(GarantiaServicio).get(id_garantia)
        else:
            raise HTTPException(400, "Tipo inválido")

        if not g:
            raise HTTPException(404, "Garantía no encontrada")

        g.estado = estado
        self.db.commit()
        return JSONResponse({"ok": True})
    
    def renovar_producto(self, id_garantia: int, id_producto_nuevo: int | None, meses: int | None, fecha_inicio: date | None):
        # 1) buscar garantía original
        g = self.db.query(GarantiaProducto).get(id_garantia)
        if not g:
            raise HTTPException(404, "Garantía no encontrada")

        # 2) calcular fechas de la nueva garantía
        f_inicio = fecha_inicio or date.today()
        if meses is None or meses <= 0:
            meses = 1
        f_fin = (f_inicio + relativedelta(months=meses)) if relativedelta else (f_inicio + timedelta(days=30*meses))

        # 3) crear la nueva garantía (mantiene cliente y venta; producto puede cambiar)
        g_nueva = GarantiaProducto(
            id_producto = id_producto_nuevo or g.id_producto,
            id_venta    = g.id_venta,
            id_cliente  = g.id_cliente,
            id_garantia_origen = g.id_garantia,   # trazabilidad (si agregaste la columna)
            fecha_inicio = f_inicio,
            fecha_fin    = f_fin,
            origen_garantia = "renovacion",
            estado = "activa",
        )
        self.db.add(g_nueva)

        # 4) marcar la anterior como 'renovada'
        g.estado = "renovada"

        self.db.commit()
        return JSONResponse({"ok": True, "nueva_garantia_id": g_nueva.id_garantia})
    
    
    def listar_garantias_servicios(self, q: str | None = None):
    # Join GarantiaServicio -> ServicioTecnico -> Cliente
        query = (
            self.db.query(
                GarantiaServicio.id_garantia.label("id_garantia"),
                Cliente.nombre_cliente.label("cliente"),
                ServicioTecnico.tipo_equipo.label("equipo"),
                GarantiaServicio.fecha_inicio.label("fecha_inicio"),
                GarantiaServicio.fecha_fin.label("fecha_fin"),
                (ServicioTecnico.descripcion_trabajo if ServicioTecnico.descripcion_trabajo is not None else ServicioTecnico.descripcion_problema).label("descripcion"),
                ServicioTecnico.id_servicio.label("id_servicio"),
            )
            .join(ServicioTecnico, GarantiaServicio.id_servicio == ServicioTecnico.id_servicio)
            .join(Cliente, ServicioTecnico.id_cliente == Cliente.id_cliente)
            .order_by(GarantiaServicio.id_garantia.desc())
        )

        if q:
            like = f"%{q}%"
            query = query.filter(
                (Cliente.nombre_cliente.ilike(like)) |
                (ServicioTecnico.tipo_equipo.ilike(like)) |
                (ServicioTecnico.descripcion_trabajo.ilike(like)) |
                (ServicioTecnico.descripcion_problema.ilike(like))
            )

        rows = query.all()
        data = [{
            "id_garantia": r.id_garantia,
            "cliente": r.cliente,
            "equipo": r.equipo,
            "fecha_inicio": r.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": r.fecha_fin.strftime("%Y-%m-%d"),
            "descripcion": r.descripcion or "",
            "id_servicio": r.id_servicio,
        } for r in rows]

        return JSONResponse(data)