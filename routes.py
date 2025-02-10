from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tasklist"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
mongo = PyMongo(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    mongo.db.users.insert_one({'username': username, 'email': email, 'password': password})
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = mongo.db.users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=user['email'], expires_delta=datetime.timedelta(days=1))
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad email or password"}), 401

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_email = get_jwt_identity()
    data = request.get_json()
    task = {
        'title': data.get('title'),
        'description': data.get('description'),
        'due_date': data.get('due_date'),
        'priority': data.get('priority'),
        'status': data.get('status'),
        'tags': data.get('tags'),
        'subtasks': data.get('subtasks'),
        'user_email': user_email
    }
    mongo.db.tasks.insert_one(task)
    return jsonify({"msg": "Task created successfully"}), 201

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_email = get_jwt_identity()
    tasks = mongo.db.tasks.find({'user_email': user_email})
    return jsonify([task for task in tasks]), 200

@app.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    update_data = {k: v for k, v in data.items() if v is not None}
    mongo.db.tasks.update_one({'_id': task_id}, {'$set': update_data})
    return jsonify({"msg": "Task updated successfully"}), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': task_id})
    return jsonify({"msg": "Task deleted successfully"}), 200

@app.route('/lists', methods=['POST'])
@jwt_required()
def create_list():
    user_email = get_jwt_identity()
    data = request.get_json()
    task_list = {
        'name': data.get('name'),
        'description': data.get('description'),
        'user_email': user_email,
        'tasks': []
    }
    mongo.db.lists.insert_one(task_list)
    return jsonify({"msg": "Task list created successfully"}), 201

@app.route('/lists', methods=['GET'])
@jwt_required()
def get_lists():
    user_email = get_jwt_identity()
    task_lists = mongo.db.lists.find({'user_email': user_email})
    return jsonify([task_list for task_list in task_lists]), 200

@app.route('/lists/<list_id>', methods=['PUT'])
@jwt_required()
def update_list(list_id):
    data = request.get_json()
    update_data = {k: v for k, v in data.items() if v is not None}
    mongo.db.lists.update_one({'_id': list_id}, {'$set': update_data})
    return jsonify({"msg": "Task list updated successfully"}), 200

@app.route('/lists/<list_id>', methods=['DELETE'])
@jwt_required()
def delete_list(list_id):
    mongo.db.lists.delete_one({'_id': list_id})
    return jsonify({"msg": "Task list deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)