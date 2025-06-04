 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");

//Funcion para ver los detalles de cada venta 
async function verDetalles(idVenta) {
  try {
    const res = await fetch(`/ventas/detalle/${idVenta}`);
    if (!res.ok) throw new Error("No se pudo obtener la venta");

    const data = await res.json();

    document.querySelector("#modaldetalle .modal-title").textContent = `Venta #${idVenta}`;
    document.querySelector("[data-cliente]").textContent = data.cliente;
    document.querySelector("[data-fecha]").textContent = data.fecha;
    document.querySelector("[data-vendedor]").textContent = data.vendedor;
    document.querySelector("[data-total]").textContent = `$${data.total.toLocaleString('es-CO')}`;

    const tbody = document.getElementById("detalle-modal-body");
    tbody.innerHTML = "";

    if (data.detalles.length === 0) {
      tbody.innerHTML = `<tr><td colspan="2" class="text-center text-muted">Sin productos en esta venta</td></tr>`;
    } else {
      data.detalles.forEach(item => {
        const fila = `
          <tr>
            <td>${item.producto}</td>
            <td>${item.descripcion}</td>
          </tr>`;
        tbody.innerHTML += fila;
      });
    }

  } catch (error) {
    console.error("❌ Error al obtener los detalles:", error);
    alert("Error al obtener detalles de la venta");
  }
}
