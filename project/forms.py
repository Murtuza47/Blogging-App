from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already exists!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")


class UpdateForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    image_file = FileField("Update Profile Picture:", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        if current_user.email != email.data:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already exists!")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Whats new...", validators=[DataRequired()])
    submit = SubmitField("Post")
