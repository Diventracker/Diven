 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  

// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'serviceIdToDelete',
    spanId: 'nombreCliente', // Puedes cambiarlo si es otro campo
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/servicio/eliminar',
    redirectUrlBase: '/servicios'
});



