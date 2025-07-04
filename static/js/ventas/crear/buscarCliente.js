async function buscarCliente() {
    const cedulaInput = document.getElementById("cc-input");
    const cedula = cedulaInput.value.trim();

    try {
        const res = await fetch(`/clientes/buscar/${cedula}`);
        const json = await res.json();

        if (!json.success) {
            throw new Error(json.error || "Cliente no encontrado");
        }

        const cliente = json.data;

        mostrarAlerta("alerta-exito", "Cliente encontrado");

        document.getElementById("nombre-cliente").value = cliente.nombre;
        document.getElementById("direccion-cliente").value = cliente.direccion;
        document.getElementById("id-cliente").value = cliente.id;

        document.getElementById("tipo-documento-cliente").value = cliente.tipo_documento;
        document.getElementById("numero-documento-cliente").value = cliente.numero_documento;

        cedulaInput.value = "";

    } catch (error) {
        mostrarAlerta("alerta-warning", "Cliente no encontrado. Se usará cliente mostrador.");

        document.getElementById("nombre-cliente").value = "Cliente Mostrador";
        document.getElementById("direccion-cliente").value = "Dirección General";
        document.getElementById("id-cliente").value = "55";

        document.getElementById("tipo-documento-cliente").value = "Cédula";
        document.getElementById("numero-documento-cliente").value = "00000000";
    }
}
