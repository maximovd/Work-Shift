from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Department


def get_departments():
    return Department.query.all()


class WorkShiftReportsForm(FlaskForm):
    start_date = DateField(
        'Начало периода',
        format='%Y-%m-%d',
        validators=[DataRequired()],
    )
    end_date = DateField(
        'Окончание периода',
        format='%Y-%m-%d',
        validators=[DataRequired()],
    )
    department = QuerySelectField(
        'Подразделение',
        validators=[DataRequired()],
        query_factory=get_departments,
    )
    submit = SubmitField('Сформировать')


class WorkShiftReportsDownloadForm(FlaskForm):
    submit = SubmitField('Скачать')
