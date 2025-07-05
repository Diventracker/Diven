$(document).ready(function () {
  const rol = document.body.dataset.rol;
  const esAdmin = rol === 'Administrador';

  const columnasVentas = [
    { data: 'id_venta' },
    { data: 'fecha_venta' },
    { data: 'nombre_cliente' },
    { data: 'cantidad_productos' },
    { data: 'valor_venta' }
  ];

  // Agregar acciones solo si es administrador
  if (esAdmin) {
    columnasVentas.push({
      data: null,
      orderable: false,
      searchable: false,
      render: function (data, type, row) {
        return `
          <button class="btn btn-sm btn-outline-secondary "
            onclick="verDetalles(${row.id_venta})" data-bs-toggle="modal"
            data-bs-target="#modalDetalles">
            <i class="bi bi-eye"></i> Detalles
          </button>
          <button onclick="location.href='/ventas/comprobante/${row.id_venta}'"
                  class="btn btn-sm btn-outline-secondary me-1">
              <i class="bi bi-receipt"></i>
          </button>
        `;
      }
    });
  }

  window.tablaVentas = inicializarDataTable('tablaVentas', '/ventas/data', columnasVentas);
});
