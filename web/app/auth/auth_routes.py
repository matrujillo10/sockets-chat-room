"""Auth routes"""

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .auth_controller import signup as signup_controller, login as login_controller
from .forms.signup_form import SignupForm
from .forms.login_form import LoginForm
from . import auth


#######################################################################################
# Login
#######################################################################################


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Process login requests"""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        valid, user = login_controller(email, password)
        if not valid:
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))
        login_user(user, remember=remember)
        return redirect(url_for("main.home"))

    return render_template("login.html", form=form)


#######################################################################################
# Sign Up
#######################################################################################


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """Process sign up requests"""
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        created, user = signup_controller(email, name, password)
        if not created:
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))

        #  Log user
        login_user(user, remember=True)
        return redirect(url_for("main.home"))

    return render_template("signup.html", form=form)


#######################################################################################
# Logout
#######################################################################################


@auth.route("/logout")
@login_required
def logout():
    """Process logout request"""
    logout_user()
    return redirect(url_for("main.index"))
