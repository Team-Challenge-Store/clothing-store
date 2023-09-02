from flask.cli import FlaskGroup

from app import app
from models import User, db

import getpass
from datetime import datetime


cli = FlaskGroup(app)


@cli.command("create_admin")
def create_admin():
    """Creates the admin user."""
    username = input("Enter your username: ")
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            user = User(
                username=username,
                email=email,
                is_admin=True,
                is_confirmed=True,
                created_on=datetime.now(),
                confirmed_on=datetime.now(),
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Admin with email {email} created successfully!")
        except Exception as error:
            print(error)


if __name__ == "__main__":
    cli()
