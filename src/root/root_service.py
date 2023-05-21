import datetime
from bson import ObjectId
from flask_mongoengine import BaseQuerySet

from src.database import models


def create_vacancy(
        title: str,
        company: str,
        city: str,
        description: str,
        salary_from: float,
        salary_to: float,
        user_id: ObjectId) -> models.Vacancy:
    """
    Function for create vacancy
    """
    time_now = datetime.datetime.now()
    vacancy = models.Vacancy(
        title=title,
        company=company,
        city=city,
        description=description,
        salary_from=salary_from,
        salary_to=salary_to,
        time_publish=time_now,
        user_id=user_id).save()
    return vacancy


def get_user_vacancies(user_id: str) -> BaseQuerySet:
    """
    Function for get all user vacancies
    """
    return models.Vacancy.objects(user_id=user_id)


def find_vacancy_by_id(vacancy_id: str) -> models.Vacancy:
    """
    Function for get vacancy by vacancy's id
    """
    return models.Vacancy.objects(id=vacancy_id).first()


def add_auto_search_pattern_to_user(user: models.User, pattern: dict) -> None:
    """
    Function for add auto search pattern to user document
    """
    auto_search_pattern = models.VacancySearchPattern(**pattern)
    user.modify(push__auto_search=auto_search_pattern)


def drop_pattern_from_user(user: models.User, pattern_id: int | str) -> None:
    """
    Function for drop auto search pattern from user document
    """
    search_patterns = user.auto_search
    for pattern in search_patterns:
        if str(pattern.id) == pattern_id:
            del search_patterns[search_patterns.index(pattern)]
    user.update(auto_search=search_patterns)
