"""Auth routes"""

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .auth_controller import signup as signup_controller, login as login_controller
from . import auth


#######################################################################################
# Login
#######################################################################################


@auth.route("/login")
def login():
    """Return login template"""
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    """Process login POST request"""
    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))
    valid, user = login_controller(email, password)
    if not valid:
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


#######################################################################################
# Sign Up
#######################################################################################


@auth.route("/signup", methods=["GET"])
def signup():
    """Return sign up template"""
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    """Process sign up POST request"""
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    created, _ = signup_controller(email, name, password)
    if not created:
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))
    return redirect(url_for("auth.login"))


#######################################################################################
# Logout
#######################################################################################


@auth.route("/logout")
@login_required
def logout():
    """Process logout request"""
    logout_user()
    return redirect(url_for("main.index"))
