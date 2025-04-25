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

