import re

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy.exc import IntegrityError

from app.factories.app_factory import db
from app.models.pre_registro import PreRegistro

pre_registro_bp = Blueprint('pre_registro', __name__)

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)


@pre_registro_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@pre_registro_bp.route('/pre-registro', methods=['POST'])
def registrar():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(status='error', message='Solicitud inválida.'), 400

    email = (data.get('email') or '').strip().lower()

    if not email:
        return jsonify(status='error', message='El correo es obligatorio.'), 400

    if not EMAIL_REGEX.match(email):
        return jsonify(status='error', message='El formato del correo no es válido.'), 400

    registro = PreRegistro(email=email)
    try:
        db.session.add(registro)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(status='error', message='Este correo ya está registrado.'), 409

    from app.services.email_service import enviar_email_bienvenida
    enviar_email_bienvenida(email)

    return jsonify(status='success', message='¡Pre-registro exitoso! Te avisaremos cuando lancemos.'), 201
