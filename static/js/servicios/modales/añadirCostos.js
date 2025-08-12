function setupCostosAdicionales({ grupoCostosId, botonAgregarId }) {
    let costoCounter = document.querySelectorAll(`#${grupoCostosId} .costo-item`).length;

    const grupoCostos = document.getElementById(grupoCostosId);
    const btnAgregarCosto = document.getElementById(botonAgregarId);

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

    function actualizarIndices() {
        const items = grupoCostos.querySelectorAll('.costo-item');
        items.forEach((item, index) => {
            item.setAttribute('data-index', index + 1);
        });
        costoCounter = items.length;
    }

    function actualizarBotonesEliminar() {
        const items = grupoCostos.querySelectorAll('.costo-item');
        const botonesEliminar = grupoCostos.querySelectorAll('.eliminar-costo');

        if (items.length > 1) {
            botonesEliminar.forEach(btn => btn.style.display = 'block');
        } else {
            botonesEliminar.forEach(btn => btn.style.display = 'none');
        }
    }

    // Inicial: asignar evento a los botones eliminar existentes
    grupoCostos.querySelectorAll('.eliminar-costo').forEach(asignarBotonEliminar);

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
                            <input type="text" class="form-control costo-valor formato-moneda" min="0">
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

        // Asignar evento eliminar
        asignarBotonEliminar(nuevoCosto.querySelector('.eliminar-costo'));

        // Formato moneda para el nuevo input
        new AutoNumeric(nuevoCosto.querySelector('.formato-moneda'), {
            currencySymbol: '$',
            decimalPlaces: 0,
            digitGroupSeparator: '.',
            decimalCharacter: ',',
            unformatOnSubmit: true,
            modifyValueOnWheel: false,
            watchExternalChanges: true,
            showOnlyNumbersOnFocus: false,
            currencySymbolPlacement: 'p',
            minimumValue: '0',
            emptyInputBehavior: 'zero'
        });

        actualizarBotonesEliminar();
    });

    // Mostrar botones correctamente al iniciar
    actualizarBotonesEliminar();
}

function resetCostosAdicionales({ toggleId, grupoCostosId, contenedorCostosId }) {
    const toggle = document.getElementById(toggleId);
    const contenedor = document.getElementById(contenedorCostosId);
    const grupo = document.getElementById(grupoCostosId);

    if (toggle) toggle.checked = false;
    if (contenedor) {
        contenedor.classList.remove('show');
        contenedor.classList.add('d-none');
    }

    if (grupo) {
        grupo.innerHTML = `
        <div class="costo-item mb-3" data-index="1">
            <div class="row g-2 align-items-end">
                <div class="col-md-5">
                    <div class="input-group">
                        <span class="input-group-text bg-success text-white">
                            <i class="bi bi-currency-dollar"></i>
                        </span>
                        <div class="form-floating">
                            <input type="text" class="form-control costo-valor formato-moneda" min="0">
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
                            <input type="text" class="form-control costo-motivo">
                            <label>Motivo del gasto</label>
                        </div>
                    </div>
                </div>
                <div class="col-md-1 d-flex align-items-end mb-2">
                    <button type="button" class="btn btn-outline-danger h-100 w-100 eliminar-costo" style="display: none;">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>
        `;

        // Activar formato moneda en el inicial
        new AutoNumeric(grupo.querySelector('.formato-moneda'), {
            currencySymbol: '$',
            decimalPlaces: 0,
            digitGroupSeparator: '.',
            decimalCharacter: ',',
            unformatOnSubmit: true,
            modifyValueOnWheel: false,
            watchExternalChanges: true,
            showOnlyNumbersOnFocus: false,
            currencySymbolPlacement: 'p',
            minimumValue: '0',
            emptyInputBehavior: 'zero'
        });

        grupo.querySelectorAll('.eliminar-costo').forEach(btn => {
            btn.addEventListener('click', function () {
                const item = this.closest('.costo-item');
                if (item) item.remove();
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    setupCostosAdicionales({
        grupoCostosId: 'grupoCostos',
        botonAgregarId: 'agregarCosto'
    });

    setupCostosAdicionales({
        grupoCostosId: 'grupoCostos2',
        botonAgregarId: 'agregarCosto2'
    });
});
