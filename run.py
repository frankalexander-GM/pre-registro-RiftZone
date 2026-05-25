import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    with open(dotenv_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

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
