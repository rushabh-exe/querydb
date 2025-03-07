from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.query_route import query_bp
from app.utils.logger import configure_logging

def create_app():
    app = Flask(__name__)
    CORS(app, origins=Config.ALLOWED_ORIGINS)
    configure_logging(Config.LOG_LEVEL)
    app.register_blueprint(query_bp)
    return app