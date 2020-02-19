from face_recognition import load_image_file, face_encodings
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required
from sqlalchemy import exc

from app import db
from app.admin import bp
from app.admin.forms import EmployeeAddingForm
from app.models import Employees, Category

UPLOAD_FOLDER = '/home/bazinga/app/Work-Shift/app/static/uploads/'


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_new_employee():
    add = EmployeeAddingForm()

    if add.validate_on_submit():

        if request.method == 'POST':

            if request.files:
                image = request.files['image']
                destination = ''.join([UPLOAD_FOLDER, image.filename])
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
