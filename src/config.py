import secrets


class Config:
	DEBUG = True
	SECRET_KEY = secrets.token_hex()
	