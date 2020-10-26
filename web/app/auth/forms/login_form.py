"""Form to login"""

from flask_wtf import Form
from wtforms.fields import BooleanField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    """Login Form"""

    email = EmailField(
        "Email",
        validators=[Required(), Length(max=100), Email()],
        render_kw={"placeholder": "Your Email"},
    )
    password = PasswordField(
        "Password",
        validators=[Required(), Length(min=5)],
        render_kw={"placeholder": "Your Password"},
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")
