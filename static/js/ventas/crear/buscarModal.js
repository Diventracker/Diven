// ======= Estado y helpers =======
let productosData = [];        // respuesta del backend
let filtrados = [];            // data tras filtros
let currentPage = 1;
let pageSize = 12;             // 3 filas (se recalcula por pantalla)
let debounceTimer = null;
let productoActual = null;     // producto actualmente seleccionado para el modal de cantidad
let reservas = {};             // { codigo: cantidad_en_tabla }

function getColsPerRow() {
  const w = window.innerWidth;
  if (w >= 992) return 4;  // lg: 4 por fila → 3 filas => 12
  if (w >= 768) return 3;  // md: 3 por fila → 3 filas => 9
  return 2;                // sm: 2 por fila → 3 filas => 6
}
function recalcPageSize() { pageSize = getColsPerRow() * 3; }

async function cargarProductos(search = "", conStock = true) {
  try {
    const res = await fetch(`/api/productos?search=${encodeURIComponent(search)}&con_stock=${conStock}`);
    const productos = await res.json();
    productosData = Array.isArray(productos) ? productos : [];
    aplicarFiltrosYRender();
  } catch (e) {
    console.error("Error al cargar productos:", e);
  }
}

// Lee la tabla de la venta (#tabla-productos) y arma el mapa de reservas
function reconstruirReservasDesdeTabla() {
  reservas = {};
  const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
  filas.forEach(fila => {
    const codigo = fila.cells[0]?.textContent.trim();
    const input = fila.querySelector(".cantidad-input");
    const cant = parseInt(input?.value || "0", 10) || 0;
    if (!codigo) return;
    reservas[codigo] = (reservas[codigo] || 0) + cant;
  });
}

function cargarProductosDesdeUI() {
  const termino = document.getElementById("input-busqueda-modal")?.value.trim() || "";
  const conStock = document.getElementById("filtro-stock")?.value === "true";
  cargarProductos(termino, conStock);
}

// ======= Filtro + render =======
function aplicarFiltrosYRender() {
  // Ajustar catálogo con lo que ya está en la tabla (reservas)
  reconstruirReservasDesdeTabla();

  const termino = document.getElementById("input-busqueda-modal")?.value.trim().toLowerCase() || "";
  const conStock = document.getElementById("filtro-stock")?.value === "true";

  filtrados = productosData.filter(p => {
    if (conStock && p.stock <= 0) return false; // si p.stock==0 ni siquiera se considera
    if (!termino) return true;
    const hay = (p.nombre || "").toLowerCase().includes(termino)
             || (p.modelo || "").toLowerCase().includes(termino)
             || (String(p.codigo) || "").toLowerCase().includes(termino);
    return hay;
  });

  const totalPages = Math.max(1, Math.ceil(filtrados.length / pageSize));
  if (currentPage > totalPages) currentPage = 1;

  renderPagina();
  actualizarInfoPaginacion();
}

function renderPagina() {
  const grid = document.getElementById("catalogoProductos");
  grid.innerHTML = "";

  const start = (currentPage - 1) * pageSize;
  const end = start + pageSize;
  const pageItems = filtrados.slice(start, end);

  pageItems.forEach(p => {
    const reservado = reservas[String(p.codigo)] || 0;
    const disponible = Math.max(0, Number(p.stock || 0) - reservado);
    const sinStock = disponible <= 0;

    const col = document.createElement("div");
    col.className = "col-6 col-md-4 col-lg-3";

    col.innerHTML = `
      <div class="card h-100 shadow-sm d-flex flex-column">
        <img src="${p.imagen_url}" class="card-img-top" alt="${p.nombre}" style="object-fit:contain;height:150px;">
        <div class="card-body d-flex flex-column">
          <h6 class="card-title" title="${p.nombre}">${p.nombre}</h6>
          <p class="text-muted small">${p.modelo || "-"}</p>
          <p class="fw-bold mb-1">$${Number(p.precio||0).toLocaleString("es-CO")}</p>
          <span class="badge ${sinStock ? "bg-danger" : "bg-success"} mb-2">
            ${sinStock ? "Sin stock" : `Disponible: ${disponible}`}
          </span>
          <button class="btn btn-sm ${sinStock?"btn-secondary":"btn-enviar"} w-100 mt-auto" ${sinStock?"disabled":""}>
            <i class="bi bi-plus-lg me-1"></i>Agregar
          </button>
        </div>
      </div>
    `;

    const btn = col.querySelector("button");
    if (!sinStock) btn.addEventListener("click", () => abrirModalCantidad(p));

    grid.appendChild(col);
  });

  if (!pageItems.length) {
    grid.innerHTML = `<div class="col-12 text-center text-muted">Sin resultados</div>`;
  }
}

