import re
from datetime import datetime, timezone, timedelta

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy.exc import IntegrityError

from app.factories.app_factory import db
from app.models.pre_registro import PreRegistro, CodigoVerificacion

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

    existente = PreRegistro.query.filter_by(email=email).first()
    if existente:
        return jsonify(status='duplicate', message='Este correo ya está registrado.'), 409

    CodigoVerificacion.query.filter_by(email=email).delete()
    db.session.commit()

    codigo = CodigoVerificacion.generar_codigo()
    nuevo_codigo = CodigoVerificacion(email=email, codigo=codigo)
    db.session.add(nuevo_codigo)
    db.session.commit()

    from app.services.email_service import enviar_email_verificacion
    enviar_email_verificacion(email, codigo)

    return jsonify(
        status='verify',
        message='Te enviamos un código de verificación a tu correo. Revisa tu bandeja de entrada o spam.'
    ), 200


@pre_registro_bp.route('/verificar', methods=['POST'])
def verificar():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(status='error', message='Solicitud inválida.'), 400

    email = (data.get('email') or '').strip().lower()
    codigo_ingresado = (data.get('codigo') or '').strip()

    if not email or not codigo_ingresado:
        return jsonify(status='error', message='Correo y código son obligatorios.'), 400

    registro_codigo = CodigoVerificacion.query.filter_by(email=email).first()

    if not registro_codigo:
        return jsonify(status='error', message='No hay código pendiente para este correo. Intenta registrarte de nuevo.'), 404

    if registro_codigo.intentos >= 5:
        db.session.delete(registro_codigo)
        db.session.commit()
        return jsonify(status='error', message='Demasiados intentos. Intenta registrarte de nuevo.'), 429

    tiempo_limite = registro_codigo.creado + timedelta(minutes=10)
    ahora = datetime.utcnow()
    if ahora > tiempo_limite:
        db.session.delete(registro_codigo)
        db.session.commit()
        return jsonify(status='error', message='El código ha expirado. Intenta registrarte de nuevo.'), 410

    if registro_codigo.codigo != codigo_ingresado:
        registro_codigo.intentos += 1
        db.session.commit()
        intentos_restantes = 5 - registro_codigo.intentos
        return jsonify(status='error', message=f'Código incorrecto. Te quedan {intentos_restantes} intentos.'), 400

    db.session.delete(registro_codigo)

    registro = PreRegistro(email=email)
    try:
        db.session.add(registro)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(status='duplicate', message='Este correo ya está registrado.'), 409

    from app.services.email_service import enviar_email_bienvenida
    enviar_email_bienvenida(email)

    return jsonify(status='success', message='¡Pre-registro exitoso! Te avisaremos cuando lancemos.'), 201
