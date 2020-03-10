import csv
from datetime import date

from celery import Celery
from flask import current_app

from app import create_app
from app.models import WorkShift, Employees

celery_app = Celery('tasks', broker='redis://localhost:6379/0')
flask_app = create_app()


@celery_app.task
def create_shift_report():
    filename = date.today()  # TODO Нужно придумать, как называть файл
    shift_dumps = WorkShift.query.outerjoin(Employees).all()

    with open(
            f'{current_app.config["CURRENT_UPLOADS_DIRECTORY"]}'
            f'{filename}',
            'w',
    ) as report:
        out = csv.writer(report)
        out.writerow([
            'id',
            'first_name',
            'last_name',
            'service_number',
            'department',
            'arrival_time',
            'depature_time',
            'marked_department',
        ],
        )

        for employee in shift_dumps:
            out.writerow([
                employee.employee_id,
                employee.Employyes.first_name,
                employee.Employyes.last_name,
                employee.Employyes.service_number,
                employee.Employyes.department,
                employee.arrival_time,
                employee.depature_time,
                employee.marked_department,
            ],
            )