from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app():

	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)

	from src.database import models
	with app.app_context():
		db.create_all()

	migrate.init_app(app, db)

	from src.auth.routes import auth_bp
	from src.search.routes import search_bp
	from src.root.routes import root_bp

	app.register_blueprint(root_bp, url_prefix="/")
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(search_bp, url_prefix="/search")

	return app

