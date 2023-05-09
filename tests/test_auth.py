import random

from src.database import models


def test_login_user(client, saved_user, user):
    login = user["email"]
    password = user["password"]
    with client:
        response = client.post(
            "/auth/login",
            data={"email": login, "password": password},
            follow_redirects=True)
        assert response.request.path == "/auth/me"
    assert response.status_code == 200


def test_register_user(client, user):
    login = user["email"]
    password = user["password"]

    with client:
        response = client.post("/auth/register",
                               data={"email": login, "password": password, "confirm_password": password},
                               follow_redirects=True)
        user = models.User.objects(email=login).first()
        assert response.request.path == "/auth/me"

    assert user is not None
    assert user.email == login
    assert response.status_code == 200
    user.delete()


def test_user_already_exist(client, user, saved_user):
    login = user["email"]
    password = user["password"]
    response = client.post(
        "/auth/register",
        data={"email": login, "password": password, "confirm_password": password},
        follow_redirects=True)
    assert bytes("User with this email already exist", "utf-8") in response.data
    assert response.status_code == 200


def test_user_unconfirmed(login_client, saved_user):
    user = saved_user
    with login_client(user=user) as client:
        response = client.get("/auth/new-password")
        assert response.status_code == 403


