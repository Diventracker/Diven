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


        item.className = "row align-items-center mb-2 product-item";
        item.innerHTML = `
        <div class="col-2 product-name text-truncate" title="${prod.producto}" style="font-weight: normal;">
            ${prod.producto}
        </div>
        <div class="col-8">
            <div class="progress" style="height: 14px; direction: rtl;">
            <div class="progress-bar" style="width: ${ancho}%"></div>
            </div>
        </div>
        <div class="col-2 text-center product-value">${prod.cantidad}</div>
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