function mostrarPorcentaje(idElemento, valor) {
    const elem = document.getElementById(idElemento);
    if (valor === null || valor === undefined) {
        elem.innerText = "Sin comparación";
        elem.className = "stat-change neutral";
        return;
    }

    const signo = valor > 0 ? "+" : "";
    const clase = valor > 0 ? "positive" : valor < 0 ? "negative" : "neutral";
    const icono = valor > 0 ? "bi-arrow-up" : valor < 0 ? "bi-arrow-down" : "bi-dash";

    elem.innerHTML = `<i class="bi ${icono}"></i> ${signo}${Math.abs(valor)}% vs período anterior`;
    elem.className = "stat-change " + clase;
}

function actualizarDashboard(data) {
    document.getElementById("ventasTotales").innerText =
        data.ventas_totales.toLocaleString("es-CO", {
            style: "currency",
            currency: "COP",
            minimumFractionDigits: 0
        });
    document.getElementById("numeroVentas").innerText =
        data.numero_ventas.toLocaleString("es-CO");
    document.getElementById("nuevosClientes").innerText =
        data.nuevos_clientes.toLocaleString("es-CO");

    mostrarPorcentaje("varVentasTotales", data.var_ventas_totales);
    mostrarPorcentaje("varNumeroVentas", data.var_numero_ventas);
    mostrarPorcentaje("varNuevosClientes", data.var_nuevos_clientes);
}

function cargarEstadisticas(periodo, fechaInicio = null, fechaFin = null) {
    let url = `/api/dashboard/stats/${periodo}`;
    if (periodo === "personalizado" && fechaInicio && fechaFin) {
        url += `?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    }

    fetch(url)
        .then(res => {
            if (!res.ok) throw new Error(`Error del servidor: ${res.status}`);
            return res.json();
        })
        .then(actualizarDashboard)
        .catch(error => console.error("Error al cargar estadísticas:", error));
}

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
    cargarEstadisticas("hoy");

    // Set texto de mes
    const meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
    const hoy = new Date();
    const texto = `${meses[hoy.getMonth()].charAt(0).toUpperCase() + meses[hoy.getMonth()].slice(1)} ${hoy.getFullYear()}`;
    document.getElementById("mesActual").innerText = texto;
});

// Botones de periodo
document.querySelectorAll("button[data-periodo]").forEach(btn => {
    btn.addEventListener("click", () => {
        const periodo = btn.getAttribute("data-periodo");

        // Solo cargar si no es personalizado
        if (periodo !== "personalizado") {
            cargarEstadisticas(periodo);
        }
    });
});

// Fecha personalizada
document.getElementById('form-control-fecha').addEventListener('submit', function (e) {
    e.preventDefault();

    const fechaInicio = this.querySelector('input[name="fecha_inicio"]').value;
    const fechaFin = this.querySelector('input[name="fecha_fin"]').value;

    if (!fechaInicio || !fechaFin || fechaInicio > fechaFin) {
        alert('Selecciona un rango de fechas válido.');
        return;
    }

    cargarEstadisticas("personalizado", fechaInicio, fechaFin);

    const modal = bootstrap.Modal.getInstance(document.getElementById('modalFechaPersonalizada'));
    modal.hide();
});