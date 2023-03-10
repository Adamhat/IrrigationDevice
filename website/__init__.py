from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Database import
from os import path

db = SQLAlchemy() # "database" is the database object we will need to use if we ever need to add something to the database
DB_NAME = "database.db"


def create_app(): 
    app = Flask(__name__) # Initializing Flask which is a web application framework for python which is what this whole website is built off of
    app.config['SECRET_KEY'] = '29048357029348752' # Not so secret anymore :)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # This line is basiclly telling the program to store the database inside of the website folder

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Alert

    with app.app_context():
        db.create_all() # automaticly checks to see if database exists before making one.

    return app
    