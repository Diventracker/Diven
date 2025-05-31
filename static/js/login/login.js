document.addEventListener("DOMContentLoaded", () => {
  // Referencias a elementos DOM
  const loginCard = document.getElementById("login-card")
  const forgotEmailCard = document.getElementById("forgot-email-card")
  const verifyCodeCard = document.getElementById("verify-code-card")
  const forgotPasswordLink = document.getElementById("forgot-password-link")
  const recoveryEmailForm = document.getElementById("recovery-email-form")
  const verificationCodeForm = document.getElementById("verification-code-form")
  const verificationCodeInput = document.getElementById("verification-code")
  const verifyBtn = document.getElementById("verify-btn")
  const emailSentTo = document.getElementById("email-sent-to")
  const resendCodeBtn = document.getElementById("resend-code")
  const backButtons = document.querySelectorAll(".back-btn")

  // Evento para mostrar formulario de recuperación de contraseña
  forgotPasswordLink.addEventListener("click", (e) => {
    e.preventDefault()
    showCard(forgotEmailCard)
  })

  // Evento para enviar correo de recuperación
  recoveryEmailForm.addEventListener("submit", async (e) => {e.preventDefault();
  
    const correo = document.getElementById("recovery-email").value;

    localStorage.setItem("recoveryEmail", correo)

    if (correo) {
      try {
        const response = await fetch("/auth/recuperar", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ correo })
        });

        if (response.ok) {
          // Éxito: mostrar mensaje y siguiente paso
          emailSentTo.textContent = `Código enviado a: ${correo}`;
          showCard(verifyCodeCard);  // Cambiar de tarjeta o pantalla
        } else {
          const data = await response.json();
          alert(data.detail || "Ocurrió un error al enviar el código.");
        }

      } catch (error) {
        console.error("Error de red:", error);
        alert("Error al conectar con el servidor.");
      }
    }
  });

  const verificationForm = document.getElementById("verification-code-form");

  verificationForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = document.getElementById("verification-code").value.trim();
    const correo = localStorage.getItem("recoveryEmail");

    if (!correo) {
      alert("No se ha detectado un correo válido. Intenta desde el inicio.");
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
        alert(data.detail || "Error al validar el token");
      }
    } catch (error) {
      console.error("Error en la validación:", error);
      alert("Error del servidor");
    }
  });

  // Evento para reenviar código
  resendCodeBtn.addEventListener("click", (e) => {
    e.preventDefault()
    alert("Código reenviado")
  })

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