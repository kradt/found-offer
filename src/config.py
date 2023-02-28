import secrets
import os


class Config:
	DEBUG = True
	SECRET_KEY = secrets.token_hex()
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
	