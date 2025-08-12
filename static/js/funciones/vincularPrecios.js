function vincularAutoNumeric(inputMostrarId, inputRealId) {
    const inputMostrar = document.getElementById(inputMostrarId);
    const inputReal = document.getElementById(inputRealId);

    if (!inputMostrar || !inputReal) return;

    const autoInstance = AutoNumeric.getAutoNumericElement(inputMostrar);
    if (!autoInstance) return; // Si no existe AutoNumeric, no hace nada

    function actualizarValorReal() {
        const valorNumerico = autoInstance.getNumber();
        inputReal.value = valorNumerico || '';
    }

    inputMostrar.addEventListener('input', actualizarValorReal);
    inputMostrar.addEventListener('change', actualizarValorReal);

    // Inicializar valor desde el principio
    actualizarValorReal();
}
// Con esta funcion se vinculan los valores de los inputs con formato
// con los que estan hidden sin formato para asi mandarlos al backend