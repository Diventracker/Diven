document.addEventListener("shown.bs.tab", function (event) {
  const target = event.target.getAttribute("data-bs-target"); // ej: "#tab2"
  if (target === "#tab2") {
    obtenerProductosBajoStock();
  }
});


//Este es el select2 de los productos
initSelect2Modal({
  selector: '#selectProducto',
  placeholder: 'Buscar producto...',
  url: '/api/productos?con_stock=false',
  processResultsMapper: p => ({
    id: p.codigo,
    text: `${p.nombre} - ${p.modelo} | $${p.precio} (Stock: ${p.stock})`,
    // En data adicional
    proveedor: p.proveedor,
    stock: p.stock,
    descripcion: p.descripcion
    }),
  parentModalSelector: null,  // si el select está dentro del modal de ventas
  language: {
    noResults: () => "No se encontraron resultados",
    searching: () => "Buscando...",
    inputTooShort: (args) => `Por favor ingresa ${args.minimum - args.input.length} o más caracteres`
  }
});

//Esto settea los inputs con los valores que vienen del select2
$('#selectProducto').on('select2:select', function (e) {
  const data = e.params.data;
  $('#proveedor').val(data.proveedor || '');
  $('#stockQuantity').val(data.stock || '0');
  $('#productoDescripcion').val(data.descripcion || '');
  actualizarPreview(); 
});

//Funcion para la card de localizar productos con bajo stock
function obtenerProductosBajoStock() {
  fetch('/stock/bajo')
    .then(response => response.json())
    .then(data => {
      const contenedor = document.querySelector("#productosBajoStock");
      contenedor.innerHTML = ""; // Limpiar

      if (data.length === 0) {
        contenedor.innerHTML = `
          <span class="text-muted small">Todos los productos tienen stock suficiente.</span>
        `;
        return;
      }

      data.forEach(producto => {
        let badgeClass = "bg-success";
        let textoEstado = "Stock suficiente";

        if (producto.stock < 5) {
          badgeClass = "bg-danger";
          textoEstado = "Stock crítico";
        } else if (producto.stock < 10) {
          badgeClass = "bg-warning text-dark";
          textoEstado = "Stock bajo";
        }

        const item = `
          <a href="#" class="list-group-item list-group-item-action py-3 producto-alerta"
            data-id="${producto.codigo}"
            data-nombre="${producto.nombre}"
            data-descripcion="${producto.descripcion}"
            data-proveedor="${producto.proveedor}"
            data-stock="${producto.stock}">
            <div class="d-flex w-100 justify-content-between">
              <h6 class="mb-1">${producto.nombre} (${producto.modelo})</h6>
              <span class="badge ${badgeClass}">${textoEstado}</span>
            </div>
            <p class="mb-1 small text-muted">Quedan ${producto.stock} unidades (mínimo: 5)</p>
          </a>
        `;
        contenedor.insertAdjacentHTML("beforeend", item);
      });
    });
}

let currentActiveItem = null; // Variable para guardar el item activo

//Hace que al darle click a los productos se setteen a la izquierda los datos
document.querySelector('.list-group.list-group-flush').addEventListener('click', function(e) {
  const target = e.target.closest('a.list-group-item');
  if (!target) return;

  e.preventDefault();

   // Quitar clase active del anterior y agregar al nuevo
  if (currentActiveItem) {
    currentActiveItem.classList.remove('active');
  }
  target.classList.add('active');
  currentActiveItem = target;

  // Setear select2 con el producto seleccionado
  const selectProducto = $('#selectProducto');
  const option = new Option(`${target.dataset.nombre} (${target.dataset.id})`, target.dataset.id, true, true);
  selectProducto.append(option).trigger('change');

  // Setear inputs
  document.getElementById('proveedor').value = target.dataset.proveedor;
  document.getElementById('stockQuantity').value = target.dataset.stock;
  document.getElementById('productoDescripcion').value = target.dataset.descripcion;
  actualizarPreview(); 
});

// Validar cambio manual en select2 y remover clase active si ya no coincide
$('#selectProducto').on('change', function(e) {
  const selectedValue = $(this).val();

  // Si hay un item activo y ya no coincide, se le quita el active
  if (currentActiveItem && currentActiveItem.dataset.id !== selectedValue) {
    currentActiveItem.classList.remove('active');
    currentActiveItem = null;
  }

  // Buscar en la lista un item que coincida con el valor seleccionado
  const matchingItem = document.querySelector(`.list-group.list-group-flush a.list-group-item[data-id="${selectedValue}"]`);
  if (matchingItem) {
    // Quitar el active anterior si existe
    if (currentActiveItem && currentActiveItem !== matchingItem) {
      currentActiveItem.classList.remove('active');
    }

    // Agregar active al nuevo matching item
    matchingItem.classList.add('active');
    currentActiveItem = matchingItem;
  }
});

//Esta funcion lo que hace es manejar el card amarillo del warning segun el stock
const inputStockNew = document.getElementById("stockNew");
const previewCard = document.getElementById("previewCard");
const previewCantidad = document.getElementById("previewCantidad");
const previewFinal = document.getElementById("previewFinal");
const selectProducto = document.getElementById("selectProducto");
const inputStockActual = document.getElementById("stockQuantity");
const submitButton = document.getElementById("btnActualizarStock"); // <-- el botón

let stockActual = 0;

function actualizarPreview() {
  const cantidad = parseInt(inputStockNew.value) || 0;
  const productoSeleccionado = selectProducto.value;

  stockActual = parseInt(inputStockActual.value) || 0;
  const total = stockActual + cantidad;

  const condicionesValidas = cantidad > 0 && productoSeleccionado;

  // Mostrar u ocultar la vista previa
  if (condicionesValidas) {
    previewCard.classList.remove("d-none");
    previewCantidad.textContent = `Se agregarán ${cantidad} unidades.`;
    previewFinal.textContent = `Stock final: ${total} unidades.`;
  } else {
    previewCard.classList.add("d-none");
  }

  // Habilitar o deshabilitar el botón
  submitButton.disabled = !condicionesValidas;
}

// ⏺ Listeners para cambios
inputStockNew.addEventListener("input", actualizarPreview);