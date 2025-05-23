let productosSeleccionados = {};

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

function llenarTablaProductosModal(productos) {
    const cuerpoTabla = document.querySelector("#tabla-productos-modal tbody");
    cuerpoTabla.innerHTML = "";

    productos.forEach(producto => {
        const fila = document.createElement("tr");
        const seleccionado = !!productosSeleccionados[producto.codigo];

        fila.innerHTML = `
            <td>${producto.codigo}</td>
            <td>${producto.descripcion}</td>
            <td>${producto.modelo || "-"}</td>
            <td>${producto.stock}</td>
            <td>$${producto.precio.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm ${seleccionado ? "btn-secondary" : "btn-enviar"}">
                    <i class="bi bi-${seleccionado ? "check" : "plus-circle"}"></i> ${seleccionado ? "Agregado" : "Agregar"}
                </button>
            </td>
        `;

        // Agregamos evento click al botón:
        const boton = fila.querySelector("button");
        boton.addEventListener("click", () => {
            seleccionarProductoDesdeModal(producto);
        });

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
            descripcion: `${producto.descripcion} ${producto.modelo}`,
            precio: producto.precio,
            stock: producto.stock
        });
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
document.getElementById("productosModal")?.addEventListener('shown.bs.modal', cargarProductosDesdeUI);

// Cargar inicialmente al abrir página (por si quieres que algo se muestre antes)
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
});