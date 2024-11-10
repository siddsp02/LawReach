# !usr/bin/env python3

from pprint import pprint
import random
import string
from flask import Flask, flash, redirect, render_template, url_for
from flask_login import current_user

from forms import (
    ClientSignUpForm,
    CreateCaseForm,
    LawyerApplicationForm,
    LawyerSignUpForm,
    LoginForm,
)


try:
    from src.models import Case, Status, db, User, UserType
except ImportError:
    from models import Case, Status, db, User, UserType


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "key"  # This will have to be replaced.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

header = [
    "ID",
    "Title",
    "Status",
    "Client",
    "Lawyer",
    "Subject",
    "Case Type",
    "Date Posted",
]
data = [
    {
        "id": 0,
        "title": "I want to sue McDonalds",
        "status": 0,
        "client_id": 1,
        "lawyer_id": 1,
        "subject": "foo",
        "case_type": "CLOSED",
        "date_posted": "08/08/2003",
    },
    {
        "id": 2,
        "title": "I want to sue McDonalds",
        "status": 0,
        "client_id": 1,
        "lawyer_id": 1,
        "subject": "foo",
        "case_type": "CLOSED",
        "date_posted": "08/08/2003",
    },
    {
        "id": 1,
        "title": "I want to sue McDonalds",
        "status": 0,
        "client_id": 1,
        "lawyer_id": 1,
        "subject": "foo",
        "case_type": "CLOSED",
        "date_posted": "08/08/2003",
    },
]


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/log-in")
def log_in():
    form = LoginForm()
    return render_template("log-in.html", form=form)


@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")


@app.route("/client")
def client():
    return render_template("client.html")


@app.route("/lawyer")
def lawyer():
    return render_template("lawyer.html")


@app.route("/lawyer-sign-up")
def lawyer_sign_up():
    form = LawyerSignUpForm()
    return render_template("lawyer-sign-up.html", form=form)


@app.route("/lawyer-application")
def lawyer_application():
    form = LawyerApplicationForm()
    return render_template("lawyer-application.html", form=form)


@app.route("/client-sign-up")
def client_sign_up():
    form = ClientSignUpForm()
    return render_template("client-sign-up.html", form=form)


@app.route("/client-requests")
def client_request():
    return render_template("client-request.html", requests=data, header=header)


# This needs more to be added.
@app.route("/client-create-case")
def client_create_case():
    form = CreateCaseForm()
    if form.validate_on_submit():
        case = Case(
            title=form.title.data,  # type: ignore
            content=form.content.data,  # type: ignore
            status=Status.PENDING,  # type: ignore
            author=current_user,  # type: ignore
        )
        db.session.add(case)
        db.session.commit()
        flash("Case created!")
        return redirect(url_for("client_request"))
    return render_template("client-create-case.html", form=form)


if __name__ == "__main__":
    app = create_app()
    with app.app_context() as ctx:
        db.create_all()
        for i in range(1):
            user_example = User(
                first_name="".join(random.sample(string.ascii_letters, k=10)),  # type: ignore
                last_name="".join(random.sample(string.ascii_letters, k=10)),  # type: ignore
                user_type=random.choice([UserType.LAWYER, UserType.CLIENT]),  # type: ignore
                username="".join(random.sample(string.ascii_letters, k=10)),  # type: ignore
                password="".join(random.sample(string.ascii_letters, k=10)),  # type: ignore
            )
            db.session.add(user_example)
            pprint(user_example)
