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
        //Recoger los detalles de costos
        detalles = Array.from(document.querySelectorAll('.costo-item')).map(item => {
            const valor = parseInt(item.querySelector('.costo-valor').value) || 0;
            const motivo = item.querySelector('.costo-motivo').value.trim();
            return { valor_adicional: valor, motivo: motivo };
        });
    }

    // Crear FormData y agregar todos los campos
    const formData = new FormData();
    formData.append("id_servicio", id_servicio);
    formData.append("meses_garantia", meses_garantia);
    formData.append("descripcion", descripcion);
    if (incluirCostos && detalles.length > 0) {
        formData.append("detalles", JSON.stringify(detalles));
    }

    try {
        const response = await fetch('/servicio/revision', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            // Ocultar el modal si está presente
            if (modal) modal.hide();
            form.reset(); // 🧹 Limpiar el formulario
            //Resetar el card de costos adicionales 
            resetCostosAdicionales({
                toggleId: 'toggleCostos',
                grupoCostosId: 'grupoCostos',
                contenedorCostosId: 'costosAdicionales',
                botonAgregarId: 'agregarCosto'
            });


            // Mostrar alerta de éxito
            mostrarAlerta("alerta-success", result.mensaje || "Servicio actualizado correctamente");

            // Recargar DataTable si existe
            if (window.tablaServicios) {
                tablaServicios.ajax.reload(null, false); // false = mantener paginación
            }

        } else {
            console.error(result);
            mostrarAlerta("alerta-warning", result.error || "No se pudo actualizar el servicio");
        }

    } catch (err) {
        console.error('Fetch error:', err);
        mostrarAlerta("alerta-warning", "Error al enviar los datos. Intenta nuevamente.");
    }
});
