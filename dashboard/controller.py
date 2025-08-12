from fastapi.responses import JSONResponse
from dashboard.crud import DashboardCRUD
from ventas.model import Venta
from ventas.repositorio import VentaRepositorio
from datetime import date, datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

class DashboardControlador:
    def __init__(self, db: Session):
        venta_repo = VentaRepositorio(db)
        self.crud = DashboardCRUD(venta_repo)

    def obtener_estadisticas(self, periodo: str, fecha_inicio: str = None, fecha_fin: str = None) -> JSONResponse:
        hoy = date.today()

        # Definir filtros
        filtro_actual = None
        filtro_anterior = None

        if periodo == "personalizado":
            if not fecha_inicio:
                raise ValueError("La fecha de inicio es requerida para el periodo personalizado")
            if not fecha_fin:
                raise ValueError("La fecha de fin es requerida para el periodo personalizado")
            try:
                fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                ff = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Fechas inválidas")

            filtro_actual = and_(Venta.fecha_venta >= fi, Venta.fecha_venta <= ff)

        elif periodo == "hoy":
            filtro_actual = Venta.fecha_venta == hoy
            filtro_anterior = Venta.fecha_venta == hoy - timedelta(days=1)

        elif periodo == "semana":
            semana_actual = hoy.isocalendar()[1]
            anio_actual = hoy.isocalendar()[0]
            semana_pasada = (hoy - timedelta(weeks=1)).isocalendar()[1]
            anio_pasado = (hoy - timedelta(weeks=1)).isocalendar()[0]

            filtro_actual = and_(
                func.extract("week", Venta.fecha_venta) == semana_actual,
                func.extract("year", Venta.fecha_venta) == anio_actual
            )
            filtro_anterior = and_(
                func.extract("week", Venta.fecha_venta) == semana_pasada,
                func.extract("year", Venta.fecha_venta) == anio_pasado
            )

        elif periodo == "mes":
            filtro_actual = and_(
                func.extract("month", Venta.fecha_venta) == hoy.month,
                func.extract("year", Venta.fecha_venta) == hoy.year
            )
            mes_anterior = hoy.replace(day=1) - timedelta(days=1)
            filtro_anterior = and_(
                func.extract("month", Venta.fecha_venta) == mes_anterior.month,
                func.extract("year", Venta.fecha_venta) == mes_anterior.year
            )

        elif periodo == "anio":
            filtro_actual = func.extract("year", Venta.fecha_venta) == hoy.year
            filtro_anterior = func.extract("year", Venta.fecha_venta) == hoy.year - 1

        else:
            raise ValueError("Periodo inválido")

        # Obtener datos actuales
        total_actual, ventas_actual, clientes_actual = self.crud.obtener_estadisticas(filtro_actual)

        # Obtener datos anteriores (si aplica)
        if filtro_anterior is not None:
            total_anterior, ventas_anterior, clientes_anterior = self.crud.obtener_estadisticas(filtro_anterior)
        else:
            total_anterior = ventas_anterior = clientes_anterior = 0


        return {
            "periodo": periodo,
            "ventas_totales": float(total_actual),
            "numero_ventas": ventas_actual,
            "nuevos_clientes": clientes_actual,
            "var_ventas_totales": self.crud.calcular_variacion(float(total_actual), float(total_anterior)) if filtro_anterior is not None else None,
            "var_numero_ventas": self.crud.calcular_variacion(ventas_actual, ventas_anterior) if filtro_anterior is not None else None,
            "var_nuevos_clientes": self.crud.calcular_variacion(clientes_actual, clientes_anterior) if filtro_anterior is not None else None
        }
