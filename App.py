from flask import Flask , request , jsonify
import firebase_admin 
import pyrebase
from firebase_admin import credentials , firestore ,auth
app = Flask(__name__)
cred = credentials.Certificate(
    "C:/Users/pc/Desktop/Flaskapp/graduation-project-d3c73-firebase-adminsdk-fbsvc-e305fc32c1.json"
    )
firebase_admin.initialize_app(cred)
db = firestore.client() 

firebaseConfig = {
  'apiKey': "AIzaSyD0yQDd2w6PZ24BE_nUreOiTar_16hgeGo",
  'authDomain': "graduation-project-d3c73.firebaseapp.com",
  'projectId': "graduation-project-d3c73",
  'storageBucket': "graduation-project-d3c73.firebasestorage.app",
  'messagingSenderId': "835986445745",
  'appId': "1:835986445745:web:3874327bbb8bee3c605990",
  'databaseURL' :""  
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route("/register" , methods = ["POST"])
def register_user():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        # Create user in Firebase Authentication
        user = auth.create_user(
            email = email,
            password = password
        )
        return jsonify({"message": f"User {user.email} created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/login" , methods = ["POST"])
def login_user():
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    try:

        user = auth.sign_in_with_email_and_password(email, password)
        id_token = user['idToken']
        return jsonify({"message": "Login successful", "id_token": id_token}), 200
    
    except Exception as e:
        return jsonify({"message": "Invalid email or password"}), 401


if __name__=="__main__":
    app.run(debug=True)