function actualizarInfoPaginacion() {
  const info = document.getElementById("catalogoPageInfo");
  const totalPages = Math.max(1, Math.ceil(filtrados.length / pageSize));
  info.textContent = `Página ${currentPage}/${totalPages}`;

  document.getElementById("catalogoPrev").disabled = currentPage <= 1;
  document.getElementById("catalogoNext").disabled = currentPage >= totalPages;
}

// ======= Modal de Cantidad =======
function abrirModalCantidad(prod) {
  productoActual = prod;

  const reservado = reservas[String(prod.codigo)] || 0;
  const disponible = Math.max(0, Number(prod.stock || 0) - reservado);

  document.getElementById("qtyProductoNombre").textContent =
    `${prod.nombre}${prod.modelo ? " ("+prod.modelo+")" : ""}`;

  // contexto visible
  document.getElementById("qtyProductoStock").textContent =
    `Stock total: ${prod.stock}  |  Ya en venta: ${reservado}`;
  document.getElementById("qtyMax").textContent = disponible;

  const qtyInput = document.getElementById("qtyInput");
  qtyInput.value = 1;
  qtyInput.min = 1;
  qtyInput.max = disponible;

  const m = bootstrap.Modal.getOrCreateInstance(document.getElementById("qtyModal"));
  m.show();
  setTimeout(()=>qtyInput.focus(), 100);
}

function confirmarCantidadYAgregar() {
  if (!productoActual) return;

  // tope por disponible (stock - reservado)
  const reservado = reservas[String(productoActual.codigo)] || 0;
  const disponible = Math.max(0, Number(productoActual.stock || 0) - reservado);

  const qtyInput = document.getElementById("qtyInput");
  let cantidad = parseInt(qtyInput.value, 10);

  if (isNaN(cantidad) || cantidad < 1) cantidad = 1;
  if (cantidad > disponible) cantidad = disponible;

  if (cantidad <= 0) {
    const m0 = bootstrap.Modal.getInstance(document.getElementById("qtyModal"));
    m0?.hide();
    productoActual = null;
    return;
  }

  agregarProductoConCantidad(productoActual, cantidad);

  const m = bootstrap.Modal.getInstance(document.getElementById("qtyModal"));
  m?.hide();
  productoActual = null;
}

