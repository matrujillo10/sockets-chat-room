"""Auth controller"""

from werkzeug.security import generate_password_hash, check_password_hash

from ..models.user import User
from .. import db


#######################################################################################
# Login
#######################################################################################


def login(email: str, password: str):
    """Return whether user with given email and password exists"""
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return False, None
    return True, user


#######################################################################################
# Sign Up
#######################################################################################


def signup(email: str, name: str, password: str):
    """Create a user if not exists"""
    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()
    if user:
        return False, user

    # create a new user
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return True, new_user
