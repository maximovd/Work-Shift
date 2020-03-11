from datetime import date

from celery import Celery
from celery.schedules import crontab

from app import create_app
from app.models import create_shift_report

celery_app = Celery('tasks', broker='redis://localhost:6379/0')
flask_app = create_app()


@celery_app.task
def create_shift_report():
    filename: date = date.today()  # TODO Нужно придумать, как называть файл
    create_shift_report(filename)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), create_shift_report.s())
