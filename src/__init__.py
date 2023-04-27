import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from google_auth_oauthlib.flow import Flow

from src.config import Config

db = MongoEngine()
login_manager = LoginManager()
flow = Flow.from_client_secrets_file(
        client_secrets_file=Config.PATH_TO_GOOGLE_CREDENTIALS,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        redirect_uri="http://localhost:5000/google-data")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"


    from src.parsing import start_parse_data_to_base
    #start_parse_data_to_base()

    from src.auth.routes import auth_bp
    from src.search.routes import search_bp
    from src.root.routes import root_bp

    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(search_bp, url_prefix="/search")

    return app
