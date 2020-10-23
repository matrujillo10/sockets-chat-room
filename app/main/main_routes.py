"""Main routes"""

from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from .forms.room_form import RoomForm
from . import main


@main.route("/")
def index():
    """Return index template"""
    return render_template("index.html")


@main.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Return home template"""
    form = RoomForm()
    if form.validate_on_submit():
        session["room"] = form.room.data
        return redirect(url_for(".chat"))
    elif request.method == "GET":
        form.room.data = session.get("room", "")
    return render_template("home.html", name=current_user.name, form=form)


@main.route("/chat")
def chat():
    """Chat room. The room must be stored in the session."""
    room = session.get("room", "")
    if room == "":
        return redirect(url_for("main.home"))
    return render_template("chat.html", room=room)
