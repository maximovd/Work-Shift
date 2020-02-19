from enum import Enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Employees(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
    )
    first_name = db.Column(db.String(30), index=True)
    last_name = db.Column(db.String(30), index=True)
    service_number = db.Column(db.String(30), index=True, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='employees')
    work_shift = db.relationship('WorkShift', backref='employees')
    encodings = db.Column(db.PickleType(), unique=True)
    photo = db.Column(db.String(128))

    def __str__(self):
        return f'Сотрудник {self.first_name} {self.last_name}'


class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Пользователь {self.username}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Department(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    name = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return self.name


class WorkShift(db.Model):
    """Table for recording arrivals and departures."""
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    arrival_time = db.Column(db.DateTime, index=True)
    depature_time = db.Column(db.DateTime, index=True)


class ServerStatus(db.Model):
    """
     Table for checking the connection of local
     computers with the main server.
    """

    date = db.Column(
        db.Date,
        primary_key=True,
        index=True,
    )
    url = db.Column(db.String, index=True)
    status = db.Column(db.Boolean)


class Category(Enum):
    """Constant for flask flash message."""

    SUCCESS = (1, 'success')
    WARNING = (2, 'warning')
    DANGER = (3, 'danger')
    INFO = (4, 'info')

    def __init__(self, id, title):
        self.id = id
        self.title = title