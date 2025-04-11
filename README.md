# 🥗 Recipe Rise — Backend
```
**Recipe Rise** is a smart recipe recommendation system. Users can select available ingredients and receive personalized recipe suggestions that include:

- ✅ Estimated preparation time  
- ✅ Step-by-step cooking method  
- ✅ Calorie information tailored to their **gender, age, BMI, BMR**, and **weight goals** (loss/gain)

This repo contains the **Flask backend** powering the logic, data handling, and API endpoints.

---

## 🧰 Tech Stack

- **Python**
- **Flask**
- **Flask SQLAlchemy**
- **PostgreSQL**
- **Flask-CORS**
- **Werkzeug** (for password hashing)


```
## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Recipe-Rise/Back-end
cd recipe-rise-backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install Flask flask_sqlalchemy flask_cors psycopg2-binary werkzeug
```

### 4. Set up environment variables (optional)
If needed, create a `.env` file to store DB credentials or secret keys.

### 5. Run the app
```bash
flask run
```

The API will be available at: `http://127.0.0.1:5000/`

---

## 📦 Main Dependencies

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
```

---

## 📡 Example Endpoints

| Method | Endpoint                     | Description                            |
|--------|------------------------------|----------------------------------------|
| POST   | `/api/register`              | Register a new user                    |
| PUT    | `/api/user/update_profile/<int:user_id>`   | Update user data (name, age, wieght etc) |
| PUT   | `/api/user/change_password/<int:user_id>/password`              | Update user Password              |
| POST   | `/api/login`            | Authenticate and log in the user       |
| GET    | `/api/user/<int:user_id>`     | Retrieve a user's profile information  |


🔧 **More endpoints will be added as the project grows.**
