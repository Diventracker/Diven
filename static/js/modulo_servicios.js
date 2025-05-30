//Funcion que actualiza la busqueda del cliente en el modal crear
crearBuscadorEntidad({
    inputId: "buscar_cliente",
    selectId: "cliente_select",
    hiddenInputId: "cliente_id",
    endpoint: "/servicios/clientes",
    placeholderOption: "⮯ Seleccione un cliente ⮯",
    format: c => `${c.nombre} (${c.cedula})`,
    useSize: true
});

// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'serviceIdToDelete',
    spanId: 'nombreCliente', // Puedes cambiarlo si es otro campo
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/servicio/eliminar',
    redirectUrlBase: '/servicios'
});


//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'serviceId',
        tipo: 'editTipoEquipo',
        marca: 'editMarca',
        modelo: 'editModeloEquipo',
        descripcion: 'editDescripcion',
        fechaRecepcion: 'editFechaRecepcion',
        fechaEntrega: 'editFechaEntrega',
        estado: 'editEstado'
    }
});


//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editServicioForm',
    buttonId: 'saveChanges',
    urlBase: '/servicio/editar',
    redirectUrlBase: '/servicios',
    idField: 'serviceId'
});


document.getElementById("ordenar-servicios").addEventListener("change", function () {
    const criterio = this.value;
    const tabla = document.getElementById("tablaServicios");
    const tbody = tabla.querySelector("tbody");
    const filas = Array.from(tbody.querySelectorAll("tr"));

    let columna = 0;
    let descendente = false;

    switch (criterio) {
        case "tipo":
            columna = 1;
            break;
        case "modelo":
            columna = 2;
            break;
        case "estado":
            columna = 6;
            break;
        case "recepcion":
            columna = 4;
            descendente = true;
            break;
        case "entrega":
            columna = 5;
            descendente = true;
            break;
        default:
            return;
    }

    filas.sort((a, b) => {
        let valorA = a.children[columna].textContent.trim();
        let valorB = b.children[columna].textContent.trim();

        // Si es una fecha, parsear a objeto Date
        if (criterio === "recepcion" || criterio === "fechaEntrega") {
            const fechaA = new Date(valorA);
            const fechaB = new Date(valorB);
            return descendente ? fechaB - fechaA : fechaA - fechaB;
        }

        // Comparación alfabética
        return valorA.localeCompare(valorB);
    });

    // Volver a insertar las filas ordenadas
    filas.forEach(fila => tbody.appendChild(fila));
});