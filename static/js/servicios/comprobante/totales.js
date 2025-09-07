document.addEventListener("DOMContentLoaded", async () => {
    // Obtener el ID del servicio desde el atributo data-
    const serviceDiv = document.querySelector(".service-number");
    const idServicio = serviceDiv.dataset.servicioId;

    // Elementos donde mostraremos los valores
    const totalsSection = document.querySelector(".totals-section");
    const filas = totalsSection.querySelectorAll(".total-row span:last-child");

    try {
        // Llamada al backend
        const response = await fetch(`/servicios/${idServicio}/totales`);
        const data = await response.json();

        if (!data.success) {
            console.error("Error obteniendo totales:", data.message);
            return;
        }

        // Desestructurar la respuesta
        const { precio_base, adicionales, subtotal, iva, total } = data.data;

        // Formatear como moneda en COP
        const formato = (valor) => {
            return "$" + valor.toLocaleString("es-CO");
        };

        // Actualizar en el HTML
        filas[0].textContent = formato(precio_base); // Precio base
        filas[1].textContent = formato(adicionales); // Adicionales
        filas[2].textContent = formato(subtotal);    // Subtotal
        filas[3].textContent = formato(iva);         // IVA
        filas[4].textContent = formato(total);       // Total

    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }
});
