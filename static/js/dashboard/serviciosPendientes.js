//Funcion que hace funcionar el dropdown 
document.addEventListener("DOMContentLoaded", async () => {
    const dropdown = document.querySelector(".dropdown");
    const dropdownMenu = document.querySelector(".notification-dropdown");
    const notificationCount = document.getElementById("notificationCount");

    try {
        const response = await fetch("/api/servicios-en-revision");
        const servicios = await response.json();

        if (servicios.length === 0) {
            dropdown.style.display = "none"; // Ocultar si no hay notificaciones
            return;
        }

        // Mostrar el número
        notificationCount.textContent = servicios.length;       

        servicios.forEach(s => {
            const item = document.createElement("div");
            item.classList.add("notification-item", "unread");
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1">Servicio #${s.id} en revisión</h6>
                        <p class="mb-1 text-muted small">${s.descripcion} - ${s.cliente}</p>                        
                    </div>
                    <i class="bi bi-exclamation-circle text-warning"></i>
                </div>
            `;
            dropdownMenu.appendChild(item);
        });

        // Botón al final
        const footer = document.createElement("div");
        footer.className = "text-center p-2";
        footer.innerHTML = `<a href="/servicios" class="btn btn-sm btn-outline-enviar">Ver todas</a>`;
        dropdownMenu.appendChild(document.createElement("div")).classList.add("dropdown-divider");
        dropdownMenu.appendChild(footer);

    } catch (err) {
        console.error("Error al cargar notificaciones:", err);
        dropdown.style.display = "none";
    }
});

