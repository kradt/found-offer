import pytest
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from src import create_app
from src.database import models


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    app.config["CELERY"].update({
        'task_always_eager': True
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def context(app):
    with app.test_request_context():
        yield app


@pytest.fixture()
def user():
    email = "a@b.c"
    password = "A9090997a"
    user = models.User.objects(email=email).first()
    user.delete() if user else None
    return dict(email=email, password=password)


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
def confirmed_user_without_login(saved_user):
    # SetUp
    saved_user.modify(confirmed=True)
    yield saved_user
    # TearDown
    saved_user.modify(confirmed=False)


@pytest.fixture()
def auto_search():
    return dict(title="Backend Developer", city="Київ", salary=32000)


@pytest.fixture()
def saved_auto_search(confirmed_user, auto_search):
    search_pattern = models.VacancySearchPattern(**auto_search)
    confirmed_user.modify(push__auto_search=search_pattern)
    yield search_pattern

    confirmed_user.modify(pull__auto_search=search_pattern)


@pytest.fixture()
def vacancy():
    return dict(title="Backend Developer", company="My new Company", city="Київ",
                description="We find Junior Python BackEnd Developer for remote\nWe offer the best experience and the "
                            "best team",
                salary_from=20000, salary_to=35000)


@pytest.fixture()
def saved_vacancy(confirmed_user, vacancy):
    vacancy_in_base = models.Vacancy(**vacancy, user_id=confirmed_user.id)
    vacancy_in_base.save()
    yield vacancy_in_base

    models.Vacancy.objects(**vacancy).delete()
