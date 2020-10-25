"""Errors blueprint"""

from flask import Blueprint


errors = Blueprint("errors", __name__)  # pylint: disable=invalid-name

from . import errors_routes
