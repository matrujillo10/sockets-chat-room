"""Form to enter a room"""

from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required, Length


class RoomForm(Form):
    """Accepts a room."""

    room = StringField(
        "Room",
        validators=[Required(), Length(min=1, max=100)],
        render_kw={"placeholder": "Chatroom name"},
    )
    submit = SubmitField("Enter Chatroom")
