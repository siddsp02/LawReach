# !usr/bin/env python3

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import jinja2

from forms import (
    ClientSignUpForm,
    CreateCaseForm,
    LawyerApplicationForm,
    LawyerSignUpForm,
    LoginForm,
)
from utils import time_diff


try:
    from src.models import Case, Status, User, UserType, db, CaseType
except ImportError:
    from models import Case, Status, User, UserType, db, CaseType


def create_app() -> Flask:
    global login_manager  # Quick hack.

    app = Flask(__name__)
    login_manager = LoginManager()
    app.config["SECRET_KEY"] = "key"  # This will have to be replaced.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "log_in"  # type: ignore

    app.jinja_env.filters["time_diff"] = time_diff

    with app.app_context():
        db.create_all()

    return app


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


@app.route("/lawyer", methods=["POST", "GET"])
@login_required
def lawyer():
    cases = Case.query.all()
    header = ["Title", "Status", "Created By", "Case Type", "Date Posted"]
    return render_template("lawyer.html", cases=cases, header=header)


def redirect_current_user_to_home(user):
    return redirect(
        url_for("lawyer" if user.user_type == UserType.LAWYER else "client")
    )


@app.route("/lawyer-sign-up", methods=["POST", "GET"])
def lawyer_sign_up():
    if current_user.is_authenticated:
        return redirect_current_user_to_home(current_user)
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
        flash("Account created! You can now log in!", "success")
        return redirect(url_for("index"))
    else:
        flash("Something went wrong.", "error")
    return render_template("lawyer-sign-up.html", form=form)


# This needs more to be added.
@app.route("/client-create-case", methods=["POST", "GET"])
@login_required
def client_create_case():
    form = CreateCaseForm()
    if form.validate_on_submit():
        case = Case(
            title=form.title.data,  # type: ignore
            content=form.content.data,  # type: ignore
            status=Status.PENDING,  # type: ignore
            case_type=CaseType[form.case_type.data],  # type: ignore
            client=current_user,  # type: ignore
        )
        db.session.add(case)
        db.session.commit()
        return redirect(url_for("client"))
    return render_template("client-create-case.html", form=form)


@app.route("/apply/<int:case_id>", methods=["POST", "GET"])
@login_required
def apply_for_case(case_id):
    form = LawyerApplicationForm()
    form.name.data = current_user.username
    if form.validate_on_submit():
        return redirect(url_for("lawyer"))
    return render_template(
        "lawyer-application.html",
        form=form,
        name=current_user.first_name + " " + current_user.last_name,
    )


@app.route("/client-sign-up", methods=["POST", "GET"])
def client_sign_up():
    if current_user.is_authenticated:
        return redirect_current_user_to_home(current_user)
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
        return redirect(url_for("index"))
    else:
        flash("Something went wrong.", "error")
    return render_template("client-sign-up.html", form=form)


# @app.route("/lawyer-application")
# @login_required
# def lawyer_application():
#     form = LawyerApplicationForm()
#     return render_template("lawyer-application.html", form=form)


@app.route("/client", methods=["POST", "GET"])
@login_required
def client():
    cases = Case.query.filter_by(client=current_user)
    header = ["Title", "Status", "Created By", "Case Type", "Date Posted"]
    return render_template("client.html", cases=cases, header=header)


@app.route("/case/<int:case_id>")
@login_required
def view_case(case_id):
    case = Case.query.get_or_404(case_id)
    return render_template("case-view.html", case=case)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
