// Función genérica para manejar edición de formularios en modales
function setupEditButtons(config) {
    const { buttonSelector, modalFields } = config;

    document.addEventListener('click', function (e) {
        const button = e.target.closest(buttonSelector);
        if (!button) return;

        for (const field in modalFields) {
            const element = document.getElementById(modalFields[field]);
            const value = button.getAttribute(`data-${field}`);
            if (element && value !== null) {
                element.value = value;
            }
        }
    });
}

function setDeleteModalData({ buttonSelector, hiddenInputId, spanId }) {
    document.addEventListener('click', function (e) {
        const button = e.target.closest(buttonSelector);
        if (!button) return;

        const entityId = button.getAttribute('data-id');
        const entityName = button.getAttribute('data-nombre');

        document.getElementById(hiddenInputId).value = entityId;
        document.getElementById(spanId).textContent = entityName;
    });
}




// Exportar la función para usarla en otros archivos
window.setupEditButtons = setupEditButtons;
window.setDeleteModalData = setDeleteModalData;