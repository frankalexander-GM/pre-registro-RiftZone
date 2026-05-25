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
