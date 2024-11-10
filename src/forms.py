from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length

try:
    from src.models import User, Case
except ImportError:
    from models import User, Case


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class LawyerSignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username: StringField) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValueError(
                f"Username {username} already taken. Please choose another username."
            )

    def validate_email(self, email: StringField) -> None:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValueError(
                f"Email {email} already in use. Please choose another email."
            )


class ClientSignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username: StringField) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValueError(
                f"Username {username} already taken. Please choose another username."
            )

    def validate_email(self, email: StringField) -> None:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValueError(
                f"Email {email} already in use. Please choose another email."
            )


class CreateCaseForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    case_type = SelectField(
        "Case Type",
        validators=[DataRequired()],
        choices=[
            ("MARRIAGE", "MARRIAGE"),
            ("ACCIDENT", "ACCIDENT"),
            ("CRIMINAL", "CRIMINAL"),
        ],
    )
    submit = SubmitField("Create", validators=[DataRequired()])


class LawyerApplicationForm(FlaskForm):
    name = StringField("Name of Lawyer: ", validators=[DataRequired()])
    status = SelectField(
        "Status",
        validators=[DataRequired()],
        choices=[
            ("professional-lawyer", "Professional Lawyer"),
            ("law-student", "Law Student"),
            ("social-worker", "Social Worker"),
            ("nonprofit-legal-advocate", "Nonprofit Legal Advocate"),
            ("community-volunteer", "Community Volunteer"),
            ("other", "Other"),
        ],
    )
    specialty = SelectField(
        "Specialty of Law",
        validators=[DataRequired()],
        choices=[
            ("family-law", "Family Law"),
            ("criminal-law", "Criminal Law"),
            ("civil-rights", "Civil Rights"),
            ("employment-law", "Employment Law"),
            ("immigration-law", "Immigration Law"),
            ("intellectual-property", "Intellectual Property"),
            ("other", "Other"),
        ],
    )
    reason = TextAreaField("Reason For Volunteering", default="Reason")
    submit = SubmitField("Apply")
