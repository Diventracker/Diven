import { eliminarImagen } from '/static/js/servicios/modales/editar/eliminarImagen.js';

// Para evitar que el uploader3 borre las imágenes del servidor cuando re-renderiza,
// volvemos a pintarlas justo después del cambio en el input de archivos.
let _hookAdjuntado = false;
let _cacheImagenesServidor = []; // [{ id_imagen, ruta }]

function obtenerNombreArchivo(ruta = '') {
  try { return ruta.split('/').pop() || 'imagen'; } catch { return 'imagen'; }
}

// Solo borra los nodos que renderizamos desde el servidor (no toca los del uploader).
function limpiarPreviewsServidor(preview) {
  preview.querySelectorAll('[data-server="1"]').forEach(n => n.remove());
}

function renderizarImagenesServidor(preview) {
  if (!preview) return;

  // Asegurar display
  preview.style.display = 'flex';

  // Elimina solo los que agregamos nosotros
  limpiarPreviewsServidor(preview);

  _cacheImagenesServidor.forEach(img => {
    const col = document.createElement('div');
    col.className = 'col-6 col-md-4';
    col.id = `img-exist-${img.id_imagen}`;
    col.setAttribute('data-server', '1'); // marca para poder limpiar solo los del server

    const nombre = obtenerNombreArchivo(img.ruta);

    col.innerHTML = `
      <div class="image-preview border position-relative">
        <img src="${img.ruta}" alt="${nombre}" class="img-fluid rounded">
        <button type="button"
                class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1"
                data-id="${img.id_imagen}">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <small class="text-muted d-block mt-1 text-truncate">${nombre}</small>
    `;

    // Botón eliminar (backend real)
    const btnEliminar = col.querySelector('button[data-id]');
    btnEliminar.addEventListener('click', async () => {
      const ok = await eliminarImagen(img.id_imagen, col);
      if (ok) {
        // Quitar de la caché local también
        _cacheImagenesServidor = _cacheImagenesServidor.filter(i => i.id_imagen !== img.id_imagen);
      }
    });

    preview.appendChild(col);
  });
}

export async function cargarImagenes(servicioId) {
  const preview = document.getElementById('imagePreview3');
  if (!preview) return;

  try {
    const res = await fetch(`/servicio/${servicioId}/imagenes`);
    if (!res.ok) throw new Error('Error al obtener imágenes');
    const imagenes = await res.json();

    // Guardamos en caché y renderizamos
    _cacheImagenesServidor = Array.isArray(imagenes) ? imagenes : [];
    renderizarImagenesServidor(preview);

    // Hook para reponer las imágenes del servidor cuando el uploader3 re-renderiza
    // (el uploader limpia #imagePreview3 en cada cambio).
    const fileInput3 = document.getElementById('fileInput3');
    if (fileInput3 && !_hookAdjuntado) {
      fileInput3.addEventListener('change', () => {
        // Espera a que el uploader termine su update y repinta las del servidor
        setTimeout(() => renderizarImagenesServidor(preview), 0);
      });
      _hookAdjuntado = true;
    }
  } catch (err) {
    console.error('Error cargando imágenes:', err);
    if (typeof mostrarAlerta === 'function') {
      mostrarAlerta('alerta-warning', 'Error al cargar imágenes del servicio');
    }
  }
}