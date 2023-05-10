from flask import current_app
from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError
from itsdangerous import URLSafeTimedSerializer, BadSignature

from src.database import models


# Function generate confirmation token for confirm email, serialize user email
def generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


# Function deserialize user email and confirm token
def get_email_and_confirm_token(token: str, expiration: int = 3600) -> str | None:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except BadSignature:
        email = None
    return email


# Function prepare data for send with Flask-Mail
def prepare_send_data(emails: list) -> dict:
    return {
        "sender": current_app.config["MAIL_DEFAULT_SENDER"],
        "recipients": emails
    }


# Function find user by email in mongo base
def find_user_by_email(email: str) -> models.User | bool:
    user = models.User.objects(email=email).first()
    return user if user else None


# Function create new user
def create_user(email: str, password: str = None, confirmed: bool = False) -> models.User:
    password = generate_password_hash(password) if password else None
    try:
        user = models.User(email=email, password=password, confirmed=confirmed).save()
    except NotUniqueError:
        user = None
    return user
