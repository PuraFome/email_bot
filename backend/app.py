from flask import Flask, send_from_directory
from flask_cors import CORS
from config.config import load_config
from logs.logger import setup_logging
from tracking.tracking import tracking_bp
from apis.service.routes import service_bp
from apis.enterprise_meling.routes import enterprise_meling_bp
from apis.models.routes import models_bp
from apis.sendings.routes import sendings_bp
from apis.email_returns.routes import email_returns_bp
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS para o frontend
setup_logging()
config = load_config()
app.config.update(config)

# Registrar blueprints
app.register_blueprint(tracking_bp)
app.register_blueprint(service_bp)
app.register_blueprint(enterprise_meling_bp)
app.register_blueprint(models_bp)
app.register_blueprint(sendings_bp)
app.register_blueprint(email_returns_bp)

# Rota para servir imagens estáticas
@app.route('/images/<filename>')
def serve_image(filename):
    """Serve imagens estáticas da pasta images"""
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(images_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
