import json
from flask import request, jsonify
from models import History ,db

def add_recipe_to_history(user_id):
    from datetime import datetime
    data = request.form.to_dict()
    if (
            not data["calories"]
            or not data["carbohydrates (PDV)"]
            or not data["description"]
            or not data["ingredients"]
            or not data["minutes"]
            or not data["n_ingredients"]
            or not data["n_steps"]
            or not data["name"]
            or not data["protein (PDV)"]
            or not data["saturated fats (PDV)"]
            or not data["similarity"]
            or not data["sodium (PDV)"]
            or not data["steps"]
            or not data["sugar (PDV)"]
            or not data["total fats (PDV)"]
            ):
        return jsonify({'message': 'Data missing'}),400
    try:
        data['steps'] = json.loads(data['steps'])
    except (KeyError, json.JSONDecodeError):
        return {"error": "Invalid or missing 'steps' array"}, 400
    new_recipe_selected = History(
        user_id = user_id,
        date_and_time = datetime.now(),
        calories = data["calories"],
        carbohydrates_pdv = data["carbohydrates (PDV)"],
        description = data["description"],
        ingredients = data["ingredients"],
        minutes = data["minutes"],
        n_ingredients = data["n_ingredients"],
        n_steps = data["n_steps"],
        name = data["name"],
        protein_pdv = data["protein (PDV)"],
        saturated_fats_pdv = data["saturated fats (PDV)"],
        similarity = data["similarity"],
        sodium_pdv = data["sodium (PDV)"],
        steps = data["steps"],
        sugar_pdv = data["sugar (PDV)"],
        total_fats_pdv = data["total fats (PDV)"],
    )
    db.session.add(new_recipe_selected)
    db.session.commit()
    return jsonify({'message': 'Recipe added'}), 200

def get_recipes_history(user_id):
    recipes = History.query.filter_by(user_id=user_id).all()
    if not recipes:
        return jsonify({"message": "No recipe history found for this user."}), 404
    result = []
    for recipe in recipes:
        result.append({
            "recipe_id": recipe.recipe_id,
            "user_id": recipe.user_id,
            "date_and_time": recipe.date_and_time.isoformat(),# Format the datetime if needed
            "calories": recipe.calories,
            "carbohydrates (PDV)": recipe.carbohydrates_pdv,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "minutes": recipe.minutes,
            "n_ingredients": recipe.n_ingredients,
            "n_steps": recipe.n_steps,
            "name": recipe.name,
            "protein (PDV)": recipe.protein_pdv,
            "saturated fats (PDV)": recipe.saturated_fats_pdv,
            "similarity": recipe.similarity,
            "sodium (PDV)": recipe.sodium_pdv,
            "steps": recipe.steps,
            "sugar (PDV)": recipe.sugar_pdv,
            "total fats (PDV)": recipe.total_fats_pdv,
        })
    return jsonify(result), 200

def recommend_recipe_by_history(user_id):
    from ML_Model.ml_model import ml_model
    recipes = History.query.filter_by(user_id=user_id).all()
    if not recipes:
        return jsonify({"message": "No recipe history found for this user."}), 404
    new_name =""
    for recipe in recipes:
        if recipe.ingredients:
            new_name += recipe.ingredients + ", "

    data = request.form.to_dict()
    data["recipe_description"] = new_name
    return ml_model(user_id, data)
