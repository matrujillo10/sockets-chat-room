"""Manage module to migrate to db"""

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models.command import Command


app = create_app()  # pylint: disable=invalid-name
app.config.from_object(os.environ["APP_SETTINGS"])

migrate = Migrate(app, db)  # pylint: disable=invalid-name
manager = Manager(app)  # pylint: disable=invalid-name

# Manager Commands

manager.add_command("db", MigrateCommand)


@manager.command
def seed():
    "Load initial commands into database."

    def upsert_cmd(cmd):
        """Update cmd if exists, insert otherwise"""
        old_cmd = db.session.query(Command).filter(Command.cmd == cmd.cmd).first()
        if old_cmd:
            old_cmd.bot_name = cmd.bot_name
            db.session.merge(old_cmd)
        else:
            db.session.add(cmd)

    upsert_cmd(Command(cmd="/stock", bot_name="Stock Bot"))
    db.session.commit()


if __name__ == "__main__":
    manager.run()
