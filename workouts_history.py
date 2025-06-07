from json import JSONDecodeError

from flask import request, jsonify
import json
from models import Workout, db

def add_workout_to_history(user_id):
    from datetime import datetime
    data = request.form.to_dict()
    if (
            not data["bodyPart"]
            or not data["gifUrl"]
            or not data["name"]
            or not data["target"]
            or not data["secondaryMuscles"]
            or not data["instructions"]
            ):
        return jsonify({'message': 'Data missing'}),400
    try:
        data['secondaryMuscles'] = json.loads(data['secondaryMuscles'])
    except (KeyError, json.JSONDecodeError) :
        return {"error": "Invalid or missing 'secondaryMuscles' array"}, 400

    try:
        data['instructions'] = json.loads(data['instructions'])
    except (KeyError, json.JSONDecodeError) :
        return {"error": "Invalid or missing 'instructions' array"}, 400


    new_workout = Workout(
        user_id = user_id,
        date_and_time = datetime.now(),
        bodyPart = data["bodyPart"],
        gifUrl = data["gifUrl"],
        name = data["name"],
        target = data["target"],
        secondaryMuscles = data["secondaryMuscles"],
        instructions = data["instructions"],
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': 'workout added'}), 200

def get_workouts_history(user_id):
    workouts = Workout.query.filter_by(user_id=user_id).all()
    if not workouts:
        return jsonify({"message": "No workouts history found for this user."}), 404
    result = []
    for workout in workouts:
        result.append({
            "workout_id": workout.workout_id,
            "user_id": workout.user_id,
            "date_and_time": workout.date_and_time.isoformat(),# Format the datetime if needed
            "bodyPart": workout.bodyPart,
            "gifUrl": workout.gifUrl,
            "name": workout.name,
            "target": workout.target,
            "secondaryMuscles": workout.secondaryMuscles,
            "instructions": workout.instructions,
        })
    return jsonify(result), 200