// Agrega N unidades a la tabla de venta usando tu flujo existente
function agregarProductoConCantidad(producto, cantidad) {
  // 1) Buscar fila existente
  const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
  let fila = null;
  filas.forEach(f => {
    const cod = f.cells[0]?.textContent.trim();
    if (cod === String(producto.codigo)) fila = f;
  });

  // 2) Si no existe, crea la fila con 1 y localízala
  if (!fila) {
    agregarFilaProducto({
      codigo: producto.codigo,
      nombre: `${producto.nombre} ${producto.modelo || ""}`.trim(),
      precio: producto.precio,
      stock: producto.stock
    });
    const filas2 = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
    filas2.forEach(f => {
      const cod = f.cells[0]?.textContent.trim();
      if (cod === String(producto.codigo)) fila = f;
    });
  }
  if (!fila) return;

  // 3) Disponible actual = stock - reservadoAntes
  const reservadoAntes = reservas[String(producto.codigo)] || 0;
  const disponible = Math.max(0, Number(producto.stock || 0) - reservadoAntes);

  // 4) Ajustar la cantidad final en la fila
  const input = fila.querySelector(".cantidad-input");
  let actual = parseInt(input.value || "1", 10);
  if (isNaN(actual) || actual < 1) actual = 1;

  // Si la fila es nueva (acabamos de crearla con 1), ponemos exactamente 'cantidad';
  // si ya existía, sumamos, pero nunca superando actual + disponible.
  let nueva;
  if (actual === 1 && reservadoAntes + 1 <= producto.stock) {
    nueva = Math.min(cantidad, disponible);    // recién creada → cantidad exacta hasta el tope
    if (nueva < 1) nueva = 1;
  } else {
    nueva = Math.min(actual + cantidad, actual + disponible); // fila ya existente
  }

  input.value = nueva;
  // dispara tu cálculo de subtotal/total (ya manejado en tu app)
  input.dispatchEvent(new Event("input", { bubbles: true }));

  // 5) Refrescar reservas y catálogo (para que el badge "Disponible" cambie en vivo)
  reconstruirReservasDesdeTabla();
  aplicarFiltrosYRender();
}

/* ======= Wiring ======= */
document.getElementById("productosModal")?.addEventListener("shown.bs.modal", () => {
  recalcPageSize();
  reconstruirReservasDesdeTabla();   // asegura reservas vigentes
  cargarProductosDesdeUI();
});

document.getElementById('filtro-stock')?.addEventListener('change', () => {
  aplicarFiltrosYRender();
});

document.getElementById("catalogoPrev")?.addEventListener("click", () => {
  if (currentPage > 1) { currentPage--; renderPagina(); actualizarInfoPaginacion(); }
});
document.getElementById("catalogoNext")?.addEventListener("click", () => {
  const totalPages = Math.max(1, Math.ceil(filtrados.length / pageSize));
  if (currentPage < totalPages) { currentPage++; renderPagina(); actualizarInfoPaginacion(); }
});

// búsqueda en vivo (debounce)
document.getElementById("input-busqueda-modal")?.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => { aplicarFiltrosYRender(); }, 250);
});

// limpiar búsqueda
document.getElementById("btn-limpiar-busqueda")?.addEventListener("click", () => {
  const input = document.getElementById("input-busqueda-modal");
  input.value = "";
  aplicarFiltrosYRender();
  input.focus();
});

// Confirmar cantidad del modal
document.getElementById("qtyConfirmBtn")?.addEventListener("click", confirmarCantidadYAgregar);

// Recalcular tamaño de página (3 filas) si cambia el ancho
window.addEventListener("resize", () => {
  const old = pageSize;
  recalcPageSize();
  if (pageSize !== old) {
    currentPage = 1;
    renderPagina();
    actualizarInfoPaginacion();
  }
});

// Mantener reservas sincronizadas si cambian cantidades o se elimina una fila en la tabla de venta
const tbodyVenta = document.querySelector("#tabla-productos tbody");
if (tbodyVenta) {
  // Cambio de cantidades
  tbodyVenta.addEventListener("input", (ev) => {
    if (ev.target && ev.target.classList.contains("cantidad-input")) {
      setTimeout(() => {
        reconstruirReservasDesdeTabla();
        aplicarFiltrosYRender();
      }, 0);
    }
  });

  // Eliminaciones / clicks en acciones
  tbodyVenta.addEventListener("click", () => {
    setTimeout(() => {
      reconstruirReservasDesdeTabla();
      aplicarFiltrosYRender();
    }, 0);
  });
}

document.addEventListener('DOMContentLoaded', () => { recalcPageSize(); });