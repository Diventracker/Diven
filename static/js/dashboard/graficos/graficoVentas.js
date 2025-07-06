document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch("/api/datos", { method: "POST" });
    const datos = await res.json();

    const ctx = document.getElementById('salesChart').getContext('2d');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: datos.labels,
        datasets: [{
          data: datos.data,
          fill: true,
          backgroundColor: 'rgba(94, 145, 136, 0.2)',
          borderColor: '#5e9188',
          pointBackgroundColor: '#5e9188',
          pointBorderColor: '#5e9188',
          tension: 0.3,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value =>
                new Intl.NumberFormat("es-CO", {
                  style: "currency",
                  currency: "COP",
                  minimumFractionDigits: 0
                }).format(value)
            }
          }
        },
        plugins: {
          legend: {
            display: false // oculta completamente la leyenda
          }
        }
      }
    });
  } catch (err) {
    console.error("Error al cargar gráfico de ventas:", err);
  }
});
