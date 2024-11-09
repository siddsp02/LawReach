# !usr/bin/env python3

from flask import Flask, render_template

from forms import ClientSignUpForm, LawyerSignUpForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"  # This will have to be replaced.


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/sign-up")
def signup():
    return render_template("signup.html")


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


@app.route("/client-sign-up")
def client_sign_up():
    form = ClientSignUpForm()
    return render_template("client-sign-up.html", form=form)


@app.route("/client-requests")
def client_request():
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

    return render_template("client-request.html", requests=data)


if __name__ == "__main__":
    app.run(debug=True)
