import numpy as np
from decimal import Decimal

def cosine_similarity(vec1, vec2):
    """
    Returns the cosine similarity between two vectors of n dimension
    """
    denom = np.sqrt(np.sum(np.square(vec1))) * np.sqrt(np.sum(np.square(vec2)))
    return np.round(np.dot(vec1, vec2) / denom * 100, 2)

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure
    activity_level: 1.2 (sedentary), 1.375 (light), 1.55 (moderate), 1.725 (very active), 1.9 (extra active)
    """
    if activity_level == "sedentary":
        activity_level_in_num = 1.2

    elif activity_level == "light":
        activity_level_in_num = 1.375

    elif activity_level == "moderate":
        activity_level_in_num = 1.55

    elif activity_level == "very active":
        activity_level_in_num = 1.725

    else:#extra active
        activity_level_in_num = 1.9

    return float(bmr * Decimal(str(activity_level_in_num)))

def get_macro_targets(tdee, goal, weight):
    """
    Calculate macronutrient targets based on fitness goal
    Returns: (protein, carbs, fats) in grams
    
    Protein per kg guidelines:
    - Weight loss: 2.2-2.4g/kg to preserve muscle
    - Muscle gain: 1.8-2.2g/kg
    - Weight gain: 1.6-2.0g/kg
    - Maintenance: 1.6-1.8g/kg
    
    Carb/Fat ratios adjust based on goals:
    - Weight loss: Lower carbs (30-35% of calories)
    - Muscle gain: Higher carbs (50-55% of calories)
    - Weight gain: High carbs (55-60% of calories)
    - Maintenance: Balanced (40-45% of calories)
    """
    
    if goal == "Loss weight":
        # Calculate adjusted TDEE for weight loss
        adjusted_tdee = tdee - 500  # 500 calorie deficit
        
        # Higher protein for muscle preservation during deficit
        protein = weight * 2.4  # 2.4g per kg
        # Lower carbs for weight loss
        carbs_calories = adjusted_tdee * 0.30  # 30% of calories from carbs
        carbs = carbs_calories / 4
        # Moderate fats
        fats_calories = adjusted_tdee * 0.35  # 35% of calories from fats
        fats = fats_calories / 9
        
    elif goal == "Loss weight and gain muscles":
        # Moderate deficit with high protein
        adjusted_tdee = tdee - 300  # 300 calorie deficit
        
        # Very high protein for muscle preservation and growth
        protein = weight * 2.6  # 2.6g per kg
        # Moderate carbs for energy during workouts
        carbs_calories = adjusted_tdee * 0.35  # 35% of calories from carbs
        carbs = carbs_calories / 4
        # Lower fats
        fats_calories = adjusted_tdee * 0.30  # 30% of calories from fats
        fats = fats_calories / 9
        
    elif goal == "Gain weight":
        # Calculate adjusted TDEE for weight gain
        adjusted_tdee = tdee + 500  # 500 calorie surplus
        
        # Moderate protein
        protein = weight * 1.8  # 1.8g per kg
        # High carbs for weight gain
        carbs_calories = adjusted_tdee * 0.55  # 55% of calories from carbs
        carbs = carbs_calories / 4
        # Moderate fats
        fats_calories = adjusted_tdee * 0.30  # 30% of calories from fats
        fats = fats_calories / 9
        
    elif goal == "Gain muscles":
        # Calculate adjusted TDEE for muscle gain
        adjusted_tdee = tdee + 300  # 300 calorie surplus
        
        # High protein for muscle growth
        protein = weight * 2.2  # 2.2g per kg
        # High carbs for energy and recovery
        carbs_calories = adjusted_tdee * 0.50  # 50% of calories from carbs
        carbs = carbs_calories / 4
        # Moderate fats
        fats_calories = adjusted_tdee * 0.25  # 25% of calories from fats
        fats = fats_calories / 9
        
    else:  # Fitness (maintain)
        # Maintenance calories
        adjusted_tdee = tdee
        
        # Moderate protein
        protein = weight * 1.8  # 1.8g per kg
        # Balanced carbs
        carbs_calories = adjusted_tdee * 0.45  # 45% of calories from carbs
        carbs = carbs_calories / 4
        # Balanced fats
        fats_calories = adjusted_tdee * 0.30  # 30% of calories from fats
        fats = fats_calories / 9

    # Calculate actual calories from macros for verification
    total_calories = (protein * 4) + (carbs * 4) + (fats * 9)
    
    # Print debug information
    print(f"\nGoal: {goal}")
    print(f"Weight: {weight}kg")
    print(f"Original TDEE: {tdee:.0f} calories")
    print(f"Adjusted TDEE: {adjusted_tdee:.0f} calories")
    print(f"Calculated calories from macros: {total_calories:.0f}")
    print("\nMacronutrient Distribution:")
    print(f"Protein: {protein:.0f}g ({(protein * 4 / total_calories * 100):.0f}%)")
    print(f"Carbs: {carbs:.0f}g ({(carbs * 4 / total_calories * 100):.0f}%)")
    print(f"Fats: {fats:.0f}g ({(fats * 9 / total_calories * 100):.0f}%)")

    return round(protein), round(carbs), round(fats)

def filter_by_macros(df, protein_target, carbs_target, fats_target, tolerance=0.5):
    """
    Filter recipes based on macronutrient targets with a tolerance
    tolerance: 50% deviation from target is allowed
    """
    # Get the nutritional information columns (indices 8:13)
    nutrition_cols = df.columns[8:13]
    print("Nutrition columns:", nutrition_cols)
    
    # Convert PDV to actual grams (assuming PDV is percentage of daily value)
    # We'll use rough estimates: protein_dv = 50g, carbs_dv = 300g, fats_dv = 65g
    protein_dv = 50
    carbs_dv = 300
    fats_dv = 65
    
    # Convert targets to PDV
    protein_pdv = (protein_target / protein_dv) * 100
    carbs_pdv = (carbs_target / carbs_dv) * 100
    fats_pdv = (fats_target / fats_dv) * 100
    
    print(f"Target PDV values: Protein={protein_pdv:.2f}%, Carbs={carbs_pdv:.2f}%, Fats={fats_pdv:.2f}%")
    
    # Apply macro filters with tolerance
    # We'll use a more lenient approach - recipes should meet at least one of the macro targets
    df_filtered = df[
        # Protein filter (using protein PDV)
        (df[nutrition_cols[3]] >= protein_pdv * (1 - tolerance)) |
        # Carbs filter (using sugar PDV as an estimate)
        (df[nutrition_cols[1]] >= carbs_pdv * (1 - tolerance)) |
        # Fats filter (using total fat PDV)
        (df[nutrition_cols[0]] >= fats_pdv * (1 - tolerance))
    ]
    
    print(f"Original recipes: {len(df)}")
    print(f"Filtered recipes: {len(df_filtered)}")
    
    # Add nutritional information to the filtered recipes
    df_filtered['protein_pdv'] = df_filtered[nutrition_cols[3]]
    df_filtered['carbs_pdv'] = df_filtered[nutrition_cols[1]]  # Using sugar PDV as an estimate
    df_filtered['fats_pdv'] = df_filtered[nutrition_cols[0]]
    
    # Sort by how well they match the targets
    df_filtered['macro_score'] = (
        (df_filtered['protein_pdv'] / protein_pdv) +
        (df_filtered['carbs_pdv'] / carbs_pdv) +
        (df_filtered['fats_pdv'] / fats_pdv)
    ) / 3
    
    df_filtered = df_filtered.sort_values('macro_score', ascending=False)
    
    return df_filtered

def filter_recipes_by_goal(df, fitness_goal, tdee,weight):
    """
    Filter recipes based on fitness goal and macro targets.
    Prioritizes recipes that match the nutritional needs of each goal.
    """
    try:
        # Get nutrition columns
        nutrition_cols = df.columns[8:13]
        protein_target, carbs_target, fats_target = get_macro_targets(tdee,fitness_goal,weight)

        # Convert nutritional values to grams
        df['protein_g'] = df[nutrition_cols[3]] * 0.5  # 50g protein is 100% DV
        df['carbs_g'] = df[nutrition_cols[1]] * 3.0    # 300g carbs is 100% DV
        df['fats_g'] = df[nutrition_cols[0]] * 0.65    # 65g fat is 100% DV

        # Calculate macro ratios per recipe
        total_cals = (df['protein_g'] * 4) + (df['carbs_g'] * 4) + (df['fats_g'] * 9)
        df['protein_ratio'] = (df['protein_g'] * 4) / total_cals
        df['carbs_ratio'] = (df['carbs_g'] * 4) / total_cals
        df['fats_ratio'] = (df['fats_g'] * 9) / total_cals

        # Score recipes based on goal
        if fitness_goal == "Loss weight":
            # Priority: High protein, low carbs, moderate fats
            df['goal_score'] = (
                (df['protein_ratio'] * 0.5) +        # 50% of score from protein content
                ((1 - df['carbs_ratio']) * 0.3) +    # 30% of score from low carbs
                ((1 - df['fats_ratio']) * 0.2)       # 20% of score from moderate fats
            )
            # Filter out very high-calorie recipes
            df = df[df['calories'] <= (protein_target * 4 + carbs_target * 4 + fats_target * 9) * 0.4]

        elif fitness_goal == "Loss weight and gain muscles":
            # Priority: Very high protein, moderate carbs, low fats
            df['goal_score'] = (
                (df['protein_ratio'] * 0.6) +        # 60% of score from protein content
                ((1 - df['carbs_ratio']) * 0.25) +   # 25% of score from moderate carbs
                ((1 - df['fats_ratio']) * 0.15)      # 15% of score from low fats
            )
            # Ensure adequate protein per serving
            df = df[df['protein_g'] >= protein_target * 0.3]  # At least 30% of daily protein target

        elif fitness_goal == "Gain weight":
            # Priority: Balanced macros, higher calories
            df['goal_score'] = (
                (df['calories'] / 1000 * 0.4) +      # 40% of score from calories
                (df['carbs_ratio'] * 0.35) +         # 35% of score from carbs
                (df['protein_ratio'] * 0.25)         # 25% of score from protein
            )
            # Filter for higher calorie recipes
            df = df[df['calories'] >= 400]

        elif fitness_goal == "Gain muscles":
            # Priority: High protein, high carbs, moderate fats
            df['goal_score'] = (
                (df['protein_ratio'] * 0.45) +       # 45% of score from protein
                (df['carbs_ratio'] * 0.45) +         # 45% of score from carbs
                ((1 - df['fats_ratio']) * 0.1)       # 10% of score from moderate fats
            )
            # Ensure good protein content
            df = df[df['protein_g'] >= protein_target * 0.25]  # At least 25% of daily protein target

        else:  # Fitness (maintain)
            # Priority: Balanced macros
            df['goal_score'] = (
                (1 - abs(df['protein_ratio'] - 0.3)) * 0.34 +  # 34% protein ratio
                (1 - abs(df['carbs_ratio'] - 0.4)) * 0.33 +    # 33% carbs ratio
                (1 - abs(df['fats_ratio'] - 0.3)) * 0.33       # 33% fats ratio
            )

        # Sort by goal score
        df = df.sort_values('goal_score', ascending=False)

        # Keep only top 60% of recipes that best match the goal
        df = df.head(int(len(df) * 0.6))

        # Clean up temporary columns
        df = df.drop(['protein_g', 'carbs_g', 'fats_g', 
                     'protein_ratio', 'carbs_ratio', 'fats_ratio', 
                     'goal_score'], axis=1)

        return df

    except Exception as e:
        print(f"Error in filter_recipes_by_goal: {str(e)}")
        print("Available columns:", df.columns.tolist())
        return df
