//Funcion que actualiza la busqueda del cliente en el modal crear
initSelect2Modal({
  selector: '#selectClientes',
  placeholder: 'Buscar cliente...',
  url: '/clientes/filtrar',
  processResultsMapper: c => ({
    id: c.id,
    text: `${c.nombre} (${c.documento})`
  }),
  parentModalSelector: '#modalRegistro',
  language: {
    noResults: () => "No se encontraron resultados",
    searching: () => "Buscando...",
    inputTooShort: (args) => `Por favor ingresa ${args.minimum - args.input.length} o más caracteres`
  }
});

document.addEventListener('DOMContentLoaded', () => {
    const inputMostrar = document.getElementById('precio_mostrar');
    const inputReal = document.getElementById('precio_real');
    const preview = document.getElementById('previewPrecio');

    // Obtener la instancia de AutoNumeric ya inicializada
    const autoInstance = AutoNumeric.getAutoNumericElement(inputMostrar);

    inputMostrar.addEventListener('input', () => {
        const valorNumerico = autoInstance.getNumber(); // sin $
        inputReal.value = valorNumerico;
        preview.textContent = `$${Number(valorNumerico).toLocaleString('es-CO')}`;
    });

    // También actualizar al cargar si ya tiene valor
    const inicial = autoInstance.getNumber();
    inputReal.value = inicial;
    preview.textContent = `$${Number(inicial).toLocaleString('es-CO')}`;
});

let selectedImages = [];

const dragArea = document.getElementById('dragArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');

// Clic en zona para abrir explorador
dragArea.addEventListener('click', () => fileInput.click());

// Arrastrar sobre la zona
dragArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dragArea.classList.add('dragover');
});

dragArea.addEventListener('dragleave', () => {
  dragArea.classList.remove('dragover');
});

dragArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dragArea.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});

// Selección manual de archivos
fileInput.addEventListener('change', (e) => {
  handleFiles(e.target.files);
});


function handleFiles(files) {
  const maxSizeMB = 10;
  const maxSizeBytes = maxSizeMB * 1024 * 1024;

  [...files].forEach(file => {
    if (!file.type.startsWith('image/')) {
      mostrarAlerta("alerta-warning", `El archivo "${file.name}" no es una imagen válida.`);
      return;
    }

    if (file.size > maxSizeBytes) {
      mostrarAlerta("alerta-warning", `La imagen "${file.name}" supera los ${maxSizeMB}MB.`);
      return;
    }

    selectedImages.push(file);
  });

  updateImagePreview();
}


function updateImagePreview() {
  imagePreview.innerHTML = '';
  if (selectedImages.length === 0) {
    imagePreview.style.display = 'none';
    return;
  }

  imagePreview.style.display = 'flex';

  selectedImages.forEach((file, index) => {
    const col = document.createElement('div');
    col.className = 'col-6 col-md-4';

    const reader = new FileReader();
    reader.onload = function(e) {
      col.innerHTML = `
        <div class="image-preview border position-relative">
          <img src="${e.target.result}" alt="Preview ${index + 1}" class="img-fluid rounded">
          <button type="button" class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1"
            onclick="removeImage(${index})">
            <i class="bi bi-trash"></i>
          </button>
        </div>
        <small class="text-muted d-block mt-1 text-truncate">${file.name}</small>
      `;
    };
    reader.readAsDataURL(file);

    imagePreview.appendChild(col);
  });
}

function removeImage(index) {
  selectedImages.splice(index, 1);
  updateImagePreview();
}
