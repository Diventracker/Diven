 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  
//Funcion que actualiza la busqueda del proveedor en el modal crear
initSelect2Modal({
  selector: '#selectProveedor',
  placeholder: 'Buscar proveedor...',
  url: '/inventario/proveedores',
  processResultsMapper: p => ({
    id: p.id,
    text: `${p.nombre} (${p.nit})`
  }),
  parentModalSelector: '#modalRegistro',
  language: {
    noResults: () => "No se encontraron resultados",
    searching: () => "Buscando...",
    inputTooShort: (args) => `Por favor ingresa ${args.minimum - args.input.length} o más caracteres`
  }
});

// Select del proveedor en el modal editar settea el proveedor actual
$('#modalEditar').on('show.bs.modal', function (event) {
  const button = $(event.relatedTarget); // Botón que activó el modal

  // Obtener los datos del botón
  const idProveedor = button.data('idproveedor');
  const nombreProveedor = button.data('nombreproveedor');

  // Seleccionar el select
  const $selectProveedor = $('#selectProveedor2');

  // Limpiar cualquier valor previo
  $selectProveedor.val(null).trigger('change');

  if (idProveedor && nombreProveedor) {
    // Si la opción ya existe, solo selecciónala
    if ($selectProveedor.find(`option[value="${idProveedor}"]`).length === 0) {
      // Crear la opción y agregarla
      const option = new Option(nombreProveedor, idProveedor, true, true);
      $selectProveedor.append(option).trigger('change');
    } else {
      // Seleccionar la opción existente
      $selectProveedor.val(idProveedor).trigger('change');
    }
  }
});

//Select del modal editar Producto
initSelect2Modal({
  selector: '#selectProveedor2',
  placeholder: 'Buscar proveedor...',
  url: '/inventario/proveedores',
  processResultsMapper: p => ({
    id: p.id,
    text: `${p.nombre} (${p.nit})`
  }),
  parentModalSelector: '#modalEditar',
  language: {
    noResults: () => "No se encontraron resultados",
    searching: () => "Buscando...",
    inputTooShort: (args) => `Por favor ingresa ${args.minimum - args.input.length} o más caracteres`
  }
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
