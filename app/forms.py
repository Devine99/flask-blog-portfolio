from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from sqlalchemy import select
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    TextAreaField,
    HiddenField,
    EmailField,
    URLField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    URL,
    ValidationError,
)
from .extensions import db


class CommentForm(FlaskForm):
    text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class ContactForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    number = StringField("Phone Number", validators=[DataRequired(), Length(max=20)])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=10, max=2000)]
    )
    honeypot = HiddenField("Honeypot")
    submit = SubmitField("Send Message")


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = URLField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    terms = BooleanField(
        "I agree to the Terms & Conditions",
        validators=[DataRequired(message="You must accept the terms")],
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        from .models import User

        if db.session.scalar(select(User).where(User.email == field.data)):
            raise ValidationError("Email already registered.")

    def validate_password(self, field):
        errors = []
        password = field.data
        if len(password) < 8:
            errors.append("at least 8 characters")
        if not any(c.isupper() for c in password):
            errors.append("an uppercase letter")
        if not any(c.islower() for c in password):
            errors.append("a lowercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("a number")
        if not any(c in "@$!%*?&" for c in password):
            errors.append("a special character (@$!%*?&)")
        if errors:
            raise ValidationError(f"Password must contain {', '.join(errors)}")
