//Funcion para la card de localizar productos con bajo stock
function obtenerProductosBajoStock() {
  fetch('/stock/bajo')
    .then(response => response.json())
    .then(data => {
      const contenedor = document.querySelector("#productosBajoStock");
      contenedor.innerHTML = ""; // Limpiar

      if (data.length === 0) {
        contenedor.innerHTML = `
          <span class="text-muted small">Todos los productos tienen stock suficiente.</span>
        `;
        return;
      }

      // Mostrar solo los primeros 4
      data.slice(0, 4).forEach(producto => {
        let badgeClass = "bg-success";
        let textoEstado = "Stock suficiente";

        if (producto.stock < 5) {
          badgeClass = "bg-danger";
          textoEstado = "Stock crítico";
        } else if (producto.stock < 10) {
          badgeClass = "bg-warning text-dark";
          textoEstado = "Stock bajo";
        }

        const item = `
          <a href="/productos" class="list-group-item list-group-item-action py-3 producto-alerta"
            data-id="${producto.codigo}"
            data-nombre="${producto.nombre}"
            data-descripcion="${producto.descripcion}"
            data-proveedor="${producto.proveedor}"
            data-stock="${producto.stock}">
            <div class="d-flex w-100 justify-content-between">
              <h6 class="mb-1">${producto.nombre} (${producto.modelo})</h6>
              <span class="badge ${badgeClass}">${textoEstado}</span>
            </div>
            <p class="mb-1 small text-muted">Quedan ${producto.stock} unidades (mínimo: 5)</p>
          </a>
        `;
        contenedor.insertAdjacentHTML("beforeend", item);
      });
    });
}

document.addEventListener("DOMContentLoaded", () => {
  obtenerProductosBajoStock();
});
