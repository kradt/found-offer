import datetime

from src.database import models


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
    user.modify(push__auto_search=auto_search_pattern)


def drop_pattern_from_user(user, pattern_id):
    search_patterns = user.auto_search
    for pattern in search_patterns:
        if str(pattern.id) == pattern_id:
            del search_patterns[search_patterns.index(pattern)]
    user.update(auto_search=search_patterns)
