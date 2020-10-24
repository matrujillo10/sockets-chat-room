"""Command model"""

import datetime
from sqlalchemy.orm import relationship
from .. import db


class Command(db.Model):
    """Command model"""

    __tablename__ = "command"

    _id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(100), unique=True)
    bot_name = db.Column(db.String(100))

    def get_id(self):
        """Return primary key"""
        return self._id
