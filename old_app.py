from flask import Flask, request, jsonify
import os  # Import the os module to access environment variables

app = Flask(__name__)

# In-memory storage for todos
todos = []
TOKEN = os.getenv("TOKEN", "default_secret_token")  # Fetches the token from environment variables or uses a default

# Middleware for authorization
@app.before_request
def check_authorization():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]  # Extract the token after 'Bearer'
    if not token or token != TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

# Route to get todo items
@app.route('/get_todos', methods=['GET'])
def get_todos():
    if not todos:
        return jsonify({"message": "No todos found"}), 404  # Return message if no todos are found
    return jsonify(todos)

# Route to create a new todo item
@app.route('/create_todo', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    new_todo = {
        "id": len(todos) + 1,
        "title": title,  # Use the title from the request
        "completed": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Route to update a todo item by id
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    if 'title' in data:
        todo["title"] = data["title"]
    if 'completed' in data:
        todo["completed"] = data["completed"]
    return jsonify(todo)

# Route to delete a todo item by id
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    todos = [todo for todo in todos if todo["id"] != id]
    return jsonify({"message": "Todo deleted"}), 200  # Inform the client that the deletion was successful

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change the port as necessary
