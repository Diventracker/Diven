//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('click', function (e) {
    const button = e.target.closest('.check-button');
    if (!button) return;

    const servicioId = button.getAttribute('data-id');
    const modelo = button.getAttribute('data-modelo');

    const idDisplay = document.getElementById('servicioIdCheck');
    if (idDisplay) {
        idDisplay.textContent = servicioId;
    }

    const idModelo = document.getElementById('idModeloCheck');
    if (idModelo) {
        idModelo.textContent = modelo;
    }
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
