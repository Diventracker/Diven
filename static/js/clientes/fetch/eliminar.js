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



function setupDeleteButtons(config) {
    const {
        buttonSelector,
        hiddenInputId,
        spanId,
        modalTitle,
        confirmButtonId,
        deleteUrlBase,
        onSuccess,
        onError
    } = config;

    // Abrir modal y llenar campos al hacer clic en botón eliminar
    document.querySelectorAll(buttonSelector).forEach(button => {
        button.addEventListener('click', function () {
            const entityId = this.getAttribute('data-id');
            const entityName = this.getAttribute('data-nombre');

            document.getElementById(hiddenInputId).value = entityId;
            document.getElementById(spanId).textContent = entityName;

            if (modalTitle) {
                document.getElementById(modalTitle).textContent = `Eliminar ${entityName}`;
            }
        });
    });

    // Confirmar y hacer fetch DELETE
    document.getElementById(confirmButtonId).addEventListener('click', async function () {
        const entityId = document.getElementById(hiddenInputId).value;

        try {
            const response = await fetch(`${deleteUrlBase}/${entityId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (data.success) {
                alert("✅ " + (data.mensaje || "Eliminado correctamente"));
                if (typeof onSuccess === 'function') onSuccess(entityId, data);
            } else {
                alert("❌ " + (data.error || "No se pudo eliminar"));
                if (typeof onError === 'function') onError(entityId, data);
            }

        } catch (error) {
            console.error("❌ Error de red al eliminar:", error);
            alert("❌ Error de red al eliminar.");
            if (typeof onError === 'function') onError(entityId, { error });
        }
    });
}
