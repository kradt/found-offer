from src.database import models
from werkzeug.security import check_password_hash


def test_login_user(client, saved_user, user):
    login = user["email"]
    password = user["password"]
    with client:
        response = client.post(
            "/auth/login",
            data={"email": login, "password": password},
            follow_redirects=True)
        assert response.request.path == "/me"
    assert response.status_code == 200


def test_register_user(client, user):
    login = user["email"]
    password = user["password"]

    with client:
        response = client.post("/auth/register",
                               data={"email": login, "password": password, "confirm_password": password},
                               follow_redirects=True)
        user = models.User.objects(email=login).first()
        assert response.request.path == "/me"

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


def test_user_unconfirmed(client, logined_user):
    with client:
        response = client.get("/auth/new-password")
        assert response.status_code == 403
        logined_user.modify(confirmed=True)
        response = client.get("/auth/new-password")
        assert response.status_code == 200
        assert response.request.path == "/auth/new-password"


def test_user_logout(client, logined_user):
    with client:
        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200


def test_new_password(client, confirmed_user):
    new_password = "12345678"

    with client:
        response = client.post(
            "/auth/new-password",
            data={"password": new_password, "confirm_password": new_password},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert confirmed_user.check_password(new_password)
