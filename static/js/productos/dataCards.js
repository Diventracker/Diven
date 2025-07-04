let lista; // para acceso global

async function actualizarProductos() {
  const response = await fetch("/productos/data");
  const productos = await response.json();

  const listaContainer = document.querySelector("#productos-lista .list");
  listaContainer.innerHTML = "";

  const rol = document.body.dataset.rol;

  for (const p of productos) {
    const card = document.createElement("div");
    card.className = "col-6 col-md-4 col-xl-2 mb-4";

    // Badge de stock
    let stockColor = "bg-success";
    if (p.stock < 5) {
      stockColor = "bg-danger";
    } else if (p.stock < 10) {
      stockColor = "bg-warning text-dark";
    }

    // Botones solo si es administrador
    let botones = "";
    if (rol === "Administrador") {
      botones = `
        <div class="mt-2">
          <button class="btn btn-sm btn-outline-secondary me-1 edit-button"
              data-bs-toggle="modal" data-bs-target="#modalEditar"
              data-id="${p.id}" data-nombre="${p.nombre}" data-modelo="${p.modelo}"
              data-descripcion="${p.descripcion}" data-precio="${p.precio}"
              data-precioVenta="${p.precio}" data-idProveedor="${p.id_proveedor}"
              data-nombreProveedor="${p.proveedor}" data-garantia="${p.garantia || ''}">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" data-bs-toggle="modal"
              data-bs-target="#modalEliminar" data-id="${p.id}" data-nombre="${p.nombre}">
            <i class="bi bi-trash"></i>
          </button>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="card h-100 shadow-sm">
        <img src="${p.imagen_url}" class="card-img-top" style="height: 120px; object-fit: cover;" alt="${p.nombre}">
        <div class="card-body d-flex flex-column">
          <div>
            <h5 class="card-title nombre">${p.nombre}</h5>
            <p class="card-text">${p.descripcion}</p>
            <p class="card-text mb-1">
              <strong>Precio:</strong> $<span class="precio">${p.precio}</span>
            </p>
          </div>
          <div class="mt-auto d-flex justify-content-between align-items-center">
            <span class="badge ${stockColor}">Stock: ${p.stock}</span>
            <div>
              ${botones}
            </div>
          </div>
        </div>
      </div>
    `;
    listaContainer.appendChild(card);
  }

  lista = new List('productos-lista', {
    valueNames: ['nombre', 'precio'],
    page: 12,
    pagination: true
  });

  createCustomPagination();
  configurarBuscador();
}

function createCustomPagination() {
  const paginationContainer = document.querySelector('#productos-lista .pagination');
  if (!paginationContainer) return;

  const totalPages = Math.ceil(lista.size() / lista.page);
  let currentPage = 1;

  const renderPagination = () => {
    paginationContainer.innerHTML = '';

    // Botón Anterior
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#">Anterior</a>`;
    prevLi.addEventListener('click', (e) => {
      e.preventDefault();
      if (currentPage > 1) {
        currentPage--;
        lista.show((currentPage - 1) * lista.page + 1, lista.page);
        renderPagination();
      }
    });
    paginationContainer.appendChild(prevLi);

    // Botones numerados
    for (let i = 1; i <= totalPages; i++) {
      const li = document.createElement('li');
      li.className = `page-item ${i === currentPage ? 'active' : ''}`;
      li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
      li.addEventListener('click', (e) => {
        e.preventDefault();
        currentPage = i;
        lista.show((currentPage - 1) * lista.page + 1, lista.page);
        renderPagination();
      });
      paginationContainer.appendChild(li);
    }

    // Botón Siguiente
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#">Siguiente</a>`;
    nextLi.addEventListener('click', (e) => {
      e.preventDefault();
      if (currentPage < totalPages) {
        currentPage++;
        lista.show((currentPage - 1) * lista.page + 1, lista.page);
        renderPagination();
      }
    });
    paginationContainer.appendChild(nextLi);
  };

  renderPagination();
}

function configurarBuscador() {
  const inputBusqueda = document.getElementById("buscador");
  const btnBuscar = document.getElementById("btn-buscar");
  const btnLimpiar = document.getElementById("btn-limpiar-filtros");

  // Buscar al hacer clic
  btnBuscar?.addEventListener("click", () => {
    const query = inputBusqueda.value.trim();
    lista.search(query);
  });

  // Buscar al presionar "Enter"
  inputBusqueda?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const query = inputBusqueda.value.trim();
      lista.search(query);
    }
  });

  // Limpiar filtros
  btnLimpiar?.addEventListener("click", () => {
    inputBusqueda.value = "";
    lista.search();
    lista.show(1, lista.page); // reinicia a la página 1
  });
}

document.addEventListener("DOMContentLoaded", actualizarProductos);
