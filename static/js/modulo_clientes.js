 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  
// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'clienteIdToDelete',
    spanId: 'nombreCliente',
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/cliente/eliminar',
    redirectUrlBase: '/clientes'
});


//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editClienteId',
        nombre: 'editNombre',
        cedula: 'editCedula',
        direccion: 'editDireccion',
        telefono: 'editTelefono',
        email: 'editEmail'
    }
});

//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editClienteForm',
    buttonId: 'saveChanges',
    urlBase: '/cliente/editar',
    redirectUrlBase: '/clientes',
    idField: 'editClienteId'
});

