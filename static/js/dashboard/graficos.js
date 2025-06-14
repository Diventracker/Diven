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

// === GRÁFICO DE PRODUCTOS MÁS VENDIDOS ===
function cargarProductosMasVendidos() {
  fetch("/api/dashboard/productos-mas-vendidos")
    .then(res => res.json())
    .then(data => {
      const contenedor = document.getElementById("productosMasVendidos");
      contenedor.innerHTML = "";

      if (data.length === 0) {
        contenedor.innerHTML = `<div class="text-center text-muted">No hay productos vendidos aún.</div>`;
        return;
      }

      const maxCantidad = data[0].cantidad;

      data.forEach(prod => {
        const item = document.createElement("div");
        const logMax = Math.log10(maxCantidad + 1);
        const escala = Math.log10(prod.cantidad + 1) / logMax;
        const ancho = Math.round(escala * 100);

        

        item.className = "product-item";
        item.innerHTML = `
          <div class="product-name">${prod.producto}</div>
          <div class="product-bar" style="width: ${ancho}%;"></div>
          <div class="product-value">${prod.cantidad}</div>
        `;
        contenedor.appendChild(item);
      });

      // Botón "ver todos"
      const verMas = document.createElement("div");
      verMas.className = "mt-3 text-center";
      verMas.innerHTML = `<a class="btn btn-outline-teal" href="/inventario">ver todos los productos</a>`;
      contenedor.appendChild(verMas);
    })
    .catch(err => {
      console.error("Error al cargar productos más vendidos:", err);
    });
}

document.addEventListener("DOMContentLoaded", cargarProductosMasVendidos);

// === TOTAL POR VENDEDOR ===
function cargarGraficoVentasPorVendedor() {
  fetch("/api/dashboard/ventas-vendedor")
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
            label: "Total vendido (COP)",
            data: totales,
            backgroundColor: "#5e9188"
          }]
        },
        options: {
          responsive: true,
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
          plugins: {
            legend: {
              position: "bottom"
            }
          }
        }
      });
    })
    .catch(err => console.error("Error al cargar gráfico tipo equipo:", err));
}

document.addEventListener("DOMContentLoaded", cargarGraficoTipoEquipo);


