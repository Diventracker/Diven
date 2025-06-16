document.getElementById('checkServicioForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const id_servicio = document.getElementById('serviceIdCheck').value;
    const meses_garantia = document.querySelector('input[name="meses_garantia"]').value;
    const descripcion = document.getElementById('descripcionTrabajo').value;
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalCheck'));

    // Recoger detalles de costos
    const detalles = Array.from(document.querySelectorAll('.costo-item')).map(item => {
        const valor = parseInt(item.querySelector('.costo-valor').value) || 0;
        const motivo = item.querySelector('.costo-motivo').value.trim();
        return { valor_adicional: valor, motivo: motivo };
    });

    // Crear FormData y agregar todos los campos
    const formData = new FormData();
    formData.append("id_servicio", id_servicio);
    formData.append("meses_garantia", meses_garantia);
    formData.append("descripcion", descripcion);
    formData.append("detalles", JSON.stringify(detalles));  // clave: JSON en string

    try {
        const response = await fetch('/api/servicio/revision', {
            method: 'POST',
            body: formData // sin headers
        });

        const result = await response.json();
        if (response.ok) {
            // Cerrar el modal            
            if (modal) {
                modal.hide();
            }
            alert('Servicio actualizado correctamente');
            window.location.reload(); //Para recargar la pagina mejor, depues lo cambio
            //mostrarAlerta("alerta-exito", "Servicio actualizado correctamente");        
        } else {
            console.error(result);
            alert('Error al guardar los cambios.');
        }
    } catch (err) {
        console.error('Fetch error:', err);
        alert('Error al enviar los datos.');
    }
});
