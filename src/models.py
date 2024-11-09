from datetime import datetime
from enum import Enum, auto

from flask_sqlalchemy import SQLAlchemy

try:
    from src.main import app
except ImportError:
    from main import app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Status(Enum):
    OPEN = auto()
    CLOSED = auto()
    PENDING = auto()


class CaseType(Enum):
    MARRIAGE = auto()
    ACCIDENT = auto()
    CRIMINAL = auto()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String())
    password = db.Column(db.String(60), unique=True, nullable=False)
    cases = db.relationship("Case", backref="author", lazy=True)

    def __repr__(self):
        return f"{type(self).__name__}('{self.first_name},{self.last_name},{self.username},{self.email}')"


class Lawyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String())
    password = db.Column(db.String(60), unique=True, nullable=False)
    # cases = db.relationship("Case", backref="author", lazy=True)

    def __repr__(self):
        return f"{type(self).__name__}('{self.first_name}' , '{self.last_name}', '{self.username}', '{self.email}')"


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    case_type = db.Column(db.Enum(Status))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.status}', '{self.user_id}', '{self.case_type}', '{self.date_posted}')"


if __name__ == "__main__":
    with app.app_context() as ctx:
        db.create_all()
        lawyer = Lawyer(
            first_name="Joe",  # type: ignore
            last_name="Mama",  # type: ignore
            username="joemama",  # type: ignore
            password="",  # type: ignore
        )
        db.session.add(lawyer)
        print(Lawyer.query.all())
