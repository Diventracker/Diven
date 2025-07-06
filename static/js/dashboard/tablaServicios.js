const tablaServicios = $(`#tablaServicios`).DataTable({
  dom: 't', // solo el contenido, sin buscador, sin info, sin paginación
  ajax: {
    url: '/servicios/data',
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
    { data: 'id_servicio' },
    { data: 'tipo_equipo' },
    { data: 'modelo_equipo' },
    { data: 'descripcion_problema' },
    {
        data: 'fecha_recepcion',
        render: function (data) {
        if (!data) return '<span class="text-muted">Sin fecha</span>';
        const partes = data.split("-");
        return `${partes[2]}/${partes[1]}/${partes[0]}`;
        }
    },
    {
        data: 'fecha_entrega',
        render: function (data) {
        if (!data) return '<span class="text-muted">Sin entregar</span>';
        const partes = data.split("-");
        return `${partes[2]}/${partes[1]}/${partes[0]}`;
        }
    },
    {
        data: 'estado_servicio',
        render: function (data) {
        let clase = "secondary";
        if (data === "En Progreso") clase = "secondary";
        else if (data === "Finalizado") clase = "success";
        else if (data === "En Revisión") clase = "warning";

        return `<span class="badge bg-${clase}">${data}</span>`;
        }
    }
  ],
  language: {
    zeroRecords: "No hay Servicios recientes."
  }
});
