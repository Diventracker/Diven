 //No Borrar-- Sirve en el sidebar
 window.parent.postMessage({
    tipo: "moduloActivo",
    url: window.location.pathname
  }, "*");

  //Funcion que modifica el rol en editar
document.querySelectorAll('.edit-button').forEach(btn => {
    btn.addEventListener('click', function () {
        const rolActual = this.getAttribute('data-rol');
        const selectRol = document.getElementById('editRol');

        // Limpiar opciones anteriores (excepto el placeholder)
        selectRol.innerHTML = '';

        // Crear y agregar la opción seleccionada primero
        const opcionSeleccionada = new Option(rolActual, rolActual, true, true);
        selectRol.add(opcionSeleccionada);

        // Lista de todos los posibles roles
        const rolesDisponibles = ['Administrador', 'Técnico', 'Vendedor'];

        // Agregar las demás opciones (excluyendo la ya seleccionada)
        rolesDisponibles
            .filter(rol => rol !== rolActual)
            .forEach(rol => {
                selectRol.add(new Option(rol, rol));
            });
    });
});

//Funcion para cuando se le da click al btn editar, y rellene los campos del form
setupEditButtons({
    buttonSelector: '.edit-button',
    modalFields: {
        id: 'editUsuarioId',
        nombre: 'editNombre',
        correo: 'editCorreo',
        telefono: 'editTelefono'        
    }
});

//Funcion Generica que enviar el form PUT y recibe la url
setupEditForm({
    formId: 'editUsuarioForm',
    buttonId: 'saveChanges',
    urlBase: '/usuario/editar',
    redirectUrlBase: '/usuarios',
    idField: 'editUsuarioId'
});

// Funcion  crud para eliminar datos 
setupDeleteButtons({
    buttonSelector: '.btn-outline-danger',
    hiddenInputId: 'usuarioIdToDelete',
    spanId: 'nombreUsuario',
    modalTitle: 'modalTitle', // Opcional: cambiar el título del modal
    confirmButtonId: 'confirmDeleteBtn',
    deleteUrlBase: '/usuario/eliminar',
    redirectUrlBase: '/usuarios'
});
