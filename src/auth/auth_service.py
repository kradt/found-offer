from flask import current_app
from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError
from itsdangerous import URLSafeTimedSerializer, BadSignature

from src.database import models


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
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


def find_user_by_email(email: str) -> models.User | bool:
    user = models.User.objects(email=email).first()
    return user if user else None


def create_user(email: str, password: str = None, confirmed: bool = False) -> models.User:
    password = generate_password_hash(password) if password else None
    try:
        user = models.User(email=email, password=password, confirmed=confirmed).save()
    except NotUniqueError:
        user = None
    return user
