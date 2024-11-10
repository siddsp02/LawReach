# !usr/bin/env python3

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import (
    current_user,
    LoginManager,
    login_user,
    logout_user,
    login_required,
)

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
    global login_manager  # Quick hack.

    app = Flask(__name__)
    login_manager = LoginManager()
    app.config["SECRET_KEY"] = "key"  # This will have to be replaced.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "log_in"  # type: ignore

    with app.app_context():
        db.create_all()

    return app


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

app = create_app()


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/log-in", methods=["POST", "GET"])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(
                url_for("lawyer" if user.user_type == UserType.LAWYER else "client")
            )
    return render_template("log-in.html", form=form)


@app.route("/log-out")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("index"))


@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")


@app.route("/lawyer")
@login_required
def lawyer():
    return render_template("lawyer.html")


@app.route("/lawyer-sign-up", methods=["POST", "GET"])
def lawyer_sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("lawyer"))
    form = LawyerSignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,  # type: ignore
            first_name=form.first_name.data,  # type: ignore
            last_name=form.last_name.data,  # type: ignore
            email=form.email.data,  # type: ignore
            user_type=UserType.LAWYER,  # type: ignore
            password=form.password.data,  # type: ignore
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created! You can now log in!")
        return redirect(url_for("index"))
    return render_template("lawyer-sign-up.html", form=form)


@app.route("/client-sign-up", methods=["POST", "GET"])
def client_sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("client"))
    form = ClientSignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,  # type: ignore
            first_name=form.first_name.data,  # type: ignore
            last_name=form.last_name.data,  # type: ignore
            email=form.email.data,  # type: ignore
            user_type=UserType.CLIENT,  # type: ignore
            password=form.password.data,  # type: ignore
        )
        db.session.add(user)
        db.session.commit()
        print(User.query.all())
        flash("Account created! You can now log in!")
        return redirect(url_for("index"))

    return render_template("client-sign-up.html", form=form)


@app.route("/lawyer-application")
def lawyer_application():
    form = LawyerApplicationForm()
    return render_template("lawyer-application.html", form=form)


@app.route("/client")
def client():
    return render_template("client.html", requests=data, header=header)


# This needs more to be added.
@app.route("/client-create-case")
@login_required
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
