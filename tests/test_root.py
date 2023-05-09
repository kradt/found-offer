from src.database import models

def test_user_auto_search(client, confirmed_user, auto_search):
    with client:
        response = client.post(
            "/auto-search",
            data={"title": auto_search["title"], "city": auto_search["city"], "salary": auto_search["salary"]},
            follow_redirects=True
        )
        assert response.request.path == "/me"
        assert response.status_code == 200

        search_pattern = confirmed_user.auto_search[0]
        assert search_pattern.title == auto_search["title"]
        assert search_pattern.city == auto_search["city"]
        assert search_pattern.salary == auto_search["salary"]


def test_user_add_vacancy(client, confirmed_user, vacancy):
    with client:
        response = client.post(
            "/new-vacancy",
            data={
                "title": vacancy["title"],
                "company": vacancy["company"],
                "city": vacancy["city"],
                "description": vacancy["description"],
                "salary_from": vacancy["salary_from"],
                "salary_to": vacancy["salary_to"], },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert response.request.path == "/me"

        vacancy_in_base = models.Vacancy.objects(user_id=confirmed_user.id).first()
        assert vacancy_in_base.title == vacancy["title"]
        assert vacancy_in_base.company == vacancy["company"]
        assert vacancy_in_base.city == vacancy["city"]
        assert vacancy_in_base.description == vacancy["description"]
        assert vacancy_in_base.salary_from == vacancy["salary_from"]
        assert vacancy_in_base.salary_to == vacancy["salary_to"]

