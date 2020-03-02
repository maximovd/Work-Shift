import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError


from app.models import Department


def get_departments():
    return Department.query.all()


class EmployeeAddingForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    service_number = StringField(
        'Табельный номер',
        validators=[DataRequired()],
    )

    department = QuerySelectField(
        'Подразделение',
        validators=[DataRequired()],
        query_factory=get_departments,
    )
    submit = SubmitField('Добавить')

    def validate_service_number(self, service_number):
        """
        The validator verifies the correctness of entering
         the service number for 1C.
        It must match the template 0000-00000(4 characters,
         dashes, 5 characters)
        """
        regex = r'^[0-9]{4}[-]{1}[0-9]{5}$'
        if re.fullmatch(regex, service_number.data) is None:
            raise ValidationError(
                'Не правильно введен табельный номер. Формат ввода 0000-00000',
            )

    def validate_first_name(self, first_name):

        regex = r'^[А-Я]{1}[а-я]{2,25}'

        if re.fullmatch(regex, first_name.data) is None:
            raise ValidationError(
                'Неправильный формат ввода имени (Пример: Иван)',
            )

        if re.fullmatch(regex, self.last_name.data) is None:
            raise ValidationError(
                'Неправильный формат ввода фамилии (Пример: Иванов)',
            )


class EmployeeShowForm(FlaskForm):
    department = QuerySelectField(
        'Подразделение',
        validators=[DataRequired()],
        query_factory=get_departments,
    )
    submit = SubmitField('Показать')


class EmployeeEditingForm(FlaskForm):
    id = HiddenField()
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    service_number = StringField(
        'Табельный номер',
        validators=[DataRequired()],
    )
    department = QuerySelectField(
        'Подразделение',
        validators=[DataRequired()],
        query_factory=get_departments,
    )
    encodings = HiddenField()
    image = HiddenField()
    submit = SubmitField('Изменить')


class EmployeeDeleteForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField('Удалить из базы')


class EmployeeShiftForm(FlaskForm):
    date = DateField(
        'Дата',
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

