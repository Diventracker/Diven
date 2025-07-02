//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.check-button',
    modalFields: {
        id: 'serviceIdCheck',
        tipoEquipo: 'checkTipoEquipo',
        tipoServicio: 'checkTipoServicio',      
        modelo: 'checkModeloEquipo',
        tecnico: 'checkTecnico',
        descripcion: 'checkDescripcion'     
    }
});

//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.check-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Obtener los valores desde los atributos data-*
            const servicioId = button.getAttribute('data-id');
            const modelo = button.getAttribute('data-modelo');

            // Mostrar el ID en el <h4 id="servicioId">
            const idDisplay = document.getElementById('servicioIdCheck');
            if (idDisplay) {
                idDisplay.textContent = servicioId;
            }

            // Mostrar el modelo de equipo en el span
            const idModelo = document.getElementById('idModeloCheck');
            if (idModelo) {
                idModelo.textContent = modelo;
            }
        });
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
