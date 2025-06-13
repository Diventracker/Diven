//funcion para porcentajes y llamado de informacion de las cards de dashboard
function mostrarPorcentaje(idElemento, valor) {
    const elem = document.getElementById(idElemento);// Asegúrate de que el elemento existe
    //toma los valores de los porcentajes y los muestra en las cards del dashboard
    const signo = valor > 0 ? "+" : valor < 0 ? "" : "";
    const clase = valor > 0 ? "positive" : valor < 0 ? "negative" : "neutral";
    const icono = valor > 0 ? "bi-arrow-up" : valor < 0 ? "bi-arrow-down" : "bi-dash";

    elem.innerHTML = `
        <i class="bi ${icono}"></i> ${signo}${Math.abs(valor)}% vs período anterior
    `;
    elem.className = "stat-change " + clase;
}

function cargarEstadisticas(periodo) {
    fetch(`/api/dashboard/stats/${periodo}`)
        .then(res => {
            if (!res.ok) throw new Error(`Error del servidor: ${res.status}`);
            return res.json();
        })
        .then(data => {
            // valores
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

            // variaciones
            mostrarPorcentaje("varVentasTotales", data.var_ventas_totales);
            mostrarPorcentaje("varNumeroVentas", data.var_numero_ventas);
            mostrarPorcentaje("varNuevosClientes", data.var_nuevos_clientes);
        })
        .catch(error => console.error("Error al cargar estadísticas:", error));
}

// Al cargar la página: periodo por defecto = hoy
document.addEventListener("DOMContentLoaded", function () {
    cargarEstadisticas("hoy");
});

// Al hacer clic en botones de periodo
document.querySelectorAll("button[data-periodo]").forEach(btn => {
    btn.addEventListener("click", () => {
        const periodo = btn.getAttribute("data-periodo");
        cargarEstadisticas(periodo);
    });
});

//span periodo automatico
document.addEventListener("DOMContentLoaded", function () {
    const meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ];
    const hoy = new Date();
    const nombreMes = meses[hoy.getMonth()];
    const anio = hoy.getFullYear();

    const texto = `${nombreMes.charAt(0).toUpperCase() + nombreMes.slice(1)} ${anio}`;
    document.getElementById("mesActual").innerText = texto;
});


//click en personalizado
document.getElementById('form-control-fecha').addEventListener('submit', function (e) {
    e.preventDefault();

    const fechaInicio = this.querySelector('input[name="fecha_inicio"]').value;
    const fechaFin = this.querySelector('input[name="fecha_fin"]').value;

    // Validar fechas
    if (!fechaInicio || !fechaFin || fechaInicio > fechaFin) {
        alert('Selecciona un rango de fechas válido.');
        return;
    }

    fetch(`/api/dashboard/stats?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`)
        .then(response => {
            if (!response.ok) throw new Error("Error en la solicitud");
            return response.json();
        })
        .then(data => {
            console.log("Datos personalizados:", data);

            document.getElementById("ventasTotales").innerText =
                data.ventas_totales.toLocaleString("es-CO", {
                    style: "currency",
                    currency: "COP",
                    minimumFractionDigits: 0
                })
                document.getElementById("numeroVentas").innerText = data.numero_ventas;
                document.getElementById("nuevosClientes").innerText = data.nuevos_clientes;

                    const modal = bootstrap.Modal.getInstance(document.getElementById('modalFechaPersonalizada'));
                    modal.hide();
                })
                    .catch(err => {
                        console.error(err);
                        alert('Ocurrió un error al obtener los datos.');
                    });
        });