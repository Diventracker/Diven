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

// Escuchar cambios en ambos campos
newPassword.addEventListener('input', validarCoincidencia);
confirmPassword.addEventListener('input', validarCoincidencia);



//Funcion para manejar el envio del formulario y ocultar ciertos campos
//cuando viene de recuperacion
document.addEventListener("DOMContentLoaded", () => {
    const passwordForm = document.getElementById("passwordForm");
    const currentPasswordDiv = document.getElementById("currentPassword").closest(".form-floating");

    const token = sessionStorage.getItem("recuperacion_token");
    const correo = sessionStorage.getItem("correo_recuperacion");

    // Si hay token, ocultar campo de contraseña actual
    if (token && correo) {
        currentPasswordDiv.style.display = "none";
    }
    if (token && correo) {
        currentPasswordDiv.style.display = "none";
        document.getElementById("currentPassword").required = false;
        } else {
        currentPasswordDiv.style.display = "block";
        document.getElementById("currentPassword").required = true;
        }

    passwordForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nuevaClave = document.getElementById("newPassword").value;
        const confirmarClave = document.getElementById("confirmPassword").value;

        const body = {
        nueva_clave: nuevaClave,
        confirmar_clave: confirmarClave,
        };

        if (token && correo) {
        body.token = token;
        body.correo = correo;
        } else {
        const claveActual = document.getElementById("currentPassword").value;
        body.clave_actual = claveActual;
        }

        try {
        const response = await fetch("/auth/cambiar-clave", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        const data = await response.json();
        if (response.ok) {
            alert("Contraseña actualizada correctamente");

            if (token) {
                sessionStorage.removeItem("recuperacion_token");
                sessionStorage.removeItem("correo_recuperacion");
                window.location.href = "/login";
                } else {
                fetch('/logout', {
                    method: 'POST',
                    credentials: 'include'
                })
                .then(() => {
                    window.location.href = '/login';
                })
                .catch(() => {
                    alert('Error al cerrar sesión');
                });
                }
        } else {
            alert(data.detail || "Error al cambiar la contraseña");
        }
        } catch (err) {
        alert("Error de red o del servidor");
        console.error(err);
        }
    });
    });

  function cancelForm() {
    window.history.back();
  }

