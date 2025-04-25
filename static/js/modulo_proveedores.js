//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editProveedorId',
        nit: 'editNit',
        nombreP: 'editNombreP',
        representante: 'editRepresentante',
        telefonoR: 'editTelefono',
        direccion: 'editDireccion'
    }
});

//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editProveedorForm',
    buttonId: 'saveChanges',
    urlBase: '/proveedor/editar',
    redirectUrlBase: '/proveedores',
    idField: 'editProveedorId'
});

// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'proveedorIdToDelete',
    spanId: 'nombreProveedor',
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/proveedor/eliminar',
    redirectUrlBase: '/proveedores'
});