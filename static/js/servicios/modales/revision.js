let precioBaseGlobal = 0;

function formatearMoneda(valor) {
    const opciones = { style: 'currency', currency: 'COP', minimumFractionDigits: 2 };
    let formateado = new Intl.NumberFormat('es-CO', opciones).format(valor);
    formateado = formateado.replace(/([,.]00)$/, '');
    console.log('formatearMoneda llamado con valor:', valor, '=>', formateado);
    return formateado;
}

function actualizarTotales() {
    console.log('actualizarTotales iniciado. precioBaseGlobal:', precioBaseGlobal);

    const precioBaseEl = document.getElementById('precioBase');
    const totalAdicionalesEl = document.getElementById('totalAdicionales');
    const totalFinalEl = document.getElementById('totalFinal');

    let sumaAdicionales = 0;
    document.querySelectorAll('#grupoCostos .costo-valor').forEach(input => {
        const val = parseFloat(input.value);
        console.log('valor costo adicional:', val);
        if (!isNaN(val)) {
            sumaAdicionales += val;
        }
    });

    console.log('Suma adicionales:', sumaAdicionales);

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

    console.log('Total final:', totalFinal);
}

document.addEventListener('click', function (e) {
    const button = e.target.closest('.check-button');
    if (!button) return;

    const servicioId = button.getAttribute('data-id');
    const modelo = button.getAttribute('data-modelo');
    const precio = parseFloat(button.getAttribute('data-precio')) || 0;

    console.log('click .check-button, id:', servicioId, 'modelo:', modelo, 'precio:', precio);

    precioBaseGlobal = precio;

    const idDisplay = document.getElementById('servicioIdCheck');
    if (idDisplay) {
        idDisplay.textContent = servicioId;
    }

    const idModelo = document.getElementById('idModeloCheck');
    if (idModelo) {
        idModelo.textContent = modelo;
    }

    actualizarTotales();
});

document.querySelectorAll('#grupoCostos .costo-valor').forEach(input => {
    input.addEventListener('input', () => {
        console.log('input costo-valor modificado:', input.value);
        actualizarTotales();
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

