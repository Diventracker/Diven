async function buscarCliente() {
    const cedulaInput = document.getElementById("cc-input");
    const cedula = cedulaInput.value;

    try {
        const res = await fetch(`/clientes/buscar/${cedula}`);

        if (!res.ok) throw new Error("Cliente no encontrado");

        const cliente = await res.json();
        mostrarAlerta("alerta-exito", "¡Cliente Actualizado!");
        document.getElementById("nombre-cliente").value = cliente.nombre;
        document.getElementById("cc-cliente").value = cliente.cedula;
        document.getElementById("direccion-cliente").value = cliente.direccion;
        document.getElementById("id-cliente").value = cliente.id;

        // Limpiar el input y mostrar el placeholder que definiste en el HTML
        cedulaInput.value = "";

    } catch (error) {
        mostrarAlerta("alerta-warning", "¡Cliente no encontrado!");

        document.getElementById("nombre-cliente").value = "Cliente Mostrador";
        document.getElementById("cc-cliente").value = "00000000";
        document.getElementById("direccion-cliente").value = "Direcion General";
        document.getElementById("id-cliente").value = "55";
    }
}