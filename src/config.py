import secrets
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(15))
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "password_salt")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    MAIL_PORT = 465
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CELERY = {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379"
    }
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    MONGODB_SETTINGS = {
        "host": os.getenv("MONGO_URI")
    }
