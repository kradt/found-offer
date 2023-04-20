from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

from src.config import Config

db = MongoEngine()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from src.database import models

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    from src.parsing import start_parse_data_to_base
    with app.app_context():
        start_parse_data_to_base()


    from src.auth.routes import auth_bp
    from src.search.routes import search_bp
    from src.root.routes import root_bp

    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(search_bp, url_prefix="/search")

    return app
