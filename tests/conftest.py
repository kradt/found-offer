import pytest
from flask_login import FlaskLoginClient, login_user
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
    user = models.User(email=user["email"], password=user["password"])
    user.save()
    # TearDown
    yield user
    user.delete()


@pytest.fixture()
def login_client(app, user):
    app.test_client_class = FlaskLoginClient

