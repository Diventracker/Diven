document.getElementById('editClienteForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const idCliente = document.getElementById('editClienteId').value;

    try {
        const response = await fetch(`/cliente/editar/${idCliente}`, {
            method: 'PUT',
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            alert("✅ " + (data.mensaje || "Cliente actualizado con éxito"));
            form.reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalEditar'));
            modal.hide();
            // Aquí puedes recargar la tabla u otra acción
        } else {
            alert("❌ " + (data.error || "Error al actualizar cliente"));
        }

    } catch (error) {
        console.error("Error de red:", error);
        alert("❌ Error de red. Intenta nuevamente.");
    }
});