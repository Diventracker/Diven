//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.aprob-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Obtener los valores desde los atributos data-*
            const servicioId = button.getAttribute('data-id');
            const modal = document.getElementById('modalAprobar');
            //Poner el id al modal
            modal.setAttribute('data-servicio-id', servicioId);  
            // Cambiar la URL del enlace con el ID
            const link = document.getElementById('verServicioLink');
            if (link && servicioId) {
                link.href = `/servicios/comprobante/${servicioId}`;
            }
        });
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

//Funcion que manda el fetch al hacer click en aprobar
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
      alert('✅ Servicio aprobado correctamente');
      bootstrap.Modal.getInstance(modal).hide();
      location.reload();
    } else {
      alert('❌ Error: ' + data.message);
    }
  })
  .catch(err => {
    console.error(err);
    alert('❌ Error inesperado');
  });
}

//Funcion para enviar el rechazo
function confirmarRechazo() {
  const modal = document.getElementById('modalRechazo');
  const servicioId = modal.getAttribute('data-servicio-id');
  const motivo = document.getElementById('motivoRechazo').value.trim();

  if (!motivo) {
    alert("❗ Por favor ingresa un motivo para el rechazo.");
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
      alert('🚫 Servicio rechazado correctamente');
      bootstrap.Modal.getInstance(modal).hide();
      bootstrap.Modal.getInstance(document.getElementById('modalAprobar')).hide();
      location.reload();
    } else {
      alert('❌ Error: ' + data.message);
    }
  })
  .catch(err => {
    console.error(err);
    alert('❌ Error inesperado al rechazar');
  });
}


