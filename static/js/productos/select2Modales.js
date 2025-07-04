//Funcion que actualiza la busqueda del proveedor en el modal crear
initSelect2Modal({
  selector: '#selectProveedor',
  placeholder: 'Buscar proveedor...',
  url: '/proveedores/filtrar',
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
document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener('show.bs.modal', function (event) {
    const modal = event.target;
    if (modal.id !== 'modalEditar') return; // solo aplicar al modalEditar

    const button = event.relatedTarget;
    if (!button) return;

    const idProveedor = button.getAttribute('data-idProveedor');
    const nombreProveedor = button.getAttribute('data-nombreProveedor');
    const $selectProveedor = $('#selectProveedor2');

    $selectProveedor.val(null).trigger('change');

    if (idProveedor && nombreProveedor) {
      if ($selectProveedor.find(`option[value="${idProveedor}"]`).length === 0) {
        const option = new Option(nombreProveedor, idProveedor, true, true);
        $selectProveedor.append(option).trigger('change');
      } else {
        $selectProveedor.val(idProveedor).trigger('change');
      }
    }
  });
});

//Select del modal editar Producto
initSelect2Modal({
  selector: '#selectProveedor2',
  placeholder: 'Buscar proveedor...',
  url: '/proveedores/filtrar',
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
