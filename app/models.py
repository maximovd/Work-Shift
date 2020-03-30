import os
import csv
from uuid import UUID
from typing import Union, NoReturn
from datetime import date
from enum import Enum

from openpyxl import Workbook
from flask import flash, current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from face_recognition import face_encodings, load_image_file

from app import db, login

filename_type = Union[date, UUID]  # TODO Перенести объявление нового типа


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
        return f'{self.first_name} {self.last_name}'


def download_image(file_name, image) -> str:
    destination = ''.join(
        [
            current_app.config['UPLOADS_DIRECTORY'],
            file_name,
        ],
    )
    destination = destination.replace(' ', '')
    try:
        image.save(destination)
    except IsADirectoryError:
        flash(
            'Необходимо добавить фотографию сотрудника',
            Category.DANGER.title,
        )
    return destination


def face_encoding_image(destination: str) -> list:
    load_photos = load_image_file(destination)
    encoding = face_encodings(load_photos, num_jitters=100)
    return encoding


def delete_photo(photo_name: str) -> NoReturn:
    destination = ''.join(
        [
            current_app.config['UPLOADS_DIRECTORY'],
            photo_name,
        ],
    )
    os.remove(destination)


def create_shift_report(employees: list, filename: filename_type) -> NoReturn:

    with open(
            f'{current_app.config["CSV_UPLOADS_DIRECTORY"]}'
            f'{filename}.csv',
            'w',
    ) as report:
        out = csv.writer(report)
        out.writerow([
            'ID смены',
            'ID сотрудника',
            'Имя',
            'Фамилия',
            'Табельный номер',
            'Подразделение',
            'Время начала смены',
            'Время окончания смены',
            'Подразделение, где отметился',
        ],
        )

        for employee in employees:
            out.writerow([
                employee.id,
                employee.employee_id,
                employee.employees.first_name,
                employee.employees.last_name,
                employee.employees.service_number,
                employee.employees.department,
                employee.arrival_time,
                employee.departure_time,
                employee.marked_department,
            ],
            )


def csv_to_xlsx(filename):
    wb = Workbook()
    ws = wb.active
    with open(
            f'{current_app.config["CSV_UPLOADS_DIRECTORY"]}{filename}.csv',
            'r',
    ) as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save(f'{current_app.config["CSV_UPLOADS_DIRECTORY"]}{filename}.xlsx')
    os.remove(f'{current_app.config["CSV_UPLOADS_DIRECTORY"]}{filename}.csv')


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

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
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
    employee = db.relationship('Employees', back_populates='work_shift')
    arrival_time = db.Column(db.DateTime, index=True)
    start_date = db.Column(db.Date, index=True)
    departure_time = db.Column(db.DateTime, index=True)
    end_date = db.Column(db.Date, index=True)
    marked_department = db.Column(db.Integer)


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
