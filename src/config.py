import os
import secrets
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(15))
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "password_salt")

    MAIL_PORT = 465
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
    GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"

    CELERY = {
        "broker_url": os.getenv("REDIS_URL"),
        "result_backend": os.getenv("REDIS_URL"),
        "timezone": "UTC"
    }

    MONGODB_SETTINGS = {
        "host": os.getenv("MONGO_URI")
    }
