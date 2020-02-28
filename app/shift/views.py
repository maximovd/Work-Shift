from flask import (
    flash,
    redirect,
    url_for,
    current_app,
    request,
    render_template,
)
from flask_login import login_required

from app.admin import bp
from app.shift.forms import EmployeeShiftForm
from app.models import Employees, WorkShift


@bp.route('/shift', methods=['GET', 'POST'])
@login_required
def employee_shift():
    shift = EmployeeShiftForm()
    page = request.args.get('page', 1, type=int)

    if shift.validate_on_submit():
        employees = (
            WorkShift.query.outerjoin(Employees).filter_by(
                department=shift.department.data,
            ).paginate(
                page=page, per_page=current_app.config['POSTS_PER_PAGE'],
            )
        )

    return render_template(
        'shift/show_shift.html',
        title='Рабочие часы',
        shift=shift,
        employees=employees,
    )

