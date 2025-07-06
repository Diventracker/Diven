// === TOTAL POR CATEGORÍA ===
function cargarGraficoTipoEquipo() {
  fetch("/api/dashboard/servicios-por-equipo")
    .then(res => res.json())
    .then(data => {
      const etiquetas = data.map(item => item.equipo);
      const valores = data.map(item => item.total);

      const colores = [
        "#0a516d", "#018790", "#7dad93", "#bacca4", "#ffc107",
        "#fd7e14", "#dc3545", "#6f42c1", "#20c997", "#17a2b8"
      ];

      const ctx = document.getElementById("graficoTipoEquipo").getContext("2d");
      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: etiquetas,
          datasets: [{
            data: valores,
            backgroundColor: colores.slice(0, valores.length),
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "right"
            }
          }
        }
      });
    })
    .catch(err => console.error("Error al cargar gráfico tipo equipo:", err));
}

document.addEventListener("DOMContentLoaded", cargarGraficoTipoEquipo);