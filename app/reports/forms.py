from flask_wtf import FlaskForm

from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


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
    submit = SubmitField('Сформировать')


class WorkShiftReportsDownloadForm(FlaskForm):
    submit = SubmitField('Скачать')
