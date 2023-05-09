import pytest
from flask_login import FlaskLoginClient, login_user, logout_user
from werkzeug.security import generate_password_hash
from mongoengine import NotUniqueError

from src import create_app
from src.database import models


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user():
    return {"email": "a@b.c", "password": "A9090997a"}


@pytest.fixture()
def saved_user(user):
    # SetUp
    user = models.User(email=user["email"], password=generate_password_hash(user["password"]))
    user.save()
    yield user
    # TearDown
    user.delete()


@pytest.fixture()
def context(app):
    with app.test_request_context():
        yield app


@pytest.fixture()
def logined_user(saved_user, context):
    # SetUp

    login_user(saved_user)
    yield user
    # TearDown
    logout_user()



@pytest.fixture()
def login_client(app):
    app.test_client_class = FlaskLoginClient
    yield app.test_client


