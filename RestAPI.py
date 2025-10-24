from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store (like a mini database)
users = {}

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# POST (add new user)
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_id = len(users) + 1
    users[user_id] = {"id": user_id, "name": data["name"], "email": data["email"]}
    return jsonify({"message": "User added", "user": users[user_id]}), 201

# PUT (update user)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = users.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify({"message": "User updated", "user": user}), 200

# DELETE (remove user)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
