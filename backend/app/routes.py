"""
Clothing Store API

This module defines a Flask API that serves as the starting point for a clothing store application.

Please note that this module is a preliminary version and should be extended to include additional
features such as login, product management, and more.
"""


import re

from datetime import datetime

from flask import jsonify, request, render_template, url_for, Blueprint

from sqlalchemy.exc import DatabaseError

from app.models import db, User

from flask_login import current_user, login_required, login_user, logout_user

from app.utils.decorators import logout_required

from app.accounts.token import confirm_token, generate_token

from app.utils.mail import send_email


main_bp = Blueprint('main', __name__)
accounts_bp = Blueprint("accounts", __name__)

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


@main_bp.route('/')
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


@main_bp.route('/login', methods=['GET', 'POST'])
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
        remember = data.get('remember')

        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            return jsonify({'message': 'Successfully logged in'}), 200
        else:
            return jsonify({'error': 'Incorrect email or password'}), 401

    return jsonify({'message': 'Login page'}), 200


@main_bp.route('/logout')
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



@main_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        data = request.get_json()
        current_password = data['current_password']
        new_password = data['new_password']
        retype_password = data['retype_password']

        if current_user.check_password(current_password):
            if new_password != current_password:
                if new_password == retype_password:
                    if is_password_valid(new_password):
                        current_user.set_password(new_password)
                        db.session.commit()
                        return jsonify({'message': 'Password changed successfully'}), 200
                    else: 
                        message = '''Your password must contain at least one uppercase letter, lowercase letter, number, and a special symbol.'''
                        return jsonify({'error': message}), 400
                else:
                    return jsonify({'error': 'New passwords do not match'}), 400
            else: 
                return jsonify({'error': 'New password cannot be the same as the current password'}), 400
        else:
            return jsonify({'error': 'Current password is incorrect'}), 400
        
    return jsonify({'message': 'Change password page'}), 200


@main_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']

        user = User.query.filter_by(email=email).first()

        if user:
            try:
                token = generate_token(user.email)
                reset_url = url_for("reset_password", token=token, _external=True)
                html = render_template("accounts/reset_password.html", reset_url=reset_url)
                subject = 'Password Reset Request'
            
                send_email(email, subject, html)
                return jsonify({'message': 'Password reset email sent'}), 200
            except Exception as e:
                return jsonify({'error': 'Email sending failed', 'details': str(e)}), 500
        else:
            return jsonify({'error': 'No user with that email found'}), 404
    return jsonify({'message': 'Reset password page'})


@main_bp.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    try:
        email = confirm_token(token)
    except:
        return jsonify('The reset link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first()

    if user:
        if request.method == 'POST':
            # Check if 'new_password' and 'retype_password' are in the form data
            if 'new_password' in request.form and 'retype_password' in request.form:
                new_password = request.form['new_password']
                retype_password = request.form['retype_password']

                if new_password == retype_password:
                    # Update the user's password
                    user.set_password(new_password)
                    db.session.commit()
                    return jsonify({'message': 'Password reset successfully'}), 200
                else:
                    return jsonify({'error': 'New passwords do not match'}), 400

        return jsonify({'reset_password_confirm page'})
    else:
        return jsonify({'error': 'No user with that email found'}), 404
    
