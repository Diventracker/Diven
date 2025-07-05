async function generarVenta() {
    const idCliente = document.getElementById("id-cliente").value;
    const idUsuario = document.getElementById("id-usuario").value;
  
    const filas = document.querySelectorAll("#tabla-productos tbody tr:not(.table-active)");
  
    const productos = [];
  
    filas.forEach(fila => {
      const id_producto = fila.cells[0].textContent.trim();
      const precio_unitario = parseFloat(fila.cells[2].textContent.replace("$", ""));
      const cantidad = parseInt(fila.querySelector(".cantidad-input").value);
  
      productos.push({ id_producto, cantidad, precio_unitario });
    });

    // Validar que hay al menos un producto
    if (productos.length === 0) {
      mostrarAlerta("alerta-warning", "Debes agregar al menos un producto antes de generar la venta.");
      return;
    }
  
    const datosVenta = {
      id_cliente: parseInt(idCliente),
      id_usuario: parseInt(idUsuario),
      productos: productos
    };
  
    try {
      const res = await fetch("/ventas/generar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datosVenta)
      });
  
      const respuesta = await res.json();
  
      if (!res.ok) throw new Error(respuesta.error || "Error al registrar la venta");
  
      window.location.href = `/ventas/comprobante/${respuesta.id_venta}`; //Aqui enviar al formulario al momento de realizar la venta
    } catch (error) {
      mostrarAlerta("alerta-warning", "Error: " + error.message);
    }
  }