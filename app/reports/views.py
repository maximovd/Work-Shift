import os
from uuid import uuid4

from flask import render_template, flash, send_file, current_app, abort
from flask_login import login_required

from app.reports import bp
from app.models import create_shift_report, Category, Employees, WorkShift

from app.reports.forms import WorkShiftReportsForm


@bp.route('/reports', methods=['GET', 'POST'])
@login_required
def create_reports():
    reports = WorkShiftReportsForm()
    filename = uuid4()
    if reports.validate_on_submit():

        employees = (
            WorkShift.query.filter_by(
                start_date=reports.start_date.data,
                end_date=reports.end_date.data,
            ).outerjoin(Employees).all()
        )

        create_shift_report(employees=employees, filename=filename)

        flash('Отчет сформирован', Category.SUCCESS.title)

    return render_template(
        'reports/reports.html',
        filename=filename,
        reports=reports,
    )


@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    try:
        return send_file(
            os.path.join(
                current_app.config["CSV_UPLOADS_DIRECTORY"],
                f'{filename}.csv',
            ),
            attachment_filename=f'{filename}.csv',
            mimetype='text/csv',
            as_attachment=True,
        )
    except FileNotFoundError:
        abort(404)
