from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['recipe-sharing']
users_collection = db['users']
recipes_collection = db['recipes']

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = {
        'username': data['username'],
        'email': data['email'],
        'password': hashed_password,
    }
    users_collection.insert_one(new_user)
    return jsonify(new_user), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({'email': data['email']})
    if not user or not bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({"message": "Invalid credentials"}), 400
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token)

# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = list(recipes_collection.find())
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])
    return jsonify(recipes)

# Create Recipe
@app.route('/recipes', methods=['POST'])
@jwt_required
