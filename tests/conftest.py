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
        "CELERY_ALWAYS_EAGER": True
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user():
    return dict(email="a@b.c", password="A9090997a")


@pytest.fixture()
def saved_user(user):
    # SetUp
    user = models.User(email=user["email"], password=generate_password_hash(user["password"]))
    user.save()
    yield user
    # TearDown
    user.delete()


@pytest.fixture()
def logined_user(saved_user, context):
    # SetUp
    login_user(saved_user)
    yield saved_user
    # TearDown
    logout_user()


@pytest.fixture()
def confirmed_user(logined_user):
    # SetUp
    logined_user.modify(confirmed=True)
    yield logined_user
    # TearDown
    logined_user.modify(confirmed=False)


@pytest.fixture()
def context(app):
    with app.test_request_context():
        yield app


@pytest.fixture()
def auto_search():
    return dict(title="Backend Developer", city="Київ", salary=32000)


@pytest.fixture()
def vacancy():
    return dict(title="Backend Developer", company="My new Company", city="Київ",
                description="We find Junior Python BackEnd Developer for remote\nWe offer the best experience and the "
                            "best team",
                salary_from=20000, salary_to=35000)
