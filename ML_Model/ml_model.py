import json
import pandas as pd
import os
from glob import glob
from flask import request, jsonify
from sentence_transformers import SentenceTransformer
from ML_Model.utils import cosine_similarity, filter_recipes_by_goal, calculate_tdee

from models import User


def init_model():
    # Step 1: Load all Parquet files from folder into a single DataFrame
    folder_path = "C:\\Users\\pc\\Desktop\\Back-end\\Back-end-Bavley\\ML_Model\\data"  # <-- Replace with your actual folder
    all_files = glob(os.path.join(folder_path, "*.parquet"))
    df = pd.concat([pd.read_parquet(f) for f in all_files], ignore_index=True)
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')



    # Step 3: Generate embeddings if not already present
    if "embedding" not in df.columns:
        df["embedding"] = model.encode(df["name"].tolist()).tolist()


    return df , model


def ml_model(user_id ,data):
    user = User.query.get(user_id)
    temp_df = input_and_execution(data["recipe_description"])

    find_similar_recipe_parameters ={
        "num_recipes":3,
        "min_calories":300,
        "max_calories":1000,
        "diabetic_friendly":False,
        "max_prep_time":60,
    }
    if data.get('num_recipes'):
        find_similar_recipe_parameters["num_recipes"] = int(data["num_recipes"])

    if data.get('min_calories'):
        find_similar_recipe_parameters["min_calories"] =int (data["min_calories"])

    if data.get('max_calories'):
        find_similar_recipe_parameters["max_calories"] = int(data["max_calories"])

    if data.get('diabetic_friendly'):
        find_similar_recipe_parameters["diabetic_friendly"] = bool(data["diabetic_friendly"])

    if data.get('max_prep_time'):
        find_similar_recipe_parameters["max_prep_time"] = int(data["max_prep_time"])


    tdee = calculate_tdee(user.bmr , user.activity_level)
    similar_recipes = find_similar_recipe(
        data["recipe_description"],
        temp_df,
        tdee,
        user.weight,
        find_similar_recipe_parameters["num_recipes"],
        find_similar_recipe_parameters["min_calories"] ,
        find_similar_recipe_parameters["max_calories"],
        find_similar_recipe_parameters["diabetic_friendly"],
        user.fitness_goal,
        find_similar_recipe_parameters["max_prep_time"],
    )
    json_df = similar_recipes.to_json(orient='records')
    data_list = json.loads(json_df)

    return jsonify({"recipes":data_list}), 200


def find_similar_recipe(
        recipe,
        df,
        tdee,
        weight,
        num_recipes = 3,
        min_calories=300,
        max_calories=1000,
        diabetic_friendly=False,
        fitness_goal=None,#["Loss weight" , "Loss weight and gain muscles" , "Gain weight" , "Gain muscles" , "fitness"]
        max_prep_time=60,

):
    """
    Find similar recipes with goal-based filtering
    """
    if recipe in df["name"].to_list():
        index = df[df["name"] == recipe].index[0]
        data = df.iloc[index]
        vector = data["embedding"]

        # Find similar recipe
        df_result = df.copy()

        # Calculate similarity scores
        df_result["similarity"] = df_result["embedding"].apply(
            lambda x: cosine_similarity(vector, x)
        )

        # Apply goal-based filtering first
        if fitness_goal and tdee:
            df_result = filter_recipes_by_goal(df_result, fitness_goal, tdee, weight)

        # Apply calorie filters
        if min_calories is not None:
            df_result = df_result[df_result["calories"] >= min_calories]
        if max_calories is not None:
            df_result = df_result[df_result["calories"] <= max_calories]

        # Apply preparation time filter
        if max_prep_time is not None:
            df_result = df_result[df_result["minutes"] <= max_prep_time]

        # Apply diabetic filter
        if diabetic_friendly:
            nutrition_cols = df_result.columns[8:13]
            df_result = df_result[df_result[nutrition_cols[1]] * 0.5 <= 25]

        # Sort by similarity among filtered results
        df_result = df_result.sort_values(by="similarity", ascending=False)

        # Get the requested number of recipes
        df_result = df_result.iloc[1:num_recipes + 1]

        # Drop the embedding column before returning
        if "embedding" in df_result.columns:
            df_result.drop("embedding", inplace=True, axis=1)

        return df_result

    return None

def input_and_execution(user_input):
    from back import df, model
    input_embedding = model.encode([user_input])[0]

    # Append the input temporarily if not in dataset
    temp_df = df.copy()
    if user_input not in temp_df["name"].values:
        temp_df.loc[len(temp_df)] = {"name": user_input, "embedding": input_embedding}

    return temp_df
