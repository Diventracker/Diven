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


//Funcion para aggregar los constos y eliminarlos
document.addEventListener('DOMContentLoaded', function () {
    let costoCounter = document.querySelectorAll('.costo-item').length;

    const grupoCostos = document.getElementById('grupoCostos');
    const btnAgregarCosto = document.getElementById('agregarCosto');

    // Función para asignar evento al botón eliminar
    function asignarBotonEliminar(btn) {
        btn.addEventListener('click', function () {
            const item = this.closest('.costo-item');
            if (item) {
                item.remove();
                actualizarIndices();
                actualizarBotonesEliminar();
            }
        });
    }

    // Asignar evento eliminar a los botones existentes
    document.querySelectorAll('.eliminar-costo').forEach(asignarBotonEliminar);

    // Función para actualizar los índices después de eliminar
    function actualizarIndices() {
        const items = document.querySelectorAll('.costo-item');
        items.forEach((item, index) => {
            item.setAttribute('data-index', index + 1);
        });
        costoCounter = items.length;
    }

    // Función para mostrar u ocultar botones de eliminar
    function actualizarBotonesEliminar() {
        const items = document.querySelectorAll('.costo-item');
        const botonesEliminar = document.querySelectorAll('.eliminar-costo');

        if (items.length > 1) {
            botonesEliminar.forEach(btn => {
                btn.style.display = 'block';
            });
        } else {
            botonesEliminar.forEach(btn => {
                btn.style.display = 'none';
            });
        }
    }

    // Evento para agregar un nuevo costo
    btnAgregarCosto.addEventListener('click', function () {
        costoCounter++;

        const nuevoCosto = document.createElement('div');
        nuevoCosto.className = 'costo-item mb-3 fade-in';
        nuevoCosto.setAttribute('data-index', costoCounter);

        nuevoCosto.innerHTML = `
            <div class="row g-2 align-items-end">
                <div class="col-md-5">
                    <div class="input-group">
                        <span class="input-group-text bg-success text-white">
                            <i class="bi bi-currency-dollar"></i>
                        </span>
                        <div class="form-floating">
                            <input type="number" class="form-control costo-valor" placeholder="0.00" step="0.01" min="0">
                            <label>Valor</label>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text bg-info text-white">
                            <i class="bi bi-chat-text"></i>
                        </span>
                        <div class="form-floating">
                            <input type="text" class="form-control costo-motivo" placeholder="Descripción del gasto">
                            <label>Motivo del gasto</label>
                        </div>
                    </div>
                </div>
                <div class="col-md-1 d-flex align-items-end mb-2">
                    <button type="button" class="btn btn-outline-danger eliminar-costo w-100 h-100">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `;

        grupoCostos.appendChild(nuevoCosto);

        const btnEliminarNuevo = nuevoCosto.querySelector('.eliminar-costo');
        asignarBotonEliminar(btnEliminarNuevo);
        actualizarBotonesEliminar();
    });

    // Mostrar botones correctamente al iniciar
    actualizarBotonesEliminar();
});


