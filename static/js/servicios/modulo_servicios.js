 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  
//Manda el fetch para crear el registro
handleFormSubmit({
    formId: 'registrarServicio',
    url: '/servicio/crear',
    modalId: 'modalRegistro',
    tablaVariable: 'tablaServicios'
});

//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'serviceId',
        tipoEquipo: 'editTipoEquipo',
        tipoServicio: 'editTipoServicio',      
        modelo: 'editModeloEquipo',
        tecnico: 'editTecnico',
        descripcion: 'editDescripcion',
        trabajo: 'editTrabajo',
        garantia: 'editGarantia'
    }
});

//Funcion para cuando se le da click al btn check, y rellene los campos del modal revision
setupEditButtons({
    buttonSelector: '.check-button',
    modalFields: {
        id: 'serviceIdCheck',
        tipoEquipo: 'checkTipoEquipo',
        tipoServicio: 'checkTipoServicio',      
        modelo: 'checkModeloEquipo',
        tecnico: 'checkTecnico',
        descripcion: 'checkDescripcion'     
    }
});

//Rellenar los campos del modal eliminar
setDeleteModalData({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'servicioIdToDelete',
    spanId: 'nombreServicio'
});

//Manda el fetch para eliminar el registro
handleDeleteConfirm({
    confirmButtonId: 'confirmDeleteBtn',
    hiddenInputId: 'servicioIdToDelete',
    deleteUrlBase: '/servicio/eliminar',
    modalActive: 'modalEliminar',
    tablaVariable: 'tablaServicios' // 👈 nombre de la DataTable global
});


