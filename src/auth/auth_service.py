import datetime

from flask import current_app
from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError
from itsdangerous import URLSafeTimedSerializer

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
    except Exception as e:
        print(e)
        return False
    return email


def find_user_by_email(email: str) -> models.User | bool:
    user = models.User.objects(email=email)
    if user:
        return user.get()
    else:
        return False


def create_user(email: str, password: str = None, confirmed=False) -> models.User:
    if password:
        password = generate_password_hash(password)
    try:
        user = models.User(email=email, password=password, confirmed=confirmed).save()
    except NotUniqueError:
        user = None
    return user


def create_vacancy(title, company, city, description, salary_from, salary_to, user_id):
    time_now = datetime.datetime.now()
    try:
        vacancy = models.Vacancy(
            title=title,
            company=company,
            city=city,
            description=description,
            salary_from=salary_from,
            salary_to=salary_to,
            time_publish=time_now,
            user_id=user_id).save()
    except Exception as e:
        print(e)
        return False
    return vacancy


def get_user_vacancies(user_id: str):
    return models.Vacancy.objects(user_id=user_id)


def find_vacancy_by_id(id: str):
    return models.Vacancy.objects(id=id).first()


def add_auto_search_pattern_to_user(user: models.User, pattern: dict):
    auto_search_pattern = models.VacancySearchPattern(**pattern)
    user.update(push__auto_search=auto_search_pattern)


def drop_pattern_from_user(user, pattern_id):
    search_patterns = user.auto_search
    for pattern in search_patterns:
        if str(pattern.id) == pattern_id:
            del search_patterns[search_patterns.index(pattern)]
    user.update(auto_search=search_patterns)
