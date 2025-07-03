//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('click', function (e) {
    const button = e.target.closest('.aprob-button');
    if (!button) return;

    const servicioId = button.getAttribute('data-id');
    const modal = document.getElementById('modalAprobar');

    if (modal && servicioId) {
        modal.setAttribute('data-servicio-id', servicioId);

        const link = document.getElementById('verServicioLink');
        if (link) {
            link.href = `/servicios/comprobante/${servicioId}`;
        }
    }
});

//Para desactivarlo si cierran el modal
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalAprobar');
  const checkbox = document.getElementById('confirmarAprobacion');
  const btnAprobar = document.getElementById('btnAprobar');

  modal.addEventListener('show.bs.modal', function () {
    checkbox.checked = false;
    btnAprobar.disabled = true;
  });
});

//Limpia el textarea del rechazo
document.addEventListener('DOMContentLoaded', function () {
  const modalRechazo = document.getElementById('modalRechazo');
  const textareaMotivo = document.getElementById('motivoRechazo');

  modalRechazo.addEventListener('show.bs.modal', function () {
    textareaMotivo.value = '';
  });
});


//Funcion que activa el boton de aprobar segun el checkbox
function toggleBotonAprobar() {
  const check = document.getElementById('confirmarAprobacion');
  const btn = document.getElementById('btnAprobar');
  btn.disabled = !check.checked;
}

function prepararModalRechazo() {
  // Toma el ID desde el primer modal y lo pasa al segundo
  const idServicio = document.getElementById('modalAprobar').getAttribute('data-servicio-id');
  document.getElementById('modalRechazo').setAttribute('data-servicio-id', idServicio);
}

// Función que manda el fetch al hacer clic en aprobar
function aprobarServicio() {
  const modal = document.getElementById('modalAprobar');
  const servicioId = modal.getAttribute('data-servicio-id');

  fetch(`/servicios/${servicioId}/estado`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ nuevo_estado: 'finalizado' })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      mostrarAlerta("alerta-success", data.mensaje || 'Servicio aprobado correctamente');
      const bsModal = bootstrap.Modal.getInstance(modal);
      if (bsModal) bsModal.hide();

      if (window.tablaServicios) {
        tablaServicios.ajax.reload(null, false);
      }
    } else {
      mostrarAlerta("alerta-warning", data.error || 'No se pudo aprobar el servicio');
    }
  })
  .catch(err => {
    console.error(err);
    mostrarAlerta("alerta-warning", 'Error inesperado al aprobar el servicio.');
  });
}


// Función para enviar el rechazo
function confirmarRechazo() {
  const modal = document.getElementById('modalRechazo');
  const servicioId = modal.getAttribute('data-servicio-id');
  const motivo = document.getElementById('motivoRechazo').value.trim();

  if (!motivo) {
    mostrarAlerta("alerta-warning", "Por favor ingresa un motivo para el rechazo.");
    return;
  }

  fetch(`/servicios/${servicioId}/estado`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nuevo_estado: 'rechazado',
      motivo: motivo
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      mostrarAlerta("alerta-success", data.mensaje || 'Servicio rechazado correctamente');

      const bsModalRechazo = bootstrap.Modal.getInstance(modal);
      if (bsModalRechazo) bsModalRechazo.hide();

      const bsModalAprobar = bootstrap.Modal.getInstance(document.getElementById('modalAprobar'));
      if (bsModalAprobar) bsModalAprobar.hide();

      if (window.tablaServicios) {
        tablaServicios.ajax.reload(null, false); 
      }
    } else {
      mostrarAlerta("alerta-warning", data.error || 'No se pudo rechazar el servicio');
    }
  })
  .catch(err => {
    console.error(err);
    mostrarAlerta("alerta-warning", 'Error inesperado al rechazar el servicio.');
  });
}



