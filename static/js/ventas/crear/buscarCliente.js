async function buscarCliente() {
    const cedulaInput = document.getElementById("cc-input");
    const cedula = cedulaInput.value;
    const alerta = document.getElementById("alerta-cliente-no-encontrado");

    try {
        const res = await fetch(`/clientes/buscar/${cedula}`);

        if (!res.ok) throw new Error("Cliente no encontrado");

        const cliente = await res.json();
        document.getElementById("nombre-cliente").value = cliente.nombre;
        document.getElementById("cc-cliente").value = cliente.cedula;
        document.getElementById("direccion-cliente").value = cliente.direccion;
        document.getElementById("id-cliente").value = cliente.id;
        // Ocultar alerta si estaba visible
        alerta.style.display = "none";

        // Limpiar el input y mostrar el placeholder que definiste en el HTML
        cedulaInput.value = "";

    } catch (error) {
        alerta.style.display = "block";

        setTimeout(() => {
            alerta.style.transition = "opacity 0.5s ease";
            alerta.style.opacity = "0";
            setTimeout(() => {
                alerta.style.display = "none";
                alerta.style.opacity = "";
                alerta.style.transition = "";
            }, 500);
        }, 3000);

        document.getElementById("nombre-cliente").value = "Cliente Mostrador";
        document.getElementById("cc-cliente").value = "00000000";
        document.getElementById("direccion-cliente").value = "Direcion General";
        document.getElementById("id-cliente").value = "55";
    }
}