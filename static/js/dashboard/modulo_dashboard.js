// Cargar gráficos al terminar de cargar el DOM
document.addEventListener('DOMContentLoaded', function () {
    // === GRÁFICO DE VENTAS ===
    async function mostrardatos() {
        const envio = await fetch("/api/datos" , { method: "post" });
        const datos = await envio.json();

        const salesCtx = document.getElementById('salesChart').getContext('2d')
        new Chart(salesCtx, {
            type: 'line',
            data: datos,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        })
    }
    mostrardatos();

    // === GRÁFICO DE CATEGORÍAS ===
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
            labels: ['Electrónicos', 'Accesorios', 'Hogar', 'Ropa', 'Otros'],
            datasets: [{
                data: [45, 25, 15, 10, 5],
                backgroundColor: [
                    '#5e9188',
                    '#3e5954',
                    '#253342',
                    '#6aaba1',
                    '#8fc3bb'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        boxWidth: 12,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: '#253342',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 10,
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });

    // === GRÁFICO DE VENDEDORES ===
    const sellerCtx = document.getElementById('sellerChart').getContext('2d');
    new Chart(sellerCtx, {
        type: 'bar',
        data: {
            labels: ['María L.', 'Carlos R.', 'Ana M.', 'Pedro D.', 'Laura S.'],
            datasets: [{
                label: 'Ventas ($)',
                data: [8500, 6200, 5100, 3800, 980],
                backgroundColor: '#5e9188',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#253342',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return `Ventas: $${context.raw.toLocaleString()}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(94, 145, 136, 0.1)'
                    },
                    ticks: {
                        callback: function (value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
});


//generar infrome
document.getElementById('form-informe').addEventListener('submit', async function (e) {
                e.preventDefault();
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());

                const response = await fetch('/api/generar-informe', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = "informe.pdf";
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                }
            });


//codigo de las cards ventas mes actual

document.addEventListener('DOMContentLoaded', function () {
        fetch('/api/ventas-totales')
            .then(response => response.json())
            .then(data => updateStats(data))
            .catch(error => console.error('Error al obtener los datos:', error));

        function updateStats(data) {
            const statValue = document.getElementById('stat-value');
            const statChange = document.getElementById('stat-change');

            statValue.textContent = `$${data.ventasTotales.toLocaleString()}`;
            statChange.innerHTML = `<i class="bi ${data.cambioPositivo ? 'bi-arrow-up' : 'bi-arrow-down'}"></i> ${data.cambioPorcentaje}% vs mes anterior`;
        }
    ;
});


//codigo cards de ventas nuevas al mes

document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/numero-ventas')
        .then(response => response.json())
        .then(data => updateNumeroVentas(data))
        .catch(error => console.error('Error al obtener número de ventas:', error));

    function updateNumeroVentas(data) {
        const statValue = document.getElementById('numeroVentas');
        const statChange = document.getElementById('cambio_ventas');

        statValue.textContent = data.ventasNumeros;
        statChange.innerHTML = `<i class="bi ${data.cambioPositivoNumero ? 'bi-arrow-up' : 'bi-arrow-down'}"></i> ${data.cambioPorcentajeNumero}% vs mes anterior`;
        statChange.classList.remove('positive', 'negative');
        statChange.classList.add(data.cambioPositivoNumero ? 'positive' : 'negative');
    }
});
