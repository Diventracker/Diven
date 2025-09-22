async function generarVenta() {
  const idCliente = document.getElementById("id-cliente").value;
  const idUsuario = document.getElementById("id-usuario").value;

  const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
  const productos = [];

  if (filas.length === 0) {
    mostrarAlerta("alerta-warning", "Debes agregar al menos un producto antes de generar la venta.");
    return;
  }

  for (const fila of filas) {
    const id_producto = fila.cells[0].textContent.trim();
    const precio_unitario = parseFloat(
      fila.cells[2].textContent.replace(/[^\d]/g, "")
    );

    const cantidad = parseInt(fila.querySelector(".cantidad-input").value, 10);


    if (isNaN(cantidad) || cantidad < 1) {
      mostrarAlerta("alerta-warning", "Las cantidades deben ser mínimo 1. Corrige antes de enviar la venta.");
      fila.querySelector(".cantidad-input").focus();
      return; // detener la función, NO enviar
    }

    productos.push({ id_producto, cantidad, precio_unitario });
  }

  const datosVenta = {
    id_cliente: parseInt(idCliente),
    id_usuario: parseInt(idUsuario),
    productos,
  };

  try {
    const res = await fetch("/ventas/generar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datosVenta),
    });

    const respuesta = await res.json();

    if (!res.ok) throw new Error(respuesta.error || "Error al registrar la venta");

    // Redirigir al comprobante
    window.location.href = `/ventas/comprobante/${respuesta.id_venta}`;
  } catch (error) {
    mostrarAlerta("alerta-warning", "Error: " + error.message);
  }
}

