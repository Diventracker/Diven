async function buscarProducto() {
    const input = document.getElementById("buscador-producto");
    const termino = input.value.trim();

    if (!termino) return;

    try {
        const res = await fetch(`/productos/buscar/${termino}`);
        if (!res.ok) throw new Error("Producto no encontrado");

        const producto = await res.json();

        // Validar stock antes de agregar
        if (producto.stock <= 0) {
            alert(`No hay stock disponible para ${producto.descripcion}`);
            return;
        }

        agregarFilaProducto(producto);
        input.value = "";
    } catch (err) {
        alert("Producto no encontrado.");
    }
}

function agregarFilaProducto(producto) {
    const tabla = document.querySelector("#tabla-productos tbody");
    const filas = tabla.querySelectorAll("tr:not(.table-active)");

    let productoYaAgregado = false;

    filas.forEach(fila => {
        const codigo = fila.cells[0]?.textContent.trim();
        if (codigo === String(producto.codigo).trim()) {
            const inputCantidad = fila.querySelector(".cantidad-input");
            let cantidadActual = parseInt(inputCantidad.value) || 0;

            if (cantidadActual + 1 > producto.stock) {
                alert(`Solo hay ${producto.stock} unidades disponibles de ${producto.descripcion}`);
                return;
            }

            cantidadActual += 1;
            inputCantidad.value = cantidadActual;

            const nuevoSubtotal = cantidadActual * producto.precio;
            fila.querySelector(".subtotal").textContent = nuevoSubtotal.toLocaleString('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });

            productoYaAgregado = true;
        }
    });

    if (!productoYaAgregado) {
        const fila = document.createElement("tr");
        const precioUnitario = producto.precio;

        fila.innerHTML = `
          <td>${producto.codigo}</td>
          <td>${producto.descripcion}</td>
          <td>${precioUnitario.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 })}</td>
          <td>
            <input type="number" value="1" min="1" class="form-control cantidad-input mx-auto" style="width: 70px;">
          </td>
          <td class="subtotal">${precioUnitario.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 })}</td>
          <td>
            <button class="btn btn-sm btn-outline-danger" onclick="this.closest('tr').remove(); actualizarTotal();"><i class="bi bi-trash"></i></button>
          </td>
        `;

        const filaTotal = tabla.querySelector("tr.table-active");
        tabla.insertBefore(fila, filaTotal);

        const inputCantidad = fila.querySelector(".cantidad-input");
        inputCantidad.addEventListener("input", () => {
            let cantidad = parseInt(inputCantidad.value) || 1;

            if (cantidad > producto.stock) {
                alert(`Solo hay ${producto.stock} unidades disponibles`);
                cantidad = producto.stock;
                inputCantidad.value = cantidad;
            }

            const subtotal = cantidad * producto.precio;
            fila.querySelector(".subtotal").textContent = subtotal.toLocaleString('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });

            actualizarTotal();
        });
    }

    actualizarTotal();
}

function actualizarTotal() {
    const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
    let total = 0;

    filas.forEach(fila => {
        const subtotalTexto = fila.querySelector(".subtotal").textContent
  .replace(/\$/g, '')      // quita el signo $
  .replace(/\./g, '')      // quita separador de miles (.)
  .replace(/,/g, '.');     // convierte coma decimal (si aparece) a punto

        total += parseFloat(subtotalTexto);
    });

    document.getElementById("total-venta").textContent = total.toLocaleString('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
}
