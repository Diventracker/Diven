const tablaMiniVentas = $(`#tablaVentas`).DataTable({
  dom: 't', // solo el contenido, sin buscador, sin info, sin paginación
  ajax: {
    url: '/ventas/data',
    dataSrc: function (json) {
      // Devuelve solo los primeros 5 registros
      return json.slice(0, 5);
    }
  },
  order: [],
  ordering: false, // Desactiva ordenamiento por columnas
  pageLength: 5,
  paging: false,     // sin paginación
  searching: false,  //  sin búsqueda
  info: false,       // sin info tipo "mostrando 1 de x"
  columns: [
    { data: 'id_venta' },
    { data: 'nombre_cliente' },
    { data: 'fecha_venta' },
    {
      data: 'cantidad_productos',
      render: function(data) {
        return data + ' Productos';
      }
    },
    { data: 'valor_venta' },
    { data: 'nombre_usuario' }
  ],
  language: {
    zeroRecords: "No hay ventas recientes."
  }
});
