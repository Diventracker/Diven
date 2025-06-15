async function buscarCliente() {
    const cedulaInput = document.getElementById("cc-input");
    const cedula = cedulaInput.value;

    try {
        const res = await fetch(`/clientes/buscar/${cedula}`);

        if (!res.ok) throw new Error("Cliente no encontrado");

        const cliente = await res.json();
        mostrarAlerta("alerta-exito", "¡Cliente Actualizado!");

        document.getElementById("nombre-cliente").value = cliente.nombre;
        document.getElementById("direccion-cliente").value = cliente.direccion;
        document.getElementById("id-cliente").value = cliente.id;

        // Campos nuevos
        document.getElementById("tipo-documento-cliente").value = cliente.tipo_documento;
        document.getElementById("numero-documento-cliente").value = cliente.numero_documento;

        cedulaInput.value = "";

    } catch (error) {
        mostrarAlerta("alerta-warning", "¡Cliente no encontrado!");

        document.getElementById("nombre-cliente").value = "Cliente Mostrador";
        document.getElementById("direccion-cliente").value = "Direcion General";
        document.getElementById("id-cliente").value = "55";

        document.getElementById("tipo-documento-cliente").value = "Cédula";
        document.getElementById("numero-documento-cliente").value = "00000000";
    }
}
