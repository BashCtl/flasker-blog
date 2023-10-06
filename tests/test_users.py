from src.models.user_model import User
import json


def test_home(client):
    response = client.get("/")
    assert b"<title>Fucking Blog</title>" in response.data


def test_registration(client, app):
    user_data = {
        "name": "Bald Dude",
        "username": "baldy",
        "email": "bald@test.com",
        "favorite_color": "Black",
        "password": "password123",
        "password_confirm": "password123"
    }
    response = client.post("/register/", data=user_data)

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "bald@test.com"


def test_valid_login(client, registered_user):
    response = client.post("/login", data={"username": registered_user["username"],
                                           "password": registered_user["password"]})
    assert b'You should be redirected automatically to the target URL: <a href="/dashboard">/dashboard</a>' in response.data
