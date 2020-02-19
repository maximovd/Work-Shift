import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired


from app.models import Department


def get_departments():
    return Department.query.all()


class EmployeeAddingForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    service_number = StringField(
        'Табельный номер',
        validators=[DataRequired()],
    )

    department = QuerySelectField(
        'Подразделение',
        validators=[DataRequired()],
        query_factory=get_departments,
        allow_blank=True,
    )
