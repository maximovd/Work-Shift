from flask_wtf import FlaskForm

from wtforms import SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

from app.models import Department


def get_departments():
    return Department.query.all()


class EmployeeShiftForm(FlaskForm):
    data = DateField(
        'Дата начала действия сертификата',
        format='%Y-%m-%d',
        validators=[DataRequired()],
    )
    department = QuerySelectField(
        'Подразделение',
        validators=[DataRequired()],
        query_factory=get_departments,
        allow_blank=True,
    )
    submit = SubmitField('Показать')
