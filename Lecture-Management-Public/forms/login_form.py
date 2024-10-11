from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    IntegerField,
    DateField,
    TimeField,
    SelectField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    name = StringField(
        "ID",
        render_kw={"placeholder": "Username"},
        validators=[DataRequired(), Length(4, 12)],
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Password"},
        validators=[DataRequired(), Length(2, 18)],
    )

    submit = SubmitField("Login")
