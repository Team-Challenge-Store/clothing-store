import os

from flask import Flask

from dotenv import load_dotenv


from app.models import db, login


from flask_migrate import Migrate

from flask_mail import Mail


from config import Config

app = Flask(__name__)
migrate = Migrate(app, db)
mail = Mail(app)

def create_app():

    load_dotenv()

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
    login.login_view = 'login_'


    from app.routes import accounts_bp, main_bp

    app.register_blueprint(accounts_bp)
    app.register_blueprint(main_bp)

    return app

