from src.models.user_model import User
import pytest


def test_home(client):
    response = client.get("/")
    assert b"<title>Fucking Blog</title>" in response.data


def test_registration(client, app, user_data):
    client.post("/register/", data=user_data)

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "bald@test.com"


def test_registration_already_registered(client, registered_user):
    response = client.post("/register/", data=registered_user)
    assert b"<strong>User already exists!</strong>" in response.data


def test_registration_different_passwords(client, app, user_data):
    user_data["password_confirm"] = "different_pass"
    client.post("/register/", data=user_data)
    with app.app_context():
        assert User.query.count() == 0


def test_valid_login(client, registered_user):
    response = client.post("/login", data={"username": registered_user["username"],
                                           "password": registered_user["password"]})
    assert b'You should be redirected automatically to the target URL: <a href="/dashboard">/dashboard</a>' in response.data


@pytest.mark.parametrize("username, password", [
    ("fakeusername", "password123"),
    ("johnblade", "fakepassword")
])
def test_invalid_login(client, username, password):
    response = client.post("/login", data={"username": username,
                                           "password": password})
    assert b"<strong>That User Doesn&#39;t Exist! Try Again!</strong>" in response.data
