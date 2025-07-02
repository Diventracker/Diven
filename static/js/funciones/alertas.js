//Esta es para mostrar alertas pero mucho mas avanzado 
function mostrarAlerta(id, mensaje = "", duracion = 3000) {
  const alerta = document.getElementById(id);

  if (!alerta) return;

  // Buscar el ícono y actualizar solo el texto (sin borrar el ícono)
  const icono = alerta.querySelector("i");
  const textoSpan = alerta.querySelector("span");

  if (textoSpan) {
    textoSpan.textContent = mensaje;
  } else {
    // Si no existe el <span>, lo crea al lado del ícono
    const span = document.createElement("span");
    span.textContent = mensaje;
    if (icono) {
      icono.after(span);
    } else {
      alerta.textContent = mensaje;
    }
  }

  alerta.style.display = "block";
  alerta.classList.add("show");

  setTimeout(() => {
    alerta.classList.remove("show");
    setTimeout(() => {
      alerta.style.display = "none";
    }, 150);
  }, duracion);
}
