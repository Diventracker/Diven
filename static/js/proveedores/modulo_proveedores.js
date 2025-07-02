 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  

//Manda el fetch para crear el registro
handleFormSubmit({
    formId: 'registrarProveedor',
    url: '/proveedores/crear',
    modalId: 'modalRegistro',
    tablaVariable: 'tablaProveedores'
});

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

// Manda el Fetch para editar registros
handleEditFormSubmit({
    formId: 'editProveedorForm',
    urlBase: '/proveedor/editar',
    modalId: 'modalEditar',
    idFieldId: 'editProveedorId',
    tablaVariable: 'tablaProveedores'
});

//Rellenar los campos del modal eliminar
setDeleteModalData({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'proveedorIdToDelete',
    spanId: 'nombreProveedor'
});

//Manda el fetch para eliminar el registro
handleDeleteConfirm({
    confirmButtonId: 'confirmDeleteBtn',
    hiddenInputId: 'proveedorIdToDelete',
    deleteUrlBase: '/proveedor/eliminar',
    modalActive: 'modalEliminar',
    tablaVariable: 'tablaProveedores' // 👈 nombre de la DataTable global
});


