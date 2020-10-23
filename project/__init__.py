"""This is the entry point to the application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .auth import auth as auth_blueprint
from .main import main as main_blueprint


db = SQLAlchemy()  # pylint: disable=invalid-name


def create_app():
    """App entry point"""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret-key-goes-here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    return app
