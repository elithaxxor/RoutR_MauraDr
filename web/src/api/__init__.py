from flask import Flask
import os
from flask_restx import Api
from flask_jwt_extended import JWTManager
from .routes_v2 import api_v2
from .routes import api_ns
from ..config import config


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "your-secret-key"
    )  # Set via env
    api = Api(app, title="SMB-Scor3 API", description="Network Scanning and Assessment")
    jwt = JWTManager(app)

    api.add_namespace(api_ns)
    api.add_namespace(api_v2, path="/api/v2")
    return app
