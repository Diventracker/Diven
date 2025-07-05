document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = new FormData(this);

    try {
        const res = await fetch("/api/login", {
            method: "POST",
            body: form
        });

        const data = await res.json();

        if (!data.success) {
            mostrarAlerta("alerta-warning", "Error: " + data.error);
            return;
        }

        // Si todo bien, redirigimos
        window.location.href = data.redirect;

    } catch (err) {
        console.error(err);
        mostrarAlerta("alerta-warning", "Error al procesar el login");
    }
});