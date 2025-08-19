export async function eliminarImagen(idImagen, elementoDomParaQuitar) {
  const confirmar = confirm('¿Seguro que deseas eliminar esta imagen?');
  if (!confirmar) return false;

  try {
    const res = await fetch(`/servicio/imagen/${idImagen}`, { method: 'DELETE' });
    const data = await res.json().catch(() => ({}));

    if (!res.ok || data?.success === false) {
      throw new Error(data?.error || 'No se pudo eliminar la imagen');
    }

    // Quitar del DOM si se pasó el elemento contenedor
    if (elementoDomParaQuitar && elementoDomParaQuitar.remove) {
      elementoDomParaQuitar.remove();
    }

    // Si usas un alert custom:
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