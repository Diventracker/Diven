//Funcion para mostrar los datos en tablas de datatable
function inicializarDataTable(tablaId, urlDatos, columnas) {
  const tabla = $(`#${tablaId}`).DataTable({
    dom: 'lrtp',
    ajax: {
      url: urlDatos,
      dataSrc: ''
    },
    order: [], // respetar el orden del servidor
    columns: columnas,
    language: {
      search: "Buscar:",
      lengthMenu: "Mostrar _MENU_ registros",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron resultados",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)"
    }
  });

  // Buscar con Enter
  $('#buscador').on('keypress', function (e) {
    if (e.which === 13) {
      tabla.search(this.value).draw();
    }
  });

  // Botón buscar
  $('#btn-buscar').on('click', function () {
    const valor = $('#buscador').val();
    tabla.search(valor).draw();
  });

  // Limpiar filtros
  $('#btn-limpiar-filtros').on('click', function () {
    $('#buscador').val('');
    tabla.search('');
    tabla.order([]);
    $('#custom-length').val(10);
    tabla.page.len(10);
    tabla.ajax.reload(null, true);
  });

  return tabla;
}

