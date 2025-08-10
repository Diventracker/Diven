let precioBaseGlobal = 0;

function formatearMoneda(valor) {
    const opciones = { style: 'currency', currency: 'COP', minimumFractionDigits: 2 };
    let formateado = new Intl.NumberFormat('es-CO', opciones).format(valor);
    formateado = formateado.replace(/([,.]00)$/, ''); // quitar .00 o ,00
    return formateado;
}

// lee correctamente el valor numérico de un input .costo-valor
function obtenerValorInput(input) {
    if (!input) return 0;

    // 1) si AutoNumeric está presente, usar su API (mejor opción)
    try {
        if (typeof AutoNumeric !== 'undefined') {
            // intentar obtener la instancia
            const inst = AutoNumeric.getAutoNumericElement(input);
            if (inst && typeof inst.getNumber === 'function') {
                const n = inst.getNumber(); // suele devolver número o string numérico
                const num = Number(n);
                if (!isNaN(num)) return num;
            }

            // fallback a la función estática si existe
            if (typeof AutoNumeric.getNumber === 'function') {
                const n2 = AutoNumeric.getNumber(input);
                const num2 = Number(n2);
                if (!isNaN(num2)) return num2;
            }
        }
    } catch (err) {
        // no es crítico: seguimos al fallback de parseo manual
        console.warn('Error leyendo AutoNumeric:', err);
    }

    // 2) fallback: limpiar el string y parsear
    const raw = (input.value || '').trim();
    if (raw === '') return 0;

    // eliminar todo lo que no sea dígito, coma, punto o signo menos
    let cleaned = raw.replace(/[^\d\-,.]/g, '');

    // convertir separadores de miles y decimales:
    // la estrategia simple: quitar puntos (miles) y cambiar coma por punto (decimal)
    cleaned = cleaned.replace(/\./g, '').replace(/,/g, '.');

    const parsed = parseFloat(cleaned);
    return isNaN(parsed) ? 0 : parsed;
}

// ---------- cálculo de totales ----------
function actualizarTotales() {
    // console.log('actualizarTotales iniciado. precioBaseGlobal:', precioBaseGlobal);

    const precioBaseEl = document.getElementById('precioBase');
    const totalAdicionalesEl = document.getElementById('totalAdicionales');
    const totalFinalEl = document.getElementById('totalFinal');

    let sumaAdicionales = 0;
    document.querySelectorAll('#grupoCostos .costo-valor').forEach(input => {
        const val = obtenerValorInput(input);
        // console.log('valor costo adicional (leer):', val);
        sumaAdicionales += val;
    });

    // actualizar UI formateada
    if (precioBaseEl) {
        precioBaseEl.textContent = formatearMoneda(precioBaseGlobal);
    }
    if (totalAdicionalesEl) {
        totalAdicionalesEl.textContent = formatearMoneda(sumaAdicionales);
    }

    const totalFinal = precioBaseGlobal + sumaAdicionales;
    if (totalFinalEl) {
        totalFinalEl.textContent = formatearMoneda(totalFinal);
    }
}

// ---------- evento al abrir modal (toma data-precio) ----------
document.addEventListener('click', function (e) {
    const button = e.target.closest('.check-button');
    if (!button) return;

    const servicioId = button.getAttribute('data-id');
    const modelo = button.getAttribute('data-modelo');
    const precio = parseFloat(button.getAttribute('data-precio')) || 0;

    precioBaseGlobal = precio;

    const idDisplay = document.getElementById('servicioIdCheck');
    if (idDisplay) idDisplay.textContent = servicioId;

    // Asignar value al input hidden
    const idHidden = document.getElementById('serviceIdCheck');
    if (idHidden) idHidden.value = servicioId;

    const idModelo = document.getElementById('idModeloCheck');
    if (idModelo) idModelo.textContent = modelo;

    actualizarTotales();
});

// ---------- delegación para inputs dinámicos (funciona para nuevos elementos) ----------
['grupoCostos','grupoCostos2'].forEach(grupoId => {
    const cont = document.getElementById(grupoId);
    if (!cont) return;
    cont.addEventListener('input', function (ev) {
        if (ev.target && ev.target.matches('.costo-valor')) {
            actualizarTotales();
        }
    });
});


//Funcion del switch que muestrar inputs para costos adicionales
document.addEventListener('DOMContentLoaded', function () {    
    const toggle = document.getElementById('toggleCostos');
    const costosDiv = document.getElementById('costosAdicionales');

    // Ocultar por defecto
    costosDiv.classList.add('d-none');

    toggle.addEventListener('change', function () {
        if (this.checked) {
            costosDiv.classList.remove('d-none');
            setTimeout(() => costosDiv.classList.add('show'), 10); // activa el fade
        } else {
            costosDiv.classList.remove('show');
            costosDiv.addEventListener('transitionend', function handler() {
                costosDiv.classList.add('d-none');
                costosDiv.removeEventListener('transitionend', handler);
            });
        }
    });
});

