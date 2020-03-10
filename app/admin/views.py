from uuid import uuid4
from flask import (
    render_template,
    flash,
    request,
    redirect,
    url_for,
    current_app,
)
from flask_login import login_required
from sqlalchemy import exc
from PIL import UnidentifiedImageError

from app import db
from app.admin import bp
from app.admin.forms import (
    EmployeeAddingForm,
    EmployeeShowForm,
    EmployeeEditingForm,
    EmployeeDeleteForm,
    EmployeeShiftForm,
)
from app.models import (
    Employees,
    WorkShift,
    Category,
    download_image,
    face_encoding_image,
    delete_photo,
)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_new_employee():
    add = EmployeeAddingForm()

    if add.validate_on_submit():
        if request.files:
            image = request.files['image']
            photo = f'{uuid4()}.jpg'
            destination = download_image(file_name=photo, image=image)

            try:
                encoding = face_encoding_image(destination)
            except UnidentifiedImageError:
                flash(
                    'Проблема с фото, загрузите еще раз',
                    Category.DANGER.title,
                )

                delete_photo(photo)
                return redirect(url_for('admin.add_new_employee'))
        employee = Employees(
            first_name=add.first_name.data,
            last_name=add.last_name.data,
            service_number=add.service_number.data,
            department=add.department.data,
            encodings=encoding,
            photo=photo,
        )
        db.session.add(employee)

        try:
            db.session.commit()
            flash('Сотрудник добавлен', Category.SUCCESS.title)
        except exc.IntegrityError:
            flash(
                'Сотрудник с таким табельным номером уже присутствует в базе!',
                Category.DANGER.title,
            )
            return redirect(url_for('admin.add_new_employee'))
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
    delete = EmployeeDeleteForm()
    show = EmployeeShowForm()
    page = request.args.get('page', 1, type=int)

    employees = (
        Employees.query.filter_by(department=show.department.data).paginate
        (page=page, per_page=current_app.config['POSTS_PER_PAGE'])
    )

    return render_template(
        'admin/show.html',
        employees=employees,
        show=show,
        delete=delete,
        title='Сотрудники',
    )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_employee():
    if request.method == 'POST':
        text = request.form['i_name']

        first_name, last_name = text.split()
        first_name = first_name.capitalize()
        last_name = last_name.capitalize()

        found_employees = Employees.query.filter_by(
            first_name=first_name,
            last_name=last_name,
        ).all()

    return render_template(
        'admin/found.html',
        title='Результаты поиска',
        employees=found_employees,
    )


@bp.route('/profile/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def employee_profile(employee_id):
    editing = EmployeeEditingForm()
    delete = EmployeeDeleteForm()

    employee = Employees.query.filter_by(id=employee_id).first()
    exist_photo = employee.photo

    if request.method == 'GET':
        employee = Employees.query.filter_by(id=employee_id).first()

        editing.id.data = employee.id
        editing.first_name.data = employee.first_name
        editing.last_name.data = employee.last_name
        editing.service_number.data = employee.service_number
        editing.department.data = employee.department
        delete.id.data = employee.id

    if editing.validate_on_submit():
        employee = Employees.query.filter_by(id=employee_id).first()

        if request.files['image']:
            image = request.files['image']
            if image.filename != '':
                photo = f'{uuid4()}.jpg'
                destination = download_image(file_name=photo, image=image)
                delete_photo(exist_photo)
                employee.encodings = None  # Overwriting face encodings
                db.session.commit()

                encodings = face_encoding_image(destination)
                employee.encodings = encodings
                employee.photo = photo

        employee.first_name = editing.first_name.data
        employee.last_name = editing.last_name.data
        employee.service_number = editing.service_number.data
        employee.department = editing.department.data

        try:
            db.session.commit()
            flash('Информация обновлена', Category.SUCCESS.title)
        except exc.IntegrityError:
            flash('Табельный номер существует', Category.DANGER.title)

            return redirect(url_for(
                'admin.employee_profile',
                employee_id=employee_id,
            ),
            )
    return render_template(
        'admin/profile.html',
        title=f'{editing.first_name.data} {editing.last_name.data}',
        editing=editing,
        delete=delete,
        image_name=exist_photo,
    )


@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    delete = EmployeeDeleteForm()
    editing = EmployeeDeleteForm()
    if delete.validate_on_submit():
        employee = Employees.query.filter_by(id=delete.id.data).first()
        if employee is not None:
            delete_photo(employee.photo)
            db.session.delete(employee)
            db.session.commit()
            flash('Сотрудник удален из базы!', Category.WARNING.title)
            return redirect(url_for('admin.add_new_employee'))
    return render_template(
        'admin/profile.html',
        delete=delete,
        editing=editing,
    )


@bp.route('/shift', methods=['GET', 'POST'])
@login_required
def employee_shift():
    shift = EmployeeShiftForm()
    page = request.args.get('page', 1, type=int)
    employees = (
        WorkShift.query.outerjoin(Employees).filter_by(
            department=shift.department.data,
        ).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        )
    )
    if shift.validate_on_submit():
        employees = (
            WorkShift.query.outerjoin(Employees).filter_by(
                department=shift.department.data,
            ).paginate(
                page=page, per_page=current_app.config['POSTS_PER_PAGE'],
            )
        )

    return render_template(
        'admin/show_shift.html',
        title='Рабочие часы',
        shift=shift,
        employees=employees,
    )
