import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

from flask import current_app, render_template


def _send_async(app, msg, smtp_server, smtp_port, smtp_user, smtp_pass):
    with app.app_context():
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            print(f"Email enviado a {msg['To']}")
        except Exception as e:
            print(f"Error enviando email a {msg['To']}: {e}")


def _enviar(app, msg):
    smtp_server = app.config.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = app.config.get('MAIL_PORT', 587)
    smtp_user = app.config.get('MAIL_USERNAME')
    smtp_pass = app.config.get('MAIL_PASSWORD')

    thread = Thread(target=_send_async, args=(app, msg, smtp_server, smtp_port, smtp_user, smtp_pass))
    thread.start()


def enviar_email_verificacion(email_destino, codigo):
    app = current_app._get_current_object()

    smtp_user = app.config.get('MAIL_USERNAME')
    smtp_pass = app.config.get('MAIL_PASSWORD')

    if not smtp_user or not smtp_pass:
        print("MAIL_USERNAME o MAIL_PASSWORD no configurados. Email no enviado.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'RiftZone - Tu código de verificación: {codigo}'
    msg['From'] = f'RiftZone <{smtp_user}>'
    msg['To'] = email_destino

    html_content = render_template('emails/verificacion.html', codigo=codigo)

    texto_plano = (
        f"Tu código de verificación para RiftZone es: {codigo}\n\n"
        "Ingresa este código en la página de pre-registro.\n"
        "El código expira en 10 minutos.\n\n"
        "- El equipo de RiftZone"
    )

    msg.attach(MIMEText(texto_plano, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    _enviar(app, msg)


def enviar_email_bienvenida(email_destino):
    app = current_app._get_current_object()

    smtp_user = app.config.get('MAIL_USERNAME')
    smtp_pass = app.config.get('MAIL_PASSWORD')

    if not smtp_user or not smtp_pass:
        print("MAIL_USERNAME o MAIL_PASSWORD no configurados. Email no enviado.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Bienvenido a RiftZone - Pre-Registro Exitoso'
    msg['From'] = f'RiftZone <{smtp_user}>'
    msg['To'] = email_destino

    html_content = render_template('emails/bienvenida.html', email=email_destino)

    texto_plano = (
        "Bienvenido a RiftZone!\n\n"
        "Tu pre-registro fue exitoso. Eres parte de los primeros en unirse.\n"
        "Te avisaremos cuando lancemos la plataforma.\n\n"
        "Únete a nuestra comunidad:\n"
        "Discord: https://discord.gg/C23PcduvTp\n"
        "WhatsApp: https://chat.whatsapp.com/tIbBcYrT6wq9C7jq5UpRTO4\n\n"
        "- El equipo de RiftZone"
    )

    msg.attach(MIMEText(texto_plano, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    _enviar(app, msg)
