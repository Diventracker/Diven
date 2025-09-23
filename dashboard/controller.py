# dashboard/controlador.py
from datetime import date, datetime, time, timedelta
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ventas.model import Venta
from .crud import DashboardCRUD
from ventas.repositorio import VentaRepositorio
from servicios.repositorio import ServicioRepositorio

class DashboardControlador:
    def __init__(self, db: Session):
        venta_repo = VentaRepositorio(db)
        servicios_repo = ServicioRepositorio(db)
        self.crud = DashboardCRUD(venta_repo)
        self.crud = DashboardCRUD(servicios_repo)

    # helpers para construir rangos [inicio, fin)
    def _rango_dia(self, d: date):
        inicio = datetime.combine(d, time.min)
        fin = inicio + timedelta(days=1)
        return inicio, fin

    def _rango_semana(self, d: date):
        # Lunes como inicio de semana
        fecha_inicio = d - timedelta(days=d.weekday())
        inicio = datetime.combine(fecha_inicio, time.min)
        fin = inicio + timedelta(days=7)
        return inicio, fin

    def _rango_mes(self, d: date):
        fecha_inicio = d.replace(day=1)
        # primer día del mes siguiente
        if d.month == 12:
            siguiente_mes = date(d.year + 1, 1, 1)
        else:
            siguiente_mes = date(d.year, d.month + 1, 1)
        inicio = datetime.combine(fecha_inicio, time.min)
        fin = datetime.combine(siguiente_mes, time.min)
        return inicio, fin

    def _rango_anio(self, d: date):
        inicio = datetime(d.year, 1, 1)
        fin = datetime(d.year + 1, 1, 1)
        return inicio, fin

    def _rango_personalizado(self, fi_str: str, ff_str: str):
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
        inicio = datetime.combine(fi_d, time.min)
        fin = datetime.combine(ff_d + timedelta(days=1), time.min)
        return inicio, fin

    def obtener_estadisticas(self, periodo: str, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
        hoy = date.today()

        # construir rango principal [inicio, fin)
        if periodo == "hoy":
            inicio, fin = self._rango_dia(hoy)
            prev_inicio, prev_fin = self._rango_dia(hoy - timedelta(days=1))

        elif periodo == "semana":
            inicio, fin = self._rango_semana(hoy)
            prev_inicio, prev_fin = self._rango_semana(hoy - timedelta(weeks=1))

        elif periodo == "mes":
            inicio, fin = self._rango_mes(hoy)
            # mes anterior: un día antes del primer día del mes actual
            ultimo_dia_mes_anterior = (hoy.replace(day=1) - timedelta(days=1))
            prev_inicio, prev_fin = self._rango_mes(ultimo_dia_mes_anterior)

        elif periodo == "anio":
            inicio, fin = self._rango_anio(hoy)
            prev_inicio, prev_fin = self._rango_anio(date(hoy.year - 1, hoy.month, hoy.day))

        elif periodo == "personalizado":
            inicio, fin = self._rango_personalizado(fecha_inicio, fecha_fin)
            prev_inicio = prev_fin = None  # no aplican comparaciones

        else:
            raise ValueError("Periodo inválido")

        # filtros por rango (funciona para DATE o DATETIME)
        filtro_actual = and_(Venta.fecha_venta >= inicio, Venta.fecha_venta < fin)
        
        total_final, total_actual, servicios_actual, ventas_actual, clientes_actual = self.crud.obtener_estadisticas(filtro_actual)

        if prev_inicio and prev_fin:
            filtro_anterior = and_(Venta.fecha_venta >= prev_inicio, Venta.fecha_venta < prev_fin)
            # Obtener totales
            total_final_anterior, servicios_anterior, total_anterior, ventas_anterior, clientes_anterior = self.crud.obtener_estadisticas(filtro_anterior)
            # calcular variación porcentajes
            var_servicio_total = self.crud.calcular_variacion(float(servicios_actual), float(servicios_anterior))
            var_ventas_totales = self.crud.calcular_variacion(float(total_actual), float(total_anterior))
            var_numero_ventas = self.crud.calcular_variacion(ventas_actual, ventas_anterior)
            var_nuevos_clientes = self.crud.calcular_variacion(clientes_actual, clientes_anterior)
        else:
            var_servicio_total = None
            var_ventas_totales = None
            var_numero_ventas = None
            var_nuevos_clientes = None

        return {
            "periodo": periodo,
            "total_final": total_final,
            "ventas_totales": total_actual,
            "numero_ventas": ventas_actual,
            "nuevos_clientes": clientes_actual,
            "var_servicio_total": var_servicio_total,
            "var_ventas_totales": var_ventas_totales,
            "var_numero_ventas": var_numero_ventas,
            "var_nuevos_clientes": var_nuevos_clientes,
        }
