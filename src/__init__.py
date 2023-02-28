from flask import Flask
from src.config import Config


def create_app():

	app = Flask(__name__)
	app.config.from_object(Config)

	from src.auth.routes import auth_bp
	from src.search.routes import search_bp
	from src.root.routes import root_bp

	app.register_blueprint(root_bp, url_prefix="/")
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(search_bp, url_prefix="/search")

	return app

