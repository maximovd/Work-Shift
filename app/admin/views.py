from face_recognition import load_image_file, face_encodings
from flask import (
    render_template,
    flash,
    request,
    redirect,
    url_for,
    current_app
)
from flask_login import login_required
from sqlalchemy import exc

from app import db
from app.admin import bp
from app.admin.forms import (
    EmployeeAddingForm,
    EmployeeShowForm,
    EmployeeSearchForm,
    EmployeeEditingForm,
)
from app.models import Employees, Category


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_new_employee():
    add = EmployeeAddingForm()

    if add.validate_on_submit():

        if request.method == 'POST':

            if request.files:
                image = request.files['image']
                destination = ''.join(
                    [
                        current_app.config['CURRENT_UPLOADS_DIRECTORY'],
                        image.filename,
                    ],
                )
                try:
                    image.save(destination)
                except IsADirectoryError:
                    flash(
                        'Необходимо добавить фотографию сотрудника',
                        Category.DANGER.title,
                    )
                    return redirect(url_for('admin.add_new_employee'))

        load_photos = load_image_file(destination)
        encoding = face_encodings(load_photos, num_jitters=100)

        employee = Employees(
            first_name=add.first_name.data,
            last_name=add.last_name.data,
            service_number=add.service_number.data,
            department=add.department.data,
            encodings=encoding,
            photo=image.filename,
        )
        db.session.add(employee)

        try:
            db.session.commit()
            flash('Сотрудник добавлен', Category.SUCCESS.title)
        except exc.IntegrityError:
            flash(
                'Табельный номер уже присутствует в базе!',
                Category.DANGER.title,
            )
            return redirect(url_for('admin.add_new_employee'))

    return render_template('admin/add.html', form=add)


@bp.route('/browse', methods=['GET', 'POST'])
@login_required
def browse_employees():
    show = EmployeeShowForm()

    if show.validate_on_submit():
        return redirect(url_for('admin.show_employees'))
    return render_template('admin/browse.html', show=show, title='Сотрудники')


@bp.route('/show', methods=['GET', 'POST'])
@login_required
def show_employees():
    show = EmployeeShowForm()
    page = request.args.get('page', 1, type=int)

    employees = (
        Employees.query.filter_by(department=show.department.data).paginate
        (page=page, per_page=current_app.config['POSTS_PER_PAGE'])
    )

    return render_template(
        'admin/show.html',
        employees=employees,
        title='Сотрудники',
    )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_employee():
    search = EmployeeSearchForm()
    editing = EmployeeEditingForm()

    if search.validate_on_submit():
        employee = Employees.query.filter_by(
            first_name=search.first_name.data,
            last_name=search.last_name.data,
            service_number=search.service_number.data,
        ).first()
        if employee is None:
            flash('Сотдрудник не найден', Category.DANGER.title)
            return redirect(url_for('admin.search'))

        editing.first_name = search.first_name.data
        editing.last_name = search.last_name.data
        editing.service_number = search.service_number.data
        editing.department = employee.department
        flash('Сотрудник найден', Category.INFO.title)

    return render_template(
        'admin/search.html',
        search=search,
        title='Поиск и редактирование',
        editing=editing,
    )
