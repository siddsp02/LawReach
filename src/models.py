from datetime import datetime
from enum import Enum, auto

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Status(Enum):
    OPEN = auto()
    CLOSED = auto()
    PENDING = auto()


class CaseType(Enum):
    MARRIAGE = auto()
    ACCIDENT = auto()
    CRIMINAL = auto()


class UserType(Enum):
    LAWYER = auto()
    CLIENT = auto()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String())
    password = db.Column(db.String(60), unique=True, nullable=False)
    client_cases = db.relationship(
        "Case", backref="client", lazy=True, foreign_keys="Case.client_id"
    )
    lawyer_cases = db.relationship(
        "Case", backref="lawyer", lazy=True, foreign_keys="Case.lawyer_id"
    )

    def __repr__(self):
        return f"{type(self).__name__}('{self.first_name}', '{self.last_name}', '{self.username}', '{self.email}')"


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    case_type = db.Column(db.Enum(CaseType))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.status}', '{self.client_id}', '{self.case_type}', '{self.date_posted}')"
