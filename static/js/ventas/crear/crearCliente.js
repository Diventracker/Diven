async function manejarEnvioCliente(e) {
  e.preventDefault();
  console.log("Evento submit ejecutado");

  const modalElement = document.getElementById("modalRegistro");
  let modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);

  const form = e.target;
  const formData = new FormData(form);
  const submitBtn = form.querySelector("button[type='submit']");
  submitBtn.disabled = true; // Evita reenvíos

  try {
    const response = await fetch("/clientes/crear", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      mostrarAlerta("alerta-warning-modal", "Error al crear cliente: " + (error.error || "Error desconocido"));
      return;
    }

    const data = await response.json();

    document.getElementById("id-cliente").value = data.id;
    document.getElementById("nombre-cliente").value = data.nombre_cliente;
    document.getElementById("tipo-documento-cliente").value = data.tipo_documento;
    document.getElementById("numero-documento-cliente").value = data.numero_documento;
    document.getElementById("direccion-cliente").value = data.direccion_cliente;

    modal.hide();
    mostrarAlerta("alerta-exito", "Cliente Creado Correctamente");
    form.reset(); // limpia el formulario después de crear

  } catch (error) {
    console.error("Error:", error);
    mostrarAlerta("alerta-warning", "Hubo un error al enviar el formulario.");
  } finally {
    submitBtn.disabled = false; //  Reactiva el botón
  }
}


document.getElementById("form-cliente").addEventListener("submit", manejarEnvioCliente);
