from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("utils/email"))

# Puedes usar Jinja2 directamente sin Request si es un correo
def enviar_correo(destinatario: str, asunto: str, template_name: str, **kwargs):
    remitente = "rimuru.work@gmail.com"
    clave_email = "zqvp dthg fgck gvxd" # Nota: No es recomendable almacenar contraseñas de esta manera

    # Renderizar el template con datos
    template = env.get_template(template_name)
    html_content = template.render(**kwargs)

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.add_alternative(html_content, subtype="html")

    # Enviar el correo
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, clave_email)
        smtp.send_message(mensaje)
