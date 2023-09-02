from functools import wraps

from flask import jsonify
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return jsonify({'message': 'The user is already logged in'}), 200
        return func(*args, **kwargs)

    return decorated_function
