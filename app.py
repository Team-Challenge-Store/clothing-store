import os

from flask import Flask, jsonify, request

from dotenv import load_dotenv
from models import db, User


load_dotenv()

app = Flask(__name__)

DB_PASSWORD = os.environ.get('DB_PWD')
DB_NAME = os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{DB_PASSWORD}@localhost/{DB_NAME}'

db.init_app(app)


@app.route('/')
def index():
    """Returns the main page"""
    return '<h1> Test environment </h1>'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing fields'}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': f'User registered successfully'}), 201
    except Exception as error:
         return jsonify({'error': {error}}), 500


#with app.app_context():
#    db.create_all()


if __name__ == '__main__':
    app.run()