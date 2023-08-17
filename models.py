
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)

    def set_password(self,password):
        """Set the password for the user.

        param password (str): Plain text password.

        returns: None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        """Check if the provided password matches the stored password hash.

        param password (str): Plain text password to check against the stored hash.

        returns: bool
        """
        return check_password_hash(self.password_hash,password)
    
