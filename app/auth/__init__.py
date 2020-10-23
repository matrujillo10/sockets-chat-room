"""Auth blueprint"""

from flask import Blueprint

auth = Blueprint("auth", __name__)  # pylint: disable=invalid-name

from . import auth_routes, auth_controller
