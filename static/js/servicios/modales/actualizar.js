//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'serviceId',
        tipoEquipo: 'editTipoEquipo',
        tipoServicio: 'editTipoServicio',      
        modelo: 'editModeloEquipo',
        tecnico: 'editTecnico',
        descripcion: 'editDescripcion',
        trabajo: 'editTrabajo',
        garantia: 'editGarantia'
    }
});

//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-button');
    const detalleCostos = document.getElementById('detalleCostos2');
    const totales = document.getElementById('totales2');
    const detalleTrabajo = document.getElementById('detallesTrabajo');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Obtener los valores desde los atributos data-*
            const servicioId = button.getAttribute('data-id');
            const estado = button.getAttribute('data-estado');

            // Mostrar el ID en el <h4 id="servicioId">
            const idDisplay = document.getElementById('servicioId');
            if (idDisplay) {
                idDisplay.textContent = servicioId;
            }

            // Mostrar el estado en el <span id="estadoActual">
            const estadoDisplay = document.getElementById('estadoActual');
            if (estadoDisplay) {
                // Cambiar clase del estado visual según su valor
                estadoDisplay.className = 'badge'; // resetear clases

                // Obtener el estado en minúsculas para comparar
                const estadoLower = estado.toLowerCase();


                switch (estadoLower) {
                    case 'en progreso':
                        estadoDisplay.classList.add('text-bg-secondary','fs-6');
                        estadoDisplay.innerHTML = '<i class="bi bi-gear-fill"></i> En Progreso';

                        // Ocultar secciones
                        if (detalleCostos) detalleCostos.classList.add('d-none');
                        if (totales) totales.classList.add('d-none');
                        if (detalleTrabajo) detalleTrabajo.classList.add('d-none');
                        break;

                    case 'en revisión':
                        estadoDisplay.classList.add('text-bg-warning','fs-6');
                        estadoDisplay.innerHTML = '<i class="bi bi-search"></i> En Revisión';

                        if (detalleCostos) detalleCostos.classList.remove('d-none');
                        if (totales) totales.classList.remove('d-none');
                        if (detalleTrabajo) detalleTrabajo.classList.remove('d-none');
                        break;

                    case 'rechazado':
                        estadoDisplay.classList.add('text-bg-danger','fs-6');
                        estadoDisplay.innerHTML = '<i class="bi bi-x"></i> Rechazado';

                        if (detalleCostos) detalleCostos.classList.remove('d-none');
                        if (totales) totales.classList.remove('d-none');
                        if (detalleTrabajo) detalleTrabajo.classList.remove('d-none');                        
                        break;

                    case 'finalizado':
                        estadoDisplay.classList.add('text-bg-success','fs-6');
                        estadoDisplay.innerHTML = '<i class="bi bi-check"></i> Finalizado';

                        if (detalleCostos) detalleCostos.classList.remove('d-none');
                        if (totales) totales.classList.remove('d-none');
                        if (detalleTrabajo) detalleTrabajo.classList.remove('d-none');                        
                        break;
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalEditar');

  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const servicioId = button.getAttribute('data-id');
    const estado = button.getAttribute('data-estado');

    if (estado === 'En Progreso') {
      console.log('No se cargan detalles porque el servicio está en progreso.');
      return; // No hace fetch
    }

    // Limpiar o mostrar loading mientras se carga
    const contenedorDetalles = document.getElementById('grupoCostos2');
    contenedorDetalles.innerHTML = '<p class="text-muted">Cargando detalles...</p>';

    fetch(`/api/servicio/${servicioId}/detalles`)
      .then(res => res.json())
      .then(detalles => {
        contenedorDetalles.innerHTML = ''; // Limpiar

        detalles.forEach((detalle, index) => {
          const item = document.createElement('div');
          item.className = 'costo-item mb-3';
          item.setAttribute('data-index', index + 1);

          item.innerHTML = `
            <div class="row g-2 align-items-end">
              <div class="col-md-5">
                <div class="input-group">
                  <span class="input-group-text bg-success text-white">
                    <i class="bi bi-currency-dollar"></i>
                  </span>
                  <div class="form-floating">
                    <input type="number" class="form-control costo-valor" value="${detalle.valor_adicional}" min="0">
                    <label>Valor</label>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text bg-info text-white">
                    <i class="bi bi-chat-text"></i>
                  </span>
                  <div class="form-floating">
                    <input type="text" class="form-control costo-motivo" value="${detalle.motivo}">
                    <label>Motivo del gasto</label>
                  </div>
                </div>
              </div>
              <div class="col-md-1 d-flex align-items-end mb-2">
                <button type="button" class="btn btn-outline-danger h-100 w-100 eliminar-costo">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          `;

          contenedorDetalles.appendChild(item);
        });
      })
      .catch(err => {
        contenedorDetalles.innerHTML = '<p class="text-danger">Error al cargar los detalles.</p>';
        console.error(err);
      });
  });
});


//Funcion que enviar el formulario al backend
document.getElementById('saveChanges').addEventListener('click', async function (e) {
    e.preventDefault();

    const form = document.getElementById('editServicioForm');
    const id_servicio = document.getElementById('serviceId').value;
    const id_usuario = parseInt(localStorage.getItem("id_usuario")) || 1;

    // Campos siempre presentes
    const modelo_equipo = form.querySelector('input[name="modelo_equipo"]').value;
    const tipo_equipo = form.querySelector('select[name="tipo_equipo"]').value;
    const tipo_servicio = form.querySelector('select[name="tipo_servicio"]').value;
    const descripcion_problema = form.querySelector('textarea[name="descripcion"]').value;

    // Campos opcionales
    const descripcion_trabajo = document.getElementById('editTrabajo')?.value || null;
    const meses_garantia_raw = document.getElementById('editGarantia')?.value || null;
    const meses_garantia = meses_garantia_raw !== null ? parseInt(meses_garantia_raw) : null;

    // Costos adicionales (si están visibles)
    const detalles = Array.from(document.querySelectorAll('#grupoCostos2 .costo-item')).map(item => {
        return {
            valor_adicional: parseInt(item.querySelector('.costo-valor').value) || 0,
            motivo: item.querySelector('.costo-motivo').value.trim()
        };
    });

    const payload = {
        id_servicio,
        id_usuario,
        modelo_equipo,
        tipo_equipo,
        tipo_servicio,
        descripcion: descripcion_problema,
        descripcion_trabajo,
        meses_garantia,
        detalles: detalles.length > 0 ? detalles : []
    };

    try {
        const res = await fetch(`/api/servicio/editar/${id_servicio}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await res.json();
        if (res.ok) {
            alert("Servicio actualizado");
            //mostrarAlerta("alerta-exito", "Cambios guardados correctamente");
            setTimeout(() => location.reload(), 1500);
        } else {
            throw new Error(result?.message || "Error inesperado");
        }
    } catch (err) {
        console.error(err);
        alert("Error al actualizar el servicio.");
    }
});