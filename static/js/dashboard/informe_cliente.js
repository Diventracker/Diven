document.addEventListener("DOMContentLoaded", () => {
    const formCliente = document.getElementById("form-informe-cliente");
    const inputCliente = document.getElementById("inputCliente");
    const datalist = document.getElementById("clientesList");

    // 🎯 Autocompletado por cédula o nombre
    inputCliente.addEventListener("input", async () => {
        const search = inputCliente.value.trim();
        if (search.length < 2) return;

        try {
            const res = await fetch(`/api/clientes/buscar?search=${encodeURIComponent(search)}`);
            const clientes = await res.json();

            datalist.innerHTML = "";
            clientes.forEach(c => {
                const option = document.createElement("option");
                option.value = c.documento; // ✅ SOLO usar la cédula como valor
                option.label = `${c.nombre} - ${c.documento}`; // para navegadores modernos
                datalist.appendChild(option);
            });
        } catch (err) {
            console.error("Error al autocompletar:", err);
        }
    });

    // 📄 Enviar el formulario
    formCliente.addEventListener("submit", async (e) => {
        e.preventDefault();

        const valor = inputCliente.value.trim();
        if (!valor) return alert("Por favor ingresa la cédula o nombre del cliente");

        try {
            const res = await fetch("/api/informe-por-cliente", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ identificador: valor })
            });

            if (!res.ok) {
                const error = await res.json();
                alert(error.detail || "No se pudo generar el informe.");
                return;
            }

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "informe_cliente.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            console.error("Error al generar informe:", err);
            alert("Ocurrió un error inesperado.");
        }
    });
});
