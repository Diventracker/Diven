
import { cargarDetalles } from '/static/js/servicios/modales/editar/cargarDetalles.js';
import { cargarImagenes } from '/static/js/servicios/modales/editar/cargarImagenes.js';


document.addEventListener('DOMContentLoaded', () => {
const modal = document.getElementById('modalEditar');
if (!modal) return;

modal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    if (!button) return;

    const servicioId = button.getAttribute('data-id');
    const estado = button.getAttribute('data-estado');

    // ID en el modal
    const idDisplay = document.getElementById('servicioId');
    if (idDisplay) idDisplay.textContent = servicioId;

    // Estado y visibilidad de secciones
    const estadoDisplay = document.getElementById('estadoActual');
    const detalleCostos = document.getElementById('detalleCostos2');
    const totales = document.getElementById('totales2');
    const detalleTrabajo = document.getElementById('detallesTrabajo');

    if (estadoDisplay) {
    estadoDisplay.className = 'badge';
    const e = (estado || '').toLowerCase();
    if (e === 'en progreso') {
        estadoDisplay.classList.add('text-bg-secondary', 'fs-6');
        estadoDisplay.innerHTML = '<i class="bi bi-gear-fill"></i> En Progreso';
        detalleCostos?.classList.add('d-none');
        totales?.classList.add('d-none');
        detalleTrabajo?.classList.add('d-none');
    } else if (e === 'en revisión') {
        estadoDisplay.classList.add('text-bg-warning', 'fs-6');
        estadoDisplay.innerHTML = '<i class="bi bi-search"></i> En Revisión';
        detalleCostos?.classList.remove('d-none');
        totales?.classList.remove('d-none');
        detalleTrabajo?.classList.remove('d-none');
    } else if (e === 'rechazado') {
        estadoDisplay.classList.add('text-bg-danger', 'fs-6');
        estadoDisplay.innerHTML = '<i class="bi bi-x"></i> Rechazado';
        detalleCostos?.classList.remove('d-none');
        totales?.classList.remove('d-none');
        detalleTrabajo?.classList.remove('d-none');
    } else if (e === 'finalizado') {
        estadoDisplay.classList.add('text-bg-success', 'fs-6');
        estadoDisplay.innerHTML = '<i class="bi bi-check"></i> Finalizado';
        detalleCostos?.classList.remove('d-none');
        totales?.classList.remove('d-none');
        detalleTrabajo?.classList.remove('d-none');
    }
    }

    //Cargar siempre las imagenes
    cargarImagenes(servicioId);

    // Si está en progreso, no cargamos data remota (Los detalles)
    if (estado === 'En Progreso') return;

    // Cargar datos
    cargarDetalles(servicioId);
});
});

