//Funcion que actualiza la busqueda del cliente en el modal crear
initSelect2Modal({
  selector: '#selectClientes',
  placeholder: 'Buscar cliente...',
  url: '/clientes/filtrar',
  processResultsMapper: c => ({
    id: c.id,
    text: `${c.nombre} (${c.documento})`
  }),
  parentModalSelector: '#modalRegistro',
  language: {
    noResults: () => "No se encontraron resultados",
    searching: () => "Buscando...",
    inputTooShort: (args) => `Por favor ingresa ${args.minimum - args.input.length} o más caracteres`
  }
});

document.addEventListener('DOMContentLoaded', () => {
    const inputMostrar = document.getElementById('precio_mostrar');
    const inputReal = document.getElementById('precio_real');
    const preview = document.getElementById('previewPrecio');

    // Obtener la instancia de AutoNumeric ya inicializada
    const autoInstance = AutoNumeric.getAutoNumericElement(inputMostrar);

    inputMostrar.addEventListener('input', () => {
        const valorNumerico = autoInstance.getNumber(); // sin $
        inputReal.value = valorNumerico;
        preview.textContent = `$${Number(valorNumerico).toLocaleString('es-CO')}`;
    });

    // También actualizar al cargar si ya tiene valor
    const inicial = autoInstance.getNumber();
    inputReal.value = inicial;
    preview.textContent = `$${Number(inicial).toLocaleString('es-CO')}`;
});
