from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """Form for user to register"""

    username = StringField("Usernamer", validators=[InputRequired(), Length(min=3 , max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6 , max=30)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=30)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """Form for users to login"""

    username = StringField("Usernamer", validators=[InputRequired(), Length(min=3 , max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6 , max=30)])

class FeedbackForm(FlaskForm):
    """Form to add feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete feedback"""
    