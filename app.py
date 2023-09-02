"""
Clothing Store API

This module defines a Flask API that serves as the starting point for a clothing store application.

Please note that this module is a preliminary version and should be extended to include additional
features such as login, product management, and more.
"""

import os

import re

from datetime import datetime

from flask import Flask, jsonify, request, Blueprint, render_template, url_for

from dotenv import load_dotenv

from sqlalchemy.exc import DatabaseError

from models import db, User, login

from flask_login import current_user, login_required, login_user, logout_user

from flask_migrate import Migrate

from utils.decorators import logout_required

from accounts.token import confirm_token, generate_token

from flask_mail import Mail

from flask_mail import Message

from config import Config

load_dotenv()

app = Flask(__name__)
migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL

DB_PASSWORD = os.environ.get('DB_PWD')
DB_NAME = os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{DB_PASSWORD}@localhost/{DB_NAME}'
app.secret_key = Config.SECRET_KEY

db.init_app(app)

login.init_app(app)
login.login_view = 'login'

accounts_bp = Blueprint("accounts", __name__)
mail = Mail(app)
app.mail = mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=Config.MAIL_DEFAULT_SENDER,
    )
    app.mail.send(msg)


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


@accounts_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user with validation checks.

    Returns:
        Response: A JSON response indicating success or error.
    """

    data = request.get_json()

    if not data or 'username' not in data or 'email' not in data or 'password' not in data \
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
            {'error': 'The user with the following username already exists'}), 400

    elif User.query.filter_by(email=email).first():
        response = jsonify(
            {'error': 'The user with the following email already exists'}), 400

    elif password != repeat_password:
        response = jsonify({'error': 'Passwords do not match'}), 400
    elif not is_password_valid(password):
        message = '''Your password must contain at least one uppercase letter,
        lowercase letter, number, and a special symbol.'''
        response = jsonify({'error': message}), 400
    else:
        new_user = User(username=username, email=email,
                        created_on=datetime.now())
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            token = generate_token(new_user.email)
            confirm_url = url_for("accounts.confirm_email",
                                  token=token, _external=True)
            html = render_template(
                "accounts/confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"

            send_email(new_user.email, subject, html)
            login_user(new_user)
            response = jsonify({'message': 'User registered successfully',
                                'username': username,
                                'email': email}), 201
        except DatabaseError as error:
            response = jsonify({'error': str(error)}), 500

    return response


@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login_():
    """ 
    Handle user login 
    return a JSON response indicating success or error
    """
    if current_user.is_authenticated:
        return jsonify({'message': 'The user is already logged in'}), 200

    if request.method == 'POST':
        data = request.get_json()

        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return jsonify({'message': 'Successfully logged in'}), 200

        return jsonify({'error': 'Incorrect email or password'}), 401

    return jsonify({'message': 'Login page'}), 200


@app.route('/logout')
@login_required
def logout():
    """ 
    Handle GET requests for the /logout url
    return a JSON response
    """
    logout_user()
    return jsonify({'message': 'Logged out'}), 200


@accounts_bp.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return jsonify('The confirmation link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        return jsonify('Account already confirmed. Please login.', 'success')
    else:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify("You have confirmed your account. Thanks!")


app.register_blueprint(accounts_bp)

if __name__ == '__main__':
    app.run(debug=True)
