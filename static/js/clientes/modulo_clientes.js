 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");


//Manda el fetch para crear el registro
handleFormSubmit({
    formId: 'registrarCliente',
    url: '/clientes/crear',
    modalId: 'modalRegistro',
    tablaVariable: 'tablaClientes'
});

//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editClienteId',
        nombre: 'editNombre',
        tipodocumento: 'editTipo',
        numerodocumento: 'editDocumento',
        direccion: 'editDireccion',
        telefono: 'editTelefono',
        email: 'editEmail'
    }
});

// Manda el Fetch para editar registros
handleEditFormSubmit({
    formId: 'editClienteForm',
    urlBase: '/cliente/editar',
    modalId: 'modalEditar',
    idFieldId: 'editClienteId',
    tablaVariable: 'tablaClientes'
});

//Rellenar los campos del modal eliminar
setDeleteModalData({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'clienteIdToDelete',
    spanId: 'nombreCliente'
});
//Manda el fetch para eliminar el registro
handleDeleteConfirm({
    confirmButtonId: 'confirmDeleteBtn',
    hiddenInputId: 'clienteIdToDelete',
    deleteUrlBase: '/cliente/eliminar',
    modalActive: 'modalEliminar',
    tablaVariable: 'tablaClientes' // 👈 nombre de la DataTable global
});









