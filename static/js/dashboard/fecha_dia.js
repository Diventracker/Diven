
document.getElementById("btn-hoy").addEventListener("click", function () {
    fetch("/api/dashboard/stats/today")
        .then(response => response.json())
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
        .catch(error => console.error("Error al obtener datos de hoy:", error));
});

