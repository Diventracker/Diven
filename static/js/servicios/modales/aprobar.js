//evento que recibe para que se muestren tambien en el id y el estado en las cards
document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.aprob-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Obtener los valores desde los atributos data-*
            const servicioId = button.getAttribute('data-id');    

            // Cambiar la URL del enlace con el ID
            const link = document.getElementById('verServicioLink');
            if (link && servicioId) {
                link.href = `/servicios/comprobante/${servicioId}`;
            }
        });
    });
});
