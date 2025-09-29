# request helps us get data that someone sends TO our API
from flask import Flask, jsonify, request

# Create our Flask app
app = Flask(__name__)

# Our database
todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build an API", "done": False}
]

# We need to keep track of the next ID to use
next_id = 3

# Our hello route (same as before)
@app.route('/')
def hello():
    return "Champions of URC 2026"

# GET request - get all todos (same as before)
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# NEW: POST request - create a new todo!
# This lets people SEND data TO our API
@app.route('/api/todos', methods=['POST'])
def create_todo():
    global next_id  # We need to modify the next_id variable
    
    # Get the JSON data that someone sent us
    data = request.get_json()
    
    # Check if they actually sent us data
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Check if they included a "task" field
    if 'task' not in data:
        return jsonify({"error": "Task is required"}), 400
    
    # Create a new todo item
    new_todo = {
        "id": next_id,
        "task": data['task'],
        "done": data.get('done', False)  # If they don't specify, default to False
    }
    
    # Add it to our list
    todos.append(new_todo)
    next_id += 1  # Increment for next time
    
    # Send back the new todo we just created
    return jsonify(new_todo), 201  # 201 means "Created successfully"

# Run the app
if __name__ == '__main__':
    print("Starting our web app...")
    print("Try these:")
    print("- GET  http://localhost:5000/api/todos (view todos)")
    print("- POST http://localhost:5000/api/todos (create todo)")
    app.run(debug=True)
