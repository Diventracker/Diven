// Funcionalidad básica para los botones
document.querySelector('.btn:has(.bi-printer)').addEventListener('click', function () {
    window.print();
});

document.querySelector('.btn:has(.bi-envelope)').addEventListener('click', function () {
    alert('Función de envío por email - Por implementar');
});

document.getElementById("btnDescargar").addEventListener("click", descargarPDF);
function descargarPDF() {
    const original = document.getElementById('comprobante');

    // Clonar el contenido del comprobante
    const clon = original.cloneNode(true);

    // Eliminar elementos no imprimibles
    clon.querySelectorAll('.no-print, .comprobante-footer, .btn-close').forEach(el => el.remove());

    // Crear un contenedor temporal oculto
    const temp = document.createElement('div');
    temp.style.position = 'fixed';
    temp.style.left = '-9999px';
    temp.style.top = '0';
    temp.style.backgroundColor = 'white';
    temp.appendChild(clon);
    document.body.appendChild(temp);

    html2pdf().set({
        margin: 10,
        filename: 'comprobante-servicio.pdf',
        html2canvas: { scale: 2, scrollY: 0 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }).from(clon).save().then(() => {
        document.body.removeChild(temp);
    });
}