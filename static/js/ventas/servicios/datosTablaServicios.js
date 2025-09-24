$(document).ready(function () {
    const rol = document.body.dataset.rol;
    const IDX_ESTADO = 6; // índice 0-based de la columna "estado_servicio"

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
                else if (data === "facturado") clase = "success"; 
                return `<span class="badge bg-${clase}">${data}</span>`;
            }
        }
    ];

    columnasServicios.push({
        data: null,
        render: function (data, type, row) {
            let botones = `
            <button onclick="location.href='/servicios/comprobante/${row.id_servicio}'"
                    class="btn btn-sm btn-outline-secondary me-1">
                <i class="bi bi-eye"></i>
            </button>`;

            //Mostrar botón de facturar solo si no está facturado
            if (row.estado_servicio !== 'facturado') {
                botones += `
                <button class="btn btn-sm btn-enviar btn-facturar" 
                        data-bs-toggle="modal"
                        data-bs-target="#modalServicio"
                        data-id="${row.id_servicio}">
                    <i class="bi bi-cash"></i>
                </button>`;
            }

            return botones;
        }
    });

    // endpoint que devuelva TODOS para poder filtrar en la tabla
    const table = window.tablaServicios = $('#tablaServicios').DataTable({
        ajax: {
            url: '/servicios/data',
            dataSrc: function (json) {
                const rows = Array.isArray(json) ? json : json.data;
                // Solo Finalizado o Facturado
                return rows.filter(r =>
                    r.estado_servicio === 'Finalizado' || r.estado_servicio === 'facturado'
                );
            }
        },
        columns: columnasServicios,
        dom: 'tp' // solo tabla y paginación (sin buscador ni info)
    });
});
