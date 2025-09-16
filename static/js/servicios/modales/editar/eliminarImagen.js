// Utilidad para mostrar modal de confirmación y devolver una promesa
function mostrarModalConfirmacion() {
  return new Promise((resolve) => {
    const modal = new bootstrap.Modal(document.getElementById('modalEliminarImagen'));
    const btnConfirmar = document.getElementById('confirmDeleteImg');

    // Asegurar que no se acumulen listeners viejos
    btnConfirmar.replaceWith(btnConfirmar.cloneNode(true));
    const nuevoBtnConfirmar = document.getElementById('confirmDeleteImg');

    nuevoBtnConfirmar.addEventListener('click', () => {
      modal.hide();
      resolve(true);
    });

    // Si cancela o cierra
    document.getElementById('modalEliminarImagen').addEventListener('hidden.bs.modal', () => {
      resolve(false);
    }, { once: true });

    modal.show();
  });
}

export async function eliminarImagen(idImagen, elementoDomParaQuitar) {
  const confirmar = await mostrarModalConfirmacion();
  if (!confirmar) return false;

  try {
    const res = await fetch(`/servicio/imagen/${idImagen}`, { method: 'DELETE' });
    const data = await res.json().catch(() => ({}));

    if (!res.ok || data?.success === false) {
      throw new Error(data?.error || 'No se pudo eliminar la imagen');
    }

    if (elementoDomParaQuitar && elementoDomParaQuitar.remove) {
      elementoDomParaQuitar.remove();
    }

    if (typeof mostrarAlerta === 'function') {
      mostrarAlerta('alerta-success', 'Imagen eliminada correctamente');
    }
    return true;
  } catch (err) {
    console.error('Error eliminando imagen:', err);
    if (typeof mostrarAlerta === 'function') {
      mostrarAlerta('alerta-warning', err.message || 'Error al eliminar la imagen');
    }
    return false;
  }
}
