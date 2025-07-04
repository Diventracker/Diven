 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  
  
handleFormSubmit({
  formId: 'registrarProducto',
  url: '/producto/crear',
  modalId: 'modalRegistro',
  tablaVariable: 'productos'  
});

//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'productoId',
        nombre: 'editNombreProducto',
        modelo: 'editModelo',
        descripcion: 'editDescripcion',
        precio: 'editPrecio',
        precioVenta: 'editPrecioVenta',
        garantia: 'editGarantia'
    }
});

// Manda el Fetch para editar registros
handleEditFormSubmit({
    formId: 'editProductoForm',
    urlBase: '/producto/editar',
    modalId: 'modalEditar',
    idFieldId: 'productoId',
    tablaVariable: 'productos'
});

//Rellenar los campos del modal eliminar
setDeleteModalData({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'productoIdToDelete',
    spanId: 'nombreProducto'
});

//Manda el fetch para eliminar el registro
handleDeleteConfirm({
    confirmButtonId: 'confirmDeleteBtn',
    hiddenInputId: 'productoIdToDelete',
    deleteUrlBase: '/producto/eliminar',
    modalActive: 'modalEliminar',
    tablaVariable: 'productos' 
});

