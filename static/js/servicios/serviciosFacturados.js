async function cargarGraficoIngresos() {
    const resp = await fetch('/ingresos/grafico/mensual'); // <- NUEVO endpoint
    const datos = await resp.json(); // { labels: [...], data: [...] }

    const ctx = document.getElementById('graficoIngresos').getContext('2d');

    if (window.chartIngresos) {
        window.chartIngresos.data.labels = datos.labels;
        window.chartIngresos.data.datasets[0].data = datos.data;
        window.chartIngresos.update();
        return;
    }

    window.chartIngresos = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datos.labels,
            datasets: [{
                label: `Ingresos por mes (COP) ${datos.year}`,
                data: datos.data,
                borderWidth: 2,
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76,175,80,0.45)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => v.toLocaleString('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 })
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: ctx => (ctx.parsed.y || 0).toLocaleString('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 })
                    }
                }
            }
        }
    });
}
