"""Models of the application"""

from flask_login import UserMixin
from .. import db


class User(UserMixin, db.Model):
    """User model"""

    __tablename__ = "users"

    _id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def get_id(self):
        return self._id
