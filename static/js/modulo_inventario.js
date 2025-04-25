//Funcion que actualiza la busqueda del proveedor en el modal crear
crearBuscadorEntidad({
    inputId: "buscar_proveedor",
    selectId: "proveedor_select",
    hiddenInputId: "proveedor_id",
    endpoint: "/inventario/proveedores",
    placeholderOption: "⮯ Seleccione un proveedor ⮯",
    format: p => `${p.nombre} (${p.nit})`,
    useSize: true
});

//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'productoId',
        nombre: 'editNombreProducto',
        marca: 'editMarca',
        modelo: 'editModelo',
        descripcion: 'editDescripcion',
        stock: 'editStock',
        precio: 'editPrecio',
        precioVenta: 'editPrecioVenta',
        nombreProveedor: 'proveedorActual',
        idProveedor: 'proveedor_id2',  //Esto coloca al campo hidden que sera enviado el id actual      
        inicio: 'editFechaInicio',
        fin: 'editFechaExpiracion',
        compra: 'editFechaCompra'
    }
});

//Funcion Para poder filtrar proveedor en el modal Editar
crearBuscadorEntidad({
    inputId: "buscar_proveedor2",
    selectId: "proveedor_select2",
    hiddenInputId: "proveedor_id2",
    endpoint: "/inventario/proveedores",
    placeholderOption: "⮯ Seleccione un proveedor ⮯",
    format: p => `${p.nombre} (${p.nit})`,
    useSize: true
});

//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editProductoForm',
    buttonId: 'saveChanges',
    urlBase: '/producto/editar',
    redirectUrlBase: '/inventario',
    idField: 'productoId'
});

// Funcion crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'productoIdToDelete',
    spanId: 'nombreProducto',
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/producto/eliminar',
    redirectUrlBase: '/inventario'
});
