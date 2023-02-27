from flask import Flask, redirect, url_for
from src import config


def create_app():

	app = Flask(__name__)
	app.config.from_object(config)

	@app.route("/")
	def index():
		return redirect(url_for("auth_bp.login"))

	from src.auth.routes import auth_bp
	from src.search.routes import search_bp

	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(search_bp, url_prefix="/search")

	return app

