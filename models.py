#models.py
#Adapted from https://github.com/PrettyPrinted/flask_auth_scotch

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    phone = db.Column(db.Unicode(20))

class History(db.Model):
    query_id = db.Column(db.Integer, primary_key=True)
    submit_text = db.Column(db.String(2000))
    returned_text = db.Column(db.String(2000))
    submit_user = db.Column(db.String(100))

class Logins(db.Model):
    login_id = db.Column(db.Integer, primary_key=True)
    login_time = db.Column(db.String(100))
    logout_time = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
