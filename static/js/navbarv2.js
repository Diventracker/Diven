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

//Funcion para el active del sidebar
// Espera a que todo esté cargado
document.addEventListener("DOMContentLoaded", function () {
   const links = document.querySelectorAll(".list-group-item");

   links.forEach(link => {
       link.addEventListener("click", function () {
       // Quitar 'active' de todos los botones
       links.forEach(l => l.classList.remove("active"));

       // Agregar 'active' solo al que se clicó
       this.classList.add("active");
       });
    });
});