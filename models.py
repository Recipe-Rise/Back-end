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

class History(db.Model):
    __tablename__ = 'entire_recipe_details'
    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)

    calories = db.Column(db.Float, nullable=False)
    carbohydrates_pdv = db.Column(db.Float, nullable=False, name="carbohydrates (PDV)")
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    minutes = db.Column(db.Float, nullable=False)
    n_ingredients = db.Column(db.Integer, nullable=False)
    n_steps = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    protein_pdv = db.Column(db.Float, nullable=False, name="protein (PDV)")
    saturated_fats_pdv = db.Column(db.Float, nullable=False, name="saturated fats (PDV)")
    similarity = db.Column(db.Float, nullable=False)
    sodium_pdv = db.Column(db.Float, nullable=False, name="sodium (PDV)")
    steps = db.Column(db.ARRAY(db.Text), nullable=False)
    sugar_pdv = db.Column(db.Float, nullable=False, name="sugar (PDV)")
    total_fats_pdv = db.Column(db.Float, nullable=False, name="total fats (PDV)")

class Workout(db.Model):
    __tablename__ = 'workouts'
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    bodyPart = db.Column(db.Text, nullable=False)
    gifUrl = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    target = db.Column(db.Text, nullable=False)
    secondaryMuscles = db.Column(db.ARRAY(db.Text), nullable=False)
    instructions = db.Column(db.ARRAY(db.Text), nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)

