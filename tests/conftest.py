import pytest
from dotenv import load_dotenv
from os import getenv, getcwd
from src import create_app, db
from src.forms.webforms import SearchForm
from src.models.user_model import User


class TestConfig:
    load_dotenv()
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("TEST_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = f"{getcwd()}/src/static/images"
    WTF_CSRF_ENABLED = False


@pytest.fixture()
def app():
    app = create_app(TestConfig)

    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def registered_user(app, client):
    user_data = {
        "name": "John Blade",
        "username": "joblade",
        "email": "joblade@test.com",
        "favorite_color": "Silver",
        "password": "password123",
        "password_confirm": "password123"
    }
    client.post("/register/", data=user_data)
    with app.app_context():
        user = User.query.filter_by(email=user_data["email"])
        assert user is not None
    return user_data


@pytest.fixture()
def auth_client(client, registered_user):
    response = client.post("/login", data={"username": registered_user["username"],
                                           "password": registered_user["password"]})
    assert response.status_code == 302
    return client
