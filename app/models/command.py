"""Command model"""

import datetime
from sqlalchemy.orm import relationship
from .. import db


class Message(db.Model):
    """Command model"""

    __tablename__ = "commmand"

    _id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(100))

    def get_id(self):
        """Return primary key"""
        return self._id
