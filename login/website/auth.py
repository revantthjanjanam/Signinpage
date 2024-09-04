from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re


def is_valid_email(email):
    # Regular expression for validating an email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regex
    if re.match(email_regex, email):
        return True
    else:
        return False
"""def password_check (password):
    s = 'Password must cointain'
    if len(password) < 8:
        s = s + '8 charecters,'
    if (for l in )
    return True"""
auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in Sucessfully',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect password!',category='error')
        else:
            flash('Email does not exists!',category='error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!',category='error')
        elif is_valid_email(email) == False:
            flash('Invalid email id', category='E')
        elif len(firstname)<2:
            flash('Length of first name should be greater than 2charecters', category='error')
        elif len(lastname)<2:
            flash('Length of second name should be greater than 2charecters', category='error')
        elif len(password1) < 8:
            flash('Length of Password should be more than 8 charecters', category='error')
        elif password1 != password2:
            flash('Password does\'t match', category='error')
        else:
            new_user = User(email = email, first_name = firstname, middle_name=middlename,last_name=lastname, password = generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created sucessfully',category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)