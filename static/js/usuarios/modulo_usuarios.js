 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");

//Manda el fetch para crear el registro
handleFormSubmit({
    formId: 'registrarUsuario',
    url: '/usuarios/crear',
    modalId: 'modalRegistro',
    tablaVariable: 'tablaUsuarios'
});

//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editUsuarioId',
        nombre: 'editNombre',
        correo: 'editCorreo',
        telefono: 'editTelefono',
        rol:'editRol'
    }
});

// Manda el Fetch para editar registros
handleEditFormSubmit({
    formId: 'editUsuarioForm',
    urlBase: '/usuario/editar',
    modalId: 'modalEditar',
    idFieldId: 'editUsuarioId',
    tablaVariable: 'tablaUsuarios'
});

//Rellenar los campos del modal eliminar
setDeleteModalData({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'usuarioIdToDelete',
    spanId: 'nombreUsuario'
});

//Manda el fetch para eliminar el registro
handleDeleteConfirm({
    confirmButtonId: 'confirmDeleteBtn',
    hiddenInputId: 'usuarioIdToDelete',
    deleteUrlBase: '/usuario/eliminar',
    modalActive: 'modalEliminar',
    tablaVariable: 'tablaUsuarios' // 👈 nombre de la DataTable global
});
