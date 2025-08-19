//Carga los detalles del servicio tecnico a editar
export async function cargarDetalles(servicioId) {
  const contenedorDetalles = document.getElementById('grupoCostos2');
  if (!contenedorDetalles) return;

  contenedorDetalles.innerHTML = '<p class="text-muted">Cargando detalles...</p>';

  try {
    const res = await fetch(`/api/servicio/${servicioId}/detalles`);
    if (!res.ok) throw new Error('Error al obtener detalles');
    const detalles = await res.json();

    contenedorDetalles.innerHTML = '';

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
  } catch (err) {
    console.error(err);
    contenedorDetalles.innerHTML = '<p class="text-danger">Error al cargar los detalles.</p>';
  }
}