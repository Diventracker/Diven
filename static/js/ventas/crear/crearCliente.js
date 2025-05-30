async function manejarEnvioCliente(e) {
  e.preventDefault();
  console.log("Evento submit ejecutado");

  const modalElement = document.getElementById("modalRegistro");
  let modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);

  const form = e.target;
  const formData = new FormData(form);

  try {
    const response = await fetch("/clientes/crear", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      alert("Error al crear cliente: " + (error.error || "Error desconocido"));
      return;
    }

    const data = await response.json();

    document.getElementById("id-cliente").value = data.id;
    document.getElementById("nombre-cliente").value = data.nombre_cliente;
    document.getElementById("cc-cliente").value = data.cedula;
    document.getElementById("direccion-cliente").value = data.direccion_cliente;

    alert("Cliente creado exitosamente");
    modal.hide();

  } catch (error) {
    console.error("Error:", error);
    alert("Hubo un error al enviar el formulario.");
  }
}

document.getElementById("form-cliente").addEventListener("submit", manejarEnvioCliente, { once: true });
