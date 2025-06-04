 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  
//Funcion que actualiza la busqueda del cliente en el modal crear
initSelect2Modal({
  selector: '#selectClientes',
  placeholder: 'Buscar cliente...',
  url: '/servicios/clientes',
  processResultsMapper: c => ({
    id: c.id,
    text: `${c.nombre} (${c.cedula})`
  }),
  parentModalSelector: '#modalRegistro',
  language: {
    noResults: () => "No se encontraron resultados",
    searching: () => "Buscando...",
    inputTooShort: (args) => `Por favor ingresa ${args.minimum - args.input.length} o más caracteres`
  }
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

