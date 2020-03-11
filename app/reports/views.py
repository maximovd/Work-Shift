from uuid import uuid4

from flask import render_template, flash
from flask_login import login_required

from app.reports import bp
from app.models import create_shift_report, Category

from app.reports.forms import (
    WorkShiftReportsForm,
)


@bp.route('/reports', methods=['GET', 'POST'])
@login_required
def create_reports():
    reports = WorkShiftReportsForm()
    filename = uuid4()
    if reports.validate_on_submit():
        create_shift_report(filename)
        flash('Отчет сформирован', Category.SUCCESS.title)

    return render_template(
        'reports/reports.html',
        filename=filename,
        reports=reports,
    )
