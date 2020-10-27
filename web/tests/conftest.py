"""Test setup"""

import os
import tempfile
import pytest
from app import create_app, db, socketio
from app.models.user import User
from werkzeug.security import generate_password_hash


os.environ["APP_SETTINGS"] = os.environ["APP_SETTINGS_TEST"]
del os.environ["DATABASE_URL"]


@pytest.fixture
def client():
    """Testing client"""
    db_fd, path = tempfile.mkstemp()
    os.environ["DATABASE_URL"] = f"sqlite:///{path}.db"
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DATABASE"] = path
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add_all(
                [
                    User(
                        email=u["email"],
                        name=u["name"],
                        password=generate_password_hash(u["password"], method="sha256"),
                    )
                    for u in [
                        {
                            "email": "john.doe@gmail.com",
                            "name": "John",
                            "password": "johnpass",
                        },
                        {
                            "email": "lorem.doe@gmail.com",
                            "name": "Lorem",
                            "password": "lorempass",
                        },
                    ]
                ]
            )
            db.session.commit()
        yield client
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


@pytest.fixture
def client_empty_db():
    """Testing client with empty db"""
    db_fd, path = tempfile.mkstemp()
    os.environ["DATABASE_URL"] = f"sqlite:///{path}.db"
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DATABASE"] = path
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()
        yield client
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


@pytest.fixture
def client_logged():
    """Testing client with logged user"""
    db_fd, path = tempfile.mkstemp()
    os.environ["DATABASE_URL"] = f"sqlite:///{path}.db"
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["DATABASE"] = path
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add_all(
                [
                    User(
                        email=u["email"],
                        name=u["name"],
                        password=generate_password_hash(u["password"], method="sha256"),
                    )
                    for u in [
                        {
                            "email": "john.doe@gmail.com",
                            "name": "John",
                            "password": "johnpass",
                        },
                        {
                            "email": "lorem.doe@gmail.com",
                            "name": "Lorem",
                            "password": "lorempass",
                        },
                    ]
                ]
            )
            db.session.commit()

        response = client.post(
            "/login",
            data={"email": "john.doe@gmail.com", "password": "johnpass"},
            follow_redirects=True,
        )
        assert response.status_code == 200

        yield client
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
