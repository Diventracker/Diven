//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editUsuarioId',
        nombre: 'editNombre',
        correo: 'editCorreo',
        telefono: 'editTelefono',
        rol: 'editRol'        
    }
});

//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editUsuarioForm',
    buttonId: 'saveChanges',
    urlBase: '/usuario/editar',
    redirectUrlBase: '/usuarios',
    idField: 'editUsuarioId'
});

// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'usuarioIdToDelete',
    spanId: 'nombreUsuario',
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/usuario/eliminar',
    redirectUrlBase: '/usuarios'
});

