from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

import db_handler.models

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    # str().title() for Title Case words
    first_name = str(request.form.get('firstname')).lower()
    last_name = str(request.form.get('lastname')).lower()
    email = request.form.get('email')
    # Hashing passwords to sha256
    password = generate_password_hash(request.form.get('password'), method='sha256')
    phone = request.form.get('phone')
    street = str(request.form.get('street')).lower()
    city = str(request.form.get('city')).lower()
    state = str(request.form.get('state')).lower()
    zip = request.form.get('zip')
    if zip:
        zip = int(zip)
    country = str(request.form.get('country')).lower()

    '''
        Check if email already exists in db
        If yes, redirect user to signup page with error
        If no, redirect user to login page
    '''

    customer = db_handler.models.Customer.query.filter_by(email=email).first()

    if customer:
        flash('User already exists.')
        return redirect(url_for('auth.signup'))

    '''
        Check if address exists
        If yes, assign it's ID to new user
        If no, create new address and assign address id to new user
    '''

    addr = db_handler.models.Address.query.filter_by(street=street, zip=zip).first()
    if addr:
        new_user = db_handler.models.Customer(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                              password=password, address=addr)
        db_handler.models.db.session.add(new_user)
    else:
        new_addr = db_handler.models.Address(street=street, city=city, state=state, zip=zip, country=country)
        db_handler.models.db.session.add(new_addr)
        new_user = db_handler.models.Customer(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                              password=password, address=new_addr)
        db_handler.models.db.session.add(new_user)
    db_handler.models.db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    user = db_handler.models.Customer.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login credentials.')
        return redirect(url_for('auth.login'))

    login_user(user)

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
