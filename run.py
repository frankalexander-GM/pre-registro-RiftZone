import os
from app.factories.app_factory import create_app

config_name = os.environ.get('FLASK_ENV', 'development')

app = create_app(config_name)

if __name__ == '__main__':
    debug_mode = config_name == 'development'
    port = int(os.environ.get('PORT', 5000))

    print(f"RiftZone Pre-Registro iniciando en modo {config_name}")
    print(f"Debug: {debug_mode}")
    print(f"Port: {port}")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
