document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    sidebarToggle.addEventListener('click', function () {
        // Alternar la clase "collapsed" para el sidebar
        sidebar.classList.toggle('collapsed');
    });
});

window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      window.location.reload();
    }
  });