//Funcion para el select2 que maneja la busqueda de tin
function initSelect2Modal({
  selector,
  placeholder = '',
  url,
  processResultsMapper,
  minimumInputLength = 1,
  parentModalSelector = null,  // Si está en modal, pasa el selector del modal, ej: '#modalProveedor'
  allowClear = true,
  width = '100%',
  language = {}  
}) {
  const config = {
    placeholder,
    minimumInputLength,
    allowClear,
    width,
    ajax: {
      url: url,
      dataType: 'json',
      delay: 250,
      data: function(params) {
        return { search: params.term };
      },
      processResults: function(data) {
        return {
          results: data.map(processResultsMapper)
        };
      },
      cache: true
    },
    // Agregamos language acá para personalizar mensajes
    language: language
  };

  if (parentModalSelector) {
    config.dropdownParent = $(parentModalSelector);
  }

  $(selector).select2(config);
}






