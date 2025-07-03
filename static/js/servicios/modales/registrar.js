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

//Funcion que muestra el valor base, segun el select
document.addEventListener('DOMContentLoaded', function () {
const select = document.getElementById('tipo_servicio');
const preview = document.getElementById('previewPrecio');
const hiddenInput = document.querySelector('input[name="precio_servicio"]');

select.addEventListener('change', function () {
    const selectedOption = select.options[select.selectedIndex];

    if (this.value !== "") {
    // Extraer la parte del precio desde el texto del option
    const texto = selectedOption.textContent;
    const precioTexto = texto.split('-')[1]?.trim(); // "$150.000"
    
    // Quitar símbolos y puntos, y convertir a entero
    const precioNumerico = parseInt(precioTexto.replace(/[\$.]/g, ''), 10);

    // Mostrar en vista previa
    preview.textContent = precioTexto;

    // Guardar valor limpio en el input hidden
    hiddenInput.value = precioNumerico;
    } else {
    preview.textContent = '$0';
    hiddenInput.value = '';
    }
});
});