// esta funcion se encarga de mostrar la informacion de dia
function cargarEstadisticasHoy() {
    fetch("/api/dashboard/stats/hoy")
        .then(res => {
            if (!res.ok) {
                throw new Error(`Error del servidor: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            document.getElementById("ventasTotales").innerText = 
                data.ventas_totales.toLocaleString("es-CO", {
                    style: "currency",
                    currency: "COP",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                });
            document.getElementById("numeroVentas").innerText = 
                data.numero_ventas.toLocaleString("es-CO");
            document.getElementById("nuevosClientes").innerText = 
                data.nuevos_clientes.toLocaleString("es-CO");
        })
        .catch(error => {
            console.error("Error al cargar estadísticas del día:", error);
        });
}

document.addEventListener("DOMContentLoaded", function () {
    cargarEstadisticasHoy();
});

// Este script se encarga de cargar las estadísticas del dashboard
function cargarEstadisticas(periodo) {
    fetch(`/api/dashboard/stats/${periodo}`)
        .then(res => {
            if (!res.ok) {
                throw new Error(`Error del servidor: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            document.getElementById("ventasTotales").innerText = 
                data.ventas_totales.toLocaleString("es-CO", {
                    style: "currency",
                    currency: "COP",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                });
            document.getElementById("numeroVentas").innerText = 
                data.numero_ventas.toLocaleString("es-CO");
            document.getElementById("nuevosClientes").innerText = 
                data.nuevos_clientes.toLocaleString("es-CO");
        })
        .catch(error => {
            console.error("Error al obtener estadísticas:", error);
        });
}

// Ejecutar automáticamente al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    cargarEstadisticas("hoy");
});

// Cargar estadísticas al inicio con el periodo por defecto
document.querySelectorAll("button[data-periodo]").forEach(btn => {
    btn.addEventListener("click", () => {
        const periodo = btn.getAttribute("data-periodo");
        fetch(`/api/dashboard/stats/${periodo}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById("ventasTotales").innerText = 
                    data.ventas_totales.toLocaleString("es-CO", {
                        style: "currency",
                        currency: "COP",
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0
                    });
                document.getElementById("numeroVentas").innerText = 
                    data.numero_ventas.toLocaleString("es-CO");
                document.getElementById("nuevosClientes").innerText = 
                    data.nuevos_clientes.toLocaleString("es-CO");
            })
            .catch(err => console.error("Error:", err));
    });
});