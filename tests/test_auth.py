import re
import os, sys

sys.path.append(os.getcwd())

from src.database import models
from src import mail


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


def test_register_and_confirm_user(client, user):
    login = user["email"]
    password = user["password"]

    with client:
        with mail.record_messages() as outbox:
            response = client.post("/auth/register",
                                   data={"email": login, "password": password, "confirm_password": password},
                                   follow_redirects=True)
            assert response.request.path == "/me"
            assert response.status_code == 200
            message_to_confirm = outbox[-1]
            assert message_to_confirm

            link = re.search('href=[\'"]?([^\'" >]+)', message_to_confirm.html).group()
            confirm_code = link.split("/")[-1]

            response = client.get(f"/auth/confirm/{confirm_code}", follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == "/me"

            user = models.User.objects(email=login).first()
            assert user is not None
            assert user.email == login
            assert user.confirmed


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
        response = client.get("/auth/new-password", follow_redirects=True)
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


def test_reset_password(client, confirmed_user_without_login):
    with client:
        with mail.record_messages() as outbox:
            response = client.post(
                "auth/reset-password",
                data={"email": confirmed_user_without_login.email}
            )
            assert response.status_code == 200
            message = outbox[-1].html
            assert message
            code = message.split("<b>")[1].split("</b>")[0]
            assert code.isdigit()
            assert len(code) == 6

            response = client.post(
                "auth/reset-password",
                data={"email": confirmed_user_without_login.email, "code": code},
                follow_redirects=True
            )
            assert response.status_code == 200
            assert response.request.path == "/auth/new-password"
