from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ML_Model.ml_model import init_model, ml_model
from user_functions import (register, login, get_user_profile,change_password,
                            update_profile
                            )
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from models import db
db.init_app(app)

try:
    df, model = init_model()
except RuntimeError as e:
    print(f"Model initialization failed: {e}")
    df = model = None

# API Endpoints

## 1. Register User
@app.route('/api/register', methods=['POST'])
def registration():
    return register()


## 2. User Login
@app.route('/api/login', methods=['POST'])
def signin():
    return login()


## 3. Retrieve User Profile
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    return get_user_profile(user_id)


## 4. Change Password
@app.route('/api/user/change_password/<int:user_id>/password', methods=['PUT'])
def update_password(user_id):
    return change_password(user_id)


## 5. Update Profile
@app.route('/api/user/update_profile/<int:user_id>', methods=['PUT'])
def update_profile_data(user_id):
    return update_profile(user_id)


## 6. Recommendation system
@app.route('/ml_model/<int:user_id>', methods=['POST'])
def recommendation_model(user_id):
    data = request.form.to_dict()
    return ml_model(user_id , data)


## 7. upload image
@app.route('/user/image_upload/<int:user_id>', methods=['POST'])
def image_upload(user_id):
    from image_functions import upload_image
    return upload_image(user_id)


## 8. retrieve image
@app.route('/user/get_image/<int:user_id>', methods=['GET'])
def image_retrieve(user_id):
    from image_functions import get_image
    return get_image(user_id)


## 9. add to chat history
@app.route('/add_chat_buble/<int:user_id>', methods=['POST'])
def post_chat_buble(user_id):
    from chat_history import add_chat_buble
    return add_chat_buble(user_id)


## 10. retrieve chat history
@app.route('/get_chat_history/<int:user_id>', methods=['GET'])
def get_chat_history(user_id):
    from chat_history import get_chat_bubbles
    return get_chat_bubbles(user_id )

## 11. add recipe to user history
@app.route('/add_recipe_to_history/<int:user_id>', methods=['POST'])
def add_recipe_to_user_history(user_id):
    from recipe_history import add_recipe_to_history
    return add_recipe_to_history(user_id)

## 12. get user recipes history
@app.route('/get_user_recipes_history/<int:user_id>', methods=['GET'])
def get_user_recipes_history(user_id):
    from recipe_history import get_recipes_history
    return get_recipes_history(user_id)

## 13. recommend recipe by user history
@app.route('/recommend_recipe_by_user_history/<int:user_id>', methods=['POST'])
def recommend_recipe_by_user_history(user_id):
    from recipe_history import recommend_recipe_by_history
    return recommend_recipe_by_history(user_id)

## 14. add workout to user history
@app.route('/add_workout_to_history/<int:user_id>', methods=['POST'])
def add_workout_to_user_history(user_id):
    from workouts_history import add_workout_to_history
    return add_workout_to_history(user_id)

## 15. get user workouts history
@app.route('/get_user_workouts_history/<int:user_id>', methods=['GET'])
def get_user_workouts_history(user_id):
    from workouts_history import get_workouts_history
    return get_workouts_history(user_id)


## 16. send verification code
@app.route('/send_verification_code', methods=['POST'])
def send_verification_code_method():
    from email_verification import send_verification_code
    return send_verification_code()

## 17. verify email
@app.route('/verify_email', methods=['POST'])
def verify_email_method():
    from email_verification import verify_secret_code
    return verify_secret_code()


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
