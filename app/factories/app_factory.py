from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """
    Fábrica de aplicaciones Flask - RiftZone Pre-Registro
    """
    import os
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'templates'),
        static_folder=os.path.join(basedir, 'static')
    )

    from app.config.config import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    csrf.init_app(app)

    register_blueprints(app)

    with app.app_context():
        from app.models.pre_registro import PreRegistro
        db.create_all()
        print("Tabla pre_registros verificada/creada con éxito.")

    return app


def register_blueprints(app):
    """Registrar todos los blueprints de la aplicación"""
    from app.controllers.pre_registro import pre_registro_bp
    app.register_blueprint(pre_registro_bp)
