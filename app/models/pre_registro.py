import random
import string
from datetime import datetime, timezone
from app.factories.app_factory import db


class PreRegistro(db.Model):
    """Modelo de Pre-Registro - RiftZone"""
    __tablename__ = 'pre_registros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    fecha_registro = db.Column(
        db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<PreRegistro {self.email}>'


class CodigoVerificacion(db.Model):
    """Código temporal de verificación de email"""
    __tablename__ = 'codigos_verificacion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    codigo = db.Column(db.String(6), nullable=False)
    creado = db.Column(
        db.DateTime, nullable=False,
        default=datetime.utcnow
    )
    intentos = db.Column(db.Integer, default=0)

    @staticmethod
    def generar_codigo():
        return ''.join(random.choices(string.digits, k=6))

    def __repr__(self):
        return f'<CodigoVerificacion {self.email}>'
