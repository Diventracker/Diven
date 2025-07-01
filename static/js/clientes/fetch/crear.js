document.getElementById('registrarCliente').addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/clientes/crear', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            alert("✅ " + (data.mensaje || "Cliente registrado"));
            form.reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalRegistro'));
            modal.hide();
        } else {
            alert("❌ Error: " + (data.detail || "No se pudo registrar el cliente"));
        }

    } catch (error) {
        console.error("Error de red:", error);
        alert("❌ Error de red. Intente nuevamente.");
    }
});