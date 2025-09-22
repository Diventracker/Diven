document.addEventListener('click', function (e) {
    const button = e.target.closest('.btn-facturar');
    if (!button) return;

    const servicioId = button.getAttribute('data-id');
    const modal = document.getElementById('modalServicio');

    if (modal && servicioId) {
        modal.setAttribute('data-servicio-id', servicioId);
    }
});


function confirmarRegistroServicio() {
    const modal = document.getElementById('modalServicio');
    const servicioId = modal.getAttribute('data-servicio-id');

    fetch(`/servicios/${servicioId}/estado`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nuevo_estado: 'facturado' })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                mostrarAlerta("alerta-success", data.mensaje || 'Servicio facturado correctamente');
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();

                if (window.tablaServicios) {
                    tablaServicios.ajax.reload(null, false);
                }
            } else {
                mostrarAlerta("alerta-warning", data.error || 'No se pudo facturar el servicio');
            }
        })
        .catch(err => {
            console.error(err);
            mostrarAlerta("alerta-warning", 'Error inesperado al facturar el servicio.');
        });
}