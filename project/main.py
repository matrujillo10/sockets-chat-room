"""Main blueprint"""

from flask import Blueprint, render_template


main = Blueprint("main", __name__)  # pylint: disable=invalid-name


@main.route("/")
def index():
    """Return index template"""
    return render_template("index.html")


@main.route("/profile")
def profile():
    """Return profile template"""
    return render_template("profile.html")
