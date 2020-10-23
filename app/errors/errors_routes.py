"""Errors routes"""

from flask import render_template
from . import errors


@errors.app_errorhandler(404)
def not_found(_):
    """Return not found template"""
    return render_template("404.html"), 404
