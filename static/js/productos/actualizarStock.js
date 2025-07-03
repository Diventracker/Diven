//Este fetch es el que recibe la informacion para actualizar el stock del producto seleccionado
document.getElementById("actualizar_stock").addEventListener("submit", async function (e) {
  e.preventDefault(); // evita envío tradicional

  const form = e.target;
  const productoId = form.selectProducto.value;
  const cantidad = parseInt(form.stockNew.value);

  if (!productoId || isNaN(cantidad) || cantidad <= 0) {
    mostrarAlerta("alerta-warning", "Selecciona un producto válido y una cantidad mayor a cero.");
    return;
  }

  try {
    const respuesta = await fetch(`/productos/${productoId}/stock`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ cantidad })
    });

    const data = await respuesta.json();

    if (!respuesta.ok) throw new Error(data.detail || "Error al actualizar");

    mostrarAlerta("alerta-success", `${data.mensaje}. Nuevo stock: ${data.stock_final}`);

    // Actualiza la vista
    document.getElementById("stockQuantity").value = data.stock_final;
    form.stockNew.value = "";
    document.getElementById("previewCard").classList.add("d-none");
    obtenerProductosBajoStock();
  } catch (error) {
    mostrarAlerta("alerta-warning", " " + error.message);
  }
});