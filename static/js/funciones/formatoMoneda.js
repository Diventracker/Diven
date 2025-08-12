document.addEventListener('DOMContentLoaded', () => {
  AutoNumeric.multiple('.formato-moneda', {
    currencySymbol: '$',
    decimalPlaces: 0,
    digitGroupSeparator: '.',
    decimalCharacter: ',',
    unformatOnSubmit: true,
    modifyValueOnWheel: false,
    watchExternalChanges: true,
    showOnlyNumbersOnFocus: false,  // ← mantiene el formato incluso al enfocar
    currencySymbolPlacement: 'p',   // ← el símbolo va a la izquierda
    minimumValue: '0',              // ← evita valores negativos si quieres
    emptyInputBehavior: 'zero'      // ← pone 0 si está vacío
  });
});
