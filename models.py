"""Module for the database models"""

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, LoginManager

login = LoginManager()

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        created_on (datetime): The timestamp of when the user's account was created.
        is_admin (bool): Indicates if the user has administrator privileges.
        is_confirmed (bool): Indicates if the user's account is confirmed.
        confirmed_on (datetime): The timestamp of when the user's account was confirmed.


    Methods:
        set_password(password: str) -> None:
            Set the password hash for the user.

        check_password(password: str) -> bool:
            Check if the provided password matches the stored password hash.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Set the password for the user.

        param password (str): Plain text password.

        returns: None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored password hash.

        param password (str): Plain text password to check against the stored hash.

        returns: bool
        """
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    """
    Load a user from database based on the provided user ID
    return the User object with ID or None
    """
    return User.query.get(int(user_id))
