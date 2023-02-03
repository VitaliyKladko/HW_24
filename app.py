from flask import Flask
from views import main_bp


def create_app() -> Flask:
    """Init flask app"""
    app: Flask = Flask(__name__)
    app.register_blueprint(main_bp)
    return app
