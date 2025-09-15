# dashboard/controlador.py
from datetime import date, datetime, time, timedelta
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ventas.model import Venta
from .crud import DashboardCRUD
from ventas.repositorio import VentaRepositorio

class DashboardControlador:
    def __init__(self, db: Session):
        venta_repo = VentaRepositorio(db)
        self.crud = DashboardCRUD(venta_repo)

    # helpers para construir rangos [inicio, fin)
    def _range_day(self, d: date):
        start = datetime.combine(d, time.min)
        end = start + timedelta(days=1)
        return start, end

    def _range_week(self, d: date):
        # Lunes como inicio de semana
        start_date = d - timedelta(days=d.weekday())
        start = datetime.combine(start_date, time.min)
        end = start + timedelta(days=7)
        return start, end

    def _range_month(self, d: date):
        start_date = d.replace(day=1)
        # primer día del mes siguiente
        if d.month == 12:
            next_month = date(d.year + 1, 1, 1)
        else:
            next_month = date(d.year, d.month + 1, 1)
        start = datetime.combine(start_date, time.min)
        end = datetime.combine(next_month, time.min)
        return start, end

    def _range_year(self, d: date):
        start = datetime(d.year, 1, 1)
        end = datetime(d.year + 1, 1, 1)
        return start, end

    def _range_custom(self, fi_str: str, ff_str: str):
        if not fi_str or not ff_str:
            raise ValueError("La fecha de inicio y fin son requeridas.")
        try:
            fi_d = datetime.strptime(fi_str, "%Y-%m-%d").date()
            ff_d = datetime.strptime(ff_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Fechas inválidas. Formato esperado: YYYY-MM-DD.")

        if fi_d > ff_d:
            raise ValueError("El rango de fechas es inválido (inicio > fin).")

        # rango inclusivo de días: [fi 00:00:00, ff + 1 día 00:00:00)
        start = datetime.combine(fi_d, time.min)
        end = datetime.combine(ff_d + timedelta(days=1), time.min)
        return start, end

    def obtener_estadisticas(self, periodo: str, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
        hoy = date.today()

        # construir rango principal [start, end)
        if periodo == "hoy":
            start, end = self._range_day(hoy)
            prev_start, prev_end = self._range_day(hoy - timedelta(days=1))
        elif periodo == "semana":
            start, end = self._range_week(hoy)
            prev_start, prev_end = self._range_week(hoy - timedelta(weeks=1))
        elif periodo == "mes":
            start, end = self._range_month(hoy)
            # mes anterior: un día antes del primer día del mes actual
            mes_anterior_ultimo = (hoy.replace(day=1) - timedelta(days=1))
            prev_start, prev_end = self._range_month(mes_anterior_ultimo)
        elif periodo == "anio":
            start, end = self._range_year(hoy)
            prev_start, prev_end = self._range_year(date(hoy.year - 1, hoy.month, hoy.day))
        elif periodo == "personalizado":
            start, end = self._range_custom(fecha_inicio, fecha_fin)
            prev_start = prev_end = None  # no aplican variaciones
        else:
            raise ValueError("Periodo inválido")

        # filtros por rango (funciona para DATE o DATETIME)
        filtro_actual = and_(Venta.fecha_venta >= start, Venta.fecha_venta < end)

        total_actual, ventas_actual, clientes_actual = self.crud.obtener_estadisticas(filtro_actual)

        if prev_start and prev_end:
            filtro_anterior = and_(Venta.fecha_venta >= prev_start, Venta.fecha_venta < prev_end)
            total_anterior, ventas_anterior, clientes_anterior = self.crud.obtener_estadisticas(filtro_anterior)
            var_ventas_totales = self.crud.calcular_variacion(float(total_actual), float(total_anterior))
            var_numero_ventas = self.crud.calcular_variacion(ventas_actual, ventas_anterior)
            var_nuevos_clientes = self.crud.calcular_variacion(clientes_actual, clientes_anterior)
        else:
            var_ventas_totales = None
            var_numero_ventas = None
            var_nuevos_clientes = None

        return {
            "periodo": periodo,
            "ventas_totales": float(total_actual),
            "numero_ventas": int(ventas_actual),
            "nuevos_clientes": int(clientes_actual),
            "var_ventas_totales": var_ventas_totales,
            "var_numero_ventas": var_numero_ventas,
            "var_nuevos_clientes": var_nuevos_clientes,
        }