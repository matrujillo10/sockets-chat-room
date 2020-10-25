"""Main blueprint"""

from flask import Blueprint


main = Blueprint("main", __name__)  # pylint: disable=invalid-name

from . import main_routes, events
