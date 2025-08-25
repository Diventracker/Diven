$(document).ready(function () {
    const rol = document.body.dataset.rol;

    const columnasServicios = [
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
                if (data === "Finalizado") clase = "success";

                return `<span class="badge bg-${clase}">${data}</span>`;
            }
        }


];
    columnasServicios.push({
        data: null,
        orderable: false,
        searchable: false,
        render: function (data, type, row) {
            let botones = '';
            // Botón para ver comprobante (todos los roles)
            botones += `
        <button onclick="location.href='/servicios/comprobante/${row.id_servicio}'"
                class="btn btn-sm btn-outline-secondary me-1">
            <i class="bi bi-eye"></i>
        </button>
        `;
            return botones;
        }
    });

    window.tablaServicios = inicializarDataTable('tablaServicios', '/servicios/finalizado', columnasServicios);
});
