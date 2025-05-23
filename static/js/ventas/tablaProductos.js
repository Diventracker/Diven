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
        const codigo = fila.cells[0]?.textContent.trim(); // primera celda = código
        if (codigo === String(producto.codigo).trim()) {
            // Producto ya existe en la tabla, actualizar cantidad y subtotal
            const inputCantidad = fila.querySelector(".cantidad-input");
            let cantidadActual = parseInt(inputCantidad.value) || 0;

            // 🔴 Validar contra el stock
            if (cantidadActual + 1 > producto.stock) {
                alert(`Solo hay ${producto.stock} unidades disponibles de ${producto.descripcion}`);
                return;
            }

            cantidadActual += 1;
            inputCantidad.value = cantidadActual;

            const nuevoSubtotal = cantidadActual * producto.precio;
            fila.querySelector(".subtotal").textContent = `$${nuevoSubtotal.toFixed(2)}`;

            productoYaAgregado = true;
        }
    });

    if (!productoYaAgregado) {
        const fila = document.createElement("tr");
        const precioUnitario = producto.precio.toFixed(2);

        fila.innerHTML = `
          <td>${producto.codigo}</td>
          <td>${producto.descripcion}</td>
          <td>$${precioUnitario}</td>
          <td>
            <input type="number" value="1" min="1" class="form-control cantidad-input mx-auto" style="width: 70px;">
          </td>
          <td class="subtotal">$${precioUnitario}</td>
          <td>
            <button class="btn btn-sm btn-outline-danger" onclick="this.closest('tr').remove(); actualizarTotal();"><i class="bi bi-trash"></i></button>
          </td>
        `;

        // Insertar antes de la fila TOTAL
        const filaTotal = tabla.querySelector("tr.table-active");
        tabla.insertBefore(fila, filaTotal);

        const inputCantidad = fila.querySelector(".cantidad-input");
        inputCantidad.addEventListener("input", () => {
            const cantidad = parseInt(inputCantidad.value) || 1;
            // 🔴 Validar stock manualmente

            if (cantidad > producto.stock) {
                alert(`Solo hay ${producto.stock} unidades disponibles`);
                inputCantidad.value = producto.stock;
                cantidad = producto.stock;
            }

            const subtotal = cantidad * producto.precio;
            fila.querySelector(".subtotal").textContent = `$${subtotal.toFixed(2)}`;
            actualizarTotal();
        });
    }

    actualizarTotal();
}



function eliminarFila(boton) {
    const fila = boton.closest("tr");
    fila.remove();
    actualizarTotal();
}

function actualizarTotal() {
    const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
    let total = 0;

    filas.forEach(fila => {
        const subtotalTexto = fila.querySelector(".subtotal").textContent.replace("$", "");
        total += parseFloat(subtotalTexto);
    });

    document.getElementById("total-venta").textContent = `$${total.toFixed(2)}`;
}
