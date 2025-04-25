document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    sidebarToggle.addEventListener('click', function () {
        // Alternar la clase "collapsed" para el sidebar
        sidebar.classList.toggle('collapsed');
    });
});