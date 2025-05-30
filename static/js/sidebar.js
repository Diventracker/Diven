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


document.addEventListener("DOMContentLoaded", function () {
   const links = document.querySelectorAll(".list-group-item");

   links.forEach(link => {
       link.addEventListener("click", function () {
           // Quitar 'active' de todos
           links.forEach(l => l.classList.remove("active"));

           // Agregar 'active' al clicado
           this.classList.add("active");

           // Guardar en localStorage el href o identificador del botón
           localStorage.setItem("activeMenu", this.getAttribute("data-link"));
       });
   });

   // Al cargar, verificar si hay uno guardado y marcarlo
   const activeLink = localStorage.getItem("activeMenu");
   if (activeLink) {
       links.forEach(link => {
           if (link.getAttribute("data-link") === activeLink) {
               link.classList.add("active");
           }
       });
   }
});

const iframe = document.getElementById("modulosIframe");

// Al cargar la página, revisa si hay una URL guardada
window.addEventListener("DOMContentLoaded", () => {
    const ultimaURL = localStorage.getItem("iframeURL");
    if (ultimaURL) {
    iframe.src = ultimaURL;
    }
});

// Cuando el usuario cambia de página dentro del iframe
function cargarPagina(url) {
    iframe.src = url;
    localStorage.setItem("iframeURL", url); // Guardar en localStorage
}