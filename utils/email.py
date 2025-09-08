import os
import requests
from jinja2 import Environment, FileSystemLoader

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

# Configurar Jinja2 para cargar plantillas
env = Environment(loader=FileSystemLoader("utils/email"))

def enviar_correo(destinatario: str, asunto: str, template_name: str, **kwargs):
    # Renderizar plantilla con datos dinámicos
    template = env.get_template(template_name)
    html_content = template.render(**kwargs)

    # Estructura del correo para SendGrid
    data = {
        "personalizations": [{"to": [{"email": destinatario}]}],
        "from": {"email": "diventracker@hotmail.com"},  # El que verificaste en SendGrid
        "subject": asunto,
        "content": [{"type": "text/html", "value": html_content}],
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(SENDGRID_URL, headers=headers, json=data)
    if response.status_code != 202:
        print("Error al enviar correo:", response.text)
    else:
        print("Correo enviado con éxito ✅")
