// === TOTAL POR VENDEDOR ===
function cargarGraficoVentasPorVendedor() {
  fetch("/ventas/ventas-vendedor")
    .then(res => res.json())
    .then(data => {
      const nombres = data.map(d => d.vendedor);
      const totales = data.map(d => d.total);

      const ctx = document.getElementById("graficoVentasVendedor").getContext("2d");

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: nombres,
          datasets: [{
            // Sin label
            data: totales,
            backgroundColor: "#5e9188"
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false // Oculta la leyenda
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const value = context.raw;
                  return new Intl.NumberFormat('es-CO', {
                    style: 'currency',
                    currency: 'COP',
                    minimumFractionDigits: 0
                  }).format(value);
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return new Intl.NumberFormat('es-CO', {
                    style: 'currency',
                    currency: 'COP',
                    minimumFractionDigits: 0
                  }).format(value);
                }
              }
            }
          }
        }
      });
    })
    .catch(err => console.error("Error al cargar gráfico de vendedores:", err));
}


document.addEventListener("DOMContentLoaded", cargarGraficoVentasPorVendedor);