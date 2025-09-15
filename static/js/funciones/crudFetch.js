// Crear registros genéricos
function handleFormSubmit({ formId, url, modalId, tablaVariable = null, uploaders = [] }) {
    const form = document.getElementById(formId);

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        //  Creamos FormData vacío y manualmente vamos llenando
        const formData = new FormData();

        // Recorremos los elementos del formulario
        Array.from(form.elements).forEach(el => {
            if (!el.name) return; // ignorar elementos sin name

            // Caso especial: inputs con AutoNumeric
            if (el.classList.contains('formato-moneda')) {
                try {
                    const anElement = AutoNumeric.getAutoNumericElement(el);
                    if (anElement) {
                        formData.append(el.name, anElement.getNumber()); // valor limpio (ej: 1500000)
                        return;
                    }
                } catch (err) {
                    console.warn("⚠️ Error al obtener AutoNumeric:", err);
                }
            }

            // Para otros inputs (text, select, textarea, number, etc.)
            if (el.type === 'file') {
                if (el.files.length > 0) {
                    Array.from(el.files).forEach(file => formData.append(el.name, file));
                }
            } else {
                formData.append(el.name, el.value);
            }
        });

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
function handleEditFormSubmit({ formId, urlBase, modalId, idFieldId, tablaVariable = null, uploaders = [] }) {
    const form = document.getElementById(formId);

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData();
        const entityId = document.getElementById(idFieldId).value;

        // Recorremos los elementos del formulario
        Array.from(form.elements).forEach(el => {
            if (!el.name) return; // ignorar elementos sin name

            // Caso especial: inputs con AutoNumeric
            if (el.classList.contains('formato-moneda')) {
                try {
                    const anElement = AutoNumeric.getAutoNumericElement(el);
                    if (anElement) {
                        formData.append(el.name, anElement.getNumber()); // valor limpio
                        return;
                    }
                } catch (err) {
                    console.warn("⚠️ Error al obtener AutoNumeric:", err);
                }
            }

            // Archivos
            if (el.type === 'file') {
                if (el.files.length > 0) {
                    Array.from(el.files).forEach(file => formData.append(el.name, file));
                }
            } else {
                formData.append(el.name, el.value);
            }
        });

        // Adjuntar imágenes desde uploaders (si existen)
        if (Array.isArray(uploaders) && uploaders.length > 0) {
            uploaders.forEach(uploader => {
                if (uploader && typeof uploader.getImages === "function") {
                    uploader.getImages().forEach(file => {
                        formData.append("imagenes", file);
                    });
                }
            });
        }

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
                    window[tablaVariable].ajax.reload(null, false);
                } else if (typeof actualizarProductos === "function") {
                    actualizarProductos();
                }

                // limpiar uploaders si aplica
                if (Array.isArray(uploaders) && uploaders.length > 0) {
                    uploaders.forEach(uploader => {
                        if (uploader && typeof uploader.clearImages === "function") {
                            uploader.clearImages();
                        }
                    });
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
