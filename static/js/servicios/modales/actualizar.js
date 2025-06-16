//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'serviceId',
        tipoEquipo: 'editTipoEquipo',
        tipoServicio: 'editTipoServicio',      
        modelo: 'editModeloEquipo',
        tecnico: 'editTecnico',
        descripcion: 'editDescripcion'     
    }
});

//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Obtener los valores desde los atributos data-*
            const servicioId = button.getAttribute('data-id');
            const estado = button.getAttribute('data-estado');

            // Mostrar el ID en el <h4 id="servicioId">
            const idDisplay = document.getElementById('servicioId');
            if (idDisplay) {
                idDisplay.textContent = servicioId;
            }

            // Mostrar el estado en el <span id="estadoActual">
            const estadoDisplay = document.getElementById('estadoActual');
            if (estadoDisplay) {
                // Cambiar clase del estado visual según su valor
                estadoDisplay.className = 'badge'; // resetear clases

                // Obtener el estado en minúsculas para comparar
                const estadoLower = estado.toLowerCase();


                switch (estadoLower) {
                    case 'en progreso':
                        estadoDisplay.classList.add('text-bg-secondary','fs-6');
                        estadoDisplay.innerHTML = '<i class="bi bi-gear-fill"></i> En Progreso';
                        break;
                    case 'en revisión':
                        estadoDisplay.classList.add('text-bg-warning','fs-6');
                        estadoDisplay.innerHTML = '<i class="bi bi-search"></i> En Revisión';
                        break;
                    case 'cancelado':
                        estadoDisplay.classList.add('status-cancelado');
                        break;
                    default:
                        estadoDisplay.classList.add('status-default');
                }
            }
        });
    });
});


//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editServicioForm',
    buttonId: 'saveChanges',
    urlBase: '/servicio/editar',
    redirectUrlBase: '/servicios',
    idField: 'serviceId'
});