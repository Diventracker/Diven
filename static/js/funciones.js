function crearBuscadorEntidad(config) {
    const input = document.getElementById(config.inputId);
    const select = document.getElementById(config.selectId);
    const hiddenInput = document.getElementById(config.hiddenInputId);

    input.addEventListener("input", function () {
        let query = this.value;

        if (query.length < 2) {
            select.style.display = "none";
            return;
        }

        fetch(`${config.endpoint}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                select.innerHTML = config.placeholderOption ? `<option value="">${config.placeholderOption}</option>` : "";

                data.forEach(entidad => {
                    let option = document.createElement("option");
                    option.value = entidad.id;
                    option.textContent = config.format(entidad);
                    select.appendChild(option);
                });

                if (data.length > 0) {
                    select.style.display = "block";
                    if (config.useSize) {
                        select.setAttribute("size", Math.min(data.length, 5));
                    }
                } else {
                    select.style.display = "none";
                }
            })
            .catch(error => console.error("Error en la búsqueda:", error));
    });

    select.addEventListener("change", function () {
        const selectedOption = this.options[this.selectedIndex];

        if (selectedOption && selectedOption.value) {
            input.value = selectedOption.textContent;
            hiddenInput.value = selectedOption.value;
        }

        select.style.display = "none";
        if (config.useSize) {
            select.removeAttribute("size");
        }
    });

    // Ocultar si se hace clic fuera
    document.addEventListener("click", function (event) {
        if (!select.contains(event.target) && event.target !== input) {
            select.style.display = "none";
            if (config.useSize) {
                select.removeAttribute("size");
            }
        }
    });
}

// Exportar la función
window.crearBuscadorEntidad = crearBuscadorEntidad;


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


// Función genérica para manejar la actualización de registros
function setupEditForm(config) {
    const { formId, buttonId, urlBase, redirectUrlBase, idField } = config;

    document.getElementById(buttonId).addEventListener('click', function (event) {
        event.preventDefault(); // Evita el envío tradicional del formulario

        let form = document.getElementById(formId);
        let formData = new FormData(form);
        let recordId = document.getElementById(idField).value;

        fetch(`${urlBase}/${recordId}`, {
            method: 'PUT',
            body: formData,
        })
            .then(response => {
                if (response.ok) {
                    return response.text(); // Leer la respuesta como texto
                } else {
                    throw new Error("Error en la actualización");
                }
            })
            .then(data => {
                if (data.includes("success")) { // Comprobamos si la respuesta incluye "success"
                    window.location.href = `${redirectUrlBase}?success=1`; // Redirigir con indicador de éxito
                } else {
                    throw new Error("Error inesperado en la respuesta del servidor.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Hubo un error al procesar la solicitud.");
            });
    });
}

// Exponer la función para usarla en otros archivos
window.setupEditForm = setupEditForm;




//Mostrar una alerta 
document.addEventListener("DOMContentLoaded", function() {
    let alertBox = document.querySelector(".alert");
    if (alertBox) {
        setTimeout(() => {
            alertBox.style.transition = "opacity 0.5s ease";
            alertBox.style.opacity = "0";
            setTimeout(() => alertBox.remove(), 500);
        }, 3000);

        // Eliminar parámetros "success=1" o "deleted=1" de la URL
        const url = new URL(window.location);
        url.searchParams.delete("success");
        url.searchParams.delete("deleted");
        url.searchParams.delete("create");
        url.searchParams.delete("error");
        window.history.replaceState({}, document.title, url);
    }
});

