# auth.py
#Adapted from https://github.com/PrettyPrinted/flask_auth_scotch

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from .sanitize import sanitize

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    mfa = request.form.get('2fa')
    remember = True if request.form.get('remember') else False
    
    if not mfa.isdigit():
        flash('Phone for 2FA is not a number!')
        return redirect(url_for('auth.login_post'))
    
    #sanitize user input trust no man
    email = sanitize(email)

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Login Failed. Please check your login details and try again.')
        return redirect(url_for('auth.login_post')) # if user doesn't exist or password is wrong, reload the page
    if not user.phone == mfa:
        flash('Login Failed. Please verify your multi factor authentication')
        return redirect(url_for('auth.login_post'))
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    phone = request.form.get('phone')

    #sanitize input. If someone does something sketch, they won't get to log in with their gargbage inputs
    email = sanitize(email)
    name = sanitize(name)
    if not phone.isdigit():
        flash('Phone for 2FA is not a number!')
        return redirect(url_for('auth.signup_post'))

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup_post'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), phone=phone)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login_post'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))