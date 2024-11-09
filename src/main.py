# !usr/bin/env python3

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


app = Flask(__name__)
app.config["SECRET_KEY"] = "key"  # This will have to be replaced.


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/login.html")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/signup.html")
def signup():
    return render_template("signup.html")


@app.route("/client.html")
def client():
    return render_template("client.html")


@app.route("/laywer.html")
def lawyer():
    return render_template("lawyer.html")


def main() -> str:  # type: ignore
    index()
    login()
    signup()


if __name__ == "__main__":
    app.run()
