$(document).ready(function () {
    $.ajax({
        url: "/api/dashboard/stats",
        method: "GET",
        success: function (data) {
            $("#ventasTotales").text(`$${Number(data.ventas_totales).toLocaleString()}`);
            $("#numeroVentas").text(data.numero_ventas);
            $("#nuevosClientes").text(data.nuevos_clientes);
        },
        error: function (xhr, status, error) {
            console.error("Error al obtener estadísticas:", error);
        }
    });
});