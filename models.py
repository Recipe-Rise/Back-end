from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Numeric(5, 2), nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    bmr = db.Column(db.Numeric(10, 2))
    bmi = db.Column(db.Numeric(5, 2))
    logged_in =db.Column(db.Boolean, default=False)
    activity_level = db.Column(db.String(20), nullable=False)
    fitness_goal = db.Column(db.String(25), nullable=False)
    profile_photo = db.Column(db.LargeBinary)
    profile_mime = db.Column(db.String(50))  # e.g., 'image/jpeg'

class Chat(db.Model):
    __tablename__ = 'chat_history'
    user_id = db.Column(db.Integer)
    chat_buble = db.Column(db.String(1024), nullable=False)
    sender = db.Column(db.String(10), nullable=False)
    time_and_date = db.Column(db.DateTime, nullable=False)
    buble_id = db.Column(db.Integer, primary_key=True )