import os
import smtplib
from email.mime.image import MIMEImage
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


def enviar_email_bienvenida(email_destino):
    app = current_app._get_current_object()

    smtp_server = app.config.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = app.config.get('MAIL_PORT', 587)
    smtp_user = app.config.get('MAIL_USERNAME')
    smtp_pass = app.config.get('MAIL_PASSWORD')

    if not smtp_user or not smtp_pass:
        print("MAIL_USERNAME o MAIL_PASSWORD no configurados. Email no enviado.")
        return

    msg = MIMEMultipart('related')

    msg['Subject'] = 'Bienvenido a RiftZone - Pre-Registro Exitoso'
    msg['From'] = f'RiftZone <{smtp_user}>'
    msg['To'] = email_destino

    html_content = render_template('emails/bienvenida.html', email=email_destino)

    texto_plano = (
        "Bienvenido a RiftZone!\n\n"
        "Tu pre-registro fue exitoso. Eres parte de los primeros en unirse.\n"
        "Te avisaremos cuando lancemos la plataforma.\n\n"
        "- El equipo de RiftZone"
    )

    alt_part = MIMEMultipart('alternative')
    alt_part.attach(MIMEText(texto_plano, 'plain'))
    alt_part.attach(MIMEText(html_content, 'html'))
    msg.attach(alt_part)

    logo_path = os.path.join(app.root_path, 'static', 'img', 'riftzone_logo_email.jpg')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_img = MIMEImage(f.read(), _subtype='jpeg')
            logo_img.add_header('Content-ID', '<riftzone_logo>')
            logo_img.add_header('Content-Disposition', 'inline', filename='riftzone_logo.jpg')
            msg.attach(logo_img)

    thread = Thread(target=_send_async, args=(app, msg, smtp_server, smtp_port, smtp_user, smtp_pass))
    thread.start()
