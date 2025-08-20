//este evento manda el formulario al backend para editar el servicio 
document.getElementById('saveChanges').addEventListener('click', async function (e) {
    e.preventDefault();

    const form = document.getElementById('editServicioForm');
    const id_servicio = document.getElementById('serviceId').value;
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalEditar'));

    // Campos siempre presentes
    const modelo_equipo = form.querySelector('input[name="modelo_equipo"]').value;
    const tipo_equipo = form.querySelector('select[name="tipo_equipo"]').value;
    const tipo_servicio = form.querySelector('select[name="tipo_servicio"]').value;
    const precio_servicio = form.querySelector('input[name="precio_servicio"]').value;
    const descripcion_problema = form.querySelector('textarea[name="descripcion"]').value;

    // Campos opcionales
    const descripcion_trabajo = document.getElementById('editTrabajo')?.value || "";
    const meses_garantia_raw = document.getElementById('editGarantia')?.value || "";
    const meses_garantia = meses_garantia_raw !== "" ? meses_garantia_raw : "";

    // ---- Costos adicionales ----
    const costoItems = Array.from(document.querySelectorAll('#grupoCostos2 .costo-item'));
    let validacionOk = true;

    const detalles = costoItems.map(item => {
        const valorInput = item.querySelector('.costo-valor');
        let valor = 0;

        try {
            if (AutoNumeric.getAutoNumericElement(valorInput)) {
                valor = AutoNumeric.getAutoNumericElement(valorInput).getNumber();
            } else {
                valor = parseInt(valorInput.value.replace(/\D/g, ''), 10) || 0;
            }
        } catch (err) {
            const raw = (valorInput.value || '').replace(/[^\d-]/g, '');
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

        // Re-formatear valores inválidos
        document.querySelectorAll('#grupoCostos2 .costo-valor').forEach(el => {
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

        const primerInvalido = document.querySelector('#grupoCostos2 .costo-item .costo-motivo');
        if (primerInvalido) primerInvalido.focus();

        return; // No enviamos si no pasa la validación
    }

    // ---- FormData ----
    const formData = new FormData();
    formData.append("modelo_equipo", modelo_equipo);
    formData.append("tipo_equipo", tipo_equipo);
    formData.append("tipo_servicio", tipo_servicio);
    formData.append("precio_servicio", precio_servicio);
    formData.append("descripcion", descripcion_problema);
    formData.append("descripcion_trabajo", descripcion_trabajo);
    if (meses_garantia !== "") {
        formData.append("meses_garantia", meses_garantia);
    }

    if (detalles.length > 0) {
        formData.append("detalles", JSON.stringify(detalles));
    }

    // imágenes (uploader3)
    if (uploader3 && typeof uploader3.getImages === "function") {
        uploader3.getImages().forEach(img => {
            formData.append("imagenes", img);
        });
    }

    try {
        const res = await fetch(`/servicio/editar/${id_servicio}`, {
            method: 'PUT',
            body: formData
        });

        const result = await res.json();

        if (result.success) {
            if (modal) modal.hide();
            form.reset();
            mostrarAlerta("alerta-success", result.mensaje || "Servicio actualizado correctamente");

            if (window.tablaServicios) {
                tablaServicios.ajax.reload(null, false);
            }

            if (uploader3 && typeof uploader3.clearImages === "function") {
                uploader3.clearImages();
            }
        } else {
            mostrarAlerta("alerta-warning", result.error || "No se pudo actualizar el servicio");
        }
    } catch (err) {
        console.error(err);
        mostrarAlerta("alerta-warning", "Error de red al actualizar el servicio.");
    }
});
