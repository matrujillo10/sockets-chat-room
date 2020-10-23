"""Auth blueprint"""

from flask import Blueprint, render_template


auth = Blueprint("auth", __name__)  # pylint: disable=invalid-name


@auth.route("/login")
def login():
    """Return login template"""
    return render_template("login.html")


@auth.route("/signup")
def signup():
    """Return sign up template"""
    return render_template("signup.html")


@auth.route("/logout")
def logout():
    """Process logout request"""
    return "Logout"
