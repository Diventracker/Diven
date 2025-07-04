$(document).ready(function () {
  const rol = document.body.dataset.rol;
  const esAdmin = rol === 'Administrador';

  const columnasProveedores = [
    { data: 'fecha_registro' },
    { data: 'nit' },
    { data: 'nombre_proveedor' },
    { data: 'representante_ventas' },
    { data: 'telefono_representante_ventas' },
    { data: 'direccion_proveedor' }
  ];

  // Agregar acciones solo si es administrador
  if (esAdmin) {
    columnasProveedores.push({
      data: null,
      orderable: false,
      searchable: false,
      render: function (data, type, row) {
        return `
          <button class="btn btn-sm btn-outline-secondary me-1 edit-button" data-bs-toggle="modal" data-bs-target="#modalEditar"
                data-id="${row.id_proveedor}"
                data-nit="${row.nit}"
                data-nombreP="${row.nombre_proveedor}"
                data-representante="${row.representante_ventas}"
                data-telefonoR="${row.telefono_representante_ventas}"
                data-direccion="${row.direccion_proveedor}">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#modalEliminar"
                    data-id="${row.id_proveedor}"
                    data-nombre="${row.nombre_proveedor}">
                <i class="bi bi-trash"></i>
            </button>
        `;
      }
    });
  }

  window.tablaProveedores = inicializarDataTable('tablaProveedores', '/proveedores/data', columnasProveedores);
});