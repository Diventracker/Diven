$(document).ready(function () {
  const rol = document.body.dataset.rol;
  const esAdmin = rol === 'Administrador';

  const columnasUsuarios = [
    { data: 'nombre_usuario' },
    { data: 'correo' },
    { data: 'telefono_usuario' },
    { data: 'rol' }
  ];

  // Agregar acciones solo si es administrador
  if (esAdmin) {
    columnasUsuarios.push({
      data: null,
      orderable: false,
      searchable: false,
      render: function (data, type, row) {
        return `
          <button
                class="btn btn-sm btn-outline-secondary me-1 edit-button"
                data-bs-toggle="modal"
                data-bs-target="#modalEditar"
                data-id="${row.id_usuario}"
                data-nombre="${row.nombre_usuario}"
                data-correo="${row.correo}"
                data-telefono="${row.telefono_usuario}"
                data-rol="${row.rol}">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger"
                data-bs-toggle="modal"
                data-bs-target="#modalEliminar"
                data-id="${row.id_usuario}"
                data-nombre="${row.nombre_usuario}">
                <i class="bi bi-trash"></i>
            </button>
        `;
      }
    });
  }

  window.tablaUsuarios = inicializarDataTable('tablaUsuarios', '/usuarios/data', columnasUsuarios);
});
