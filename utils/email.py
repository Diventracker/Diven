from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader

# Puedes usar Jinja2 directamente sin Request si es un correo
env = Environment(loader=FileSystemLoader("usuarios/templates/email"))

def enviar_correo(destinatario: str, asunto: str, nombre: str, clave: str):
    remitente = "rimuru.work@gmail.com"
    clave_email = "zqvp dthg fgck gvxd"  # Nota: No es recomendable almacenar contraseñas de esta manera

    # Renderizar el template con datos
    template = env.get_template("email_pass.html")
    html_content = template.render(nombre=nombre, clave=clave)

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.add_alternative(html_content, subtype="html")

    # Enviar el correo
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, clave_email)
        smtp.send_message(mensaje)
