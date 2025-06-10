//generar infrome
document.getElementById('form-informe').addEventListener('submit', async function (e) {
                e.preventDefault();
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());

                const response = await fetch('/api/generar-informe', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = "informe.pdf";
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                }
            });