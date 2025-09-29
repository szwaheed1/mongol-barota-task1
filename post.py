import requests

# Create a new todo
response = requests.post('http://localhost:5000/api/todos', 
                        json={"task": "Learn POST requests"})
print("Response:", response.json())

# Get all todos to see our new one
response = requests.get('http://localhost:5000/api/todos')
print("All todos:", response.json())