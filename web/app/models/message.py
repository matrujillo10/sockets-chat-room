"""Message model"""

import datetime
from sqlalchemy.orm import relationship
from .. import db


class Message(db.Model):
    """Message model"""

    __tablename__ = "message"

    _id = db.Column(db.Integer, primary_key=True)
    sent_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.String(1000))
    room = db.Column(db.String(100))
    sender_id = db.Column(db.Integer, db.ForeignKey("user._id"))
    sender = relationship("User", back_populates="messages")

    def get_id(self):
        """Return primary key"""
        return self._id
