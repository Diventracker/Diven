document.addEventListener("DOMContentLoaded", () => {
  // Referencias a elementos DOM
  const loginCard = document.getElementById("login-card")
  const forgotEmailCard = document.getElementById("forgot-email-card")
  const verifyCodeCard = document.getElementById("verify-code-card")
  const forgotPasswordLink = document.getElementById("forgot-password-link")
  const recoveryEmailForm = document.getElementById("recovery-email-form")
  const verificationForm = document.getElementById("verification-code-form");
  const verificationCodeInput = document.getElementById("verification-code")
  const verifyBtn = document.getElementById("verify-btn")
  const emailSentTo = document.getElementById("email-sent-to")
  const backButtons = document.querySelectorAll(".back-btn")
  const resendCodeBtn = document.getElementById("resendCodeBtn");
  const spinner = resendCodeBtn.querySelector(".spinner-border");
  const btnText = resendCodeBtn.querySelector(".btn-text");
  const enviarBtn = recoveryEmailForm.querySelector("button[type='submit']");

  // Evento para mostrar formulario de recuperación de contraseña
  forgotPasswordLink.addEventListener("click", (e) => {
    e.preventDefault()
    showCard(forgotEmailCard)
  })

  // Función reutilizable para enviar código

async function enviarCodigoRecuperacion(correo) {
  try {
    // Desactivar el botón y mostrar "Enviando..."
    enviarBtn.disabled = true;
    enviarBtn.textContent = "Enviando...";

    const response = await fetch("/auth/recuperar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ correo })
    });

    if (response.ok) {
      emailSentTo.textContent = `Código enviado a: ${correo}`;
      showCard(verifyCodeCard);  // Cambiar pantalla
    } else {
      const data = await response.json();
      mostrarAlerta("alerta-warning", data.detail || "Ocurrió un error al enviar el código.");
    }

  } catch (error) {
    console.error("Error de red:", error);
    mostrarAlerta("alerta-warning", "Error al conectar con el servidor.");
  } finally {
    // Rehabilitar el botón
    enviarBtn.disabled = false;
    enviarBtn.textContent = "Enviar Código";
  }
}

// Evento para enviar correo de recuperación
recoveryEmailForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const correo = document.getElementById("recovery-email").value;
  localStorage.setItem("recoveryEmail", correo);

  if (correo) {
    await enviarCodigoRecuperacion(correo);
  }
});

// Evento para reenviar código
resendCodeBtn.addEventListener("click", async (e) => {
  e.preventDefault();

  const correo = localStorage.getItem("recoveryEmail");
  if (!correo) {
    mostrarAlerta("alerta-warning", "No se encontró el correo para reenviar el código.");
    return;
  }

  // Desactivar botón y mostrar spinner
  resendCodeBtn.disabled = true;
  spinner.classList.remove("d-none");
  let seconds = 30;

  const updateButtonText = () => {
    btnText.textContent = `Reenviar en ${seconds}s`;
  };

  updateButtonText();

  const interval = setInterval(() => {
    seconds--;
    updateButtonText();

    if (seconds <= 0) {
      clearInterval(interval);
      resendCodeBtn.disabled = false;
      btnText.textContent = "Reenviar código";
      spinner.classList.add("d-none");
    }
  }, 3000);

  // Reenviar código
  try {
    const response = await fetch("/auth/recuperar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ correo })
    });

    if (response.ok) {
      mostrarAlerta("alerta-success", "Código reenviado");
    } else {
      const data = await response.json();
      mostrarAlerta("alerta-warning", data.detail || "Ocurrió un error al reenviar el código.");
    }
  } catch (error) {
    mostrarAlerta("alerta-warning", "Error de red");
    console.error(error);
  }
});


  //Evento para validar el token enviado
  verificationForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = document.getElementById("verification-code").value.trim();
    const correo = localStorage.getItem("recoveryEmail");

    if (!correo) {
      mostrarAlerta("alerta-warning", "No se ha detectado un correo válido. Intenta desde el inicio.");
      return;
    }

    try {
      const response = await fetch("/auth/validar-token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          correo: correo,
          token: token
        })
      });

      const data = await response.json();

      if (response.ok && data.recuperacion) {
        // Guardar el token y el correo de recuperación
        sessionStorage.setItem("recuperacion_token", data.token);
        sessionStorage.setItem("correo_recuperacion", data.correo);
        window.location.href = "/cambiar-clave";
      } else {
        mostrarAlerta("alerta-warning", data.detail || "Error al validar el token");
      }
    } catch (error) {
      console.error("Error en la validación:", error);
      mostrarAlerta("alerta-warning", "Error del servidor");
    }
  });

  // Eventos para botones de regreso
  backButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const targetCard = document.getElementById(this.dataset.target)
      showCard(targetCard)
    })
  })

  // Validación del código de verificación (solo números y máximo 6 dígitos)
  verificationCodeInput.addEventListener("input", function () {
    this.value = this.value.replace(/\D/g, "").slice(0, 6)
    verifyBtn.disabled = this.value.length !== 6
  })

  // Función para mostrar una tarjeta y ocultar las demás
  function showCard(cardToShow) {
    ;[loginCard, forgotEmailCard, verifyCodeCard].forEach((card) => {
      if (card === cardToShow) {
        card.classList.remove("d-none")
      } else {
        card.classList.add("d-none")
      }
    })
  }
})

// Obtener los parámetros de la URL
const params = new URLSearchParams(window.location.search);

if (params.get("error") === "1") {
  mostrarAlerta("alerta-warning", "¡Credenciales Incorrectos!");
}
if (params.get("error") === "2") {
  mostrarAlerta("alerta-warning", "¡No has Iniciado Sessión!");
}