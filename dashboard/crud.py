from sqlalchemy import func, and_, distinct
from datetime import datetime
from ventas.model import Venta
from sqlalchemy.orm import Session

from ventas.repositorio import VentaRepositorio

class DashboardCRUD:
    def __init__(self, venta_repo: VentaRepositorio):
        self.venta_repo = venta_repo
        self.db: Session = venta_repo.db

    def calcular_variacion(self, actual, anterior):
        if anterior == 0:
            return 100 if actual > 0 else 0
        return round(((actual - anterior) / anterior) * 100, 1)

    def obtener_estadisticas(self, filtro):
        total = self.db.query(func.coalesce(func.sum(Venta.total_venta), 0)).filter(filtro).scalar()
        ventas = self.db.query(func.count()).filter(filtro).scalar()
        clientes = self.db.query(func.count(distinct(Venta.id_cliente))).filter(filtro).scalar()
        return float(total), ventas, clientes

