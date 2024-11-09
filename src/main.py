# !usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route("/")
def main() -> str:
    return "<p> Hello </p>"


if __name__ == "__main__":
    app.run()

db = SQLAlchemy(app)

class Client (db.model):
    id = db.Column(db.Integer, primary = True)
    first_name = db.Column(db.String(20), unique = False, nullable = False )
    last_name = db.Column(db.String(20), unique = False, nullable = False )
    username = db.Column(db.String(20) , unique = True, nullable = False)
    email = db.Column(db.String())
    password = db.Column(db.String(60) , unique =True , nullable = False)

    def __repr__(self):
        return f"User('{self.first_name},{self.last_name},{self.username},{self.email}')"

class Lawyer (db.model):
    id = db.Column(db.Integer, primary = True)
    first_name = db.Column(db.String(20), unique = False, nullable = False )
    last_name = db.Column(db.String(20), unique = False, nullable = False )
    username = db.Column(db.String(20) , unique = True, nullable = False)
    email = db.Column(db.String())
    password = db.Column(db.String(60) , unique =True , nullable = False)

    def __repr__(self):
        return f"User('{self.first_name},{self.last_name},{self.username},{self.email}')"