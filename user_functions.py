from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User ,db

def register():
    data= request.form.to_dict()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    logged_in = True

    # Calculate BMI if height and weight are provided
    bmi = None
    if data.get('height') and data.get('weight'):
        height_m = float(data['height']) / 100
        weight_kg = float(data['weight'])
        bmi = weight_kg / (height_m * height_m)

    # Calculate BMR
    bmr = None
    if data.get('weight') and data.get('height') and data.get('age') and data.get('gender'):
        weight_kg = float(data['weight'])
        height_cm = float(data['height'])
        age = int(data['age'])
        gender = data['gender'].lower()
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        elif gender == 'female':
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        age=data.get('age'),
        height=data.get('height'),
        weight=data.get('weight'),
        gender=data.get('gender'),
        bmi=bmi,
        bmr=bmr,
        logged_in =logged_in,
        activity_level=data["activity_level"],
        fitness_goal = data["fitness_goal"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user_id': new_user.user_id,
        'name': new_user.name,
        'email': new_user.email,
        'age': new_user.age,
        'height': str(new_user.height),
        'weight': str(new_user.weight),
        'gender': new_user.gender,
        'bmr': str(new_user.bmr),
        'bmi': str(new_user.bmi),
        "activity_level": new_user.activity_level,
        'fitness_goal': new_user.fitness_goal,
    }), 201

def login():
    data = request.form.to_dict()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    if user.logged_in:
        return jsonify({'message': 'user logged in on another device'}), 403

    user.logged_in = True
    db.session.commit()
    return jsonify({
        'message': 'Login successful',
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email
    }), 200

def get_user_profile(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'height': str(user.height),
        'weight': str(user.weight),
        'gender': user.gender,
        'bmr': str(user.bmr),
        'bmi': str(user.bmi),
        "activity_level": user.activity_level,
        'fitness_goal': user.fitness_goal,
    }), 200

def change_password(user_id):
    data= request.form.to_dict()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not check_password_hash(user.password, data['old_password']):
        return jsonify({'message': 'Incorrect old password'}), 401

    user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    db.session.commit()


    return jsonify({'message': 'Password updated successfully'}), 200

def update_profile(user_id):
    data= request.form.to_dict()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if data.get('name'):
        user.name = data['name']

    if data.get('activity_level'):
        user.activity_level = data['activity_level']

    if data.get('fitness_goal'):
        user.fitness_goal = data['fitness_goal']

    if data.get('email'):
        user.email = data['email']

    if data.get('age'):
        user.age = int(data['age'])

    if data.get('height'):
        user.height = int(data['height'])

    if data.get('weight'):
        user.weight = int(data['weight'])

    if data.get('gender'):
        user.gender = data['gender']

    # Recalculate BMI if height and weight are updated
    if data.get('height') and data.get('weight'):
        height_m = float(data['height']) / 100
        weight_kg = float(data['weight'])
        user.bmi = weight_kg / (height_m * height_m)

    # Recalculate BMR
    if data.get('weight') and data.get('height') and data.get('age') and data.get('gender'):
        weight_kg = float(data['weight'])
        height_cm = float(data['height'])
        age = int(data['age'])
        gender = data['gender'].lower()
        if gender == 'male':
            user.bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        elif gender == 'female':
            user.bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'}), 200

def logout(user_id):
    user = User.query.get(user_id)
    user.logged_in = False
    db.session.commit()


    return jsonify({'message': 'Logged out successfully'}), 200