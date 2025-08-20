// ---------- utilidades ----------
function formatearMoneda(valor) {
    const opciones = { style: 'currency', currency: 'COP', minimumFractionDigits: 2 };
    let formateado = new Intl.NumberFormat('es-CO', opciones).format(valor);
    return formateado.replace(/([,.]00)$/, ''); // quita .00 o ,00
}

// ---- Función para leer valores (compatible con AutoNumeric) ----
function obtenerValorInput(input) {
    if (!input) return 0;

    // Si el input está controlado por AutoNumeric
    const anElement = AutoNumeric.getAutoNumericElement(input);
    if (anElement) {
        const num = anElement.getNumber(); // número limpio
        return isNaN(num) ? 0 : num;
    }

    // fallback normal (por si acaso)
    const raw = (input.value || '').trim();
    if (raw === '') return 0;

    let cleaned = raw.replace(/[^\d\-,.]/g, '');
    cleaned = cleaned.replace(/\./g, '').replace(/,/g, '.');

    const parsed = parseFloat(cleaned);
    return isNaN(parsed) ? 0 : parsed;
}

// ---- Función principal para actualizar totales ----
function actualizarTotalesEdicion() {
    const precioBaseInput = document.getElementById('editPrecio');
    const totalHidden = document.getElementById('ediPrecioReal'); // <-- corregido

    // elementos de vista previa
    const precioBaseSpan = document.getElementById('precioBase2');
    const adicionalesSpan = document.getElementById('totalAdicionales2');
    const totalSpan = document.getElementById('totalFinal2');

    if (!precioBaseInput || !precioBaseSpan || !adicionalesSpan || !totalSpan || !totalHidden) {
        console.warn("Faltan elementos en el DOM");
        return;
    }

    // Precio base
    const precioBase = obtenerValorInput(precioBaseInput);

    // Costos adicionales
    let totalAdicionales = 0;
    document.querySelectorAll('#grupoCostos2 .costo-valor').forEach(input => {
        totalAdicionales += obtenerValorInput(input);
    });

    // Total general
    const total = precioBase + totalAdicionales;

    // Mostrar en el preview formateado
    const formato = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    });

    precioBaseSpan.textContent = formato.format(precioBase);
    adicionalesSpan.textContent = formato.format(totalAdicionales);
    totalSpan.textContent = formato.format(total);

    // Guardar limpio en hidden
    totalHidden.value = total;
}



document.addEventListener('DOMContentLoaded', () => {
    const precioBaseInput = document.getElementById('editPrecio');
    const grupoCostos = document.getElementById('grupoCostos2');

    // Cuando cambie el precio base
    if (precioBaseInput) {
        precioBaseInput.addEventListener('input', actualizarTotalesEdicion);
        precioBaseInput.addEventListener('change', actualizarTotalesEdicion);
    }

    // Cuando cambien los costos adicionales (delegado por si agregas dinámicamente)
    if (grupoCostos) {
        grupoCostos.addEventListener('input', e => {
            if (e.target.classList.contains('costo-valor')) {
                actualizarTotalesEdicion();
            }
        });
    }

    // Ejecutar una vez al cargar (para inicializar el total)
    actualizarTotalesEdicion();
});

document.addEventListener("DOMContentLoaded", function () {
    const modalEditar = document.getElementById("modalEditar");

    if (modalEditar) {
        modalEditar.addEventListener("shown.bs.modal", function () {
            actualizarTotalesEdicion(); // recalcula totales al abrir
        });
    }
});