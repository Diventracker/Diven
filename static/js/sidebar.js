// Toggle sidebar on mobile
document.getElementById("menu-toggle").addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("sidebar-wrapper").classList.toggle("show");
});

// Handle window resize to reset sidebar state on desktop view
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
    document.getElementById("sidebar-wrapper").classList.remove("show");
}
});

//esta funcion es la del active sidebar, y los iframes
document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".list-group-item");
    const iframe = document.getElementById("modulosIframe");

    // Quitar cualquier clase 'active' existente
    links.forEach(l => l.classList.remove("active"));

    // Al cargar, verificar si hay uno guardado y marcarlo
    const activeLink = localStorage.getItem("activeMenu");
    let found = false;

    if (activeLink) {
        links.forEach(link => {
            if (link.getAttribute("data-link") === activeLink) {
                link.classList.add("active");
                found = true;
            }
        });
    }

    // Si no se encontró, marcar el primero como activo por defecto
    if (!found && links.length > 0) {
        links[0].classList.add("active");
        localStorage.setItem("activeMenu", links[0].getAttribute("data-link"));
    }

    // Cargar URL guardada para el iframe
    const ultimaURL = localStorage.getItem("iframeURL");
    if (ultimaURL) {
        iframe.src = ultimaURL;
    } else if (found) {
        // Si hay menú activo guardado pero no URL, puedes cargar esa URL en iframe
        iframe.src = activeLink;
    } else if (links.length > 0) {
        // Si no hay nada guardado, cargar URL del primer link
        iframe.src = links[0].getAttribute("data-link");
        localStorage.setItem("iframeURL", iframe.src);
    }

    // Escuchar clics para actualizar el active y el iframe
    links.forEach(link => {
        link.addEventListener("click", function () {
            links.forEach(l => l.classList.remove("active"));
            this.classList.add("active");
            const url = this.getAttribute("data-link");
            localStorage.setItem("activeMenu", url);
            iframe.src = url;
            localStorage.setItem("iframeURL", url);
        });
    });
});


// Cuando el usuario cambia de página dentro del iframe
function cargarPagina(url) {
    iframe.src = url;
    localStorage.setItem("iframeURL", url); // Guardar en localStorage
}

//fetch para cerrar session y eliminar todo el cache y esas mmadas
function cerrarSesion() {
  // Limpiar cualquier dato en localStorage relacionado con la sesión
  localStorage.removeItem("iframeURL");
  localStorage.removeItem("activeMenu");

  // Hacer la solicitud POST al backend para cerrar sesión
  fetch("/logout", {
    method: "POST",
    credentials: "include"
  }).then(() => {
    window.location.href = "/login";
  }).catch(() => {
    alert("Error al cerrar sesión");
  });
}