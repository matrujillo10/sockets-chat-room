"""Form to enter a room"""

from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class RoomForm(Form):
    """Accepts a room."""

    room = StringField(
        "Room", validators=[Required()], render_kw={"placeholder": "Chatroom name"}
    )
    submit = SubmitField("Enter Chatroom")
