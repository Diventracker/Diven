document.querySelector("form").addEventListener("submit", function(e) {
    let valido = true;

    const inputsArchivos = [
        { input: document.getElementById("fileInput"), error: document.getElementById("errorImagenes") },
        { input: document.getElementById("fileInput2"), error: document.getElementById("errorImagenes2") },
        { input: document.getElementById("fileInput3"), error: document.getElementById("errorImagenes3") }
    ];

    inputsArchivos.forEach(({input, error}) => {
        if (input) {
            if (input.files.length === 0) {
                valido = false;
                error.style.display = "block";
            } else {
                error.style.display = "none";
            }
        }
    });

    if (!valido) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
});


//Funcion que para almacenar las imagenes en cada recuadro
function initImageUploader(dragAreaId, fileInputId, imagePreviewId) {
    let selectedImages = [];

    const dragArea = document.getElementById(dragAreaId);
    const fileInput = document.getElementById(fileInputId);
    const imagePreview = document.getElementById(imagePreviewId);

    // Clic en zona para abrir explorador
    dragArea.addEventListener('click', () => fileInput.click());

    // Drag & Drop
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

    // Selección manual
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
                            data-index="${index}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                    <small class="text-muted d-block mt-1 text-truncate">${file.name}</small>
                `;

                // Botón de borrado después de que el HTML ya existe
                col.querySelector('button[data-index]').addEventListener('click', () => {
                    removeImage(index);
                });
            };
            reader.readAsDataURL(file);

            imagePreview.appendChild(col);
        });
    }

    function removeImage(index) {
        selectedImages.splice(index, 1);
        updateImagePreview();
    }

    // 👇 Nuevo: limpiar imágenes desde fuera
    function clearImages() {
        selectedImages = [];
        fileInput.value = "";  // reset input
        updateImagePreview();
    }

    return {
        getImages: () => selectedImages,
        clearImages
    };
}

// Inicializar los dos apartados
const uploader1 = initImageUploader('dragArea', 'fileInput', 'imagePreview');
const uploader2 = initImageUploader('dragArea2', 'fileInput2', 'imagePreview2');
const uploader3 = initImageUploader('dragArea3', 'fileInput3', 'imagePreview3');
