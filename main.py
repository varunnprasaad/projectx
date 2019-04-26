from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

import db_handler.models

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    reservations = db_handler.models.Reservation.query.filter_by(customer_id=current_user.id).all()
    return render_template('profile.html', reservations=reservations)


@main.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    offices = db_handler.models.Office.query.all()
    categories = db_handler.models.Category.query.all()

    if request.method == 'GET':
        return render_template('reservation.html', offices=offices, categories=categories)

    office = request.form.get('office')
    category = request.form.get('category')

    vehicles = db_handler.models.Vehicle.query.filter_by(office_id=office, category_id=category, availability=1).all()
    p = db_handler.models.Category.query.filter_by(id=category).first()

    return render_template('reservation.html', vehicles=vehicles, selected_ofc=office, selected_cat=category,
                           offices=offices, categories=categories, price=p.price)


@main.route('/delreservation', methods=['GET', 'POST'])
def delreservation():
    res = int(request.args.get('res'))
    from app import db

    reservation = db_handler.models.Reservation.query.filter_by(id=res).first()
    vehicle = db_handler.models.Vehicle.query.filter_by(id=reservation.vehicle_id).first()

    db_handler.models.Reservation.query.filter_by(id=res).delete()
    vehicle.availability = 1
    db.session.commit()

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    vehicle_id = request.form.get('vehicle')
    price = request.form.get('price')

    vehicle = db_handler.models.Vehicle.query.filter_by(id=vehicle_id).first()
    category = db_handler.models.Category.query.filter_by(id=vehicle.category_id).first()

    return render_template('checkout.html', vehicle=vehicle, price=price, category=category)


@main.route('/confirmation', methods=['GET', 'POST'])
@login_required
def confirmation():
    from datetime import datetime
    py, pm, pd = (request.form.get('pickup_date')).split('-')
    pickup_date = datetime(int(py), int(pm), int(pd))

    dy, dm, dd = request.form.get('dropoff_date').split('-')
    dropoff_date = datetime(int(dy), int(dm), int(dd))

    customer = current_user.id

    vehicle_id = int(request.form.get('vehicle'))
    vehicle = db_handler.models.Vehicle.query.filter_by(id=vehicle_id).first()
    office = db_handler.models.Office.query.filter_by(id=vehicle.office_id).first()
    from app import db

    new_reservation = db_handler.models.Reservation(pickup_date=pickup_date, dropoff_date=dropoff_date,
                                                    customer_id=customer, office_id=office.id,
                                                    vehicle_id=vehicle.id)

    db.session.add(new_reservation)

    vehicle.availability = 0
    db.session.commit()

    return render_template('confirmation.html')


@main.route('/update', methods=['GET', 'POST'])
@login_required
def update_reservation():
    reservation_id = int(request.form.get('r'))

    res = db_handler.models.Reservation.query.filter_by(id=reservation_id).first()

    return render_template('update_reservation.html', res=res)


@main.route('/_updatereservation', methods=['GET', 'POST'])
@login_required
def _updatereservation():
    reservation_id = request.form.get('r')
    _pickup = request.form.get('pickup_date')
    _dropoff = request.form.get('dropoff_date')

    res = db_handler.models.Reservation.query.filter_by(id=reservation_id).first()

    res.pickup_date = _pickup
    res.dropoff_date = _dropoff

    from app import db

    db.session.commit()

    return redirect('/profile')
