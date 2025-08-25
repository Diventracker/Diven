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
        if (data === "En Progreso") clase = "secondary";
        else if (data === "Finalizado") clase = "success";
        else if (data === "En Revisión") clase = "warning";

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

        if (row.estado_servicio === "En Progreso") {
        botones += `
            <button class="btn btn-sm btn-outline-enviar me-1 check-button"
                    data-bs-toggle="modal"
                    data-bs-target="#modalCheck"
                    data-id="${row.id_servicio}"
                    data-precio="${row.precio_servicio}"
                    data-modelo="${row.modelo_equipo}">
            <i class="bi bi-clipboard2-check"></i>
            </button>
        `;
        }

        if (rol === "Administrador") {
        if (row.estado_servicio === "En Revisión") {
            botones += `
            <button class="btn btn-sm btn-outline-enviar me-1 aprob-button"
                    data-bs-toggle="modal"
                    data-bs-target="#modalAprobar"
                    data-id="${row.id_servicio}">
                <i class="bi bi-check-circle"></i>
            </button>
            `;
        }

        botones += `
            <button class="btn btn-sm btn-outline-secondary me-1 edit-button"
                    data-bs-toggle="modal"
                    data-bs-target="#modalEditar"
                    data-id="${row.id_servicio}"
                    data-tipoequipo="${row.tipo_equipo}"
                    data-tiposervicio="${row.tipo_servicio}"
                    data-modelo="${row.modelo_equipo}"
                    data-descripcion="${row.descripcion_problema}"
                    data-tecnico="${row.usuario.nombre_usuario}"
                    data-precio="${row.precio_servicio}"
                    data-estado="${row.estado_servicio}"
                    ${row.estado_servicio !== 'En Progreso'
                    ? `data-trabajo="${row.descripcion_trabajo}"
                        data-garantia="${row.meses_garantia}"`
                    : ''
                    }>
            <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger me-1"
                    data-id="${row.id_servicio}"
                    data-nombre="${row.modelo_equipo}"
                    data-bs-toggle="modal"
                    data-bs-target="#modalEliminar">
            <i class="bi bi-trash"></i>
            </button>
        `;
        }

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

    window.tablaServicios = inicializarDataTable('tablaServicios', '/servicios/data', columnasServicios);
});

