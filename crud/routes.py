from flask import render_template, redirect, url_for, flash, request
from crud import app, db
from crud.models import Data
from crud.forms import EmployeeForm


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def index():
    all_data = Data.query.all()

    return render_template("index.html", employees=all_data)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Data(name=form.name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("insert.html", title='Insert', form=form, legend='Add Employee')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    employee = Data.query.get_or_404(id)

    form = EmployeeForm()
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.email = form.email.data
        employee.phone = form.phone.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.name.data = employee.name
        form.email.data = employee.email
        form.phone.data = employee.phone

    return render_template('update.html', title='Update', form=form, legend='Update Employee')


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    employee = Data.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('index'))
