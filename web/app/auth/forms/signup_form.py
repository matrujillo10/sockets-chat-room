"""Form to signup"""

from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class SignupForm(Form):
    """Signup Form"""

    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(max=100), Email()],
        render_kw={"placeholder": "Email"},
    )
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"placeholder": "Name"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=5)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Sign Up")
