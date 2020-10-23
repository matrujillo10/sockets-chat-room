"""..."""

import os
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # pylint: disable=invalid-name
socketio = SocketIO()  # pylint: disable=invalid-name


def create_app():
    """App entry point"""
    app = Flask(__name__)

    app.config.from_object(os.environ["APP_SETTINGS"])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    socketio.init_app(app)

    # === Begin Login configs ===
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # === End Login configs ===

    # blueprint for auth routes in our app
    from .auth import auth

    app.register_blueprint(auth)

    # blueprint for non-auth parts of app
    from .main import main

    app.register_blueprint(main)

    # blueprint for errors parts of app
    from .errors import errors

    app.register_blueprint(errors)

    return app
