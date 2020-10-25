"""Manage module to migrate to db"""

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db


app = create_app()  # pylint: disable=invalid-name
app.config.from_object(os.environ["APP_SETTINGS"])

migrate = Migrate(app, db)  # pylint: disable=invalid-name
manager = Manager(app)  # pylint: disable=invalid-name

manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
