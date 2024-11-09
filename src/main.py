# !usr/bin/env python3

from flask import Flask, render_template

from forms import (
    ClientSignUpForm,
    CreateCaseForm,
    LawyerApplicationForm,
    LawyerSignUpForm,
    LoginForm,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"  # This will have to be replaced.


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/login")
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

    return render_template("client-request.html", requests=data, header=header)


@app.route("/client-create-case")
def client_create_case():
    form = CreateCaseForm()
    return render_template("client-create-case.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
