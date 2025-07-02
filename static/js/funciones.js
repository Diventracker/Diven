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


// Función para manejar la eliminación genérica
function setupDeleteButtons(config) {
    const { buttonSelector, hiddenInputId, spanId, modalTitle, confirmButtonId, deleteUrlBase, redirectUrlBase } = config;

    // Manejar clic en los botones de eliminar para llenar el modal
    document.querySelectorAll(buttonSelector).forEach(button => {
        button.addEventListener('click', function () {
            const entityId = this.getAttribute('data-id');
            const entityName = this.getAttribute('data-nombre');

            document.getElementById(hiddenInputId).value = entityId;
            document.getElementById(spanId).textContent = entityName;

            // Opcional: cambiar el título del modal
            if (modalTitle) {
                document.getElementById(modalTitle).textContent = `Eliminar ${entityName}`;
            }
        });
    });

    // Manejar la confirmación de eliminación
    document.getElementById(confirmButtonId).addEventListener('click', function () {
        const entityId = document.getElementById(hiddenInputId).value;

        fetch(`${deleteUrlBase}/${entityId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => response.text())
            .then(data => {
                if (data.includes("success") || data.includes("deleted")) {
                    window.location.href = `${redirectUrlBase}?deleted=1`;
                } else if (data.includes("error")) {
                    window.location.href = `${redirectUrlBase}?error=1`;
                } else {
                    throw new Error("Error inesperado en la respuesta del servidor.");
                }
            })
            .catch(error => {
                console.error("Error al eliminar:", error);
            });
    });
}

// Exportar la función para ser usada en otros archivos
window.setupDeleteButtons = setupDeleteButtons;


// Función genérica para manejar edición de formularios en modales
function setupEditButtons(config) {
    const { buttonSelector, modalFields } = config;

    document.querySelectorAll(buttonSelector).forEach(button => {
        button.addEventListener('click', function() {
            // Iterar sobre cada campo definido en la configuración
            for (const field in modalFields) {
                let element = document.getElementById(modalFields[field]);
                let value = this.getAttribute(`data-${field}`);
                
                if (element && value !== null) {
                    element.value = value;
                }
            }
        });
    });
}

// Exportar la función para usarla en otros archivos
window.setupEditButtons = setupEditButtons;

// Exponer la función para usarla en otros archivos
window.setupEditForm = setupEditForm;

//Para el uso del select que ordena las cosas
document.querySelectorAll('.ordenar-tabla').forEach(select => {
        select.addEventListener('change', function () {
            const [columnaStr, direccion] = this.value.split("-");
            const columna = parseInt(columnaStr);
            const descendente = direccion === "desc";

            const tablaID = this.dataset.tabla;
            const tabla = document.getElementById(tablaID);
            const tbody = tabla.querySelector("tbody");
            const filas = Array.from(tbody.querySelectorAll("tr"));

            filas.sort((a, b) => {
                let valorA = a.children[columna].getAttribute("data-valor") || a.children[columna].textContent.trim();
                let valorB = b.children[columna].getAttribute("data-valor") || b.children[columna].textContent.trim();

                // Verificar si es una fecha en formato YYYY-MM-DD
                const esFormatoFecha = /^\d{4}-\d{2}-\d{2}$/;

                if (esFormatoFecha.test(valorA) && esFormatoFecha.test(valorB)) {
                    const fechaA = new Date(valorA);
                    const fechaB = new Date(valorB);
                    return descendente ? fechaB - fechaA : fechaA - fechaB;
                }

                // Intentar convertir a número
                const numA = parseFloat(valorA.replace(/\./g, '').replace(/,/g, '.'));
                const numB = parseFloat(valorB.replace(/\./g, '').replace(/,/g, '.'));

                const esNumero = !isNaN(numA) && !isNaN(numB);
                if (esNumero) {
                    return descendente ? numB - numA : numA - numB;
                }

                // Comparación alfabética por defecto
                return descendente ? valorB.localeCompare(valorA) : valorA.localeCompare(valorB);
            });

            // Reinsertar las filas ordenadas
            filas.forEach(fila => tbody.appendChild(fila));
        });
    });