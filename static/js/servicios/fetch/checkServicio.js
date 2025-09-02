document.getElementById('checkServicioForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const id_servicio = document.getElementById('serviceIdCheck').value;
    const form = document.getElementById('checkServicioForm');
    const meses_garantia = parseInt(document.querySelector('input[name="meses_garantiaCheck"]').value);
    const descripcion = document.getElementById('descripcionTrabajo').value;
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalCheck'));

    const incluirCostos = document.getElementById('toggleCostos').checked;
    let detalles = [];

    if (incluirCostos) {
        const costoItems = Array.from(document.querySelectorAll('.costo-item'));
        let validacionOk = true;

        detalles = costoItems.map(item => {
            const anElement = item.querySelector('.costo-valor');
            let valor = 0;
            try {
                valor = Number(AutoNumeric.getNumber(anElement)) || 0;
            } catch (err) {
                const raw = (anElement.value || '').replace(/[^\d-]/g, '');
                valor = parseInt(raw) || 0;
            }

            const motivo = item.querySelector('.costo-motivo').value.trim();

            if (valor <= 0 || motivo === "") {
                validacionOk = false;
            }
            return { valor_adicional: valor, motivo: motivo };
        });

        if (!validacionOk) {
            mostrarAlerta("alerta-warning", "Debe completar todos los costos (valor y motivo) antes de continuar.");

            document.querySelectorAll('.costo-valor').forEach(el => {
                try {
                    const inst = (typeof AutoNumeric !== 'undefined') ? AutoNumeric.getAutoNumericElement(el) : null;
                    if (inst && typeof inst.getNumber === 'function') {
                        const n = inst.getNumber();
                        const num = Number(n);
                        setTimeout(() => inst.set(num), 0);
                    } else {
                        const cleaned = (el.value || '').replace(/[^\d]/g, '');
                        if (cleaned) {
                            el.value = new Intl.NumberFormat('es-CO').format(Number(cleaned));
                        }
                    }
                } catch (err) {
                    console.warn('Reformat failed for element:', el, err);
                }
            });

            const primerInvalido = document.querySelector('.costo-item').querySelector('.costo-motivo');
            if (primerInvalido) primerInvalido.focus();

            return; // Evita el envío
        }
    }

    // 📌 Validar si hay imágenes
    if (!uploader2 || typeof uploader2.getImages !== "function" || uploader2.getImages().length === 0) {
        mostrarAlerta("alerta-warning", "Debe incluir al menos una imagen.");
        return; // Evita el envío
    }

    // Crear FormData
    const formData = new FormData();
    formData.append("id_servicio", id_servicio);
    formData.append("meses_garantia", meses_garantia);
    formData.append("descripcion", descripcion);
    if (incluirCostos && detalles.length > 0) {
        formData.append("detalles", JSON.stringify(detalles));
    }

    // Adjuntar imágenes desde uploader2
    uploader2.getImages().forEach(file => {
        formData.append("imagenes", file); // mismo nombre esperado en backend
    });

    try {
        const response = await fetch('/servicio/revision', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            if (modal) modal.hide();
            form.reset();

            if (typeof uploader2.clearImages === "function") {
                uploader2.clearImages();
            }

            resetCostosAdicionales({
                toggleId: 'toggleCostos',
                grupoCostosId: 'grupoCostos',
                contenedorCostosId: 'costosAdicionales',
                botonAgregarId: 'agregarCosto'
            });

            mostrarAlerta("alerta-success", result.mensaje || "Servicio actualizado correctamente");

            if (window.tablaServicios) tablaServicios.ajax.reload(null, false);
        } else {
            console.error(result);
            mostrarAlerta("alerta-warning", result.error || "No se pudo actualizar el servicio");
        }
    } catch (err) {
        console.error('Fetch error:', err);
        mostrarAlerta("alerta-warning", "Error al enviar los datos. Intenta nuevamente.");
    }
});
