"""Form to enter a room"""

from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RoomForm(Form):
    """Accepts a room."""

    room = StringField(
        "Room",
        validators=[DataRequired(), Length(min=1, max=100)],
        render_kw={"placeholder": "Chatroom name"},
    )
    submit = SubmitField("Enter Chatroom")
