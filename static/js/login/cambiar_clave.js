// Función para mostrar/ocultar contraseña
function togglePassword(inputId, button) {
  const input = document.getElementById(inputId);
  const icon = button.querySelector('i');

  if (input.type === 'password') {
    input.type = 'text';
    icon.className = 'bi bi-eye-slash';
  } else {
    input.type = 'password';
    icon.className = 'bi bi-eye';
  }
}

// Validación de confirmación de contraseña
const newPassword = document.getElementById('newPassword');
const confirmPassword = document.getElementById('confirmPassword');

function validarCoincidencia() {
  if (confirmPassword.value && newPassword.value !== confirmPassword.value) {
    confirmPassword.setCustomValidity('Las contraseñas no coinciden');
    confirmPassword.classList.add('is-invalid');
  } else {
    confirmPassword.setCustomValidity('');
    confirmPassword.classList.remove('is-invalid');
  }
}

newPassword.addEventListener('input', validarCoincidencia);
confirmPassword.addEventListener('input', validarCoincidencia);

// Función principal
document.addEventListener("DOMContentLoaded", () => {
  const passwordForm = document.getElementById("passwordForm");
  const currentPasswordInput = document.getElementById("currentPassword");
  const currentPasswordDiv = currentPasswordInput.closest(".form-floating");

  const token = sessionStorage.getItem("recuperacion_token");
  const correo = sessionStorage.getItem("correo_recuperacion");

  const vieneDeRecuperacion = token && correo;

  // Si viene de recuperación, ocultar campo de contraseña actual
  if (vieneDeRecuperacion) {
    currentPasswordDiv.style.display = "none";
    currentPasswordInput.required = false;
  }

  passwordForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nuevaClave = document.getElementById("newPassword").value;
    const confirmarClave = document.getElementById("confirmPassword").value;

    const body = {
      nueva_clave: nuevaClave,
      confirmar_clave: confirmarClave,
    };

    if (vieneDeRecuperacion) {
      body.token = token;
      body.correo = correo;
    } else {
      body.clave_actual = currentPasswordInput.value;
    }

    try {
      const response = await fetch("/use/cambiar-clave", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();
      if (response.ok) {
        mostrarAlerta("alerta-success", "Contraseña actualizada correctamente");

        if (vieneDeRecuperacion) {
          sessionStorage.removeItem("recuperacion_token");
          sessionStorage.removeItem("correo_recuperacion");
          window.location.href = "/login";
        } else {
          fetch('/logout', {
            method: 'POST',
            credentials: 'include'
          }).then(() => {
            localStorage.removeItem("iframeURL");
            localStorage.removeItem("activeMenu");
            window.location.href = '/login';
          }).catch(() => {
            mostrarAlerta("alerta-warning", "Error al cerrar sesión");
          });
        }
      } else {
        mostrarAlerta("alerta-warning", data.detail || "Error al cambiar la contraseña");
      }
    } catch (err) {
      mostrarAlerta("alerta-warning", "Error de red o del servidor");
      console.error(err);
    }
  });
});

function cancelForm() {
  window.history.back();
}
