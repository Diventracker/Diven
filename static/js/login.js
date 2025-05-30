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
  recoveryEmailForm.addEventListener("submit", (e) => {
    e.preventDefault()
    const email = document.getElementById("recovery-email").value
    if (email) {
      emailSentTo.textContent = `Código enviado a: ${email}`
      showCard(verifyCodeCard)
    }
  })

  // Evento para verificar código
  verificationCodeForm.addEventListener("submit", (e) => {
    e.preventDefault()
    const code = verificationCodeInput.value
    if (code.length === 6) {
      alert("Código verificado correctamente")
      // Aquí puedes agregar la lógica para restablecer la contraseña
      showCard(loginCard)
      verificationCodeInput.value = ""
      document.getElementById("recovery-email").value = ""
    }
  })

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