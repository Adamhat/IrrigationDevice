from . import db # this is basically saying from the website folder, import the database object created inside auth.py
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Automaticlly grabs date and time and stores it within the database.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Assosiate the data with a user

class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    flowRate = db.Column(db.Float)
    crossSection = db.Column(db.Float)
    volume = db.Column(db.Float)
    channelArea = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # A primary key basically means that it will generate a value unique to a specified user
    email = db.Column(db.String(150), unique=True) # Unique = True means you cannot store the same email twice. The (150) means the email cannot be above 150 char.
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')

class Alert(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)

class Options(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    channelWidth = db.Column(db.String(150))
    channelFloor = db.Column(db.String(150))
    channelHight = db.Column(db.String(150))
    
