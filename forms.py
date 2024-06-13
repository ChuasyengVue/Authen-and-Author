from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class UserForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=2, max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=6, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=3, max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])


class DeleteForm(FlaskForm):
    """Delete Form"""