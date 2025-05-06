from flask import Flask
from flask_cors import CORS
from ML_Model.ml_model import init_model, ml_model
from user_functions import (register, login, get_user_profile,change_password,
                            update_profile, logout
                            )



app = Flask(__name__)
CORS(app)

# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/Recipe-Rise_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import User, db
db.init_app(app)

df, model = init_model()

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


## 6. User Logout
@app.route('/api/logout/<int:user_id>', methods=['POST'])
def sign_out(user_id):
    return logout(user_id)


## 7. Recommendation system
@app.route('/ml_model/<int:user_id>', methods=['GET'])
def recommendation_model(user_id):
    return ml_model(user_id)


## 8. upload image
@app.route('/user/image_upload/<int:user_id>', methods=['POST'])
def image_upload(user_id):
    from image_functions import upload_image
    return upload_image(user_id)


## 9. retrieve image
@app.route('/user/get_image/<int:user_id>', methods=['GET'])
def image_retrieve(user_id):
    from image_functions import get_image
    return get_image(user_id)


## 10. add to chat history
@app.route('/add_chat_buble/<int:user_id>', methods=['POST'])
def post_chat_buble(user_id):
    from chat_history import add_chat_buble
    return add_chat_buble(user_id)


## 11. retrieve chat history
@app.route('/get_chat_history/<int:user_id>', methods=['GET'])
def get_chat_history(user_id):
    from chat_history import get_chat_bubbles
    return get_chat_bubbles(user_id )




# Run the application
if __name__ == '__main__':
    app.run(debug=True ,host = "0.0.0.0")
