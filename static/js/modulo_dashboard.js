// Cargar gráficos al terminar de cargar el DOM
document.addEventListener('DOMContentLoaded', function () {
    // === GRÁFICO DE VENTAS ===
    const salesCtx = document.getElementById('salesChart').getContext('2d');
    new Chart(salesCtx, {
        type: 'line',
        data: {
            labels: ['1 May', '5 May', '10 May', '15 May', '20 May', '25 May', '30 May'],
            datasets: [{
                label: 'Ventas ($)',
                data: [5200, 7800, 12500, 14800, 18200, 21500, 24580],
                backgroundColor: 'rgba(94, 145, 136, 0.2)',
                borderColor: '#5e9188',
                borderWidth: 2,
                tension: 0.3,
                pointBackgroundColor: '#5e9188',
                pointBorderColor: '#fff',
                pointRadius: 4
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
