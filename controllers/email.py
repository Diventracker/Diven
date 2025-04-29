from fastapi.templating import Jinja2Templates
from email.message import EmailMessage
import smtplib
from starlette.requests import Request
from jinja2 import Environment, FileSystemLoader

# Cargar las plantillas
templates = Jinja2Templates(directory="templates")


# Puedes usar Jinja2 directamente sin Request si es un correo
env = Environment(loader=FileSystemLoader("templates/email"))

def enviar_correo(destinatario: str, asunto: str, nombre: str, clave: str):
    remitente = "rimuru.work@gmail.com"
    clave_email = "zqvp dthg fgck gvxd"

    # Renderizar el template con datos
    template = env.get_template("email_pass.html")
    html_content = template.render(nombre=nombre, clave=clave)

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, clave_email)
        smtp.send_message(mensaje)