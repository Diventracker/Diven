$(document).ready(function () {
  const rol = document.body.dataset.rol;
  const esAdmin = rol === 'Administrador';

  const columnasClientes = [
    { data: 'fecha_registro' },
    { data: 'nombre_cliente' },
    { data: 'tipo_documento' },
    { data: 'numero_documento' },
    { data: 'direccion_cliente' },
    { data: 'telefono_cliente' },
    { data: 'email_cliente' }
  ];

  // Agregar acciones solo si es administrador
  if (esAdmin) {
    columnasClientes.push({
      data: null,
      orderable: false,
      searchable: false,
      render: function (data, type, row) {
        return `
          <button class="btn btn-sm btn-outline-secondary me-1 edit-button"
                  data-bs-toggle="modal" data-bs-target="#modalEditar"
                  data-id="${row.id_cliente}"
                  data-nombre="${row.nombre_cliente}"
                  data-tipodocumento="${row.tipo_documento}"
                  data-numerodocumento="${row.numero_documento}"
                  data-telefono="${row.telefono_cliente}"
                  data-direccion="${row.direccion_cliente}"
                  data-email="${row.email_cliente}">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger"
                  data-bs-toggle="modal" data-bs-target="#modalEliminar"
                  data-id="${row.id_cliente}"
                  data-nombre="${row.nombre_cliente}">
            <i class="bi bi-trash"></i>
          </button>
        `;
      }
    });
  }

  window.tablaClientes = inicializarDataTable('tablaClientes', '/clientes/data', columnasClientes);
});
