//Crear Registros
function handleFormSubmit({ formId, url, modalId, tablaVariable = null, uploaders = [] }) {
    const form = document.getElementById(formId);

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        // Adjuntar imágenes desde uploaders (si existen)
        if (Array.isArray(uploaders) && uploaders.length > 0) {
            uploaders.forEach(uploader => {
                if (uploader && typeof uploader.getImages === "function") {
                    uploader.getImages().forEach(file => {
                        formData.append("imagenes", file); // Nombre esperado en backend
                    });
                }
            });
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                form.reset();

                if (modalId) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
                    if (modal) modal.hide();
                }

                mostrarAlerta("alerta-success", data.mensaje || "Registro exitoso");

                if (tablaVariable && window[tablaVariable]) {
                    // Es un DataTable
                    window[tablaVariable].ajax?.reload(null, false);
                } else if (typeof actualizarProductos === "function") {
                    actualizarProductos();
                }

            } else {
                mostrarAlerta("alerta-warning", "Error: " + (data.error || "No se pudo completar la operación"));
            }

        } catch (error) {
            console.error("❌ Error de red:", error);
            alert("❌ Error de red. Intente nuevamente.");
        }
    });
}

//Editar Registros
function handleEditFormSubmit({ formId, urlBase, modalId, idFieldId, tablaVariable = null }) {
    const form = document.getElementById(formId);

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        const entityId = document.getElementById(idFieldId).value;
        try {
            const response = await fetch(`${urlBase}/${entityId}`, {
                method: 'PUT',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                mostrarAlerta("alerta-success", data.mensaje || "Actualizado con éxito");
                form.reset();

                if (modalId) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
                    if (modal) modal.hide();
                }

                if (tablaVariable && window[tablaVariable]) {
                    // Si hay DataTable activa
                    window[tablaVariable].ajax.reload(null, false); // false: mantener paginación
                } else if (typeof actualizarProductos === "function") {
                    // Si estás en el módulo de productos con List.js
                    actualizarProductos();
                }

            } else {
                mostrarAlerta("alerta-warning", "Error: " + (data.error || "No se pudo actualizar"));
            }

        } catch (error) {
            console.error("❌ Error de red:", error);
            alert("❌ Error de red. Intente nuevamente.");
        }
    });
}

//Eliminar Registros
function handleDeleteConfirm({ confirmButtonId, hiddenInputId, deleteUrlBase, modalActive, tablaVariable = null }) {
    document.getElementById(confirmButtonId).addEventListener('click', async function () {
        const entityId = document.getElementById(hiddenInputId).value;
        const modalElement = document.getElementById(modalActive);
        const modal = bootstrap.Modal.getInstance(modalElement);

        try {
            const response = await fetch(`${deleteUrlBase}/${entityId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (data.success) {
                if (modal) modal.hide();
                mostrarAlerta("alerta-eliminado", data.mensaje || "Eliminado correctamente");

                if (tablaVariable && window[tablaVariable]) {
                    window[tablaVariable].ajax.reload(null, false); // false: mantener paginación
                } else if (typeof actualizarProductos === "function") {
                    actualizarProductos(); // recargar la lista de productos en List.js
                }

            } else {
                mostrarAlerta("alerta-warning", (data.error || "No se pudo eliminar"));
            }

        } catch (error) {
            console.error("❌ Error de red al eliminar:", error);
            mostrarAlerta("alerta-warning", "Error de red al eliminar.");
        }
    });
}
