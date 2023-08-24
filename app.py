"""
Clothing Store API

This module defines a Flask API that serves as the starting point for a clothing store application.

Please note that this module is a preliminary version and should be extended to include additional
features such as login, product management, and more.
"""

import os

import re

from flask import Flask, jsonify, request, redirect, flash, url_for

from dotenv import load_dotenv

from sqlalchemy.exc import DatabaseError

from models import db, User, login

from flask_login import current_user, login_required, login_user, logout_user


load_dotenv()

app = Flask(__name__)

DB_PASSWORD = os.environ.get('DB_PWD')
DB_NAME = os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{DB_PASSWORD}@localhost/{DB_NAME}'

db.init_app(app)

login.init_app(app)
login.login_view = 'login'

def is_password_valid(string_pass):
    """Verifies that password contains at leats one uppercase letter, lowercase letter, number,
    and a special symbol.

    Args:
        string_pass(str): password to check.

    Returns:
        bool: True if password is valid, False otherwise.
    """

    reg_ex = r'^(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
    return re.search(pattern=reg_ex, string=string_pass) is not None


def are_unsername_and_email_valid(username, email):
    """
    Validates whether a username and email meet specific criteria.

    Args:
        username (str): The username to validate.
        email (str): The email to validate.

    Returns:
        bool: True if both username and email are valid, False otherwise.
    """

    if not re.match("^[A-Za-z0-9_-]*$", username):
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True


@app.route('/')
def index():
    """Returns the main page"""
    return '<h1> Test environment </h1>'


@app.route('/register', methods=['POST'])
def register():
    """
    Registers a new user with validation checks.

    Returns:
        Response: A JSON response indicating success or error.
    """

    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data\
            or 'repeat_password' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    repeat_password = data['repeat_password']

    if not are_unsername_and_email_valid(username, email):
        response = jsonify(
            {'error': 'The username or email do not meet the requirements'}), 400

    elif User.query.filter_by(username=username).first():
        response = jsonify(
            {'error': 'The user with the following username is already exsists'}), 400

    elif User.query.filter_by(email=email).first():
        response = jsonify(
            {'error': 'The user with the following email is already exsists'}), 400

    elif password != repeat_password:
        response = jsonify({'error': 'Passwords do not match'}), 400
    elif not is_password_valid(password):
        message = ''''Your password must contain at leats one uppercase letter,
        lowercase letter, number, and a special symbol.'''
        response = jsonify({'error': message}), 400
    else:

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            response = jsonify({'message': 'User registered successfully',
                                'username': username,
                                'email': email}), 201
        except DatabaseError:
            response = jsonify({'error': 'DatabaseError'}), 500
        else:
            response = jsonify({'error': 'An unexpected error occurred'}), 500
        return response

    return response


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    """ 
    Handle user login 
    returns:
        If the user is already authenticated-redirect to the home page.
        Home page if the request method is POST and the email and password are correct.
        If the email or password is incorrect redirect login page with an error flash message.
        If the request method is not POST, return the login page.
    """
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect('/')

        flash('Email or Password is incorrect!')
        return redirect('/login')

    return 'login page'


@app.route('/logout')
@login_required
def logout():
    """ 
    Handle GET requests for the /logout url
    return redirect to the home page
    """
    logout_user()
    return 'Logged out'


