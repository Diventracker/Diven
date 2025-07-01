 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");
  

  
// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'clienteIdToDelete',
    spanId: 'nombreCliente',
    modalTitle: 'modalTitle',
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/cliente/eliminar',
    onSuccess: function (id, data) {
        // Actualiza la tabla, elimina fila o recarga
        location.reload(); // o usa JS para borrar la fila sin recargar
    },
    onError: function (id, data) {
        console.log("Error eliminando cliente:", data);
    }
});



//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editClienteId',
        nombre: 'editNombre',
        tipodocumento: 'editTipo',
        numerodocumento: 'editDocumento',
        direccion: 'editDireccion',
        telefono: 'editTelefono',
        email: 'editEmail'
    }
});



