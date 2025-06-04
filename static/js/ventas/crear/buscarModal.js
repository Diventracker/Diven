let productosSeleccionados = {};
let productosYaAgregados = new Set();

function reconstruirProductosYaAgregados() {
    productosYaAgregados.clear();

    const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
    filas.forEach(fila => {
        const codigo = fila.cells[0]?.textContent.trim();
        if (codigo) productosYaAgregados.add(codigo);
    });
}



async function cargarProductos(search = "", conStock = true) {
    try {
        const res = await fetch(`/api/productos?search=${encodeURIComponent(search)}&con_stock=${conStock}`);
        const productos = await res.json();
        llenarTablaProductosModal(productos);
    } catch (error) {
        console.error("Error al cargar productos:", error);
    }
}

function cargarProductosDesdeUI() {
    const termino = document.getElementById("input-busqueda-modal")?.value.trim() || "";
    const conStock = document.getElementById("filtro-stock")?.value === "true";
    cargarProductos(termino, conStock);
}

//ya esta funcion llena los productos en la tabla, segun si no fueron seleccionados ya
function llenarTablaProductosModal(productos) {
    const cuerpoTabla = document.querySelector("#tabla-productos-modal tbody");
    cuerpoTabla.innerHTML = "";

    productos.forEach(producto => {
        if (productosYaAgregados.has(producto.codigo)) return; // <-- Salta los ya agregados

        const fila = document.createElement("tr");
        const seleccionado = !!productosSeleccionados[producto.codigo];
        const sinStock = producto.stock <= 0;

        const botonHtml = sinStock
            ? `<button class="btn btn-sm btn-secondary" disabled>
                <i class="bi bi-x-circle"></i> Sin stock
            </button>`
            : `<button class="btn btn-sm ${seleccionado ? "btn-secondary" : "btn-enviar"}">
                <i class="bi bi-${seleccionado ? "check" : "plus-circle"}"></i> ${seleccionado ? "Agregado" : "Agregar"}
            </button>`;

        fila.innerHTML = `
            <td>${producto.codigo}</td>
            <td>${producto.nombre}</td>
            <td>${producto.modelo || "-"}</td>
            <td>${producto.stock}</td>
            <td>$${producto.precio.toLocaleString("es-CO")}</td>
            <td>${botonHtml}</td>
        `;

        const boton = fila.querySelector("button");
        if (!sinStock) {
            boton.addEventListener("click", () => {
                seleccionarProductoDesdeModal(producto);
            });
        }

        cuerpoTabla.appendChild(fila);
    });
}



function seleccionarProductoDesdeModal(producto) {
    if (productosSeleccionados[producto.codigo]) {
        delete productosSeleccionados[producto.codigo];
    } else {
        productosSeleccionados[producto.codigo] = producto;
    }
    cargarProductosDesdeUI(); // refrescar botones
}

function agregarSeleccionadosATabla() {
    Object.values(productosSeleccionados).forEach(producto => {
        agregarFilaProducto({
            codigo: producto.codigo,
            nombre: `${producto.nombre} ${producto.modelo}`,
            precio: producto.precio,
            stock: producto.stock
        });

        // 🚫 Marcar como ya agregado
        productosYaAgregados.add(producto.codigo);
    });

    productosSeleccionados = {};
    cargarProductosDesdeUI(); // refrescar botones en el modal

    const modal = bootstrap.Modal.getInstance(document.getElementById("productosModal"));
    modal.hide(); // cerrar modal
}

// Eventos para filtros dentro del modal
// document.getElementById('input-busqueda-modal')?.addEventListener('input', cargarProductosDesdeUI);
// el de arriba lo comento por que busca autumaticamente mientras se escribe sxdxd
document.getElementById('filtro-stock')?.addEventListener('change', cargarProductosDesdeUI);

// Cargar productos cuando el modal se muestre
document.getElementById("productosModal")?.addEventListener('shown.bs.modal', () => {
    reconstruirProductosYaAgregados(); // Actualiza lo que ya está en la tabla
    cargarProductosDesdeUI();          // Vuelve a cargar el modal
});

// Cargar inicialmente al abrir página (por si quieres que algo se muestre antes)
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
});